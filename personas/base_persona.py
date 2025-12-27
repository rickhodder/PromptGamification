"""
Base persona class using Strategy pattern
All AI personas inherit from this abstract base
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Tuple
from models import Prompt


class BasePersona(ABC):
    """Abstract base class for all AI personas"""
    
    def __init__(self):
        self.name = "Base"
        self.description = "Base persona"
        self.system_prompt = ""
    
    @abstractmethod
    def get_system_prompt(self) -> str:
        """Return the system prompt that defines this persona's behavior"""
        pass
    
    @abstractmethod
    def review_prompt(self, prompt: Prompt) -> Dict[str, any]:
        """
        Review a prompt and provide feedback
        
        Returns:
            Dict containing:
                - suggested_prompt: str (improved version)
                - questions: List[str] (clarifying questions)
                - refinements: List[str] (specific improvements)
                - ratings: Dict[str, float] (quality scores)
                - feedback: str (general feedback)
        """
        pass
    
    def _build_review_prompt(self, prompt: Prompt) -> str:
        """Build the prompt to send to AI for review"""
        review_text = f"""Please review this AI prompt and provide detailed feedback.

**Original Prompt:**
{prompt.prompt_text}
"""
        
        if prompt.description:
            review_text += f"""
**Intended Purpose:**
{prompt.description}
"""
        
        if prompt.what_i_learned:
            review_text += f"""
**What the User Learned:**
{prompt.what_i_learned}
"""
        
        if prompt.what_went_well:
            review_text += f"""
**What Went Well:**
{prompt.what_went_well}
"""
        
        review_text += """

Please provide:
1. An improved version of the prompt
2. 3-5 clarifying questions to better understand the user's intent
3. 3-5 specific refinements that could be made
4. Quality ratings (0-10) for: length, complexity, specificity, clarity, creativity, context
5. General encouraging feedback with security considerations (watch for prompt injection risks)

Format your response as JSON with keys: suggested_prompt, questions, refinements, ratings, feedback
"""
        return review_text
    
    def ask_questions(self, prompt: Prompt) -> List[str]:
        """Generate clarifying questions about the prompt"""
        # This will be implemented by calling the AI
        pass
    
    def suggest_refinements(self, prompt: Prompt, answers: List[str] = None) -> List[str]:
        """Suggest specific refinements, optionally based on user answers"""
        # This will be implemented by calling the AI
        pass
    
    def rate_prompt(self, prompt: Prompt) -> Dict[str, float]:
        """
        Rate prompt on six dimensions
        Returns dict with keys: length, complexity, specificity, clarity, creativity, context
        """
        # This will be implemented by calling the AI
        pass
