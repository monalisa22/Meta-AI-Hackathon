"""
Code Review Intelligence Environment
Main OpenEnv implementation for code review tasks
"""

import os
from typing import Dict, Tuple, Any
from models import Action, Observation, Reward, TaskResult
from graders.bug_grader import BugGrader
from graders.security_grader import SecurityGrader
from graders.refactoring_grader import RefactoringGrader


class CodeReviewEnv:
    """
    OpenEnv-compliant environment for code review tasks
    """
    
    def __init__(self, task_id: str = "bug_detection"):
        """
        Initialize the environment
        
        Args:
            task_id: One of 'bug_detection', 'security_audit', 'refactoring_analysis'
        """
        self.task_id = task_id
        self.current_step = 0
        self.max_steps = self._get_max_steps(task_id)
        self.done = False
        self.findings = []
        self.total_reward = 0.0
        self.last_action_error = None
        
        # Load task data
        self.task_data = self._load_task_data(task_id)
        
        # Initialize grader
        self.grader = self._get_grader(task_id)
    
    def _get_max_steps(self, task_id: str) -> int:
        """Get maximum steps for task"""
        max_steps_map = {
            "bug_detection": 30,
            "security_audit": 50,
            "refactoring_analysis": 100
        }
        return max_steps_map.get(task_id, 50)
    
    def _get_grader(self, task_id: str):
        """Get appropriate grader for task"""
        grader_map = {
            "bug_detection": BugGrader(),
            "security_audit": SecurityGrader(),
            "refactoring_analysis": RefactoringGrader()
        }
        return grader_map.get(task_id)
    
    def _load_task_data(self, task_id: str) -> Dict:
        """Load task-specific data"""
        base_path = os.path.dirname(__file__)
        
        if task_id == "bug_detection":
            file_path = os.path.join(base_path, "data", "buggy_code", "task1_sample.py")
            with open(file_path, 'r') as f:
                code = f.read()
            return {
                "description": "Identify common bugs in the Python code",
                "files": {"task1_sample.py": code},
                "focus": "task1_sample.py"
            }
        
        elif task_id == "security_audit":
            file_path = os.path.join(base_path, "data", "vulnerable_code", "api.py")
            with open(file_path, 'r') as f:
                code = f.read()
            return {
                "description": "Detect security vulnerabilities in the API code",
                "files": {"api.py": code},
                "focus": "api.py"
            }
        
        elif task_id == "refactoring_analysis":
            user_service_path = os.path.join(base_path, "data", "refactoring_scenarios", "user_service.py")
            notification_path = os.path.join(base_path, "data", "refactoring_scenarios", "notification_service.py")
            
            with open(user_service_path, 'r') as f:
                user_code = f.read()
            with open(notification_path, 'r') as f:
                notification_code = f.read()
            
            return {
                "description": "Analyze code and suggest architectural improvements",
                "files": {
                    "user_service.py": user_code,
                    "notification_service.py": notification_code
                },
                "focus": "user_service.py"
            }
        
        return {}
    
    def reset(self) -> Observation:
        """
        Reset the environment to initial state
        
        Returns:
            Initial observation
        """
        self.current_step = 0
        self.done = False
        self.findings = []
        self.total_reward = 0.0
        self.last_action_error = None
        
        observation = Observation(
            task_id=self.task_id,
            task_description=self.task_data["description"],
            files=self.task_data["files"],
            current_focus=self.task_data["focus"],
            findings_so_far=[],
            remaining_files=len(self.task_data["files"]),
            step_count=0,
            max_steps=self.max_steps
        )
        
        return observation
    
    def step(self, action: Action) -> Tuple[Observation, float, bool, Dict[str, Any]]:
        """
        Execute one step in the environment
        
        Args:
            action: Action to take
            
        Returns:
            Tuple of (observation, reward, done, info)
        """
        self.current_step += 1
        self.last_action_error = None
        reward = 0.0
        
        # Validate action
        try:
            if not isinstance(action, Action):
                action = Action(**action)
        except Exception as e:
            self.last_action_error = f"Invalid action format: {str(e)}"
            reward = -0.1
        else:
            # Process action
            action_dict = action.model_dump()
            self.findings.append(action_dict)
            
            # Calculate incremental reward
            if action.action_type == "submit_review":
                # Final grading
                score, breakdown = self.grader.grade(self.findings)
                reward = score
                self.done = True
            else:
                # Incremental reward for valid actions
                reward = 0.01
        
        # Check if max steps reached
        if self.current_step >= self.max_steps:
            self.done = True
            if action.action_type != "submit_review":
                # Auto-grade if max steps reached without submission
                score, breakdown = self.grader.grade(self.findings)
                reward = score * 0.8  # Penalty for not submitting
        
        self.total_reward += reward
        
        # Create observation
        observation = Observation(
            task_id=self.task_id,
            task_description=self.task_data["description"],
            files=self.task_data["files"],
            current_focus=self.task_data["focus"],
            findings_so_far=self.findings,
            remaining_files=len(self.task_data["files"]),
            step_count=self.current_step,
            max_steps=self.max_steps
        )
        
        # Info dict
        info = {
            "step": self.current_step,
            "total_reward": round(self.total_reward, 2),
            "findings_count": len(self.findings),
            "last_action_error": self.last_action_error
        }
        
        return observation, reward, self.done, info
    
    def state(self) -> Dict[str, Any]:
        """
        Get current environment state
        
        Returns:
            Dictionary containing current state
        """
        return {
            "task_id": self.task_id,
            "current_step": self.current_step,
            "max_steps": self.max_steps,
            "done": self.done,
            "total_reward": round(self.total_reward, 2),
            "findings_count": len(self.findings),
            "last_action_error": self.last_action_error
        }
    
    def close(self):
        """Clean up environment resources"""
        pass
    
    def get_final_score(self) -> float:
        """
        Get final score for the task
        
        Returns:
            Score between 0.0 and 1.0
        """
        if not self.done:
            return 0.0
        
        score, breakdown = self.grader.grade(self.findings)
        return score
