"""
OpenAI service implementation
"""

import os
import time
from typing import Dict, Optional
from openai import OpenAI, APIError, APITimeoutError as OpenAITimeout, RateLimitError as OpenAIRateLimit
from utils.ai_service import (
    AIService,
    AIProvider,
    APIKeyError,
    APITimeoutError,
    RateLimitError,
    ParseError,
    AIServiceFactory
)


class OpenAIService(AIService):
    """OpenAI API service implementation"""
    
    # Pricing per 1M tokens (as of Dec 2025)
    PRICING = {
        "gpt-4-turbo": {"input": 10.0, "output": 30.0},
        "gpt-4": {"input": 30.0, "output": 60.0},
        "gpt-3.5-turbo": {"input": 0.50, "output": 1.50},
    }
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """Initialize OpenAI service"""
        super().__init__(api_key, model)
        self.client = OpenAI(api_key=self.api_key)
        self.max_retries = 3
        self.retry_delay = 2  # seconds
    
    def _get_api_key_from_env(self) -> Optional[str]:
        """Get OpenAI API key from environment"""
        return os.getenv("OPENAI_API_KEY")
    
    def _get_default_model(self) -> str:
        """Get default OpenAI model"""
        return "gpt-4-turbo"
    
    def _get_provider(self) -> AIProvider:
        """Get the provider enum for this service"""
        return AIProvider.OPENAI
    
    def _validate_api_key(self) -> bool:
        """Validate API key is present and has correct format"""
        if not self.api_key:
            raise APIKeyError(
                "OpenAI API key not found. Please set OPENAI_API_KEY environment variable."
            )
        
        if not self.api_key.startswith("sk-"):
            raise APIKeyError(
                "Invalid OpenAI API key format. Key should start with 'sk-'"
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
        Generate a review using OpenAI API
        
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
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_message}
                    ],
                    temperature=temperature,
                    max_tokens=max_tokens,
                    response_format={"type": "json_object"}  # Force JSON response
                )
                
                # Extract response
                content = response.choices[0].message.content
                
                # Parse and validate
                result = self.parse_json_response(content)
                
                if not self.validate_review_response(result):
                    raise ParseError("Response missing required fields")
                
                return result
                
            except OpenAIRateLimit as e:
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay * (attempt + 1))
                    continue
                raise RateLimitError(f"OpenAI rate limit exceeded: {e}")
            
            except OpenAITimeout as e:
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                    continue
                raise APITimeoutError(f"OpenAI API timeout: {e}")
            
            except APIError as e:
                if attempt < self.max_retries - 1 and e.status_code >= 500:
                    time.sleep(self.retry_delay)
                    continue
                raise APIKeyError(f"OpenAI API error: {e}")
            
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
        # For more accurate counting, use tiktoken library
        return len(text) // 4
    
    def estimate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """
        Estimate cost for OpenAI API call
        
        Args:
            input_tokens: Input token count
            output_tokens: Expected output tokens
            
        Returns:
            Estimated cost in USD
        """
        pricing = self.PRICING.get(self.model, self.PRICING["gpt-4-turbo"])
        
        input_cost = (input_tokens / 1_000_000) * pricing["input"]
        output_cost = (output_tokens / 1_000_000) * pricing["output"]
        
        return input_cost + output_cost


# Register OpenAI service
AIServiceFactory.register_service(AIProvider.OPENAI, OpenAIService)
