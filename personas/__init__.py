"""
Persona factory - Creates and manages persona instances
"""

from personas.base_persona import BasePersona
from personas.beginner import BeginnerPersona
from personas.intermediate import IntermediatePersona
from personas.advanced import AdvancedPersona
from personas.interviewer import InterviewerPersona
from typing import Dict


class PersonaFactory:
    """Factory for creating persona instances"""
    
    _personas: Dict[str, BasePersona] = {
        "beginner": BeginnerPersona(),
        "intermediate": IntermediatePersona(),
        "advanced": AdvancedPersona(),
        "interviewer": InterviewerPersona()
    }
    
    @classmethod
    def get_persona(cls, persona_type: str) -> BasePersona:
        """Get a persona instance by type"""
        persona = cls._personas.get(persona_type.lower())
        if not persona:
            raise ValueError(f"Unknown persona type: {persona_type}")
        return persona
    
    @classmethod
    def list_personas(cls) -> Dict[str, str]:
        """List all available personas with descriptions"""
        return {
            name: persona.description
            for name, persona in cls._personas.items()
        }
    
    @classmethod
    def get_persona_names(cls) -> list:
        """Get list of all persona names"""
        return list(cls._personas.keys())
