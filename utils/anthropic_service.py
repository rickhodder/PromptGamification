"""
Anthropic service implementation
"""

import os
import time
from typing import Dict, Optional
from anthropic import Anthropic, APIError, APITimeoutError as AnthropicTimeout, RateLimitError as AnthropicRateLimit
from utils.ai_service import (
    AIService,
    AIProvider,
    APIKeyError,
    APITimeoutError,
    RateLimitError,
    ParseError,
    AIServiceFactory
)


class AnthropicService(AIService):
    """Anthropic API service implementation"""
    
    # Pricing per 1M tokens (as of Dec 2025)
    PRICING = {
        "claude-3-5-sonnet-20241022": {"input": 3.0, "output": 15.0},
        "claude-3-opus-20240229": {"input": 15.0, "output": 75.0},
        "claude-3-sonnet-20240229": {"input": 3.0, "output": 15.0},
        "claude-3-haiku-20240307": {"input": 0.25, "output": 1.25},
    }
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """Initialize Anthropic service"""
        super().__init__(api_key, model)
        self.client = Anthropic(api_key=self.api_key)
        self.max_retries = 3
        self.retry_delay = 2  # seconds
    
    def _get_api_key_from_env(self) -> Optional[str]:
        """Get Anthropic API key from environment"""
        return os.getenv("ANTHROPIC_API_KEY")
    
    def _get_default_model(self) -> str:
        """Get default Anthropic model"""
        return "claude-3-5-sonnet-20241022"
    
    def _get_provider(self) -> AIProvider:
        """Get the provider enum for this service"""
        return AIProvider.ANTHROPIC
    
    def _validate_api_key(self) -> bool:
        """Validate API key is present and has correct format"""
        if not self.api_key:
            raise APIKeyError(
                "Anthropic API key not found. Please set ANTHROPIC_API_KEY environment variable."
            )
        
        if not self.api_key.startswith("sk-ant-"):
            raise APIKeyError(
                "Invalid Anthropic API key format. Key should start with 'sk-ant-'"
            )
        
        return True
    
    def generate_review(
        self,
        prompt_text: str,
        system_prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> Dict:
        """
        Generate a review using Anthropic API
        
        Args:
            prompt_text: The prompt to review
            system_prompt: System instructions
            temperature: Creativity (0-1)
            max_tokens: Max response tokens
            
        Returns:
            Dict with review results
        """
        # Build the review request
        user_message = f"""Please review this AI prompt and provide detailed feedback.

**Prompt to Review:**
{prompt_text}

Please provide your response in JSON format with these exact keys:
{{
    "suggested_prompt": "An improved version of the prompt",
    "questions": ["question 1", "question 2", "question 3"],
    "refinements": ["refinement 1", "refinement 2", "refinement 3"],
    "ratings": {{
        "length": 7.5,
        "complexity": 6.0,
        "specificity": 8.0,
        "clarity": 7.0,
        "creativity": 6.5,
        "context": 7.0
    }},
    "feedback": "General encouraging feedback with security considerations"
}}

Ensure ratings are numbers between 0-10."""
        
        # Try with retries
        for attempt in range(self.max_retries):
            try:
                response = self.client.messages.create(
                    model=self.model,
                    system=system_prompt,
                    messages=[
                        {"role": "user", "content": user_message}
                    ],
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                
                # Extract response
                content = response.content[0].text
                
                # Parse and validate
                result = self.parse_json_response(content)
                
                if not self.validate_review_response(result):
                    raise ParseError("Response missing required fields")
                
                return result
                
            except AnthropicRateLimit as e:
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay * (attempt + 1))
                    continue
                raise RateLimitError(f"Anthropic rate limit exceeded: {e}")
            
            except AnthropicTimeout as e:
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                    continue
                raise APITimeoutError(f"Anthropic API timeout: {e}")
            
            except APIError as e:
                if attempt < self.max_retries - 1 and hasattr(e, 'status_code') and e.status_code >= 500:
                    time.sleep(self.retry_delay)
                    continue
                raise APIKeyError(f"Anthropic API error: {e}")
            
            except ParseError:
                if attempt < self.max_retries - 1:
                    # Retry parsing errors
                    time.sleep(self.retry_delay)
                    continue
                raise
        
        raise APITimeoutError("Max retries exceeded")
    
    def count_tokens(self, text: str) -> int:
        """
        Estimate token count for text
        Uses rough approximation: 1 token ≈ 4 characters
        
        Args:
            text: Text to count
            
        Returns:
            Approximate token count
        """
        # Rough approximation
        # Anthropic API provides actual token counts in usage metadata
        return len(text) // 4
    
    def estimate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """
        Estimate cost for Anthropic API call
        
        Args:
            input_tokens: Input token count
            output_tokens: Expected output tokens
            
        Returns:
            Estimated cost in USD
        """
        pricing = self.PRICING.get(self.model, self.PRICING["claude-3-5-sonnet-20241022"])
        
        input_cost = (input_tokens / 1_000_000) * pricing["input"]
        output_cost = (output_tokens / 1_000_000) * pricing["output"]
        
        return input_cost + output_cost


# Register Anthropic service
AIServiceFactory.register_service(AIProvider.ANTHROPIC, AnthropicService)
