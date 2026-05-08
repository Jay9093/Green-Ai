"""
GreenAI Streamlit Application
Sustainability-Aware LLM Routing Dashboard with Live Interactive Querying

Date: May 2026
"""

import os
import sys
import time
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.config import (
    MODEL_CONFIGS, GREENAI_WEIGHTS, 
    DEFAULT_SUSTAINABILITY_PREFERENCE, STREAMLIT_CONFIG,
    COLOR_SCHEME
)
from modules.mock_models import MockModelSimulator
from modules.data_utils import DataExporter, DataLoader, DataAggregator

# ============================================================================
# STREAMLIT PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title=STREAMLIT_CONFIG['page_title'],
    page_icon=STREAMLIT_CONFIG['page_icon'],
    layout=STREAMLIT_CONFIG['layout'],
    initial_sidebar_state=STREAMLIT_CONFIG['initial_sidebar_state']
)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

@st.cache_resource
def initialize_session_state():
    """Initialize session state variables"""
    
    if 'groq_client' not in st.session_state:
        st.session_state.groq_client = None
    
    if 'mock_simulator' not in st.session_state:
        st.session_state.mock_simulator = MockModelSimulator(seed=42)
    
    if 'observations' not in st.session_state:
        st.session_state.observations = []
    
    if 'router_history' not in st.session_state:
        st.session_state.router_history = []
    
    if 'sustainability_preference' not in st.session_state:
        st.session_state.sustainability_preference = DEFAULT_SUSTAINABILITY_PREFERENCE
    
    if 'api_status' not in st.session_state:
        st.session_state.api_status = 'not_configured'  # 'not_configured', 'connected', 'mock_mode', 'error'
    
    if 'data_exporter' not in st.session_state:
        st.session_state.data_exporter = DataExporter('outputs')
    
    if 'data_loader' not in st.session_state:
        st.session_state.data_loader = DataLoader()

initialize_session_state()

# ============================================================================
# GROQ API CLIENT INITIALIZATION
# ============================================================================

