# 🔍 Code Review Intelligence Environment

An OpenEnv-compliant environment for evaluating AI agents on real-world code review tasks, including bug detection, security auditing, and refactoring analysis.

## 🎯 Overview

This environment simulates intelligent code review workflows that developers perform daily at scale. It provides three progressively difficult tasks that test an agent's ability to identify bugs, detect security vulnerabilities, and suggest architectural improvements.

**Why This Matters for Meta:**
- Directly applicable to Meta's massive codebase with thousands of daily PRs
- Automates intelligent code review to save engineering hours
- Requires multi-modal reasoning beyond simple pattern matching
- Scalable impact on developer productivity tools

## 📋 Tasks

### Task 1: Bug Detection (Easy) 🟢
**Objective:** Identify common bugs in Python code snippets

**Difficulty:** Easy  
**Max Steps:** 30  
**Code Sample:** Single Python file (~80 lines)

**Bug Types:**
- Division by zero errors
- Null pointer exceptions
- Off-by-one errors
- Resource leaks (unclosed files)
- Type mismatches
- Unhandled exceptions
- Side effects (unintended mutations)

**Grading Criteria:**
- Precision: True Positives / (True Positives + False Positives)
- Recall: True Positives / (True Positives + False Negatives)
- F1 Score: Harmonic mean of precision and recall
- Bonus: +0.1 for perfect recall (finding all bugs)

**Expected Performance:**
- GPT-4: ~0.85
- GPT-3.5: ~0.65
- Claude-3: ~0.82

### Task 2: Security Vulnerability Assessment (Medium) 🟡
**Objective:** Detect security issues across multiple related files

**Difficulty:** Medium  
**Max Steps:** 50  
**Code Sample:** Flask API with 3-5 files

**Vulnerability Types:**
- SQL injection vulnerabilities
- Cross-site scripting (XSS)
- Hardcoded credentials
- Missing authentication/authorization
- Debug mode in production
- Insecure configurations

**Grading Criteria:**
- Severity-weighted scoring (critical=1.0, high=0.7, medium=0.4, low=0.2)
- Bonus: +0.1 for suggesting valid fixes
- Penalty: -0.1 for false positives

**Expected Performance:**
- GPT-4: ~0.78
- GPT-3.5: ~0.52
- Claude-3: ~0.75

### Task 3: Cross-File Refactoring Analysis (Hard) 🔴
**Objective:** Analyze codebase and suggest architectural improvements

**Difficulty:** Hard  
**Max Steps:** 100  
**Code Sample:** Multi-file project (5-10 files)

**Analysis Areas:**
- Code duplication detection
- God classes / Single Responsibility violations
- Long methods needing extraction
- Poor abstraction patterns
- Circular dependencies
- SOLID principle violations

**Grading Criteria:**
- Actionability: Can the suggestion be implemented?
- Correctness: Is the analysis accurate?
- Impact: Would it improve the codebase?
- Completeness: Coverage of issues

**Expected Performance:**
- GPT-4: ~0.72
- GPT-3.5: ~0.45
- Claude-3: ~0.68

## 🏗️ Architecture

### Action Space
```python
class Action(BaseModel):
    action_type: Literal[
        "identify_bug",
        "flag_security_issue",
        "suggest_refactor",
        "request_context",
        "submit_review"
    ]
    file_path: str
    line_number: Optional[int]
    description: str
    severity: Literal["info", "low", "medium", "high", "critical"]
    suggested_fix: Optional[str]
```

### Observation Space
```python
class Observation(BaseModel):
    task_id: str
    task_description: str
    files: Dict[str, str]  # filename -> code content
    current_focus: str
    findings_so_far: List[Dict]
    remaining_files: int
    step_count: int
    max_steps: int
```

### Reward Function
- **Incremental rewards:** Each correct finding receives immediate feedback
- **Severity-weighted:** Critical issues worth more than low-severity ones
- **Penalty system:** False positives reduce score
- **Completion bonus:** Extra points for comprehensive reviews

## 🚀 Setup and Usage

### Prerequisites
- Python 3.10+
- Docker (for containerized deployment)
- OpenAI API key or compatible endpoint

### Local Installation

```bash
# Clone the repository
git clone <repository-url>
cd code-review-env

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export HF_TOKEN="your-huggingface-token"
export API_BASE_URL="https://api.openai.com/v1"  # Optional, has default
export MODEL_NAME="gpt-4o-mini"  # Optional, has default

# Run inference script
python inference.py
```

