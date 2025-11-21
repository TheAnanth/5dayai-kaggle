"""
Configuration module for EduQuest
Handles API keys and model settings
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Gemini API Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found. Please create a .env file with your API key. "
        "You can get one from https://makersuite.google.com/app/apikey"
    )

# Model configurations
MANAGER_MODEL = "models/gemini-2.0-flash"
PLANNER_MODEL = "models/gemini-2.0-flash"
QUIZ_MODEL = "models/gemini-2.0-flash"

# Agent configurations
MANAGER_TEMPERATURE = 0.3
PLANNER_TEMPERATURE = 0.5
QUIZ_TEMPERATURE = 0.7

# Session settings
MAX_QUIZ_QUESTIONS = 10
DEFAULT_STUDY_HOURS_PER_DAY = 3
