"""
Gradio interface for Code Review Environment
Deployed on Hugging Face Spaces
"""

import gradio as gr
import os
from environment import CodeReviewEnv
from models import Action


def run_demo_task(task_id: str, num_steps: int = 5):
    """
    Run a demo of the code review task
    
    Args:
        task_id: Task to run
        num_steps: Number of demo steps
        
    Returns:
        Formatted output string
    """
    env = CodeReviewEnv(task_id=task_id)
    obs = env.reset()
    
    output = f"# Code Review Environment Demo\n\n"
    output += f"**Task:** {task_id}\n"
    output += f"**Description:** {obs.task_description}\n\n"
    output += f"## Files to Review:\n"
    for filename in obs.files.keys():
        output += f"- {filename}\n"
    
    output += f"\n## Code Sample:\n```python\n"
    output += obs.files[obs.current_focus][:500] + "...\n```\n\n"
    
    output += f"## Environment Info:\n"
    output += f"- Max Steps: {obs.max_steps}\n"
    output += f"- Current Step: {obs.step_count}\n"
    output += f"- Files: {len(obs.files)}\n\n"
    
    output += f"## Action Space:\n"
    output += "- identify_bug\n"
    output += "- flag_security_issue\n"
    output += "- suggest_refactor\n"
    output += "- request_context\n"
    output += "- submit_review\n\n"
    
    output += f"## Observation Space:\n"
    output += f"- Task ID: {obs.task_id}\n"
    output += f"- Files: Dict[str, str]\n"
    output += f"- Findings: List[Dict]\n"
    output += f"- Step Count: int\n"
    
    return output


def create_interface():
    """Create Gradio interface"""
    
    with gr.Blocks(title="Code Review Intelligence Environment") as demo:
        gr.Markdown("""
        # 🔍 Code Review Intelligence Environment
        
        An OpenEnv-compliant environment for evaluating AI agents on code review tasks.
        
        ## Features
        - **Task 1 (Easy):** Bug Detection - Identify common bugs in Python code
        - **Task 2 (Medium):** Security Audit - Detect security vulnerabilities
        - **Task 3 (Hard):** Refactoring Analysis - Suggest architectural improvements
        
        ## Environment Details
        - **Action Space:** Structured actions for code review (identify_bug, flag_security_issue, suggest_refactor)
        - **Observation Space:** Code files, task description, findings history
        - **Reward Function:** Incremental rewards based on accuracy and completeness
        - **Grading:** Deterministic graders with precision/recall metrics
        
        ## Usage
        Select a task below to see a demo of the environment.
        """)
        
        with gr.Row():
            task_dropdown = gr.Dropdown(
                choices=["bug_detection", "security_audit", "refactoring_analysis"],
                value="bug_detection",
                label="Select Task"
            )
            steps_slider = gr.Slider(
                minimum=1,
                maximum=10,
                value=5,
                step=1,
                label="Demo Steps"
            )
        
        run_button = gr.Button("Run Demo", variant="primary")
        output_text = gr.Markdown()
        
        run_button.click(
            fn=run_demo_task,
            inputs=[task_dropdown, steps_slider],
            outputs=output_text
        )
        
        gr.Markdown("""
        ## Inference Script
        
        The environment includes an `inference.py` script that follows OpenEnv guidelines:
        
        ```bash
        # Set environment variables
        export HF_TOKEN="your-token"
        export API_BASE_URL="https://api.openai.com/v1"
        export MODEL_NAME="gpt-4o-mini"
        
        # Run inference
        python inference.py
        ```
        
        ## Output Format
        
        The inference script produces output in the required format:
        ```
        [START] task=<task_name> env=code-review model=<model_name>
        [STEP] step=<n> action=<action_str> reward=<0.00> done=<true|false> error=<msg|null>
        [END] success=<true|false> steps=<n> rewards=<r1,r2,...,rn>
        ```
        
        ## Repository
        
        - GitHub: [Code Review Environment](https://github.com/your-repo)
        - Documentation: See README.md for full details
        - OpenEnv Spec: Fully compliant with OpenEnv interface
        
        ## Hardware Requirements
        
        - 2 vCPU
        - 8 GB RAM
        - Docker compatible
        """)
    
    return demo


if __name__ == "__main__":
    demo = create_interface()
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False
    )
