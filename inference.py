"""
Inference script for Code Review Environment
Follows OpenEnv Hackathon guidelines for output format
"""

import os
import sys
import json
from openai import OpenAI
from environment import CodeReviewEnv
from models import Action


# ✅ Required environment variables with defaults
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
HF_TOKEN = os.getenv("HF_TOKEN")

# ✅ HF_TOKEN is mandatory
if HF_TOKEN is None:
    raise ValueError("HF_TOKEN environment variable is required")

# ✅ Initialize OpenAI client
client = OpenAI(
    base_url=API_BASE_URL,
    api_key=HF_TOKEN
)


def get_llm_response(prompt: str, max_tokens: int = 500) -> str:
    """
    Get response from LLM using OpenAI client
    
    Args:
        prompt: The prompt to send to the LLM
        max_tokens: Maximum tokens in response
        
    Returns:
        LLM response text
    """
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a code review expert. Analyze code and identify issues."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"


def parse_llm_action(llm_response: str, file_path: str) -> Action:
    """
    Parse LLM response into an Action
    
    Args:
        llm_response: Response from LLM
        file_path: Current file being reviewed
        
    Returns:
        Action object
    """
    # Simple parsing - in production, this would be more sophisticated
    response_lower = llm_response.lower()
    
    # Determine action type
    if "submit" in response_lower or "complete" in response_lower:
        action_type = "submit_review"
    elif "security" in response_lower or "vulnerability" in response_lower or "sql injection" in response_lower:
        action_type = "flag_security_issue"
    elif "refactor" in response_lower or "improve" in response_lower:
        action_type = "suggest_refactor"
    else:
        action_type = "identify_bug"
    
    # Extract line number if mentioned
    line_number = None
    for word in llm_response.split():
        if word.isdigit():
            line_number = int(word)
            break
    
    # Determine severity
    severity = "medium"
    if "critical" in response_lower:
        severity = "critical"
    elif "high" in response_lower:
        severity = "high"
    elif "low" in response_lower:
        severity = "low"
    
    return Action(
        action_type=action_type,
        file_path=file_path,
        line_number=line_number,
        description=llm_response[:200],  # Truncate for brevity
        severity=severity,
        suggested_fix=None
    )


def run_task(task_id: str, max_steps: int = 10):
    """
    Run a single task with the LLM agent
    
    Args:
        task_id: Task identifier
        max_steps: Maximum number of steps to run
    """
    env = CodeReviewEnv(task_id=task_id)
    
    # ✅ [START] line - exactly as specified in guidelines
    print(f"[START] task={task_id} env=code-review model={MODEL_NAME}")
    
    rewards = []
    
    try:
        # Reset environment
        obs = env.reset()
        
        # Run episode
        for step in range(1, max_steps + 1):
            # Create prompt for LLM
            prompt = f"""Review the following code and identify issues:

Task: {obs.task_description}
File: {obs.current_focus}

Code:
{obs.files[obs.current_focus][:1000]}  # Truncate for token limits

Previous findings: {len(obs.findings_so_far)}

Provide your next finding or type 'submit' if review is complete."""
            
            # Get LLM response
            llm_response = get_llm_response(prompt)
            
            # Parse into action
            action = parse_llm_action(llm_response, obs.current_focus)
            
            # Execute action
            obs, reward, done, info = env.step(action)
            rewards.append(reward)
            
            # ✅ [STEP] line - exactly as specified in guidelines
            error_str = info.get('last_action_error') if info.get('last_action_error') else "null"
            done_str = "true" if done else "false"
            action_str = f"{action.action_type}('{action.file_path}',{action.line_number})"
            
            print(f"[STEP] step={step} action={action_str} reward={reward:.2f} done={done_str} error={error_str}")
            
            if done:
                break
        
        success = done and env.get_final_score() > 0.5
        
    except Exception as e:
        # Handle errors gracefully
        success = False
        print(f"[STEP] step={len(rewards)+1} action=error() reward=0.00 done=true error={str(e)}", file=sys.stderr)
    
    finally:
        # ✅ [END] line - always emitted, exactly as specified in guidelines
        success_str = "true" if success else "false"
        rewards_str = ",".join([f"{r:.2f}" for r in rewards])
        print(f"[END] success={success_str} steps={len(rewards)} rewards={rewards_str}")
        
        env.close()


def main():
    """Main entry point"""
    # Run all three tasks
    tasks = ["bug_detection", "security_audit", "refactoring_analysis"]
    
    for task_id in tasks:
        print(f"\n{'='*60}")
        print(f"Running task: {task_id}")
        print(f"{'='*60}\n")
        
        run_task(task_id, max_steps=10)
        print()


if __name__ == "__main__":
    main()
