"""
Tests for response processing utilities
"""

import pytest
from utils.response_processor import ResponseProcessor


class TestProcessSuggestedPrompt:
    """Tests for suggested prompt processing"""
    
    def test_clean_basic_prompt(self):
        """Test cleaning a basic prompt"""
        result = ResponseProcessor._process_suggested_prompt("  Test prompt  ")
        assert result == "Test prompt"
    
    def test_remove_markdown_code_blocks(self):
        """Test removing markdown code blocks"""
        result = ResponseProcessor._process_suggested_prompt("```\nTest prompt\n```")
        assert result == "Test prompt"
        
        result = ResponseProcessor._process_suggested_prompt("```python\nTest prompt\n```")
        assert result == "Test prompt"
    
    def test_remove_quotes(self):
        """Test removing surrounding quotes"""
        result = ResponseProcessor._process_suggested_prompt('"Test prompt"')
        assert result == "Test prompt"
        
        result = ResponseProcessor._process_suggested_prompt("'Test prompt'")
        assert result == "Test prompt"
    
    def test_normalize_line_breaks(self):
        """Test normalizing excessive line breaks"""
        result = ResponseProcessor._process_suggested_prompt("Line 1\n\n\n\nLine 2")
        assert result == "Line 1\n\nLine 2"
    
    def test_handle_non_string(self):
        """Test handling non-string input"""
        result = ResponseProcessor._process_suggested_prompt(None)
        assert result == ""
        
        result = ResponseProcessor._process_suggested_prompt(123)
        assert result == ""


class TestProcessQuestions:
    """Tests for questions processing"""
    
    def test_clean_valid_questions(self):
        """Test cleaning valid questions"""
        questions = ["What is this", "How does it work"]
        result = ResponseProcessor._process_questions(questions)
        
        assert len(result) == 2
        assert result[0] == "What is this?"
        assert result[1] == "How does it work?"
    
    def test_skip_empty_questions(self):
        """Test skipping empty questions"""
        questions = ["Valid question", "", "  ", "Another question"]
        result = ResponseProcessor._process_questions(questions)
        
        assert len(result) == 2
        assert "Valid question?" in result
        assert "Another question?" in result
    
    def test_remove_markdown_formatting(self):
        """Test removing markdown from questions"""
        questions = ["**Bold question**", "*Italic question*"]
        result = ResponseProcessor._process_questions(questions)
        
        assert result[0] == "Bold question?"
        assert result[1] == "Italic question?"
    
    def test_limit_number_of_questions(self):
        """Test limiting questions to 10"""
        questions = [f"Question {i}" for i in range(20)]
        result = ResponseProcessor._process_questions(questions)
        
        assert len(result) == 10
    
    def test_handle_non_list(self):
        """Test handling non-list input"""
        result = ResponseProcessor._process_questions("not a list")
        assert result == []
        
        result = ResponseProcessor._process_questions(None)
        assert result == []
    
    def test_handle_non_string_items(self):
        """Test handling non-string items in list"""
        questions = ["Valid question", 123, None, "Another question"]
        result = ResponseProcessor._process_questions(questions)
        
        assert len(result) == 2


class TestProcessRefinements:
    """Tests for refinements processing"""
    
    def test_clean_valid_refinements(self):
        """Test cleaning valid refinements"""
        refinements = ["add more detail", "improve clarity"]
        result = ResponseProcessor._process_refinements(refinements)
        
        assert len(result) == 2
        assert result[0] == "Add more detail"
        assert result[1] == "Improve clarity"
    
    def test_remove_bullet_points(self):
        """Test removing bullet points"""
        refinements = ["- First point", "* Second point", "• Third point"]
        result = ResponseProcessor._process_refinements(refinements)
        
        assert all(not r.startswith(('-', '*', '•')) for r in result)
    
    def test_capitalize_first_letter(self):
        """Test capitalizing first letter"""
        refinements = ["lowercase start", "already Capitalized"]
        result = ResponseProcessor._process_refinements(refinements)
        
        assert result[0][0].isupper()
        assert result[1][0].isupper()
    
    def test_limit_number_of_refinements(self):
        """Test limiting refinements to 15"""
        refinements = [f"Refinement {i}" for i in range(20)]
        result = ResponseProcessor._process_refinements(refinements)
        
        assert len(result) == 15
    
    def test_skip_empty_refinements(self):
        """Test skipping empty refinements"""
        refinements = ["Valid", "", "  ", "Another"]
        result = ResponseProcessor._process_refinements(refinements)
        
        assert len(result) == 2


