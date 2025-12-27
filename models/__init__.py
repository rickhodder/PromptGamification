"""
Data models for Promptification application
Based on PRD specifications
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from datetime import datetime
from uuid import uuid4


class PromptRatings(BaseModel):
    """Six-dimensional quality assessment for prompts"""
    length: float = Field(default=0.0, ge=0, le=10, description="Appropriate verbosity")
    complexity: float = Field(default=0.0, ge=0, le=10, description="Sophistication of instructions")
    specificity: float = Field(default=0.0, ge=0, le=10, description="Clarity of requirements")
    clarity: float = Field(default=0.0, ge=0, le=10, description="Readability and structure")
    creativity: float = Field(default=0.0, ge=0, le=10, description="Novel approaches")
    context: float = Field(default=0.0, ge=0, le=10, description="Sufficient background information")


class ReviewHistoryEntry(BaseModel):
    """Single review interaction history"""
    timestamp: datetime = Field(default_factory=datetime.now)
    questions: List[str] = Field(default_factory=list)
    answers: List[str] = Field(default_factory=list)
    refinements: List[str] = Field(default_factory=list)
    persona_used: str


class Prompt(BaseModel):
    """Prompt object matching PRD specifications"""
    id: str = Field(default_factory=lambda: str(uuid4()))
    user_id: str
    prompt_text: str = Field(min_length=1)
    description: Optional[str] = None
    what_i_learned: Optional[str] = None
    what_went_well: Optional[str] = None
    ai_suggested_prompt: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    is_template: bool = False
    sharing_preference: Literal["private", "public", "selective"] = "private"
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    ratings: PromptRatings = Field(default_factory=PromptRatings)
    persona_used: Optional[str] = None
    review_history: List[ReviewHistoryEntry] = Field(default_factory=list)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class UserPreferences(BaseModel):
    """User preference settings"""
    default_persona: Literal["beginner", "intermediate", "advanced", "interviewer"] = "beginner"
    daily_goal: int = Field(default=2, ge=1)
    weekly_goal: int = Field(default=14, ge=1)


class UserStats(BaseModel):
    """User statistics for tracking progress"""
    total_prompts: int = 0
    prompts_this_week: int = 0
    prompts_this_month: int = 0
    average_rating: float = 0.0
    streak_days: int = 0


class User(BaseModel):
    """User object matching PRD specifications"""
    user_id: str = Field(default_factory=lambda: str(uuid4()))
    username: str
    email: Optional[str] = None
    preferences: UserPreferences = Field(default_factory=UserPreferences)
    stats: UserStats = Field(default_factory=UserStats)
    created_at: datetime = Field(default_factory=datetime.now)
    last_active_at: datetime = Field(default_factory=datetime.now)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
