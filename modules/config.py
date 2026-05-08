"""
GreenAI Configuration Constants
Centralized hyperparameters, energy constants, and model configurations
"""

# ============================================================================
# MODEL CONFIGURATION
# ============================================================================

# Groq agent configurations (simulated via temperature + max_tokens)
MODEL_CONFIGS = {
    "llama3-8b-8192": {
        "display_name": "Llama3 8B",
        "temperature": 0.7,
        "max_tokens": 512
    },

    "mixtral-8x7b-32768": {
        "display_name": "Mixtral 8x7B",
        "temperature": 0.5,
        "max_tokens": 1024
    },

    "llama3-70b-8192": {
        "display_name": "Llama3 70B",
        "temperature": 0.2,
        "max_tokens": 2048
    },

    "gemma2-9b-it": {
        "display_name": "Gemma2 9B",
        "temperature": 0.6,
        "max_tokens": 768
    }
}

# ============================================================================
# ENERGY & SUSTAINABILITY CONSTANTS
# ============================================================================

# Energy per token (kWh per token) - based on research literature
ENERGY_PER_TOKEN = {
    'llama3-8b-8192': 0.0000012,      # Fast (low max_tokens)
    'gemma2-9b-it': 0.0000015,        # Balanced (medium max_tokens)
    'mixtral-8x7b-32768': 0.0000015,  # Balanced (medium max_tokens)
    'llama3-70b-8192': 0.0000020,     # Precise (high max_tokens)
    'default': 0.0000015
}

# Carbon intensity (g CO2/kWh) - global average ~475
CARBON_INTENSITY = 475  # grams CO2 per kWh

# ============================================================================
# GREENAI SCORING WEIGHTS
# ============================================================================

GREENAI_WEIGHTS = {
    'quality': 0.40,            # Most important (0-40%)
    'carbon': 0.30,             # Sustainability (30%)
    'token_efficiency': 0.20,   # Conciseness (20%)
    'latency': 0.10             # Speed (10%)
}

# ============================================================================
# ROUTING & LEARNING PARAMETERS
# ============================================================================

DEFAULT_SUSTAINABILITY_PREFERENCE = 0.5  # Balance between quality (0) and sustainability (1)

ROUTING_EXPLORATION_RATE = 0.1  # 10% chance to try second-best model

# Online learning window (only look at last N observations)
OBSERVATION_WINDOW = 20

# ============================================================================
# TASK TYPES & DIFFICULTY
# ============================================================================

TASK_TYPES = {
    'sentiment': {'difficulty': 'easy', 'avg_quality_multiplier': 1.0},
    'qa': {'difficulty': 'easy', 'avg_quality_multiplier': 0.95},
    'spam': {'difficulty': 'medium', 'avg_quality_multiplier': 0.90},
    'reasoning': {'difficulty': 'hard', 'avg_quality_multiplier': 0.80}
}

# ============================================================================
# MOCK RESPONSE GENERATION PARAMETERS
# ============================================================================

# Base token counts for mock responses (tokens = base + prompt_tokens * multiplier)
MOCK_TOKEN_CONFIG = {
    'llama3-8b-8192': {
        'base_output_tokens': 50,
        'output_multiplier': 0.5,
        'latency_base': 0.5,
        'latency_multiplier': 0.3
    },
    'gemma2-9b-it': {
        'base_output_tokens': 150,
        'output_multiplier': 0.8,
        'latency_base': 0.8,
        'latency_multiplier': 0.4
    },
    'mixtral-8x7b-32768': {
        'base_output_tokens': 150,
        'output_multiplier': 0.8,
        'latency_base': 1.0,
        'latency_multiplier': 0.5
    },
    'llama3-70b-8192': {
        'base_output_tokens': 300,
        'output_multiplier': 1.2,
        'latency_base': 1.5,
        'latency_multiplier': 0.7
    }
}

# Quality score ranges based on task difficulty (for mock responses)
MOCK_QUALITY_RANGES = {
    'easy': (0.85, 0.95),      # Easy tasks: high quality
    'medium': (0.70, 0.85),    # Medium tasks: moderate quality
    'hard': (0.60, 0.80)       # Hard tasks: lower quality
}

# ============================================================================
# CSV OUTPUT CONFIGURATION
# ============================================================================

CSV_COLUMNS = [
    'timestamp',
    'model',
    'task_id',
    'task_type',
    'prompt',
    'response',
    'input_tokens',
    'output_tokens',
    'total_tokens',
    'latency',
    'quality_score',
    'carbon_g',
    'energy_kwh',
    'greenai_score',
    'routing_utility',
    'predicted_quality',
    'predicted_carbon',
    'sustainability_preference'
]

# ============================================================================
# API & TIMEOUT CONFIGURATION
# ============================================================================

GROQ_API_TIMEOUT = 30  # seconds
REQUEST_RETRY_COUNT = 2
RATE_LIMIT_DELAY = 0.5  # seconds between requests

# ============================================================================
# UI/STREAMLIT CONFIGURATION
# ============================================================================

STREAMLIT_CONFIG = {
    'page_title': '🌿 GreenAI - Sustainability-Aware LLM Routing',
    'page_icon': '🌿',
    'layout': 'wide',
    'initial_sidebar_state': 'expanded'
}

# Sidebar settings
SIDEBAR_CONFIG = {
    'max_api_key_display_length': 20,  # Show only last N chars of API key
    'sustainability_min': 0.0,
    'sustainability_max': 1.0,
    'sustainability_step': 0.1
}

# Color scheme for visualizations
COLOR_SCHEME = {
    'primary': '#2ecc71',        # Green (sustainability)
    'secondary': '#3498db',      # Blue (quality)
    'warning': '#f39c12',        # Orange (latency)
    'danger': '#e74c3c',         # Red (carbon)
    'neutral': '#95a5a6'         # Gray
}

# ============================================================================
# MOCK DATA GENERATION (for demo)
# ============================================================================

MOCK_RESPONSES = {
    'sentiment': {
        'positive': 'The sentiment in this text is positive. The language conveys enthusiasm, satisfaction, or positive emotion.',
        'negative': 'The sentiment in this text is negative. The language indicates dissatisfaction, frustration, or negative emotion.',
        'neutral': 'The sentiment in this text is neutral. The language is factual and does not strongly convey positive or negative emotion.'
    },
    'qa': {
        'short': 'The answer is provided above in the question.',
        'medium': 'Based on the information provided in the question, a comprehensive answer would be the one stated.',
        'long': 'This question requires a detailed response that considers multiple aspects and provides thorough explanation.'
    },
    'spam': {
        'spam': 'This appears to be SPAM - it contains typical spam indicators.',
        'not_spam': 'This does not appear to be spam - it seems to be legitimate communication.'
    },
    'reasoning': {
        'logic': 'Based on logical inference and deduction, the conclusion is valid.',
        'calculation': 'Through step-by-step calculation, the answer can be determined.',
        'analysis': 'After careful analysis of the given constraints, the result follows logically.'
    }
}

# ============================================================================
# LOGGING & DEBUGGING
# ============================================================================

DEBUG_MODE = False  # Set to True for verbose logging
LOG_QUERIES = True  # Log all API queries
LOG_ROUTING_DECISIONS = True  # Log routing decisions

print("✅ GreenAI Configuration loaded successfully")
