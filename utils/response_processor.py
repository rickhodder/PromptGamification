"""
Response processing utilities for AI-generated reviews
Handles validation, sanitization, and enhancement of AI responses
"""

import re
from typing import Dict, List, Any, Optional
from models import PromptRatings


class ResponseProcessor:
    """Process and validate AI-generated review responses"""
    
    # Valid rating dimensions
    RATING_DIMENSIONS = ["length", "complexity", "specificity", "clarity", "creativity", "context"]
    
    # Rating bounds
    MIN_RATING = 0.0
    MAX_RATING = 10.0
    
    @staticmethod
    def process_review_response(response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process and validate a complete review response
        
        Args:
            response: Raw response from AI service
            
        Returns:
            Processed and validated response
        """
        processed = {
            "suggested_prompt": ResponseProcessor._process_suggested_prompt(
                response.get("suggested_prompt", "")
            ),
            "questions": ResponseProcessor._process_questions(
                response.get("questions", [])
            ),
            "refinements": ResponseProcessor._process_refinements(
                response.get("refinements", [])
            ),
            "ratings": ResponseProcessor._process_ratings(
                response.get("ratings", {})
            ),
            "feedback": ResponseProcessor._process_feedback(
                response.get("feedback", "")
            )
        }
        
        # Preserve metadata
        if "persona" in response:
            processed["persona"] = response["persona"]
        if "ai_used" in response:
            processed["ai_used"] = response["ai_used"]
        if "error" in response:
            processed["error"] = response["error"]
            
        return processed
    
    @staticmethod
    def _process_suggested_prompt(suggested_prompt: str) -> str:
        """
        Clean and validate suggested prompt
        
        Args:
            suggested_prompt: Raw suggested prompt text
            
        Returns:
            Cleaned suggested prompt
        """
        if not isinstance(suggested_prompt, str):
            return ""
        
        # Strip excessive whitespace
        cleaned = suggested_prompt.strip()
        
        # Remove any markdown code blocks
        cleaned = re.sub(r'^```[\w]*\n?', '', cleaned)
        cleaned = re.sub(r'\n?```$', '', cleaned)
        
        # Normalize line breaks (max 2 consecutive)
        cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)
        
        # Remove any leading/trailing quotes if present
        if cleaned.startswith('"') and cleaned.endswith('"'):
            cleaned = cleaned[1:-1]
        if cleaned.startswith("'") and cleaned.endswith("'"):
            cleaned = cleaned[1:-1]
        
        return cleaned
    
    @staticmethod
    def _process_questions(questions: List[Any]) -> List[str]:
        """
        Clean and validate questions list
        
        Args:
            questions: Raw questions list
            
        Returns:
            Cleaned list of questions
        """
        if not isinstance(questions, list):
            return []
        
        cleaned_questions = []
        for q in questions:
            if not isinstance(q, str):
                continue
                
            # Clean the question
            cleaned = q.strip()
            
            # Skip empty questions
            if not cleaned:
                continue
            
            # Ensure question ends with question mark
            if cleaned and not cleaned.endswith('?'):
                cleaned += '?'
            
            # Remove markdown formatting
            cleaned = re.sub(r'\*\*([^*]+)\*\*', r'\1', cleaned)  # Remove bold
            cleaned = re.sub(r'\*([^*]+)\*', r'\1', cleaned)  # Remove italic
            
            cleaned_questions.append(cleaned)
        
        # Limit to reasonable number
        return cleaned_questions[:10]
    
    @staticmethod
    def _process_refinements(refinements: List[Any]) -> List[str]:
        """
        Clean and validate refinements list
        
        Args:
            refinements: Raw refinements list
            
        Returns:
            Cleaned list of refinements
        """
        if not isinstance(refinements, list):
            return []
        
        cleaned_refinements = []
        for r in refinements:
            if not isinstance(r, str):
                continue
                
            # Clean the refinement
            cleaned = r.strip()
            
            # Skip empty refinements
            if not cleaned:
                continue
            
            # Remove markdown formatting
            cleaned = re.sub(r'\*\*([^*]+)\*\*', r'\1', cleaned)  # Remove bold
            cleaned = re.sub(r'\*([^*]+)\*', r'\1', cleaned)  # Remove italic
            cleaned = re.sub(r'^[-*•]\s*', '', cleaned)  # Remove bullet points
            
            # Capitalize first letter
            if cleaned:
                cleaned = cleaned[0].upper() + cleaned[1:]
            
            cleaned_refinements.append(cleaned)
        
        # Limit to reasonable number
        return cleaned_refinements[:15]
    
    @staticmethod
    def _process_ratings(ratings: Dict[str, Any]) -> Dict[str, float]:
        """
        Validate and normalize ratings
        
        Args:
            ratings: Raw ratings dictionary
            
        Returns:
            Validated ratings dictionary with all required dimensions
        """
        if not isinstance(ratings, dict):
            ratings = {}
        
        processed_ratings = {}
        
        for dimension in ResponseProcessor.RATING_DIMENSIONS:
            value = ratings.get(dimension, 5.0)
            
            # Convert to float
            try:
                value = float(value)
            except (ValueError, TypeError):
                value = 5.0
            
            # Clamp to valid range
            value = max(ResponseProcessor.MIN_RATING, min(ResponseProcessor.MAX_RATING, value))
            
            # Round to 1 decimal place
            value = round(value, 1)
            
            processed_ratings[dimension] = value
        
        return processed_ratings
    
    @staticmethod
    def _process_feedback(feedback: str) -> str:
        """
        Clean and validate feedback text
        
        Args:
            feedback: Raw feedback text
            
        Returns:
            Cleaned feedback text
        """
        if not isinstance(feedback, str):
            return ""
        
        # Strip whitespace
        cleaned = feedback.strip()
        
        # Remove markdown formatting
        cleaned = re.sub(r'\*\*([^*]+)\*\*', r'\1', cleaned)  # Remove bold
        cleaned = re.sub(r'\*([^*]+)\*', r'\1', cleaned)  # Remove italic
        cleaned = re.sub(r'^#+\s+', '', cleaned, flags=re.MULTILINE)  # Remove headers
        
        # Normalize whitespace
        cleaned = re.sub(r'\s+', ' ', cleaned)
        
        # Limit length (max 500 characters)
        if len(cleaned) > 500:
            cleaned = cleaned[:497] + "..."
        
        return cleaned
    
    @staticmethod
    def calculate_average_rating(ratings: Dict[str, float]) -> float:
        """
        Calculate average rating across all dimensions
        
        Args:
            ratings: Ratings dictionary
            
        Returns:
            Average rating (0-10)
        """
        if not ratings:
            return 5.0
        
        values = [v for k, v in ratings.items() if k in ResponseProcessor.RATING_DIMENSIONS]
        if not values:
            return 5.0
        
        return round(sum(values) / len(values), 1)
    
    @staticmethod
    def validate_response_completeness(response: Dict[str, Any]) -> tuple[bool, List[str]]:
        """
        Check if response has all required fields
        
        Args:
            response: Response to validate
            
        Returns:
            Tuple of (is_valid, list_of_missing_fields)
        """
        required_fields = ["suggested_prompt", "questions", "refinements", "ratings", "feedback"]
        missing_fields = []
        
        for field in required_fields:
            if field not in response or not response[field]:
                missing_fields.append(field)
        
        # Check ratings dimensions
        if "ratings" in response and isinstance(response["ratings"], dict):
            for dimension in ResponseProcessor.RATING_DIMENSIONS:
                if dimension not in response["ratings"]:
                    missing_fields.append(f"ratings.{dimension}")
        
        return len(missing_fields) == 0, missing_fields
    
    @staticmethod
    def sanitize_for_display(text: str) -> str:
        """
        Sanitize text for safe display in UI
        
        Args:
            text: Text to sanitize
            
        Returns:
            Sanitized text
        """
        if not isinstance(text, str):
            return ""
        
        # Remove any HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        
        # Remove script tags and content
        text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL | re.IGNORECASE)
        
        # Escape special characters that could cause issues
        text = text.replace('&', '&amp;')
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')
        
        return text
    
    @staticmethod
    def extract_key_insights(response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract key insights from response for quick display
        
        Args:
            response: Processed response
            
        Returns:
            Dictionary with key insights
        """
        ratings = response.get("ratings", {})
        
        # Find strongest and weakest dimensions
        if ratings:
            sorted_ratings = sorted(ratings.items(), key=lambda x: x[1], reverse=True)
            strongest = sorted_ratings[0] if sorted_ratings else ("none", 0)
            weakest = sorted_ratings[-1] if sorted_ratings else ("none", 0)
        else:
            strongest = ("none", 0)
            weakest = ("none", 0)
        
        # Count items
        num_questions = len(response.get("questions", []))
        num_refinements = len(response.get("refinements", []))
        
        return {
            "average_rating": ResponseProcessor.calculate_average_rating(ratings),
            "strongest_dimension": strongest[0],
            "strongest_rating": strongest[1],
            "weakest_dimension": weakest[0],
            "weakest_rating": weakest[1],
            "num_questions": num_questions,
            "num_refinements": num_refinements,
            "has_suggestions": bool(response.get("suggested_prompt")),
            "feedback_length": len(response.get("feedback", ""))
        }
