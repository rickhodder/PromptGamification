"""
Beginner persona - Simple, encouraging, patient
"""

from personas.base_persona import BasePersona
from models import Prompt
from typing import Dict
import os
import json


class BeginnerPersona(BasePersona):
    """Beginner-level AI persona for newcomers to prompt engineering"""
    
    def __init__(self):
        super().__init__()
        self.name = "Friendly Guide"
        self.description = "Patient, encouraging guidance for beginners"
        self.use_ai = os.getenv("USE_AI_REVIEW", "false").lower() == "true"
    
    def get_system_prompt(self) -> str:
        """Return system prompt for beginner persona"""
        return """You are a friendly, patient AI mentor helping beginners learn prompt engineering.

Your role:
- Use simple, clear language
- Explain concepts without jargon
- Provide encouraging, positive feedback
- Break down complex ideas into simple steps
- Give concrete, actionable examples
- Celebrate small improvements
- Never be condescending or make users feel bad

When reviewing prompts:
- Start with what they did well
- Gently suggest 2-3 simple improvements
- Ask clarifying questions that help them think
- Provide examples of better phrasings
- Rate generously but honestly
- Focus on the most important fixes first

Your tone is warm, supportive, patient, and enthusiastic about their learning journey."""
    
    def _build_review_prompt(self, prompt: Prompt) -> str:
        """Build the user prompt for AI review"""
        return f"""Please review this prompt from a beginner prompt engineer:

**Prompt Text:**
{prompt.prompt_text}

**Context:**
{prompt.description or "No additional context provided"}

**User's Reflections:**
{prompt.reflections or "No reflections provided"}

Please provide:
1. A suggested improved version of the prompt
2. 3-4 clarifying questions to help them think deeper
3. 3-5 specific refinement suggestions
4. Ratings (1-10) for: length, complexity, specificity, clarity, creativity, context
5. Brief encouraging feedback (2-3 sentences)

Respond in JSON format."""
    
    def _get_fallback_response(self, prompt: Prompt) -> Dict[str, any]:
        """Return fallback response when AI is disabled or fails"""
        return {
            "suggested_prompt": prompt.prompt_text,
            "questions": [
                "What specific result do you want from this prompt?",
                "Can you add more details about your use case?",
                "What format do you want the response in?"
            ],
            "refinements": [
                "Try adding specific examples of what you want",
                "Clarify the expected output format",
                "Add more context about your goal"
            ],
            "ratings": {
                "length": 6.0,
                "complexity": 5.0,
                "specificity": 6.0,
                "clarity": 6.0,
                "creativity": 6.0,
                "context": 5.0
            },
            "feedback": "Great start! Keep practicing with more specific details."
        }
    
    def review_prompt(self, prompt: Prompt) -> Dict[str, any]:
        """Review prompt with beginner-level feedback"""
        
        if not self.use_ai:
            return self._get_fallback_response(prompt)
        
        try:
            from utils.ai_service import AIServiceFactory
            
            ai_service = AIServiceFactory.get_service()
            system_prompt = self.get_system_prompt()
            user_prompt = self._build_review_prompt(prompt)
            
            response = ai_service.generate_review(
                prompt_text=user_prompt,
                system_prompt=system_prompt,
                temperature=0.7,
                max_tokens=1000
            )
            
            response["persona"] = self.name
            response["ai_used"] = True
            return response
            
        except Exception as e:
            print(f"AI review failed: {str(e)}")
            fallback = self._get_fallback_response(prompt)
            fallback["ai_used"] = False
            fallback["error"] = str(e)
            return fallback
