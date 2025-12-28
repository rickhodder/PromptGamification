"""
AI Service abstraction layer for Promptification
Provides unified interface to different AI providers (OpenAI, Anthropic)
"""

from abc import ABC, abstractmethod
from typing import Dict, Optional, List
from enum import Enum
import os
from datetime import datetime
import json


class AIProvider(str, Enum):
    """Supported AI providers"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"


class AIServiceError(Exception):
    """Base exception for AI service errors"""
    pass


class APIKeyError(AIServiceError):
    """Exception for API key related errors"""
    pass


class APITimeoutError(AIServiceError):
    """Exception for API timeout errors"""
    pass


class RateLimitError(AIServiceError):
    """Exception for rate limit errors"""
    pass


class ParseError(AIServiceError):
    """Exception for response parsing errors"""
    pass


class AIService(ABC):
    """
    Abstract base class for AI services
    Defines the interface that all AI providers must implement
    """
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """
        Initialize AI service
        
        Args:
            api_key: API key for the service (reads from env if not provided)
            model: Model to use (uses default if not provided)
        """
        self.api_key = api_key or self._get_api_key_from_env()
        self.model = model or self._get_default_model()
        self.provider = self._get_provider()
        self._validate_api_key()
    
    @abstractmethod
    def _get_api_key_from_env(self) -> Optional[str]:
        """Get API key from environment variable"""
        pass
    
    @abstractmethod
    def _get_default_model(self) -> str:
        """Get default model for this provider"""
        pass
    
    @abstractmethod
    def _get_provider(self) -> AIProvider:
        """Get the provider enum for this service"""
        pass
    
    @abstractmethod
    def _validate_api_key(self) -> bool:
        """Validate that API key is present and valid format"""
        pass
    
    @abstractmethod
    def generate_review(
        self,
        prompt_text: str,
        system_prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> Dict:
        """
        Generate a review for a prompt
        
        Args:
            prompt_text: The user's prompt to review
            system_prompt: System instructions for the AI
            temperature: Creativity level (0-1)
            max_tokens: Maximum response length
            
        Returns:
            Dict with review results containing:
                - suggested_prompt: str
                - questions: List[str]
                - refinements: List[str]
                - ratings: Dict[str, float]
                - feedback: str
                
        Raises:
            APIKeyError: If API key is invalid
            APITimeoutError: If request times out
            RateLimitError: If rate limit is exceeded
            ParseError: If response cannot be parsed
        """
        pass
    
    @abstractmethod
    def count_tokens(self, text: str) -> int:
        """
        Count tokens in text for cost estimation
        
        Args:
            text: Text to count tokens for
            
        Returns:
            Number of tokens
        """
        pass
    
    def estimate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """
        Estimate cost for a request
        
        Args:
            input_tokens: Number of input tokens
            output_tokens: Expected number of output tokens
            
        Returns:
            Estimated cost in USD
        """
        return 0.0  # Override in subclasses with actual pricing
    
    def parse_json_response(self, response: str) -> Dict:
        """
        Parse JSON response from AI
        
        Args:
            response: Raw response string
            
        Returns:
            Parsed dictionary
            
        Raises:
            ParseError: If response is not valid JSON
        """
        try:
            # Try to extract JSON from markdown code blocks if present
            if "```json" in response:
                start = response.find("```json") + 7
                end = response.find("```", start)
                response = response[start:end].strip()
            elif "```" in response:
                start = response.find("```") + 3
                end = response.find("```", start)
                response = response[start:end].strip()
            
            return json.loads(response)
        except json.JSONDecodeError as e:
            raise ParseError(f"Failed to parse JSON response: {e}")
    
    def validate_review_response(self, response: Dict) -> bool:
        """
        Validate that response has required fields
        
        Args:
            response: Parsed response dictionary
            
        Returns:
            True if valid, False otherwise
        """
        required_fields = [
            "suggested_prompt",
            "questions",
            "refinements",
            "ratings",
            "feedback"
        ]
        
        if not all(field in response for field in required_fields):
            return False
        
        # Validate ratings structure
        if "ratings" in response:
            required_ratings = ["length", "complexity", "specificity", "clarity", "creativity", "context"]
            if not all(rating in response["ratings"] for rating in required_ratings):
                return False
        
        return True


class AIServiceFactory:
    """Factory for creating AI service instances"""
    
    _services = {}
    
    @classmethod
    def register_service(cls, provider: AIProvider, service_class):
        """Register a service implementation"""
        cls._services[provider] = service_class
    
    @classmethod
    def get_service(
        cls,
        provider: Optional[AIProvider] = None,
        api_key: Optional[str] = None,
        model: Optional[str] = None
    ) -> AIService:
        """
        Get an AI service instance
        
        Args:
            provider: AI provider to use (reads from AI_PROVIDER env var if not provided)
            api_key: Optional API key (reads from env if not provided)
            model: Optional model name
            
        Returns:
            AIService instance
            
        Raises:
            ValueError: If provider is not supported
        """
        # Read provider from environment if not specified
        if provider is None:
            provider_str = os.getenv("AI_PROVIDER", "openai").lower()
            try:
                provider = AIProvider(provider_str)
            except ValueError:
                raise ValueError(f"Invalid AI_PROVIDER in .env: {provider_str}. Must be 'openai' or 'anthropic'")
        
        if provider not in cls._services:
            raise ValueError(f"Unsupported AI provider: {provider}")
        
        service_class = cls._services[provider]
        return service_class(api_key=api_key, model=model)
    
    @classmethod
    def list_providers(cls) -> List[str]:
        """List all registered providers"""
        return [provider.value for provider in cls._services.keys()]


# Import service implementations to trigger registration
# This must be at the end to avoid circular imports
try:
    from utils.openai_service import OpenAIService
except ImportError:
    pass  # OpenAI not installed

try:
    from utils.anthropic_service import AnthropicService
except ImportError:
    pass  # Anthropic not installed