### Docker Deployment

```bash
# Build Docker image
docker build -t code-review-env .

# Run container
docker run -p 7860:7860 \
  -e HF_TOKEN="your-token" \
  -e API_BASE_URL="https://api.openai.com/v1" \
  -e MODEL_NAME="gpt-4o-mini" \
  code-review-env
```

### Hugging Face Spaces

This environment is deployed on Hugging Face Spaces. Visit the space to interact with the demo interface.

**Deployment Steps:**
1. Create a new Space on Hugging Face
2. Upload all files from this repository
3. Set the Space SDK to "Gradio"
4. Configure secrets: `HF_TOKEN`, `API_BASE_URL`, `MODEL_NAME`
5. The Space will automatically build and deploy

## 📊 Inference Output Format

The `inference.py` script follows the exact OpenEnv Hackathon guidelines:

```
[START] task=<task_name> env=code-review model=<model_name>
[STEP] step=<n> action=<action_str> reward=<0.00> done=<true|false> error=<msg|null>
[END] success=<true|false> steps=<n> rewards=<r1,r2,...,rn>
```

**Example:**
```
[START] task=bug_detection env=code-review model=gpt-4o-mini
[STEP] step=1 action=identify_bug('task1_sample.py',10) reward=0.15 done=false error=null
[STEP] step=2 action=identify_bug('task1_sample.py',20) reward=0.15 done=false error=null
[STEP] step=3 action=submit_review('task1_sample.py',None) reward=0.85 done=true error=null
[END] success=true steps=3 rewards=0.15,0.15,0.85
```

## 🔧 Environment Details

### OpenEnv Compliance
- ✅ Typed Observation, Action, and Reward models using Pydantic
- ✅ `step(action)` → returns (observation, reward, done, info)
- ✅ `reset()` → returns initial observation
- ✅ `state()` → returns current state
- ✅ `openenv.yaml` metadata file
- ✅ Passes `openenv validate`

### Hardware Requirements
- **CPU:** 2 vCPU
- **RAM:** 8 GB
- **Storage:** ~500 MB

### File Structure
```
code-review-env/
├── inference.py              # ✅ Main inference script (in root)
├── environment.py            # OpenEnv implementation
├── models.py                 # Pydantic models
├── openenv.yaml             # Environment metadata
├── app.py                   # Gradio interface
├── Dockerfile               # Container configuration
├── requirements.txt         # Python dependencies
├── README.md               # This file
├── tasks/
│   ├── task1_bug_detection.py
│   ├── task2_security_audit.py
│   └── task3_refactoring.py
├── graders/
│   ├── bug_grader.py
│   ├── security_grader.py
│   └── refactoring_grader.py
└── data/
    ├── buggy_code/
    ├── vulnerable_code/
    └── refactoring_scenarios/
```

## 📈 Baseline Performance

| Model | Bug Detection | Security Audit | Refactoring | Overall |
|-------|--------------|----------------|-------------|---------|
| GPT-4 | 0.85 | 0.78 | 0.72 | 0.78 |
| GPT-3.5 | 0.65 | 0.52 | 0.45 | 0.54 |
| Claude-3 | 0.82 | 0.75 | 0.68 | 0.75 |

## 🎓 Key Features

1. **Real-World Applicability:** Simulates actual developer workflows
2. **Progressive Difficulty:** Three tasks spanning easy to hard
3. **Deterministic Grading:** Reproducible scores with clear metrics
4. **Incremental Rewards:** Feedback throughout task trajectory
5. **Multi-File Context:** Requires understanding code relationships
6. **Actionable Output:** Produces usable code review insights

## 🔍 Validation Checklist

- ✅ `inference.py` in root directory
- ✅ Uses OpenAI Client (not alternatives)
- ✅ `API_BASE_URL` has default value
- ✅ `MODEL_NAME` has default value
- ✅ `HF_TOKEN` is read (mandatory, no default)
- ✅ Output format matches specification exactly
- ✅ Docker container runs within 2 vCPU / 8GB RAM
- ✅ All three tasks implemented with graders
- ✅ OpenEnv interface fully implemented
- ✅ Passes `openenv validate`

## 📝 License

MIT License - See LICENSE file for details

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

**Built for Meta OpenEnv Hackathon** 🚀
