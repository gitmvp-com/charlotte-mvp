"""
CHARLOTTE MVP - Configuration

Simplified configuration for MVP.
Supports environment variable overrides.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
PLUGINS_DIR = PROJECT_ROOT / "plugins"

# Ensure directories exist
DATA_DIR.mkdir(exist_ok=True)
(DATA_DIR / "findings").mkdir(exist_ok=True)
(DATA_DIR / "reports").mkdir(exist_ok=True)

# Core configuration
CHARLOTTE_CONFIG = {
    # LLM Settings
    "LLM_PROVIDER": os.getenv("LLM_PROVIDER", "local"),
    "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY", ""),
    "OPENAI_MODEL": os.getenv("OPENAI_MODEL", "gpt-4"),
    "HUGGINGFACE_MODEL": os.getenv("HUGGINGFACE_MODEL", "microsoft/codebert-base"),
    
    # Code Reasoner
    "CODE_REASONER_MODEL": os.getenv("CODE_REASONER_MODEL", "microsoft/codebert-base"),
    "CODE_REASONER_DEVICE": os.getenv("CODE_REASONER_DEVICE", "auto"),  # auto, cpu, cuda
    "CODE_REASONER_MAX_LENGTH": int(os.getenv("CODE_REASONER_MAX_LENGTH", "512")),
    
    # Scanning
    "SCAN_RECURSIVE": os.getenv("SCAN_RECURSIVE", "true").lower() == "true",
    "SCAN_MAX_FILES": int(os.getenv("SCAN_MAX_FILES", "1000")),
    
    # Output
    "VERBOSE": os.getenv("CHARLOTTE_VERBOSE", "true").lower() == "true",
    "SAVE_RESULTS": os.getenv("CHARLOTTE_SAVE_RESULTS", "true").lower() == "true",
    "RESULTS_DIR": DATA_DIR / "findings",
    
    # Paths
    "DATA_DIR": DATA_DIR,
    "PLUGINS_DIR": PLUGINS_DIR,
}

def get_config(key: str, default=None):
    """Get configuration value"""
    return CHARLOTTE_CONFIG.get(key, default)

def set_config(key: str, value):
    """Set configuration value"""
    CHARLOTTE_CONFIG[key] = value
