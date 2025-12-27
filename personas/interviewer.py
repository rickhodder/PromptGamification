"""
Interviewer persona - Critical, direct, challenging
"""

from personas.base_persona import BasePersona
from models import Prompt
from typing import Dict
import os
import json
from utils.response_processor import ResponseProcessor


class InterviewerPersona(BasePersona):
    """Interviewer-level AI persona for interview practice"""
    
    def __init__(self):
        super().__init__()
        self.name = "Critical Interviewer"
        self.description = "Direct, critical feedback like a tough interviewer"
        self.use_ai = os.getenv("USE_AI_REVIEW", "false").lower() == "true"
    
    def get_system_prompt(self) -> str:
        """Return system prompt for interviewer persona"""
        return """You are a critical AI interviewer evaluating prompt engineering skills.

Your role:
- Be direct and honest, even if harsh
- Point out flaws and weaknesses immediately
- Ask tough, probing questions
- Challenge assumptions
- Expect professional-level quality
- Don't sugarcoat feedback
- Focus on what's wrong, then what could be better

When reviewing prompts:
- Start with critical observations
- Ask difficult follow-up questions
- Identify all weaknesses and gaps
- Rate strictly - don't be generous
- Provide tough but fair feedback
- Push candidates to defend their choices
- Simulate real interview pressure

Your tone is professional, direct, critical, and challenging."""
    
    def _build_review_prompt(self, prompt: Prompt) -> str:
        """Build the user prompt for AI review"""
        return f"""You are conducting a prompt engineering interview. Critically evaluate this prompt:

**Candidate's Prompt:**
{prompt.prompt_text}

**Context:**
{prompt.description or "No context provided - this is a red flag"}

**Reflections:**
{prompt.reflections or "No reflections - candidate didn't think through the problem"}

**Tags:** {', '.join(prompt.tags) if prompt.tags else "None - poor organization"}

Provide critical interview feedback:
1. A significantly improved version showing what professional quality looks like
2. 4-6 tough interview questions exposing weaknesses
3. 6-8 critical issues that need fixing
4. Strict ratings (1-10) - be harsh but fair
5. Direct feedback on what's wrong and why this wouldn't pass an interview (3-4 sentences)

Respond in JSON format."""
    
    def _get_fallback_response(self, prompt: Prompt) -> Dict[str, any]:
        """Return fallback response when AI is disabled or fails"""
        return {
            "suggested_prompt": prompt.prompt_text,
            "questions": [
                "Why didn't you include specific output format requirements?",
                "What makes you think this prompt is clear enough?",
                "How would you handle edge cases?",
                "Where are your examples?",
                "Why is there no error handling?"
            ],
            "refinements": [
                "Add clear structure - this is basic",
                "Include specific examples",
                "Define output format explicitly",
                "Handle edge cases properly",
                "Add constraints and limitations",
                "Use professional formatting",
                "Think through requirements first"
            ],
            "ratings": {
                "length": 5.0,
                "complexity": 5.0,
                "specificity": 5.0,
                "clarity": 5.0,
                "creativity": 5.0,
                "context": 5.0
            },
            "feedback": "This needs work. Add structure, examples, and think through requirements more carefully."
        }
    
    def review_prompt(self, prompt: Prompt) -> Dict[str, any]:
        """Review prompt with critical interviewer feedback"""
        
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
                temperature=0.5,
                max_tokens=1200
            )
            
            # Process and validate response
            processed = ResponseProcessor.process_review_response(response)
            processed["persona"] = self.name
            processed["ai_used"] = True
            return processed
            
        except Exception as e:
            print(f"AI review failed: {str(e)}")
            fallback = self._get_fallback_response(prompt)
            fallback["ai_used"] = False
            fallback["error"] = str(e)
            return fallback
