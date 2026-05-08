#!/usr/bin/env python
"""Generate sample observations for GreenAI demo"""

import sys
import json
from datetime import datetime, timedelta
sys.path.insert(0, '.')

from modules.mock_models import MockModelSimulator
from modules.data_utils import DataExporter
from modules.config import AGENT_CONFIGS

print("=" * 70)
print("🌿 GreenAI - Sample Data Generator")
print("=" * 70)

# Sample prompts for variety
SAMPLE_PROMPTS = [
    ("What is machine learning?", "qa"),
    ("I love this product! Excellent quality.", "sentiment"),
    ("Explain quantum computing in simple terms.", "qa"),
    ("This is the worst service ever!", "sentiment"),
    ("What is the capital of France?", "qa"),
    ("Classify: Is this spam - 'Click here to win $1000'?", "spam"),
    ("If A > B and B > C, is A > C?", "reasoning"),
    ("The movie was okay, nothing special.", "sentiment"),
    ("How do neural networks work?", "qa"),
    ("Urgent: Verify your account now!", "spam"),
]

# Initialize simulator
simulator = MockModelSimulator(seed=42)
exporter = DataExporter('outputs')

print(f"\n📊 Generating {len(SAMPLE_PROMPTS)} sample queries...")
print(f"📦 Querying {len(AGENT_CONFIGS)} agents per prompt...\n")

observations = []
timestamp_base = datetime.now() - timedelta(hours=len(SAMPLE_PROMPTS))

# Generate observations
for idx, (prompt, task_type) in enumerate(SAMPLE_PROMPTS):
    print(f"[{idx+1}/{len(SAMPLE_PROMPTS)}] {prompt[:40]}...")
    
    timestamp = timestamp_base + timedelta(minutes=idx*10)
    
    for agent_idx, (agent_name, agent_config) in enumerate(AGENT_CONFIGS.items()):
        # Generate response
        response = simulator.generate_response(agent_name, prompt, task_type)
        
        # Calculate GreenAI score (simplified)
        quality = response['quality_score']
        carbon = response['carbon_g']
        tokens = response['total_tokens']
        latency = response['latency']
        
        # Simplified scoring
        carbon_norm = 1 - min(carbon / 0.005, 1)
        token_eff = response['output_tokens'] / tokens if tokens > 0 else 0.5
        latency_eff = max(0, min(1, 1 - (latency / 10)))
        
        greenai_score = (
            0.4 * quality +
            0.3 * carbon_norm +
            0.2 * token_eff +
            0.1 * latency_eff
        ) * 100
        
        # Simulate routing utility
        pref = 0.5  # Balanced preference
        utility = (1 - pref) * quality + pref * carbon_norm
        
        observation = {
            'timestamp': timestamp.isoformat(),
            'model': agent_name,
            'task_id': f"{task_type}_{idx:03d}",
            'task_type': task_type,
            'prompt': prompt[:100],
            'response': response['response'][:200],
            'input_tokens': response['input_tokens'],
            'output_tokens': response['output_tokens'],
            'total_tokens': response['total_tokens'],
            'latency': round(response['latency'], 2),
            'quality_score': round(response['quality_score'], 3),
            'carbon_g': round(response['carbon_g'], 6),
            'energy_kwh': round(response['energy_kwh'], 8),
            'greenai_score': round(greenai_score, 1),
            'routing_utility': round(utility, 3),
            'predicted_quality': round(quality, 3),
            'predicted_carbon': round(carbon, 6),
            'sustainability_preference': 0.5
        }
        
        observations.append(observation)

print(f"\n✅ Generated {len(observations)} observations")

# Export to CSV
try:
    path = exporter.export_observations(observations, 'all_observations.csv')
    print(f"💾 Saved to: {path}")
except Exception as e:
    print(f"❌ Export failed: {e}")

# Create summary
print("\n📊 Sample Data Summary:")
print(f"   • Total observations: {len(observations)}")
print(f"   • Prompts: {len(SAMPLE_PROMPTS)}")
print(f"   • Agents: {len(AGENT_CONFIGS)}")
print(f"   • Time span: {(timestamp - timestamp_base).total_seconds() / 3600:.1f} hours")

# Calculate stats
import pandas as pd
df = pd.DataFrame(observations)

print(f"\n📈 Statistics:")
print(f"   • Avg Quality: {df['quality_score'].mean():.3f}")
print(f"   • Avg Carbon: {df['carbon_g'].mean():.6f}g")
print(f"   • Avg Latency: {df['latency'].mean():.2f}s")
print(f"   • Avg GreenAI: {df['greenai_score'].mean():.1f}")

print(f"\n🎯 By Model:")
for model in df['model'].unique():
    model_data = df[df['model'] == model]
    config = AGENT_CONFIGS.get(model, {})
    display_name = config.get('display_name', model)
    print(f"   • {display_name}: {len(model_data)} queries, quality={model_data['quality_score'].mean():.2f}, carbon={model_data['carbon_g'].mean():.6f}g")

print("\n" + "=" * 70)
print("✅ Sample data generated successfully!")
print("=" * 70)
print("\n🚀 Ready to run: streamlit run streamlit_app/app.py")