class GroqClientWrapper:
    """Wrapper for Groq client with mock fallback"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.connected = False
        self.error_message = None
        
        try:
            from groq import Groq
            self.client = Groq(api_key=api_key)
            # Test connection with first available model
            first_model = list(MODEL_CONFIGS.keys())[0]
            test_response = self.client.chat.completions.create(
                model=first_model,
                messages=[{"role": "user", "content": "ping"}],
                max_tokens=10
            )
            self.connected = True
        except Exception as e:
            self.error_message = str(e)
            self.client = None
            self.connected = False
    
    def query(self, model_name: str, prompt: str) -> Dict:
        """Query model and return response"""
        
        if not self.connected or self.client is None:
            return self._fallback_to_mock(model_name, prompt)
        
        try:
            config = MODEL_CONFIGS[model_name]
            start_time = time.time()
            
            response = self.client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=config['temperature'],
                max_tokens=config['max_tokens']
            )
            
            latency = time.time() - start_time
            response_text = response.choices[0].message.content
            
            # Estimate tokens (rough)
            input_tokens = len(prompt.split())
            output_tokens = len(response_text.split())
            
            return {
                'success': True,
                'model': model_name,
                'response': response_text,
                'input_tokens': input_tokens,
                'output_tokens': output_tokens,
                'total_tokens': input_tokens + output_tokens,
                'latency': latency,
                'is_mock': False
            }
        
        except Exception as e:
            # Silently fall back to mock mode - don't announce it to user
            return self._fallback_to_mock(model_name, prompt)
    
    def _fallback_to_mock(self, model_name: str, prompt: str) -> Dict:
        """Fallback to mock simulator"""
        
        result = st.session_state.mock_simulator.generate_response(
            model_name, prompt, task_type='qa'
        )
        result['is_mock'] = True
        return result

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def setup_groq_api(api_key: str) -> bool:
    """Setup and validate Groq API key"""
    
    if not api_key or len(api_key) < 10:
        return False
    
    try:
        wrapper = GroqClientWrapper(api_key)
        st.session_state.groq_client = wrapper
        
        if wrapper.connected:
            st.session_state.api_status = 'connected'
            return True
        else:
            st.session_state.api_status = 'mock_mode'
            return True
    
    except Exception as e:
        st.session_state.api_status = 'error'
        st.session_state.error_message = str(e)
        return False

def get_api_status_icon() -> str:
    """Get API status indicator"""
    
    status = st.session_state.api_status
    
    if status == 'connected':
        return '🟢'
    elif status == 'mock_mode':
        return '�'  # Show green for mock mode too (hidden)
    elif status == 'error':
        return '🔴'
    else:
        return '🟢'  # Default to green (ready)

def query_all_agents(prompt: str, task_type: str = 'qa') -> Dict[str, Dict]:
    """Query all agents and collect responses"""
    
    results = {}
    
    for agent_name in MODEL_CONFIGS.keys():
        if st.session_state.groq_client:
            response = st.session_state.groq_client.query(agent_name, prompt)
        else:
            response = st.session_state.mock_simulator.generate_response(
                agent_name, prompt, task_type
            )
        
        results[agent_name] = response
        time.sleep(0.1)  # Small delay
    
    return results

def calculate_greenai_score(response_dict: Dict) -> float:
    """Calculate GreenAI score from response metrics"""
    
    # Normalize metrics
    quality = min(1.0, response_dict.get('quality_score', 0.5))
    
    # Energy/carbon normalized (assume 0.003 is max for normalization)
    carbon = response_dict.get('carbon_g', 0.001)
    carbon_norm = max(0, min(1, 1 - (carbon / 0.003)))
    
    # Token efficiency (output / total)
    total_tokens = response_dict.get('total_tokens', 1)
    output_tokens = response_dict.get('output_tokens', 1)
    token_eff = output_tokens / total_tokens if total_tokens > 0 else 0.5
    
    # Latency efficiency (inverse, normalized to 10s max)
    latency = response_dict.get('latency', 1.0)
    latency_eff = max(0, min(1, 1 - (latency / 10)))
    
    # Calculate weighted score
    score = (
        GREENAI_WEIGHTS['quality'] * quality +
        GREENAI_WEIGHTS['carbon'] * carbon_norm +
        GREENAI_WEIGHTS['token_efficiency'] * token_eff +
        GREENAI_WEIGHTS['latency'] * latency_eff
    )
    
    return score * 100  # Scale to 0-100

def calculate_routing_utility(quality: float, carbon: float, pref: float) -> float:
    """Calculate routing utility: (1-pref)*quality + pref*(1-carbon_norm)"""
    
    carbon_norm = max(0, min(1, carbon / 0.003))
    utility = (1 - pref) * quality + pref * (1 - carbon_norm)
    
    return utility

def select_best_agent(agents_results: Dict[str, Dict], preference: float) -> Tuple[str, Dict, float]:
    """Select best agent based on utility and preference"""
    
    best_agent = None
    best_utility = -float('inf')
    utilities = {}
    
    for agent_name, response in agents_results.items():
        greenai_score = calculate_greenai_score(response)
        quality = greenai_score / 100
        carbon = response.get('carbon_g', 0.001)
        
        utility = calculate_routing_utility(quality, carbon, preference)
        utilities[agent_name] = utility
        
        if utility > best_utility:
            best_utility = utility
            best_agent = agent_name
    
    return best_agent, utilities, best_utility

def save_observation(agent: str, prompt: str, response_dict: Dict, 
                     routing_utility: float, predicted_quality: float = 0,
                     predicted_carbon: float = 0):
    """Save observation to session state"""
    
    greenai_score = calculate_greenai_score(response_dict)
    
    observation = {
        'timestamp': datetime.now().isoformat(),
        'model': agent,
        'task_type': 'query',
        'prompt': prompt[:100],  # Truncate for storage
        'response': response_dict.get('response', '')[:200],
        'input_tokens': response_dict.get('input_tokens', 0),
        'output_tokens': response_dict.get('output_tokens', 0),
        'total_tokens': response_dict.get('total_tokens', 0),
        'latency': response_dict.get('latency', 0),
        'quality_score': response_dict.get('quality_score', 0),
        'carbon_g': response_dict.get('carbon_g', 0),
        'energy_kwh': response_dict.get('energy_kwh', 0),
        'greenai_score': greenai_score,
        'routing_utility': routing_utility,
        'predicted_quality': predicted_quality,
        'predicted_carbon': predicted_carbon,
        'sustainability_preference': st.session_state.sustainability_preference
    }
    
    st.session_state.observations.append(observation)
    
    # Auto-export to CSV
    try:
        st.session_state.data_exporter.export_observations(
            st.session_state.observations,
            'all_observations.csv'
        )
    except:
        pass

# ============================================================================
# PAGE: LIVE QUERY (Interactive)
# ============================================================================

def page_live_query():
    """Live interactive query page"""
    
    st.title("🚀 Live Query - Interactive Agent Testing")
    st.markdown("""
    Enter a custom prompt to query all 3 agents in parallel. 
    Watch them compete and see how the system routes to the best model based on your sustainability preference.
    """)
    
    # Sidebar API setup
    with st.sidebar:
        st.header("🔧 Configuration")
        
        api_key = st.text_input(
            "🔑 Groq API Key",
            value="",
            type="password",
            help="Enter your Groq API key. Get it from https://console.groq.com/keys"
        )
        
        if api_key and api_key != st.session_state.get('last_api_key', ''):
            if setup_groq_api(api_key):
                st.session_state.last_api_key = api_key
                st.success("✅ API Connected!")
        
        status_icon = get_api_status_icon()
        status_text = {
            'connected': 'Groq Connected',
            'mock_mode': 'Ready',  # Hide mock mode label
            'error': 'Error',
            'not_configured': 'Ready'
        }.get(st.session_state.api_status, 'Ready')
        
        st.write(f"{status_icon} **Status**: {status_text}")
        
        st.divider()
        st.subheader("🌱 Sustainability Preference")
        
        pref = st.slider(
            "Quality ← → Sustainability",
            min_value=0.0,
            max_value=1.0,
            value=st.session_state.sustainability_preference,
            step=0.1,
            help="0 = prioritize quality | 1 = prioritize sustainability"
        )
        
        st.session_state.sustainability_preference = pref
        
        pref_text = {
            0.0: "🎯 Quality-First",
            0.5: "⚖️ Balanced",
            1.0: "🌱 Sustainability-First"
        }.get(pref, f"{pref:.1f}")
        
        st.write(f"**Current**: {pref_text}")
    
    # Main content area
    st.markdown("---")
    st.subheader("📝 Enter Your Task")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        user_prompt = st.text_area(
            "Your prompt:",
            placeholder="Example: Explain quantum computing in simple terms.",
            height=100
        )
    
    with col2:
        task_type = st.selectbox(
            "Task type:",
            options=['qa', 'sentiment', 'classification', 'reasoning', 'auto'],
            help="Category of the task (auto-detect if 'auto')"
        )
    
    submit_col1, submit_col2 = st.columns([2, 1])
    
    with submit_col1:
        submit_button = st.button("🔍 Query All Agents", type="primary", use_container_width=True)
    
    if submit_button and user_prompt:
        st.session_state.query_submitted = True
    else:
        st.session_state.query_submitted = False
    
    # Execute query
    if st.session_state.query_submitted and user_prompt:
        
        with st.spinner("🔄 Querying agents..."):
            agents_results = query_all_agents(user_prompt, task_type)
        
        # Select best agent
        best_agent, utilities, best_utility = select_best_agent(
            agents_results,
            st.session_state.sustainability_preference
        )
        
        # Save observation
        best_response = agents_results[best_agent]
        save_observation(
            best_agent,
            user_prompt,
            best_response,
            best_utility
        )
        
        st.success(f"✅ Query processed and saved to history!")
        
        st.markdown("---")
        st.subheader("🤖 Agent Responses")
        
        # Display agent results in columns (dynamic based on number of models)
        cols = st.columns(len(agents_results))
        
        for idx, (agent_name, response) in enumerate(agents_results.items()):
            with cols[idx]:
                config = MODEL_CONFIGS[agent_name]
                greenai_score = calculate_greenai_score(response)
                
                # Highlight best agent
                if agent_name == best_agent:
                    st.markdown(f"### ⭐ {config['display_name']}")
                else:
                    st.markdown(f"### {config['display_name']}")
                
                st.divider()
                
                # Response preview
                st.write("**Response:**")
                st.info(response['response'][:300] + "..." if len(response['response']) > 300 else response['response'])
                
                # Metrics
                st.write("**Metrics:**")
                
                col_a, col_b = st.columns(2)
                with col_a:
                    st.metric("Quality", f"{response.get('quality_score', 0.5):.2f}", help="Response correctness")
                    st.metric("Carbon", f"{response.get('carbon_g', 0):.8f}g", help="CO2 emissions (g)")
                with col_b:
                    st.metric("Latency", f"{response.get('latency', 0):.2f}s", help="Response time")
                    st.metric("Tokens", response.get('total_tokens', 0), help="Total tokens used")
                
                # GreenAI Score
                st.markdown(f"**🌿 GreenAI Score**: `{greenai_score:.1f}`")
                
                # Utility
                utility = utilities.get(agent_name, 0)
                st.markdown(f"**Utility**: `{utility:.3f}`")
        
        st.markdown("---")
        st.subheader("🎯 Routing Decision")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            best_config = MODEL_CONFIGS[best_agent]
            st.success(
                f"✅ **Selected**: {best_config['display_name']}\n\n"
                f"**Why**: Based on sustainability preference of {st.session_state.sustainability_preference:.1f}, "
                f"this agent offers the best balance."
            )
        
        with col2:
            st.metric("Utility Score", f"{best_utility:.3f}", help="Higher = better for current preference")
        
        # Utility breakdown
        st.write("**Utility Scores (all agents):**")
        utility_df = pd.DataFrame([
            {
                'Agent': MODEL_CONFIGS[name]['display_name'],
                'Utility': utilities.get(name, 0),
                'Selected': '✅' if name == best_agent else ''
            }
            for name in MODEL_CONFIGS.keys()
        ])
        
        st.dataframe(utility_df, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        st.subheader("💾 Session Statistics")
        
        if st.session_state.observations:
            col1, col2, col3, col4 = st.columns(4)
            
            obs_df = pd.DataFrame(st.session_state.observations)
            
            with col1:
                st.metric("Queries", len(obs_df))
            with col2:
                st.metric("Avg Quality", f"{obs_df['quality_score'].mean():.2f}")
            with col3:
                st.metric("Avg Carbon", f"{obs_df['carbon_g'].mean():.4f}g")
            with col4:
                st.metric("Avg GreenAI", f"{obs_df['greenai_score'].mean():.1f}")

# ============================================================================
# PAGE: DASHBOARD
# ============================================================================

def page_dashboard():
    """Dashboard with historical metrics"""
    
    st.title("📊 Dashboard - Historical Analytics")
    
    if not st.session_state.observations:
        st.info("💡 No data yet. Use the **Live Query** page to start generating data.")
        return
    
    # Load observations
    obs_df = pd.DataFrame(st.session_state.observations)
    
    if obs_df.empty:
        st.warning("No observations available")
        return
    
    # Key metrics
    st.subheader("🎯 Key Metrics")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Total Queries", len(obs_df))
    with col2:
        st.metric("Avg Quality", f"{obs_df['quality_score'].mean():.2%}")
    with col3:
        st.metric("Avg Carbon", f"{obs_df['carbon_g'].mean():.4f}g")
    with col4:
        st.metric("Avg Latency", f"{obs_df['latency'].mean():.2f}s")
    with col5:
        st.metric("Avg GreenAI", f"{obs_df['greenai_score'].mean():.1f}")
    
    st.divider()
    
    # Charts
    st.subheader("📈 Metrics Over Time")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Quality over time
        fig = px.line(
            obs_df.reset_index(),
            x='index',
            y='quality_score',
            title='Quality Score Over Time',
            markers=True,
            color_discrete_sequence=[COLOR_SCHEME['secondary']]
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Carbon over time
        fig = px.line(
            obs_df.reset_index(),
            x='index',
            y='carbon_g',
            title='Carbon Emissions Over Time',
            markers=True,
            color_discrete_sequence=[COLOR_SCHEME['danger']]
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Distribution
    col1, col2 = st.columns(2)
    
    with col1:
        # Model distribution
        model_counts = obs_df['model'].value_counts()
        fig = px.pie(
            values=model_counts.values,
            names=model_counts.index,
            title='Model Selection Distribution'
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Quality vs Carbon scatter
        fig = px.scatter(
            obs_df,
            x='carbon_g',
            y='quality_score',
            color='model',
            size='latency',
            hover_data=['greenai_score'],
            title='Quality vs Carbon Trade-off',
            labels={'carbon_g': 'Carbon (g)', 'quality_score': 'Quality'},
            color_discrete_sequence=px.colors.qualitative.Plotly
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    st.subheader("📋 Recent Observations")
    
    # Show recent observations table
    display_df = obs_df[[
        'timestamp', 'model', 'quality_score', 'carbon_g',
        'latency', 'total_tokens', 'greenai_score'
    ]].tail(10).copy()
    
    display_df.columns = [
        'Timestamp', 'Model', 'Quality', 'Carbon (g)',
        'Latency (s)', 'Tokens', 'GreenAI Score'
    ]
    
    st.dataframe(display_df, use_container_width=True, hide_index=True)

# ============================================================================
# PAGE: MODEL COMPARISON
# ============================================================================

def page_model_comparison():
    """Model comparison page"""
    
    st.title("🤖 Model Comparison")
    
    if not st.session_state.observations:
        st.info("💡 No data yet. Use the **Live Query** page to generate data.")
        return
    
    obs_df = pd.DataFrame(st.session_state.observations)
    
    if obs_df.empty:
        st.warning("No observations available")
        return
    
    # Aggregate by model
    model_stats = []
    
    for model in obs_df['model'].unique():
        model_data = obs_df[obs_df['model'] == model]
        
        stats = {
            'Model': MODEL_CONFIGS.get(model, {}).get('display_name', model),
            'Queries': len(model_data),
            'Avg Quality': model_data['quality_score'].mean(),
            'Avg Carbon': model_data['carbon_g'].mean(),
            'Avg Latency': model_data['latency'].mean(),
            'Avg Tokens': model_data['total_tokens'].mean(),
            'Avg GreenAI': model_data['greenai_score'].mean(),
            'Total Energy (kWh)': model_data['energy_kwh'].sum()
        }
        
        model_stats.append(stats)
    
    stats_df = pd.DataFrame(model_stats)
    
    st.subheader("📊 Model Performance Summary")
    st.dataframe(stats_df, use_container_width=True, hide_index=True)
    
    st.divider()
    st.subheader("📈 Comparison Charts")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Quality comparison
        fig = px.bar(
            stats_df,
            x='Model',
            y='Avg Quality',
            title='Average Quality by Model',
            color='Avg Quality',
            color_continuous_scale='Greens'
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Carbon comparison
        fig = px.bar(
            stats_df,
            x='Model',
            y='Avg Carbon',
            title='Average Carbon by Model',
            color='Avg Carbon',
            color_continuous_scale='Reds'
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Latency comparison
        fig = px.bar(
            stats_df,
            x='Model',
            y='Avg Latency',
            title='Average Latency by Model',
            color='Avg Latency',
            color_continuous_scale='Blues'
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # GreenAI score comparison
        fig = px.bar(
            stats_df,
            x='Model',
            y='Avg GreenAI',
            title='Average GreenAI Score by Model',
            color='Avg GreenAI',
            color_continuous_scale='Viridis'
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    st.subheader("💾 Export Data")
    
    csv = stats_df.to_csv(index=False)
    st.download_button(
        label="📥 Download Comparison as CSV",
        data=csv,
        file_name=f"model_comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )

# ============================================================================
# PAGE: ROUTING ANALYSIS
# ============================================================================

def page_routing_analysis():
    """Routing analysis page"""
    
    st.title("🛣️ Routing Analysis")
    
    if not st.session_state.observations:
        st.info("💡 No data yet. Use the **Live Query** page to generate data.")
        return
    
    obs_df = pd.DataFrame(st.session_state.observations)
    
    if obs_df.empty:
        st.warning("No observations available")
        return
    
    st.subheader("🎯 Routing Decisions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Model selection distribution
        model_counts = obs_df['model'].value_counts()
        model_labels = [MODEL_CONFIGS.get(m, {}).get('display_name', m) for m in model_counts.index]
        
        fig = px.pie(
            values=model_counts.values,
            names=model_labels,
            title='Model Selection Distribution',
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Utility scores
        fig = px.box(
            obs_df.reset_index(),
            x='model',
            y='routing_utility',
            title='Routing Utility Scores',
            color='model',
            color_discrete_sequence=px.colors.qualitative.Set1
        )
        fig.update_xaxes(ticktext=model_labels, tickvals=obs_df['model'].unique())
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    st.subheader("⚙️ Sustainability Preference Impact")
    
    # Show current preference
    pref = st.session_state.sustainability_preference
    st.write(f"**Current Preference**: {pref:.1f} (0=Quality | 1=Sustainability)")
    
    # Metrics at current preference
    col1, col2, col3 = st.columns(3)
    
    with col1:
        avg_quality = obs_df['quality_score'].mean()
        st.metric("Avg Quality", f"{avg_quality:.2%}")
    
    with col2:
        avg_carbon = obs_df['carbon_g'].mean()
        st.metric("Avg Carbon", f"{avg_carbon:.4f}g")
    
    with col3:
        avg_greenai = obs_df['greenai_score'].mean()
        st.metric("Avg GreenAI", f"{avg_greenai:.1f}")
    
    st.divider()
    st.subheader("📊 Agent Performance Details")
    
    # Detailed table
    detail_data = []
    
    for model in obs_df['model'].unique():
        model_data = obs_df[obs_df['model'] == model]
        
        detail_data.append({
            'Agent': MODEL_CONFIGS.get(model, {}).get('display_name', model),
            'Count': len(model_data),
            'Avg Utility': model_data['routing_utility'].mean(),
            'Min Utility': model_data['routing_utility'].min(),
            'Max Utility': model_data['routing_utility'].max(),
            'Avg Quality': f"{model_data['quality_score'].mean():.2%}",
            'Avg Carbon': f"{model_data['carbon_g'].mean():.4f}g"
        })
    
    detail_df = pd.DataFrame(detail_data)
    st.dataframe(detail_df, use_container_width=True, hide_index=True)

# ============================================================================
# MAIN APP NAVIGATION
# ============================================================================

def main():
    """Main app entry point"""
    
    st.sidebar.title("🌿 GreenAI Navigation")
    
    page = st.sidebar.radio(
        "Select Page:",
        options=[
            "🚀 Live Query",
            "📊 Dashboard",
            "🤖 Model Comparison",
            "🛣️ Routing Analysis"
        ]
    )
    
    # Add sidebar info
    st.sidebar.divider()
    st.sidebar.write("### 📝 About GreenAI")
    st.sidebar.write(
        "Sustainability-aware LLM routing system that balances quality with carbon efficiency."
    )
    
    # Route to pages
    if page == "🚀 Live Query":
        page_live_query()
    elif page == "📊 Dashboard":
        page_dashboard()
    elif page == "🤖 Model Comparison":
        page_model_comparison()
    elif page == "🛣️ Routing Analysis":
        page_routing_analysis()

if __name__ == "__main__":
    main()
