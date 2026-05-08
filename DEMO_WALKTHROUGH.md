# 🎬 GreenAI Demo Walkthrough

A step-by-step guide to demonstrate GreenAI's capabilities to an audience.

---

## Pre-Demo Checklist ✅

Before presenting:

- [ ] Python 3.10+ installed
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] Groq API key obtained (https://console.groq.com/keys)
- [ ] Streamlit app tested: `streamlit run streamlit_app/app.py`
- [ ] Internet connection stable
- [ ] Terminal/PowerShell open in project directory

---

## Demo Duration: ~10-15 minutes

---

## Part 1: Introduction (1-2 minutes)

### Opening Slide / Talking Points

> "GreenAI is a **sustainability-aware LLM routing system** that makes AI deployment environmentally responsible while maintaining quality."

**Key Points:**
- 🌍 Climate impact of AI is growing
- 🎯 Can we deploy AI effectively AND sustainably?
- ⚖️ GreenAI balances quality vs. carbon efficiency
- 🚀 Uses intelligent routing to pick the best agent

**Show the README or a simple diagram:**
- 3 LLM agents (Fast, Balanced, Precise)
- Smart router (learns continuously)
- Real-time sustainability scoring

---

## Part 2: Live Demo (8-10 minutes)

### Step 1: Launch the App (30 seconds)

```bash
cd c:\Users\g3gay\major
streamlit run streamlit_app/app.py
```

**Expected Output:**
```
  You can now view your Streamlit app in your browser.
  Local URL: http://localhost:8501
```

The browser should open automatically. If not, manually go to `http://localhost:8501`

### Step 2: Setup (1 minute)

**On the Live Query page** (default):

1. **Paste Groq API Key** in sidebar
   - "🔑 Groq API Key" input field
   - Paste your key: `gsk_...`
   - Press Enter

2. **Watch status change**
   - 🔴 → 🟡 → 🟢 (connecting... mock... connected!)
   - You'll see: "Status: Groq Connected" ✅

3. **Explain the components:**
   - "This is the configuration section"
   - "Sustainability preference controls quality vs. carbon trade-off"

### Step 3: First Query Demo (3-4 minutes)

**Query 1: Simple Question**

In the prompt field, enter:
```
Explain quantum computing in simple terms. What makes it different from regular computers?
```

Click "🔍 Query All Agents"

**While loading (show loading spinner):**
- "The system is now querying all 3 agents in parallel..."
- "Each agent has different parameters: temperature, max tokens"
- "They're optimized for different speed/quality trade-offs"

**Results appear:**

Show the 3 agent responses side-by-side:

1. **⚡ Fast Agent**
   - ✨ "Notice: Short response, very quick"
   - Point out: "Shortest response, 0.5s latency"
   - Carbon: Minimal (uses fewer tokens)

2. **⚖️ Balanced Agent** (highlighted with ⭐)
   - "This one was selected! Why?"
   - Explain: "Based on our preference of 0.5, it offers best utility"
   - Quality: Good, Carbon: Medium, Speed: Fast

3. **🔬 Precise Agent**
   - "Longest, most detailed response"
   - Latency: ~1.8s
   - Carbon: Highest (more tokens)

**Show the Routing Decision:**
- "Selected: agent_balanced (Utility: 0.XX)"
- "Green AI Score: XX.X"
- Explain the utility calculation

### Step 4: Sustainability Preference Impact (2-3 minutes)

**Interactive Demo:**

1. **Set preference to 0.0 (Quality First)**
   - Slider all the way left
   - Status changes: "🎯 Quality-First"

2. **Query again with same prompt** (copy-paste):
   ```
   Explain quantum computing in simple terms. What makes it different from regular computers?
   ```

3. **Watch routing change!**
   - "Notice which agent got selected this time"
   - Likely: Precise Agent (better quality)
   - Show utility scores changed
   - Quality is now valued higher

4. **Set preference to 1.0 (Sustainability First)**
   - Slider all the way right
   - Status: "🌱 Sustainability-First"

5. **Query one more time**

6. **Routing changes again!**
   - Likely: Fast Agent (minimal carbon)
   - Show: "See how changing the preference changes routing?"
   - Utility favors carbon efficiency

**Key Insight to Share:**
> "This demonstrates the core innovation: dynamic routing based on sustainability goals. Different organizations have different preferences, and GreenAI adapts automatically."

---

## Part 3: Analytics (2-3 minutes)

### Dashboard Page

Click: "📊 Dashboard" in sidebar

**Show:**
1. **Key Metrics Cards at top**
   - Total Queries: 3
   - Avg Quality: ~0.88
   - Avg Carbon: ~0.0012g
   - Avg Latency: ~1.1s
   - Avg GreenAI: ~83.4

2. **Time Series Graphs**
   - "Quality stayed consistent"
   - "Carbon varied based on which agent was selected"

3. **Model Selection Pie Chart**
   - "See how many times each agent was selected"
   - Changes based on the preference settings we used

4. **Quality vs Carbon Scatter**
   - "Each dot is a query"
   - "Notice the trade-off: Fast is low-carbon, Precise is high-quality"

**Insight:**
> "This is the classic sustainability trade-off visualization. No one agent is best at everything."

### Model Comparison Page

Click: "🤖 Model Comparison" in sidebar

**Show:**
1. **Summary Table**
   - Agent stats (queries, quality, carbon, latency, GreenAI score)
   - "Fast Agent: Low carbon, lower quality"
   - "Precise Agent: High quality, higher carbon"
   - "Balanced Agent: Sweet spot"

2. **Bar Charts**
   - Quality by agent
   - Carbon by agent
   - Latency by agent
   - GreenAI score by agent

### Routing Analysis Page

Click: "🛣️ Routing Analysis" in sidebar

**Show:**
1. **Model Selection Pie**
   - "This shows routing history"
   - How many times each agent was selected

2. **Routing Utility Box Plot**
   - "Higher utility = better selection for current preference"

3. **Agent Performance Table**
   - Shows min/max/avg utility for each agent

**Narrate:**
> "This is how we measure routing effectiveness. We track predicted utility and actual performance. Over time, the system learns which agent performs best under which conditions."

---

## Part 4: Key Takeaways (1 minute)

**Summarize:**

1. **Live Querying**
   - Users can submit any task
   - See all agents compete
   - Understand routing decisions

2. **Sustainability Preference**
   - Simple slider to control quality vs. carbon trade-off
   - Different needs → different preferences
   - Dynamic routing adapts automatically

3. **Real-Time Analytics**
   - Track sustainability metrics
   - Monitor model performance
   - Learn from each query

4. **Research Innovation**
   - Online learning for continuous improvement
   - Carbon estimation for environmental impact
   - Intelligent routing balancing multiple objectives

**Future Vision:**
> "Imagine deploying thousands of AI agents across your infrastructure, each making smart decisions about quality and sustainability. That's the power of GreenAI."

---

## Q&A Talking Points

### Q: "How do you estimate carbon?"
**A:** "We track token usage (input + output) and multiply by energy per token based on research literature. Different model sizes have different energy profiles. Then we multiply by carbon intensity of electricity grid."

### Q: "What if I don't have a Groq API key?"
**A:** "The system automatically falls back to mock mode (🟡). For demos, it's actually perfect since you get instant responses without API costs!"

### Q: "Can I add my own models?"
**A:** "Yes! Edit the agent config. You can add any model accessible via API. The routing and scoring works with any LLM backend."

### Q: "How much does this save in carbon?"
**A:** "Depends on baseline. If you were using the Precise agent for everything, routing intelligently to Fast agent for simple queries can reduce carbon by 50-80% with minimal quality loss."

### Q: "Is this production-ready?"
**A:** "This is a research demonstration of the core concepts. For production, you'd add database persistence, multi-user auth, error handling, etc. But the routing and learning logic is solid."

---

## Troubleshooting During Demo

### App Won't Start
```bash
# Kill any existing Streamlit process
# Then run:
python -m streamlit run streamlit_app/app.py --logger.level=debug
```

### API Key Won't Connect
- **Don't panic!** Immediately say: "Let me show you mock mode, which is great for demos anyway"
- Remove/clear the key
- Refresh page: F5
- System auto-switches to 🟡 Mock Mode

### Graphs Don't Show
- Usually Plotly rendering issue
- Try refreshing browser (F5)
- Or click a different page and back

### Streamlit Lags
- Make sure internet is stable
- Groq API is typically very fast
- Latency is from rendering, not API

---

## Post-Demo Discussion

### Topics to Mention

1. **Limitations**
   - Currently supports Groq models
   - Mock mode uses simple simulation
   - No database (CSV only)
   - Single-user demo

2. **What's Next**
   - Add real LLMs (OpenAI, HuggingFace)
   - Batch processing
   - Multi-tenant support
   - Advanced ML models

3. **Real-World Impact**
   - Companies use similar routing for cost optimization
   - Carbon tracking is emerging ESG requirement
   - Combination is novel

### Suggested Questions for Audience

- "What if your company had sustainability goals? How would this help?"
- "How would you decide between quality and carbon?"
- "Can you think of use cases where carbon matters most?"

---

## Recording Tips (if recording)

1. **Frame**: Show browser full-screen
2. **Resolution**: 1920x1080 minimum
3. **Font Size**: Use Streamlit zoom if needed (`Ctrl + +`)
4. **Mic**: Speak clearly and pause between actions
5. **Pacing**: Let queries finish before next action

---

## Time Breakdown

| Section | Time | Actions |
|---------|------|---------|
| Intro | 1-2 min | Explain concept |
| Setup | 1 min | Add API key |
| Query 1 | 1 min | Simple question, see results |
| Query 2 | 1 min | Preference 0.0, different routing |
| Query 3 | 1 min | Preference 1.0, see change again |
| Dashboard | 1 min | Show metrics & charts |
| Comparison | 1 min | Show agent stats |
| Routing | 1 min | Show routing decisions |
| Summary | 1 min | Key takeaways |
| Q&A | 2-3 min | Answer questions |

**Total: 11-15 minutes** (flexible)

---

## Success Metrics

✅ Successful demo if:
- App launches without errors
- API connects (or mock mode activates)
- User can see agent responses
- Routing changes when preference changes
- Dashboard shows meaningful metrics
- Audience understands the concept

---

## Post-Demo Materials

After the demo, you can:

1. **Share Results**
   - Download comparison CSV (button on comparison page)
   - Screenshot dashboard
   - Share outputs folder

2. **Code**
   - Share GitHub link (if available)
   - Show streamlit_app/app.py source
   - Highlight key routing logic

3. **Contact**
   - Email address for follow-ups
   - Links to Groq (https://groq.com)
   - LinkedIn/Twitter handles

---

**Happy Demoing! 🌿**

Remember: This is about **impact**, not perfection. Even small hiccups can be learning moments ("See how the system automatically handled that?")

---

**Last Updated**: May 2026
**Duration**: ~15 minutes
**Best For**: Academic presentations, investor pitches, technical audiences
