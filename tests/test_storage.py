"""
Tests for JSON storage functionality
"""

import pytest
from models import Prompt, User


class TestJSONStorage:
    """Test JSON storage operations"""
    
    def test_save_and_get_prompt(self, test_storage, sample_prompt):
        """Test saving and retrieving a prompt"""
        saved = test_storage.save_prompt(sample_prompt)
        retrieved = test_storage.get_prompt(saved.id)
        
        assert retrieved is not None
        assert retrieved.id == saved.id
        assert retrieved.prompt_text == sample_prompt.prompt_text
        assert retrieved.user_id == sample_prompt.user_id
    
    def test_get_nonexistent_prompt(self, test_storage):
        """Test getting a prompt that doesn't exist"""
        result = test_storage.get_prompt("nonexistent_id")
        assert result is None
    
    def test_update_prompt(self, test_storage, sample_prompt):
        """Test updating an existing prompt"""
        saved = test_storage.save_prompt(sample_prompt)
        
        # Update the prompt
        saved.prompt_text = "Updated prompt text"
        saved.tags.append("new_tag")
        
        updated = test_storage.save_prompt(saved)
        retrieved = test_storage.get_prompt(saved.id)
        
        assert retrieved.prompt_text == "Updated prompt text"
        assert "new_tag" in retrieved.tags
    
    def test_get_user_prompts(self, test_storage):
        """Test getting all prompts for a user"""
        from tests.conftest import create_test_prompts
        
        prompts = create_test_prompts(test_storage, "user1", count=5)
        prompts2 = create_test_prompts(test_storage, "user2", count=3)
        
        user1_prompts = test_storage.get_user_prompts("user1")
        user2_prompts = test_storage.get_user_prompts("user2")
        
        assert len(user1_prompts) == 5
        assert len(user2_prompts) == 3
        assert all(p.user_id == "user1" for p in user1_prompts)
    
    def test_search_prompts_by_text(self, test_storage):
        """Test searching prompts by text"""
        p1 = Prompt(user_id="user1", prompt_text="Python factorial function")
        p2 = Prompt(user_id="user1", prompt_text="JavaScript sort array")
        p3 = Prompt(user_id="user1", prompt_text="Python list comprehension")
        
        test_storage.save_prompt(p1)
        test_storage.save_prompt(p2)
        test_storage.save_prompt(p3)
        
        results = test_storage.search_prompts("user1", query="Python")
        
        assert len(results) == 2
        assert all("Python" in p.prompt_text for p in results)
    
    def test_search_prompts_by_tags(self, test_storage):
        """Test searching prompts by tags"""
        p1 = Prompt(user_id="user1", prompt_text="Test 1", tags=["python", "beginner"])
        p2 = Prompt(user_id="user1", prompt_text="Test 2", tags=["javascript", "advanced"])
        p3 = Prompt(user_id="user1", prompt_text="Test 3", tags=["python", "advanced"])
        
        test_storage.save_prompt(p1)
        test_storage.save_prompt(p2)
        test_storage.save_prompt(p3)
        
        results = test_storage.search_prompts("user1", tags=["python"])
        
        assert len(results) == 2
        assert all("python" in p.tags for p in results)
    
    def test_get_templates(self, test_storage):
        """Test getting only template prompts"""
        p1 = Prompt(user_id="user1", prompt_text="Template 1", is_template=True)
        p2 = Prompt(user_id="user1", prompt_text="Regular prompt", is_template=False)
        p3 = Prompt(user_id="user1", prompt_text="Template 2", is_template=True)
        
        test_storage.save_prompt(p1)
        test_storage.save_prompt(p2)
        test_storage.save_prompt(p3)
        
        templates = test_storage.get_templates("user1")
        
        assert len(templates) == 2
        assert all(p.is_template for p in templates)
    
    def test_delete_prompt(self, test_storage, sample_prompt):
        """Test deleting a prompt"""
        saved = test_storage.save_prompt(sample_prompt)
        
        # Verify it exists
        assert test_storage.get_prompt(saved.id) is not None
        
        # Delete it
        result = test_storage.delete_prompt(saved.id)
        assert result == True
        
        # Verify it's gone
        assert test_storage.get_prompt(saved.id) is None
    
    def test_save_and_get_user(self, test_storage, sample_user):
        """Test saving and retrieving a user"""
        saved = test_storage.save_user(sample_user)
        retrieved = test_storage.get_user(saved.user_id)
        
        assert retrieved is not None
        assert retrieved.user_id == saved.user_id
        assert retrieved.username == sample_user.username
    
    def test_get_or_create_user(self, test_storage):
        """Test get or create user functionality"""
        # Should create new user
        user1 = test_storage.get_or_create_user("new_user", username="New User")
        assert user1.username == "New User"
        
        # Should get existing user
        user2 = test_storage.get_or_create_user("new_user")
        assert user2.user_id == user1.user_id
        assert user2.username == "New User"
    
    def test_update_user(self, test_storage, sample_user):
        """Test updating user information"""
        saved = test_storage.save_user(sample_user)
        
        # Update preferences
        saved.preferences.daily_goal = 5
        saved.stats.total_prompts = 10
        
        updated = test_storage.save_user(saved)
        retrieved = test_storage.get_user(saved.user_id)
        
        assert retrieved.preferences.daily_goal == 5
        assert retrieved.stats.total_prompts == 10
