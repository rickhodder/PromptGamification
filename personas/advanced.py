"""
Advanced persona - Expert-level, technical, challenging
"""

from personas.base_persona import BasePersona
from models import Prompt
from typing import Dict


class AdvancedPersona(BasePersona):
    """Advanced-level AI persona for experienced prompt engineers"""
    
    def __init__(self):
        super().__init__()
        self.name = "Advanced Mentor"
        self.description = "Expert-level guidance with challenging questions"
    
    def get_system_prompt(self) -> str:
        """Return system prompt for advanced persona"""
        return """You are an expert AI prompt engineering mentor for advanced practitioners.

Your role:
- Provide sophisticated, technical analysis
- Expect users to understand advanced concepts
- Ask challenging questions that push boundaries
- Reference cutting-edge techniques and research
- Discuss complex topics like adversarial prompting, chain-of-thought, meta-prompting
- Provide deep technical explanations of security vulnerabilities
- Challenge assumptions and encourage experimentation

When reviewing prompts:
- Analyze subtle nuances and implications
- Suggest advanced optimization techniques
- Consider computational efficiency and scaling
- Discuss trade-offs between different approaches
- Reference academic research and best practices
- Identify potential failure modes
- Push for excellence and innovation

Your tone is professional, direct, intellectually rigorous, yet supportive."""
    
    def review_prompt(self, prompt: Prompt) -> Dict[str, any]:
        """Review prompt with advanced-level feedback"""
        return {
            "suggested_prompt": prompt.prompt_text,
            "questions": [
                "How does this prompt leverage chain-of-thought reasoning?",
                "What are the potential adversarial inputs you've considered?",
                "How would this scale across different model architectures?",
                "What's your strategy for handling hallucinations?"
            ],
            "refinements": [
                "Implement meta-prompting for better control",
                "Add constitutional AI principles",
                "Consider multi-step reasoning decomposition",
                "Optimize token usage with compression techniques"
            ],
            "ratings": {
                "length": 7.0,
                "complexity": 7.0,
                "specificity": 7.0,
                "clarity": 7.0,
                "creativity": 7.0,
                "context": 7.0
            },
            "feedback": "Interesting approach. Consider these advanced optimizations."
        }
