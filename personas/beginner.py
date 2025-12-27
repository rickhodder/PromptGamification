"""
Beginner persona - Patient, simple explanations, non-technical
"""

from personas.base_persona import BasePersona
from models import Prompt
from typing import Dict
import json


class BeginnerPersona(BasePersona):
    """Beginner-level AI persona for new prompt engineers"""
    
    def __init__(self):
        super().__init__()
        self.name = "Beginner Guide"
        self.description = "Patient and encouraging, explains concepts simply"
    
    def get_system_prompt(self) -> str:
        """Return system prompt for beginner persona"""
        return """You are a kind, patient, and encouraging AI prompt engineering mentor for beginners.

Your role:
- Explain concepts in simple, non-technical language
- Be very supportive and encouraging
- Avoid jargon and complex terminology
- Ask basic clarifying questions
- Provide foundational guidance
- Always warn about security issues like prompt injection in simple terms
- Make learning fun and accessible

When reviewing prompts:
- Focus on fundamental improvements
- Explain WHY each suggestion helps
- Use examples to illustrate concepts
- Be generous with praise for good practices
- Keep feedback constructive and never discouraging

Your tone is warm, friendly, and educational."""
    
    def review_prompt(self, prompt: Prompt) -> Dict[str, any]:
        """Review prompt with beginner-friendly feedback"""
        # This will call the AI API with the system prompt
        # For now, return a placeholder structure
        return {
            "suggested_prompt": prompt.prompt_text,
            "questions": [
                "What kind of response are you hoping to get from the AI?",
                "Who is the audience for this AI output?",
                "Are there any specific details or examples you'd like to include?"
            ],
            "refinements": [
                "Add more context about what you want",
                "Be specific about the format you need",
                "Include an example if possible"
            ],
            "ratings": {
                "length": 5.0,
                "complexity": 5.0,
                "specificity": 5.0,
                "clarity": 5.0,
                "creativity": 5.0,
                "context": 5.0
            },
            "feedback": "Great start! You're on the right track with this prompt."
        }