class TestProcessRatings:
    """Tests for ratings processing"""
    
    def test_valid_ratings(self):
        """Test processing valid ratings"""
        ratings = {
            "length": 7.5,
            "complexity": 6.0,
            "specificity": 8.0,
            "clarity": 7.0,
            "creativity": 6.5,
            "context": 7.0
        }
        result = ResponseProcessor._process_ratings(ratings)
        
        assert len(result) == 6
        assert result["length"] == 7.5
        assert result["clarity"] == 7.0
    
    def test_clamp_ratings_to_range(self):
        """Test clamping ratings to 0-10 range"""
        ratings = {
            "length": -5.0,
            "complexity": 15.0,
            "specificity": 8.0,
            "clarity": 7.0,
            "creativity": 6.5,
            "context": 7.0
        }
        result = ResponseProcessor._process_ratings(ratings)
        
        assert result["length"] == 0.0
        assert result["complexity"] == 10.0
    
    def test_fill_missing_dimensions(self):
        """Test filling missing rating dimensions with defaults"""
        ratings = {"length": 7.5, "clarity": 8.0}
        result = ResponseProcessor._process_ratings(ratings)
        
        assert len(result) == 6
        assert "complexity" in result
        assert "specificity" in result
        assert result["complexity"] == 5.0  # default
    
    def test_convert_string_ratings(self):
        """Test converting string ratings to float"""
        ratings = {
            "length": "7.5",
            "complexity": "6",
            "specificity": 8.0,
            "clarity": 7.0,
            "creativity": 6.5,
            "context": 7.0
        }
        result = ResponseProcessor._process_ratings(ratings)
        
        assert isinstance(result["length"], float)
        assert result["length"] == 7.5
    
    def test_handle_invalid_ratings(self):
        """Test handling invalid rating values"""
        ratings = {
            "length": "invalid",
            "complexity": None,
            "specificity": 8.0,
            "clarity": 7.0,
            "creativity": 6.5,
            "context": 7.0
        }
        result = ResponseProcessor._process_ratings(ratings)
        
        assert result["length"] == 5.0  # default for invalid
        assert result["complexity"] == 5.0  # default for None
    
    def test_round_to_one_decimal(self):
        """Test rounding ratings to 1 decimal place"""
        ratings = {
            "length": 7.555,
            "complexity": 6.123,
            "specificity": 8.0,
            "clarity": 7.0,
            "creativity": 6.5,
            "context": 7.0
        }
        result = ResponseProcessor._process_ratings(ratings)
        
        assert result["length"] == 7.6
        assert result["complexity"] == 6.1


class TestProcessFeedback:
    """Tests for feedback processing"""
    
    def test_clean_basic_feedback(self):
        """Test cleaning basic feedback"""
        result = ResponseProcessor._process_feedback("  Good job!  ")
        assert result == "Good job!"
    
    def test_remove_markdown(self):
        """Test removing markdown formatting"""
        result = ResponseProcessor._process_feedback("**Bold** and *italic* text")
        assert result == "Bold and italic text"
    
    def test_remove_headers(self):
        """Test removing markdown headers"""
        result = ResponseProcessor._process_feedback("# Header\nContent")
        assert "Header" in result
        assert not result.startswith("#")
    
    def test_normalize_whitespace(self):
        """Test normalizing whitespace"""
        result = ResponseProcessor._process_feedback("Multiple    spaces   here")
        assert "Multiple spaces here" == result
    
    def test_limit_length(self):
        """Test limiting feedback length"""
        long_feedback = "A" * 600
        result = ResponseProcessor._process_feedback(long_feedback)
        
        assert len(result) <= 500
        assert result.endswith("...")
    
    def test_handle_non_string(self):
        """Test handling non-string input"""
        result = ResponseProcessor._process_feedback(None)
        assert result == ""


