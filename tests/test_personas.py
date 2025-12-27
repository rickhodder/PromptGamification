"""
Tests for persona system
"""

import pytest
from personas import PersonaFactory
from personas.beginner import BeginnerPersona
from personas.intermediate import IntermediatePersona
from personas.advanced import AdvancedPersona
from personas.interviewer import InterviewerPersona


class TestPersonaFactory:
    """Test PersonaFactory"""
    
    def test_get_persona_beginner(self):
        """Test getting beginner persona"""
        persona = PersonaFactory.get_persona("beginner")
        assert isinstance(persona, BeginnerPersona)
        assert persona.name == "Friendly Guide"
    
    def test_get_persona_intermediate(self):
        """Test getting intermediate persona"""
        persona = PersonaFactory.get_persona("intermediate")
        assert isinstance(persona, IntermediatePersona)
        assert persona.name == "Practical Coach"
    
    def test_get_persona_advanced(self):
        """Test getting advanced persona"""
        persona = PersonaFactory.get_persona("advanced")
        assert isinstance(persona, AdvancedPersona)
        assert persona.name == "Advanced Mentor"
    
    def test_get_persona_interviewer(self):
        """Test getting interviewer persona"""
        persona = PersonaFactory.get_persona("interviewer")
        assert isinstance(persona, InterviewerPersona)
        assert persona.name == "Critical Interviewer"
    
    def test_get_invalid_persona(self):
        """Test getting invalid persona raises error"""
        with pytest.raises(ValueError):
            PersonaFactory.get_persona("invalid")
    
    def test_list_personas(self):
        """Test listing all personas"""
        personas = PersonaFactory.list_personas()
        
        assert len(personas) == 4
        assert "beginner" in personas
        assert "intermediate" in personas
        assert "advanced" in personas
        assert "interviewer" in personas
    
    def test_get_persona_names(self):
        """Test getting persona names"""
        names = PersonaFactory.get_persona_names()
        
        assert len(names) == 4
        assert "beginner" in names
        assert "intermediate" in names


class TestPersonas:
    """Test individual persona implementations"""
    
    def test_beginner_system_prompt(self):
        """Test beginner persona system prompt"""
        persona = BeginnerPersona()
        prompt = persona.get_system_prompt()
        
        assert "beginner" in prompt.lower()
        assert "simple" in prompt.lower()
        assert "encouraging" in prompt.lower()
    
    def test_intermediate_system_prompt(self):
        """Test intermediate persona system prompt"""
        persona = IntermediatePersona()
        prompt = persona.get_system_prompt()
        
        assert "intermediate" in prompt.lower()
        assert "practical" in prompt.lower() or "technical" in prompt.lower()
    
    def test_advanced_system_prompt(self):
        """Test advanced persona system prompt"""
        persona = AdvancedPersona()
        prompt = persona.get_system_prompt()
        
        assert "advanced" in prompt.lower() or "expert" in prompt.lower()
        assert "technical" in prompt.lower()
    
    def test_interviewer_system_prompt(self):
        """Test interviewer persona system prompt"""
        persona = InterviewerPersona()
        prompt = persona.get_system_prompt()
        
        assert "interview" in prompt.lower()
        assert "direct" in prompt.lower()
    
    def test_persona_review_structure(self, sample_prompt):
        """Test that persona review returns expected structure"""
        persona = BeginnerPersona()
        review = persona.review_prompt(sample_prompt)
        
        # Check all required keys are present
        assert "suggested_prompt" in review
        assert "questions" in review
        assert "refinements" in review
        assert "ratings" in review
        assert "feedback" in review
        
        # Check types
        assert isinstance(review["suggested_prompt"], str)
        assert isinstance(review["questions"], list)
        assert isinstance(review["refinements"], list)
        assert isinstance(review["ratings"], dict)
        assert isinstance(review["feedback"], str)
        
        # Check ratings structure
        assert "length" in review["ratings"]
        assert "complexity" in review["ratings"]
        assert "specificity" in review["ratings"]
        assert "clarity" in review["ratings"]
        assert "creativity" in review["ratings"]
        assert "context" in review["ratings"]
