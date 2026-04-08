"""
Pydantic models for Code Review Environment
Defines Action, Observation, and Reward structures
"""

from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Literal


class Action(BaseModel):
    """Action space for code review tasks"""
    action_type: Literal[
        "identify_bug",
        "flag_security_issue",
        "suggest_refactor",
        "request_context",
        "submit_review"
    ] = Field(description="Type of review action to perform")
    
    file_path: str = Field(description="Path to the file being reviewed")
    line_number: Optional[int] = Field(default=None, description="Line number of the issue")
    description: str = Field(description="Description of the finding or suggestion")
    severity: Literal["info", "low", "medium", "high", "critical"] = Field(
        default="medium",
        description="Severity level of the issue"
    )
    suggested_fix: Optional[str] = Field(default=None, description="Suggested code fix")


class Observation(BaseModel):
    """Observation space for code review tasks"""
    task_id: str = Field(description="Unique identifier for the task")
    task_description: str = Field(description="Description of what to review")
    files: Dict[str, str] = Field(description="Dictionary of filename to code content")
    current_focus: str = Field(description="Current file being reviewed")
    findings_so_far: List[Dict] = Field(default_factory=list, description="List of findings made so far")
    remaining_files: int = Field(description="Number of files left to review")
    step_count: int = Field(default=0, description="Current step number")
    max_steps: int = Field(default=50, description="Maximum allowed steps")


class Reward(BaseModel):
    """Reward structure for code review tasks"""
    value: float = Field(description="Total reward value (0.0 to 1.0)")
    breakdown: Dict[str, float] = Field(default_factory=dict, description="Component scores")
    feedback: str = Field(default="", description="Feedback message")


class TaskResult(BaseModel):
    """Final result of a task"""
    success: bool = Field(description="Whether the task was completed successfully")
    total_reward: float = Field(description="Total accumulated reward")
    steps_taken: int = Field(description="Number of steps taken")
    findings: List[Dict] = Field(description="All findings made during the task")
    score: float = Field(description="Final score (0.0 to 1.0)")
