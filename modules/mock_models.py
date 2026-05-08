"""
GreenAI Mock LLM Simulator
Generates realistic mock responses when Groq API is unavailable
"""

import time
import random
import numpy as np
from typing import Dict, Tuple
from modules.config import (
    MOCK_QUALITY_RANGES, MOCK_TOKEN_CONFIG, MOCK_RESPONSES,
    TASK_TYPES, ENERGY_PER_TOKEN, CARBON_INTENSITY
)


class MockModelSimulator:
    """Generates realistic mock responses for testing without API"""
    
    def __init__(self, seed: int = 42):
        self.seed = seed
        random.seed(seed)
        np.random.seed(seed)
    
    def generate_response(
        self,
        model_name: str,
        prompt: str,
        task_type: str = 'qa'
    ) -> Dict:
        """
        Generate a mock response with realistic metrics
        
        Args:
            model_name: 'agent_fast', 'agent_balanced', 'agent_precise'
            prompt: Input prompt text
            task_type: 'sentiment', 'qa', 'spam', 'reasoning'
        
        Returns:
            Dict with response, tokens, latency, quality
        """
        
        # Get task difficulty
        task_info = TASK_TYPES.get(task_type, TASK_TYPES['qa'])
        difficulty = task_info['difficulty']
        
        # Generate response text
        response_text = self._generate_response_text(task_type, model_name)
        
        # Calculate tokens
        input_tokens = len(prompt.split())
        output_tokens = self._calculate_output_tokens(model_name, response_text, input_tokens)
        total_tokens = input_tokens + output_tokens
        
        # Calculate latency (with some randomness)
        latency = self._calculate_latency(model_name, total_tokens)
        
        # Generate quality score based on task difficulty and model
        quality_score = self._generate_quality_score(model_name, difficulty, task_type)
        
        # Calculate energy and carbon
        energy_kwh = self._calculate_energy(model_name, total_tokens)
        carbon_g = energy_kwh * CARBON_INTENSITY
        
        return {
            'success': True,
            'model': model_name,
            'response': response_text,
            'input_tokens': input_tokens,
            'output_tokens': output_tokens,
            'total_tokens': total_tokens,
            'latency': latency,
            'quality_score': quality_score,
            'energy_kwh': energy_kwh,
            'carbon_g': carbon_g,
            'timestamp': time.time(),
            'is_mock': True
        }
    
    def _generate_response_text(self, task_type: str, model_name: str) -> str:
        """Generate contextual response based on task type"""
        
        responses = MOCK_RESPONSES.get(task_type, {})
        if not responses:
            return "This is a mock response generated for testing purposes."
        
        # Select a response
        response = random.choice(list(responses.values()))
        
        # Add model-specific variations based on max_tokens (speed/quality trade-off)
        from modules.config import MODEL_CONFIGS
        model_config = MODEL_CONFIGS.get(model_name, {})
        max_tokens = model_config.get('max_tokens', 512)
        
        if max_tokens <= 512:  # Fast models
            # Shorter response
            sentences = response.split('.')
            response = '.'.join(sentences[:max(1, len(sentences)//2)]) + '.'
        elif max_tokens >= 2048:  # Precise models
            # Add more detail
            response += ' This response has been carefully considered to ensure accuracy and completeness.'
        
        return response
    
    def _calculate_output_tokens(self, model_name: str, response: str, input_tokens: int) -> int:
        """Calculate output tokens based on response length and model config"""
        
        config = MOCK_TOKEN_CONFIG.get(model_name)
        if config is None:
            # Fallback to balanced config if model not found
            config = MOCK_TOKEN_CONFIG.get('mixtral-8x7b-32768', MOCK_TOKEN_CONFIG['gemma2-9b-it'])
        
        # Base tokens + adjustments
        base = config['base_output_tokens']
        response_tokens = len(response.split())
        
        # Add some randomness (±10%)
        multiplier = random.uniform(0.9, 1.1)
        output_tokens = int((base + response_tokens) * multiplier)
        
        return max(10, output_tokens)  # Minimum 10 tokens
    
    def _calculate_latency(self, model_name: str, total_tokens: int) -> float:
        """Calculate latency based on model and token count"""
        
        config = MOCK_TOKEN_CONFIG.get(model_name)
        if config is None:
            # Fallback to balanced config if model not found
            config = MOCK_TOKEN_CONFIG.get('mixtral-8x7b-32768', MOCK_TOKEN_CONFIG['gemma2-9b-it'])
        
        # Base latency + token-dependent latency
        base_latency = config['latency_base']
        token_latency = (total_tokens / 1000) * config['latency_multiplier']
        
        latency = base_latency + token_latency
        
        # Add small random jitter (±5%)
        jitter = random.uniform(0.95, 1.05)
        
        return latency * jitter
    
    def _generate_quality_score(self, model_name: str, difficulty: str, task_type: str) -> float:
        """Generate quality score based on model, difficulty, and task type"""
        
        # Base quality range for this difficulty
        quality_min, quality_max = MOCK_QUALITY_RANGES.get(difficulty, (0.7, 0.85))
        
        # Model-specific adjustments based on model tier
        from modules.config import MODEL_CONFIGS
        model_config = MODEL_CONFIGS.get(model_name, {})
        max_tokens = model_config.get('max_tokens', 512)
        
        if max_tokens <= 512:  # Fast models
            quality_min -= 0.05  # Fast is less accurate
            quality_max -= 0.05
        elif max_tokens >= 2048:  # Precise models
            quality_min += 0.05  # Precise is more accurate
            quality_max += 0.05
        
        # Clamp to [0, 1]
        quality_min = max(0, min(1, quality_min))
        quality_max = max(0, min(1, quality_max))
        
        # Generate quality with some randomness
        quality = random.uniform(quality_min, quality_max)
        
        return round(quality, 3)
    
    def _calculate_energy(self, model_name: str, total_tokens: int) -> float:
        """Calculate energy consumption in kWh"""
        
        energy_per_token = ENERGY_PER_TOKEN.get(model_name, ENERGY_PER_TOKEN['default'])
        energy_kwh = total_tokens * energy_per_token
        
        return energy_kwh
    
    def generate_batch(self, model_name: str, prompts: list, task_types: list = None) -> list:
        """Generate responses for multiple prompts"""
        
        if task_types is None:
            task_types = ['qa'] * len(prompts)
        
        results = []
        for prompt, task_type in zip(prompts, task_types):
            result = self.generate_response(model_name, prompt, task_type)
            results.append(result)
            time.sleep(0.01)  # Small delay between requests
        
        return results


# Convenience function
def create_mock_simulator(seed: int = 42) -> MockModelSimulator:
    """Factory function to create simulator"""
    return MockModelSimulator(seed=seed)


if __name__ == '__main__':
    # Test the simulator
    simulator = MockModelSimulator()
    
    test_prompts = [
        "I love this product! It's amazing.",
        "What is the capital of France?",
        "Classify as SPAM or NOT SPAM: 'Click here to win $1000!'",
        "If A > B and B > C, is A > C?"
    ]
    
    test_types = ['sentiment', 'qa', 'spam', 'reasoning']
    
    for prompt, task_type in zip(test_prompts, test_types):
        print(f"\n📝 Task: {task_type}")
        print(f"Prompt: {prompt}")
        
        for model in ['agent_fast', 'agent_balanced', 'agent_precise']:
            result = simulator.generate_response(model, prompt, task_type)
            print(f"\n  {model}:")
            print(f"    Response: {result['response'][:60]}...")
            print(f"    Tokens: {result['total_tokens']} | Quality: {result['quality_score']:.2f}")
            print(f"    Carbon: {result['carbon_g']:.4f}g | Latency: {result['latency']:.2f}s")
