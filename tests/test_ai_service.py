"""
Tests for AI service layer
"""

import pytest
from unittest.mock import Mock, patch
from utils.ai_service import (
    AIService,
    AIProvider,
    AIServiceFactory,
    APIKeyError,
    APITimeoutError,
    RateLimitError,
    ParseError
)
from utils.openai_service import OpenAIService
from utils.anthropic_service import AnthropicService


class TestAIServiceFactory:
    """Tests for AI service factory"""
    
    def test_get_openai_service(self):
        """Test getting OpenAI service"""
        with patch.dict('os.environ', {'OPENAI_API_KEY': 'sk-test123'}):
            service = AIServiceFactory.get_service(AIProvider.OPENAI)
            assert isinstance(service, OpenAIService)
            assert service.provider == AIProvider.OPENAI
    
    def test_get_anthropic_service(self):
        """Test getting Anthropic service"""
        with patch.dict('os.environ', {'ANTHROPIC_API_KEY': 'sk-ant-test123'}):
            service = AIServiceFactory.get_service(AIProvider.ANTHROPIC)
            assert isinstance(service, AnthropicService)
            assert service.provider == AIProvider.ANTHROPIC
    
    def test_get_service_with_custom_api_key(self):
        """Test getting service with custom API key"""
        service = AIServiceFactory.get_service(
            AIProvider.OPENAI,
            api_key="sk-custom123"
        )
        assert service.api_key == "sk-custom123"
    
    def test_get_service_with_custom_model(self):
        """Test getting service with custom model"""
        with patch.dict('os.environ', {'OPENAI_API_KEY': 'sk-test123'}):
            service = AIServiceFactory.get_service(
                AIProvider.OPENAI,
                model="gpt-3.5-turbo"
            )
            assert service.model == "gpt-3.5-turbo"


class TestOpenAIService:
    """Tests for OpenAI service"""
    
    def test_init_with_api_key(self):
        """Test initializing with API key"""
        service = OpenAIService(api_key="sk-test123")
        assert service.api_key == "sk-test123"
        assert service.provider == AIProvider.OPENAI
    
    def test_init_from_env(self):
        """Test initializing from environment"""
        with patch.dict('os.environ', {'OPENAI_API_KEY': 'sk-env123'}):
            service = OpenAIService()
            assert service.api_key == "sk-env123"
    
    def test_validate_api_key_missing(self):
        """Test validation with missing API key"""
        with patch.dict('os.environ', {}, clear=True):
            with pytest.raises(APIKeyError, match="API key not found"):
                OpenAIService()  # Raises during __init__
    
    def test_validate_api_key_invalid_format(self):
        """Test validation with invalid format"""
        with pytest.raises(APIKeyError, match="Invalid.*format"):
            OpenAIService(api_key="invalid-key")  # Raises during __init__
    
    def test_validate_api_key_valid(self):
        """Test validation with valid key"""
        service = OpenAIService(api_key="sk-test123")
        assert service._validate_api_key() is True
    
    @patch('utils.openai_service.OpenAI')
    def test_generate_review_success(self, mock_openai):
        """Test successful review generation"""
        # Mock response
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = '''{
            "suggested_prompt": "Improved prompt",
            "questions": ["Q1", "Q2", "Q3"],
            "refinements": ["R1", "R2", "R3"],
            "ratings": {
                "length": 7.5,
                "complexity": 6.0,
                "specificity": 8.0,
                "clarity": 7.0,
                "creativity": 6.5,
                "context": 7.0
            },
            "feedback": "Great work!"
        }'''
        
        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        service = OpenAIService(api_key="sk-test123")
        result = service.generate_review(
            prompt_text="Test prompt",
            system_prompt="System prompt"
        )
        
        assert result["suggested_prompt"] == "Improved prompt"
        assert len(result["questions"]) == 3
        assert result["ratings"]["length"] == 7.5
    
    @patch('utils.openai_service.OpenAI')
    def test_generate_review_rate_limit(self, mock_openai):
        """Test rate limit handling"""
        from openai import RateLimitError as OpenAIRateLimit
        
        # Create proper mock response for error
        mock_response = Mock()
        mock_response.status_code = 429
        mock_body = {"error": {"message": "Rate limited"}}
        
        mock_client = Mock()
        mock_client.chat.completions.create.side_effect = OpenAIRateLimit(
            "Rate limited",
            response=mock_response,
            body=mock_body
        )
        mock_openai.return_value = mock_client
        
        service = OpenAIService(api_key="sk-test123")
        service.max_retries = 1  # Reduce retries for test
        
        with pytest.raises(RateLimitError):
            service.generate_review("Test", "System")
    
    def test_count_tokens(self):
        """Test token counting"""
        service = OpenAIService(api_key="sk-test123")
        text = "This is a test prompt"
        tokens = service.count_tokens(text)
        assert tokens == len(text) // 4
    
    def test_estimate_cost(self):
        """Test cost estimation"""
        service = OpenAIService(api_key="sk-test123", model="gpt-4-turbo")
        cost = service.estimate_cost(input_tokens=1000, output_tokens=500)
        
        # gpt-4-turbo: $10/1M input, $30/1M output
        expected = (1000/1_000_000 * 10) + (500/1_000_000 * 30)
        assert cost == expected


