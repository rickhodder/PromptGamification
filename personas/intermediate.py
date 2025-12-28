"""
Intermediate persona - Balanced, practical, constructive
"""

from personas.base_persona import BasePersona
from models import Prompt
from typing import Dict
import os
import json
from utils.response_processor import ResponseProcessor


class IntermediatePersona(BasePersona):
    """Intermediate-level AI persona for developing prompt engineers"""
    
    def __init__(self):
        super().__init__()
        self.name = "Practical Coach"
        self.description = "Balanced guidance with practical tips"
        self.use_ai = os.getenv("USE_AI_REVIEW", "false").lower() == "true"
    
    def get_system_prompt(self) -> str:
        """Return system prompt for intermediate persona"""
        return """You are a practical AI coach for intermediate prompt engineers.

Your role:
- Use industry terminology appropriately
- Balance encouragement with honest critique
- Provide actionable, specific feedback
- Reference best practices and techniques
- Point out both strengths and weaknesses
- Suggest concrete improvements with examples
- Explain the "why" behind suggestions

When reviewing prompts:
- Acknowledge good techniques used
- Identify 3-5 specific improvement areas
- Ask probing questions about intent and context
- Suggest advanced techniques they're ready for
- Rate fairly based on intermediate standards
- Balance positive and constructive feedback

Your tone is professional, supportive, and focused on practical improvement."""
    
    def _build_review_prompt(self, prompt: Prompt) -> str:
        """Build the user prompt for AI review"""
        return f"""Please review this prompt from an intermediate prompt engineer:

**Prompt Text:**
{prompt.prompt_text}

**Description:**
{prompt.description or "No description provided"}

**User's Reflections:**
What I learned: {prompt.what_i_learned or "Not provided"}
What went well: {prompt.what_went_well or "Not provided"}

**Tags:** {', '.join(prompt.tags) if prompt.tags else "None"}

Please provide:
1. An improved version with specific enhancements
2. 4-5 probing questions about intent and edge cases
3. 5-7 specific, actionable refinement suggestions
4. Ratings (1-10) for: length, complexity, specificity, clarity, creativity, context
5. Balanced feedback highlighting strengths and areas for improvement (3-4 sentences)

Respond in JSON format."""
    
    def _get_fallback_response(self, prompt: Prompt) -> Dict[str, any]:
        """Return fallback response when AI is disabled or fails"""
        return {
            "suggested_prompt": prompt.prompt_text,
            "questions": [
                "What edge cases should this handle?",
                "How can you make the output format more explicit?",
                "What examples would clarify your intent?",
                "Are there any constraints you should specify?"
            ],
            "refinements": [
                "Structure your prompt with clear sections (Context, Task, Format)",
                "Add specific examples of desired output",
                "Include constraints and limitations",
                "Specify how to handle edge cases",
                "Use formatting hints (bullet points, numbered lists, etc.)"
            ],
            "ratings": {
                "length": 7.0,
                "complexity": 6.0,
                "specificity": 7.0,
                "clarity": 7.0,
                "creativity": 7.0,
                "context": 6.0
            },
            "feedback": "Solid prompt! Consider adding more structure and explicit examples to improve consistency."
        }
    
    def review_prompt(self, prompt: Prompt) -> Dict[str, any]:
        """Review prompt with intermediate-level feedback"""
        
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
                max_tokens=1200
            )
            
            # Process and validate response
            processed = ResponseProcessor.process_review_response(response)
            processed["persona"] = self.name
            processed["ai_used"] = True
            
            # Store both raw and processed feedback in prompt
            prompt.raw_questions = processed.get("raw_questions")
            prompt.raw_refinements = processed.get("raw_refinements")
            prompt.raw_feedback = processed.get("raw_feedback")
            prompt.processed_questions = processed.get("processed_questions")
            prompt.processed_refinements = processed.get("processed_refinements")
            prompt.processed_feedback = processed.get("processed_feedback")
            
            return processed
            
        except Exception as e:
            print(f"AI review failed: {str(e)}")
            fallback = self._get_fallback_response(prompt)
            fallback["ai_used"] = False
            fallback["error"] = str(e)
            return fallback
