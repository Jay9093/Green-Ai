#!/usr/bin/env python
"""Quick test of GreenAI modules"""

import sys
sys.path.insert(0, '.')

print("=" * 60)
print("🌿 GreenAI Module Test")
print("=" * 60)

# Test 1: Config
print("\n1️⃣  Testing Config Module...")
try:
    from modules.config import AGENT_CONFIGS, GREENAI_WEIGHTS, ENERGY_PER_TOKEN
    print("   ✅ Config imported successfully")
    print(f"   - Agents: {list(AGENT_CONFIGS.keys())}")
    print(f"   - Weights: {GREENAI_WEIGHTS}")
    print(f"   - Energy per token defined for {len(ENERGY_PER_TOKEN)} models")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 2: Mock Models
print("\n2️⃣  Testing Mock Models...")
try:
    from modules.mock_models import MockModelSimulator
    sim = MockModelSimulator()
    result = sim.generate_response('agent_fast', 'What is AI?', 'qa')
    print("   ✅ Mock simulator working")
    print(f"   - Response: {result['response'][:60]}...")
    print(f"   - Tokens: {result['total_tokens']} | Carbon: {result['carbon_g']:.6f}g")
    print(f"   - Latency: {result['latency']:.2f}s | Quality: {result['quality_score']:.2f}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 3: Data Utils
print("\n3️⃣  Testing Data Utils...")
try:
    from modules.data_utils import DataExporter, DataLoader, DataAggregator
    import pandas as pd
    
    exporter = DataExporter('outputs')
    print("   ✅ Data utilities loaded")
    
    # Create sample data
    sample = [
        {
            'timestamp': '2026-05-07T10:00:00',
            'model': 'agent_fast',
            'quality_score': 0.85,
            'carbon_g': 0.001,
            'greenai_score': 82.5
        }
    ]
    
    # Try export
    path = exporter.export_observations(sample, 'test_sample.csv')
    print(f"   - Exported sample to: {path}")
    
    # Try load
    df = DataLoader.load_observations(path)
    print(f"   - Loaded {len(df)} observations back")
    
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 4: Integration
print("\n4️⃣  Testing Integration...")
try:
    from modules.config import GREENAI_WEIGHTS
    from modules.mock_models import MockModelSimulator
    
    # Simulate a query and scoring
    sim = MockModelSimulator()
    responses = {}
    
    for agent in AGENT_CONFIGS.keys():
        result = sim.generate_response(agent, 'Test question', 'qa')
        responses[agent] = result
    
    print(f"   ✅ Generated responses from all {len(responses)} agents")
    
    # Show summary
    for agent, resp in responses.items():
        print(f"   - {agent}: {resp['total_tokens']} tokens, {resp['carbon_g']:.6f}g CO2")
        
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "=" * 60)
print("✅ All module tests completed!")
print("=" * 60)
print("\n🚀 Next: Run 'streamlit run streamlit_app/app.py'")
