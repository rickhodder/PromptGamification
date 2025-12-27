"""
Advanced persona - Expert-level, technical, challenging
"""

from personas.base_persona import BasePersona
from models import Prompt
from typing import Dict
import os
import json
from utils.response_processor import ResponseProcessor


class AdvancedPersona(BasePersona):
    """Advanced-level AI persona for experienced prompt engineers"""
    
    def __init__(self):
        super().__init__()
        self.name = "Advanced Mentor"
        self.description = "Expert-level guidance with challenging questions"
        self.use_ai = os.getenv("USE_AI_REVIEW", "false").lower() == "true"
    
    def get_system_prompt(self) -> str:
        """Return system prompt for advanced persona"""
        return """You are an expert AI prompt engineering mentor for advanced practitioners.

Your role:
- Provide sophisticated, technical analysis
- Expect users to understand advanced concepts
- Ask challenging questions that push boundaries
- Reference cutting-edge techniques and research
- Discuss complex topics like adversarial prompting, chain-of-thought, meta-prompting
- Provide deep technical explanations
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
    
    def _build_review_prompt(self, prompt: Prompt) -> str:
        """Build the user prompt for AI review"""
        return f"""Please review this prompt from an advanced prompt engineer:

**Prompt Text:**
{prompt.prompt_text}

**Description:**
{prompt.description or "No description provided"}

**Reflections:**
{prompt.reflections or "No reflections provided"}

**Tags:** {', '.join(prompt.tags) if prompt.tags else "None"}

Please provide expert-level analysis:
1. A technically optimized version leveraging advanced techniques
2. 5-6 challenging questions about edge cases, failure modes, and optimizations
3. 7-10 sophisticated refinements (chain-of-thought, few-shot, meta-prompting, etc.)
4. Strict ratings (1-10) based on advanced standards
5. Technical feedback discussing trade-offs and advanced concepts (4-5 sentences)

Respond in JSON format."""
    
    def _get_fallback_response(self, prompt: Prompt) -> Dict[str, any]:
        """Return fallback response when AI is disabled or fails"""
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
                "Optimize token usage with compression techniques",
                "Add adversarial robustness checks",
                "Implement chain-of-thought scaffolding",
                "Consider model-specific optimizations"
            ],
            "ratings": {
                "length": 7.0,
                "complexity": 7.0,
                "specificity": 7.0,
                "clarity": 7.0,
                "creativity": 7.0,
                "context": 7.0
            },
            "feedback": "Interesting approach. Consider these advanced optimizations for production-grade prompt engineering."
        }
    
    def review_prompt(self, prompt: Prompt) -> Dict[str, any]:
        """Review prompt with advanced-level feedback"""
        
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
                temperature=0.6,
                max_tokens=1500
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