class TestProcessReviewResponse:
    """Tests for complete response processing"""
    
    def test_process_complete_response(self):
        """Test processing a complete valid response"""
        response = {
            "suggested_prompt": "  Improved prompt  ",
            "questions": ["Question 1", "Question 2"],
            "refinements": ["refinement 1", "refinement 2"],
            "ratings": {
                "length": 7.5,
                "complexity": 6.0,
                "specificity": 8.0,
                "clarity": 7.0,
                "creativity": 6.5,
                "context": 7.0
            },
            "feedback": "  Good work!  "
        }
        
        result = ResponseProcessor.process_review_response(response)
        
        assert result["suggested_prompt"] == "Improved prompt"
        assert len(result["questions"]) == 2
        assert len(result["refinements"]) == 2
        assert len(result["ratings"]) == 6
        assert result["feedback"] == "Good work!"
    
    def test_preserve_metadata(self):
        """Test preserving metadata fields"""
        response = {
            "suggested_prompt": "Test",
            "questions": [],
            "refinements": [],
            "ratings": {},
            "feedback": "Test",
            "persona": "Friendly Guide",
            "ai_used": True,
            "error": "Some error"
        }
        
        result = ResponseProcessor.process_review_response(response)
        
        assert result["persona"] == "Friendly Guide"
        assert result["ai_used"] is True
        assert result["error"] == "Some error"


class TestValidateResponse:
    """Tests for response validation"""
    
    def test_valid_complete_response(self):
        """Test validating a complete response"""
        response = {
            "suggested_prompt": "Test",
            "questions": ["Q1"],
            "refinements": ["R1"],
            "ratings": {
                "length": 7.0,
                "complexity": 6.0,
                "specificity": 8.0,
                "clarity": 7.0,
                "creativity": 6.5,
                "context": 7.0
            },
            "feedback": "Good"
        }
        
        is_valid, missing = ResponseProcessor.validate_response_completeness(response)
        
        assert is_valid
        assert len(missing) == 0
    
    def test_missing_fields(self):
        """Test detecting missing fields"""
        response = {
            "suggested_prompt": "Test",
            "questions": ["Q1"]
            # Missing refinements, ratings, feedback
        }
        
        is_valid, missing = ResponseProcessor.validate_response_completeness(response)
        
        assert not is_valid
        assert "refinements" in missing
        assert "ratings" in missing
        assert "feedback" in missing
    
    def test_missing_rating_dimensions(self):
        """Test detecting missing rating dimensions"""
        response = {
            "suggested_prompt": "Test",
            "questions": ["Q1"],
            "refinements": ["R1"],
            "ratings": {
                "length": 7.0,
                "clarity": 7.0
                # Missing other dimensions
            },
            "feedback": "Good"
        }
        
        is_valid, missing = ResponseProcessor.validate_response_completeness(response)
        
        assert not is_valid
        assert any("ratings." in m for m in missing)


class TestUtilityMethods:
    """Tests for utility methods"""
    
    def test_calculate_average_rating(self):
        """Test calculating average rating"""
        ratings = {
            "length": 8.0,
            "complexity": 6.0,
            "specificity": 7.0,
            "clarity": 9.0,
            "creativity": 7.0,
            "context": 8.0
        }
        
        avg = ResponseProcessor.calculate_average_rating(ratings)
        assert avg == 7.5
    
    def test_sanitize_for_display(self):
        """Test sanitizing text for display"""
        text = "<script>alert('xss')</script>Normal text"
        result = ResponseProcessor.sanitize_for_display(text)
        
        assert "<script>" not in result
        assert "Normal text" in result
    
    def test_extract_key_insights(self):
        """Test extracting key insights"""
        response = {
            "suggested_prompt": "Test",
            "questions": ["Q1", "Q2", "Q3"],
            "refinements": ["R1", "R2"],
            "ratings": {
                "length": 8.0,
                "complexity": 6.0,
                "specificity": 9.0,
                "clarity": 7.0,
                "creativity": 5.0,
                "context": 7.0
            },
            "feedback": "Good work"
        }
        
        insights = ResponseProcessor.extract_key_insights(response)
        
        assert insights["average_rating"] == 7.0
        assert insights["strongest_dimension"] == "specificity"
        assert insights["weakest_dimension"] == "creativity"
        assert insights["num_questions"] == 3
        assert insights["num_refinements"] == 2
        assert insights["has_suggestions"] is True
