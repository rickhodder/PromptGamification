"""
Intermediate persona - Balanced technical depth, assumes some knowledge
"""

from personas.base_persona import BasePersona
from models import Prompt
from typing import Dict


class IntermediatePersona(BasePersona):
    """Intermediate-level AI persona for developing prompt engineers"""
    
    def __init__(self):
        super().__init__()
        self.name = "Intermediate Coach"
        self.description = "Balances challenge and support with medium technical depth"
    
    def get_system_prompt(self) -> str:
        """Return system prompt for intermediate persona"""
        return """You are a knowledgeable and encouraging AI prompt engineering coach for intermediate users.

Your role:
- Provide medium-difficulty technical guidance
- Assume basic prompt engineering knowledge
- Introduce advanced concepts gradually
- Ask probing questions that develop critical thinking
- Balance challenge with support
- Explain security considerations like prompt injection with technical detail
- Help users refine their prompting intuition

When reviewing prompts:
- Point out both strengths and areas for improvement
- Explain the reasoning behind suggestions
- Reference common prompt engineering patterns
- Challenge users to think deeper about their approach
- Provide actionable, specific feedback
- Acknowledge good practices while pushing for excellence

Your tone is professional, encouraging, and thought-provoking."""
    
    def review_prompt(self, prompt: Prompt) -> Dict[str, any]:
        """Review prompt with intermediate-level feedback"""
        return {
            "suggested_prompt": prompt.prompt_text,
            "questions": [
                "What prompt engineering patterns are you applying here?",
                "How might you structure this for better token efficiency?",
                "Have you considered edge cases in the AI's response?"
            ],
            "refinements": [
                "Consider using few-shot examples",
                "Add explicit output formatting instructions",
                "Define constraints more precisely"
            ],
            "ratings": {
                "length": 6.0,
                "complexity": 6.0,
                "specificity": 6.0,
                "clarity": 6.0,
                "creativity": 6.0,
                "context": 6.0
            },
            "feedback": "Solid approach. Let's refine this to make it even more effective."
        }
