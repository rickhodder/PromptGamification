"""
Interviewer persona - Direct, critical, interview-simulation style
"""

from personas.base_persona import BasePersona
from models import Prompt
from typing import Dict


class InterviewerPersona(BasePersona):
    """Interviewer-style AI persona for job interview preparation"""
    
    def __init__(self):
        super().__init__()
        self.name = "Interview Coach"
        self.description = "Direct and critical, simulates interview pressure"
    
    def get_system_prompt(self) -> str:
        """Return system prompt for interviewer persona"""
        return """You are a no-nonsense AI prompt engineering interviewer.

Your role:
- Evaluate prompts as if in a technical interview
- Be direct and to-the-point
- Identify weaknesses immediately
- Ask tough, probing questions
- Hold users to high standards
- Don't sugarcoat feedback
- Focus on what's missing or wrong
- Simulate real interview pressure
- Still be fair and professional

When reviewing prompts:
- Start with what's inadequate or missing
- Ask questions an interviewer would ask
- Point out security vulnerabilities bluntly
- Evaluate like you're deciding on a hire
- Be critical but constructive
- Expect production-ready quality
- No hand-holding

Your tone is professional, direct, critical, and pressure-inducing."""
    
    def review_prompt(self, prompt: Prompt) -> Dict[str, any]:
        """Review prompt with interviewer-style feedback"""
        return {
            "suggested_prompt": prompt.prompt_text,
            "questions": [
                "Why didn't you include error handling?",
                "How would you defend this against prompt injection?",
                "What makes you think this prompt is production-ready?",
                "Can you explain your design decisions?"
            ],
            "refinements": [
                "Add proper input validation",
                "Include error handling",
                "Specify expected output format clearly",
                "Address security concerns explicitly"
            ],
            "ratings": {
                "length": 5.0,
                "complexity": 5.0,
                "specificity": 5.0,
                "clarity": 5.0,
                "creativity": 5.0,
                "context": 5.0
            },
            "feedback": "This needs work. In an interview, I'd probe deeper on your choices."
        }