class TestAnthropicService:
    """Tests for Anthropic service"""
    
    def test_init_with_api_key(self):
        """Test initializing with API key"""
        service = AnthropicService(api_key="sk-ant-test123")
        assert service.api_key == "sk-ant-test123"
        assert service.provider == AIProvider.ANTHROPIC
    
    def test_init_from_env(self):
        """Test initializing from environment"""
        with patch.dict('os.environ', {'ANTHROPIC_API_KEY': 'sk-ant-env123'}):
            service = AnthropicService()
            assert service.api_key == "sk-ant-env123"
    
    def test_validate_api_key_missing(self):
        """Test validation with missing API key"""
        with patch.dict('os.environ', {}, clear=True):
            with pytest.raises(APIKeyError, match="API key not found"):
                AnthropicService()  # Raises during __init__
    
    def test_validate_api_key_invalid_format(self):
        """Test validation with invalid format"""
        with pytest.raises(APIKeyError, match="Invalid.*format"):
            AnthropicService(api_key="invalid-key")  # Raises during __init__
    
    def test_validate_api_key_valid(self):
        """Test validation with valid key"""
        service = AnthropicService(api_key="sk-ant-test123")
        assert service._validate_api_key() is True
    
    @patch('utils.anthropic_service.Anthropic')
    def test_generate_review_success(self, mock_anthropic):
        """Test successful review generation"""
        # Mock response
        mock_response = Mock()
        mock_response.content = [Mock()]
        mock_response.content[0].text = '''{
            "suggested_prompt": "Improved prompt",
            "questions": ["Q1", "Q2", "Q3"],
            "refinements": ["R1", "R2", "R3"],
            "ratings": {
                "length": 7.5,
                "complexity": 6.0,
                "specificity": 8.0,
                "clarity": 7.0,
                "creativity": 6.5,
                "context": 7.0
            },
            "feedback": "Great work!"
        }'''
        
        mock_client = Mock()
        mock_client.messages.create.return_value = mock_response
        mock_anthropic.return_value = mock_client
        
        service = AnthropicService(api_key="sk-ant-test123")
        result = service.generate_review(
            prompt_text="Test prompt",
            system_prompt="System prompt"
        )
        
        assert result["suggested_prompt"] == "Improved prompt"
        assert len(result["questions"]) == 3
        assert result["ratings"]["length"] == 7.5
    
    def test_count_tokens(self):
        """Test token counting"""
        service = AnthropicService(api_key="sk-ant-test123")
        text = "This is a test prompt"
        tokens = service.count_tokens(text)
        assert tokens == len(text) // 4
    
    def test_estimate_cost(self):
        """Test cost estimation"""
        service = AnthropicService(
            api_key="sk-ant-test123",
            model="claude-3-5-sonnet-20241022"
        )
        cost = service.estimate_cost(input_tokens=1000, output_tokens=500)
        
        # claude-3-5-sonnet: $3/1M input, $15/1M output
        expected = (1000/1_000_000 * 3) + (500/1_000_000 * 15)
        assert cost == expected


class TestAIServiceHelpers:
    """Tests for AI service helper methods"""
    
    def test_parse_json_response_clean(self):
        """Test parsing clean JSON"""
        service = OpenAIService(api_key="sk-test123")
        json_str = '{"key": "value"}'
        result = service.parse_json_response(json_str)
        assert result == {"key": "value"}
    
    def test_parse_json_response_with_markdown(self):
        """Test parsing JSON wrapped in markdown"""
        service = OpenAIService(api_key="sk-test123")
        json_str = '''```json
        {"key": "value"}
        ```'''
        result = service.parse_json_response(json_str)
        assert result == {"key": "value"}
    
    def test_parse_json_response_invalid(self):
        """Test parsing invalid JSON"""
        service = OpenAIService(api_key="sk-test123")
        with pytest.raises(ParseError):
            service.parse_json_response("not json")
    
    def test_validate_review_response_valid(self):
        """Test validating valid response"""
        service = OpenAIService(api_key="sk-test123")
        response = {
            "suggested_prompt": "Test",
            "questions": ["Q1"],
            "refinements": ["R1"],
            "ratings": {
                "length": 7.5,
                "complexity": 6.0,
                "specificity": 8.0,
                "clarity": 7.0,
                "creativity": 6.5,
                "context": 7.0
            },
            "feedback": "Good"
        }
        assert service.validate_review_response(response) is True
    
    def test_validate_review_response_missing_field(self):
        """Test validating response missing field"""
        service = OpenAIService(api_key="sk-test123")
        response = {
            "suggested_prompt": "Test",
            "questions": ["Q1"]
            # Missing other fields
        }
        assert service.validate_review_response(response) is False
    
    def test_validate_review_response_missing_rating(self):
        """Test validating response missing rating dimension"""
        service = OpenAIService(api_key="sk-test123")
        response = {
            "suggested_prompt": "Test",
            "questions": ["Q1"],
            "refinements": ["R1"],
            "ratings": {
                "length": 7.5,
                # Missing other dimensions
            },
            "feedback": "Good"
        }
        assert service.validate_review_response(response) is False
