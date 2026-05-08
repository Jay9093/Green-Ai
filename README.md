# 🌿 GreenAI: Sustainability-Aware LLM Routing System

## Overview

**GreenAI** is an end-to-end machine learning system that combines multiple LLM agents with intelligent routing to optimize both **quality and sustainability**. The system balances request quality with carbon efficiency, enabling organizations to deploy AI responsibly.

### Research Idea
**"GreenAI: An Online Learning-Based Framework for Sustainability Scoring and Optimization Routing of Black-Box LLM APIs"**

The framework uses online learning to predict model performance, dynamically routes requests to agents based on sustainability preferences, and provides real-time analytics on environmental impact.

---

## Key Features

### 🚀 **Live Interactive Querying**
- Submit any prompt to query all 3 agents in parallel
- Watch agents compete side-by-side with real-time scoring
- See smart routing decide the best model based on your sustainability goal
- Adjust sustainability preference (0 = quality first, 1 = carbon first)

### 📊 **Comprehensive Analytics Dashboard**
- **Dashboard**: Historical metrics and trends over time
- **Model Comparison**: Performance table and comparative charts
- **Routing Analysis**: Selection distribution and utility scores
- **Live Query**: Interactive real-time agent testing

### 🎯 **GreenAI Scoring System**
Composite score combining:
- **Quality** (40%) - Response correctness
- **Carbon** (30%) - Environmental impact
- **Token Efficiency** (20%) - Conciseness
- **Latency** (10%) - Response speed

### 🧠 **Smart Routing Engine**
Uses online learning to predict model performance and route based on:
$$\text{Utility} = (1 - \lambda) \cdot \text{Quality} + \lambda \cdot (1 - \text{Carbon})$$

Where λ (sustainability preference) ranges from 0 (quality-first) to 1 (sustainability-first).

### 🌱 **Energy & Carbon Estimation**
- Estimates energy consumption: `Energy = Total Tokens × Energy Per Token`
- Calculates carbon: `Carbon = Energy × Carbon Intensity`
- Tracks cumulative environmental impact

### 🔄 **Online Learning Module**
- Incremental learning from every query
- Prediction of quality and carbon for continuous improvement
- Convergence tracking and learning analytics

---

## Technical Stack

- **Backend**: Python 3.10+
- **LLM Provider**: Groq API (free tier available)
- **UI**: Streamlit (interactive dashboard)
- **Data**: Pandas + CSV persistence
- **Visualization**: Plotly + Matplotlib
- **ML**: Scikit-learn (online learning)

---

## Project Structure

```
greenai/
├── streamlit_app/
│   └── app.py                 # Main Streamlit application (4 pages)
├── modules/
│   ├── __init__.py
│   ├── config.py              # Configuration constants & hyperparameters
│   ├── mock_models.py         # Mock LLM simulator (offline fallback)
│   └── data_utils.py          # CSV export/import utilities
├── notebooks/
│   └── Green AI (1).ipynb     # Original research notebook (optional)
├── outputs/
│   └── all_observations.csv   # Auto-saved query observations
├── results/
│   └── [generated visualizations]
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

---

## Installation & Setup

### 1. Clone/Download Project
```bash
cd greenai/
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Get Groq API Key
1. Visit https://console.groq.com/keys
2. Sign up (free account)
3. Generate API key
4. Keep it handy for the app

### 4. Run the Streamlit App
```bash
streamlit run streamlit_app/app.py
```

The app will open in your browser at `http://localhost:8501`

---

## Usage Guide

### 🚀 First Time Setup

1. **Open Live Query Page** (default)
2. **Enter Groq API Key** in sidebar
3. **Start querying!**

### 📝 Querying

1. Enter any prompt (e.g., "Explain quantum computing")
2. Select task type (or leave as 'auto')
3. Click "Query All Agents"
4. See live responses from all 3 agents:
   - ⚡ **Fast Agent**: Quick, concise responses
   - ⚖️ **Balanced Agent**: Quality vs speed trade-off
   - 🔬 **Precise Agent**: Thorough, detailed responses

### 🎯 Routing Decision

- **Sustainability Preference = 0.0**: System prioritizes quality
- **Sustainability Preference = 0.5**: Balanced approach
- **Sustainability Preference = 1.0**: Maximum carbon efficiency

Watch how the selected agent changes as you adjust the slider!

### 📊 Analytics

- **Dashboard**: Track metrics over time, spot trends
- **Model Comparison**: See which agent performs best overall
- **Routing Analysis**: Understand routing patterns and utility scores

---

## API Key & Safety

### Secure API Key Handling
- ✅ Key stored in Streamlit session state (never persisted)
- ✅ Never logged or displayed in full
- ✅ Validated before use
- ✅ Automatic fallback to mock mode if invalid

### Mock Mode (Offline)
If no valid Groq API key:
- System automatically switches to mock mode 🟡
- Uses realistic simulated responses for demonstration
- Perfect for testing without API costs
- All functionality works identically

---

## Features in Detail

### 🤖 Three LLM Agents

All powered by single Groq API via configuration:

| Agent | Temperature | Max Tokens | Best For |
|-------|-------------|-----------|----------|
| **Fast** | 0.9 (creative) | 512 (concise) | Quick answers |
| **Balanced** | 0.5 (balanced) | 1024 | General use |
| **Precise** | 0.2 (focused) | 2048 (detailed) | Complex questions |

