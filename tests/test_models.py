"""
Tests for data models
"""

import pytest
from datetime import datetime
from models import Prompt, User, PromptRatings, UserPreferences, UserStats


class TestPromptModel:
    """Test Prompt model"""
    
    def test_create_prompt_with_defaults(self):
        """Test creating a prompt with default values"""
        prompt = Prompt(
            user_id="test_user",
            prompt_text="Test prompt"
        )
        
        assert prompt.user_id == "test_user"
        assert prompt.prompt_text == "Test prompt"
        assert prompt.sharing_preference == "private"
        assert prompt.is_template == False
        assert len(prompt.tags) == 0
        assert isinstance(prompt.id, str)
        assert isinstance(prompt.created_at, datetime)
    
    def test_create_prompt_with_all_fields(self):
        """Test creating a prompt with all fields populated"""
        prompt = Prompt(
            user_id="test_user",
            prompt_text="Test prompt",
            description="Test description",
            what_i_learned="Test learning",
            what_went_well="Test success",
            tags=["test", "python"],
            is_template=True,
            sharing_preference="public"
        )
        
        assert prompt.description == "Test description"
        assert prompt.what_i_learned == "Test learning"
        assert prompt.what_went_well == "Test success"
        assert len(prompt.tags) == 2
        assert prompt.is_template == True
        assert prompt.sharing_preference == "public"
    
    def test_prompt_ratings(self):
        """Test prompt ratings"""
        ratings = PromptRatings(
            length=8.5,
            complexity=7.0,
            specificity=9.0,
            clarity=8.0,
            creativity=6.5,
            context=7.5
        )
        
        assert ratings.length == 8.5
        assert ratings.complexity == 7.0
        assert all(0 <= getattr(ratings, field) <= 10 
                  for field in ['length', 'complexity', 'specificity', 'clarity', 'creativity', 'context'])
    
    def test_invalid_sharing_preference(self):
        """Test that invalid sharing preference raises error"""
        with pytest.raises(ValueError):
            Prompt(
                user_id="test_user",
                prompt_text="Test",
                sharing_preference="invalid"
            )


class TestUserModel:
    """Test User model"""
    
    def test_create_user_with_defaults(self):
        """Test creating a user with default values"""
        user = User(username="testuser")
        
        assert user.username == "testuser"
        assert isinstance(user.user_id, str)
        assert user.preferences.default_persona == "beginner"
        assert user.preferences.daily_goal == 2
        assert user.stats.total_prompts == 0
    
    def test_user_preferences(self):
        """Test user preferences"""
        prefs = UserPreferences(
            default_persona="advanced",
            daily_goal=5,
            weekly_goal=35
        )
        
        assert prefs.default_persona == "advanced"
        assert prefs.daily_goal == 5
        assert prefs.weekly_goal == 35
    
    def test_user_stats(self):
        """Test user stats"""
        stats = UserStats(
            total_prompts=100,
            prompts_this_week=15,
            prompts_this_month=50,
            average_rating=7.5,
            streak_days=10
        )
        
        assert stats.total_prompts == 100
        assert stats.prompts_this_week == 15
        assert stats.average_rating == 7.5