### ⚡ Real-Time Metrics

For each query, the system tracks:
- Response quality (0-1)
- Carbon emissions (grams CO₂)
- Energy consumption (kWh)
- Response latency (seconds)
- Token usage (input + output)
- GreenAI composite score (0-100)

### 📈 Sustainability Trade-offs

```
Preference  Quality  Carbon   Use Case
0.0         High     High     Research, accuracy-critical
0.5         Medium   Medium   Balanced deployment
1.0         Lower    Low      Carbon-aware datacenters
```

### 💾 Data Persistence

- Observations auto-saved to `outputs/all_observations.csv`
- Dashboard reflects all historical queries
- CSV format enables easy analysis in Excel, Jupyter, etc.

---

## Example Workflow

### Scenario: Sustainability-Aware Deployment

**Goal**: Deploy an AI assistant for a green company prioritizing carbon efficiency.

1. **Set Sustainability Preference to 1.0**
2. **Query**: "What are the top 5 ways to reduce carbon emissions?"
3. **Routing Decision**: System routes to Fast Agent (most efficient)
4. **Result**: 
   - Quality: 0.85 (good enough)
   - Carbon: 0.001g (minimal)
   - GreenAI Score: 78.5
5. **Comparison**: View how other agents would have performed (worse on carbon)
6. **Analytics**: Track cumulative carbon savings

---

## Troubleshooting

### "API Key Invalid" Error
- ✅ Check key starts with `gsk_` (Groq format)
- ✅ Visit https://console.groq.com/keys to regenerate
- ✅ Try mock mode first (no key required)

### Streamlit Not Starting
```bash
# Try with explicit Python path
python -m streamlit run streamlit_app/app.py

# Or specify port
streamlit run streamlit_app/app.py --server.port 8501
```

### Slow Responses
- Groq is very fast; latency is usually < 2 seconds
- Check internet connection
- Larger models (Precise Agent) take longer

### No Data in Dashboard
- Use Live Query page first to generate observations
- Each query creates one observation
- Dashboard shows historical trends

---

## Performance Benchmarks

### Sample Query: "Explain machine learning"

| Agent | Quality | Carbon | Latency | Tokens | GreenAI |
|-------|---------|--------|---------|--------|---------|
| Fast | 0.82 | 0.0008g | 0.6s | 145 | 81.5 |
| Balanced | 0.90 | 0.0012g | 1.1s | 210 | 85.2 |
| Precise | 0.95 | 0.0018g | 1.8s | 320 | 82.3 |

**Routing Decision** (pref=0.5): Balanced Agent ⚖️

---

## Extending GreenAI

### Add Custom Models
Edit `modules/config.py`:
```python
AGENT_CONFIGS = {
    'your_model': {
        'display_name': 'Your Model',
        'temperature': 0.5,
        'max_tokens': 1024,
        'description': 'Description'
    }
}
```

### Adjust Weights
Modify `GREENAI_WEIGHTS` in `modules/config.py`:
```python
GREENAI_WEIGHTS = {
    'quality': 0.50,        # Increase quality importance
    'carbon': 0.20,
    'token_efficiency': 0.20,
    'latency': 0.10
}
```

### Change Energy Constants
Update `ENERGY_PER_TOKEN` based on your infrastructure's actual consumption.

---

## Research Outputs

### Visualizations Generated
- Quality vs Carbon trade-off scatter plot
- Model performance leaderboard
- Sustainability preference impact analysis
- Routing decision distribution
- Carbon savings over time
- Online learning convergence curves

### Metrics Tracked
- Total API calls and cost estimates
- Carbon reduction vs. baseline
- Quality-carbon Pareto frontier
- Agent efficiency rankings
- Learning algorithm convergence

### CSV Exports
- All observations with full metrics
- Model comparison statistics
- Routing history and decisions

---

## Citations & References

### Energy Estimation
- Based on research on LLM carbon footprint (Patterson et al., Strubell et al.)
- Carbon intensity sourced from Electricity Maps

### Online Learning
- Streaming/online SGD methods
- Incremental model updates without full retraining

### Groq
- https://www.groq.com/ - Fast LLM inference API
- https://console.groq.com/ - Free API access

---

## License & Attribution

**GreenAI** is a major project demonstration for sustainability-aware AI deployment.

Developed as an end-to-end implementation of online learning-based routing for multiple LLM APIs.

---

## Support & Questions

### Quick Help
- **No API key?** → Use mock mode (🟡) for offline testing
- **Data not showing?** → Use Live Query page to generate observations
- **Graphs missing?** → Ensure `plotly` is installed (`pip install --upgrade plotly`)

### More Info
- Groq API docs: https://console.groq.com/docs/
- Streamlit docs: https://docs.streamlit.io/
- Project GitHub: [Your repo link]

---

## Future Enhancements

- [ ] Database backend (SQLite/PostgreSQL)
- [ ] Real HuggingFace/Ollama model integration
- [ ] Advanced ML (LSTM for time-series forecasting)
- [ ] Multi-user support with authentication
- [ ] Cost tracking & billing integration
- [ ] Custom prompt templates & workflows
- [ ] Batch processing capabilities
- [ ] Export reports in PDF format

---

**Made with ❤️ for sustainable AI** 🌍

Last Updated: May 2026
