#!/usr/bin/env bash
#
# validate-submission.sh — OpenEnv Submission Validator
#
# Checks that your submission meets all hackathon requirements:
# - File structure
# - inference.py requirements
# - Environment variables
# - OpenEnv compliance
# - Tasks and graders
# - Output format
# - Docker configuration
# - Documentation
#
# Usage:
#   chmod +x validate-submission.sh
#   ./validate-submission.sh [repo_dir]
#
# Arguments:
#   repo_dir   Path to your repo (default: current directory)
#

set -uo pipefail

# Color codes
if [ -t 1 ]; then
  RED='\033[0;31m'
  GREEN='\033[0;32m'
  YELLOW='\033[1;33m'
  BLUE='\033[0;34m'
  BOLD='\033[1m'
  NC='\033[0m'
else
  RED='' GREEN='' YELLOW='' BLUE='' BOLD='' NC=''
fi

REPO_DIR="${1:-.}"
ERRORS=0
WARNINGS=0
PASSED=0

print_header() {
  echo ""
  echo -e "${BOLD}${BLUE}============================================================${NC}"
  echo -e "${BOLD}${BLUE}$1${NC}"
  echo -e "${BOLD}${BLUE}============================================================${NC}"
  echo ""
}

print_success() {
  echo -e "${GREEN}✅ $1${NC}"
  ((PASSED++))
}

print_error() {
  echo -e "${RED}❌ $1${NC}"
  ((ERRORS++))
}

print_warning() {
  echo -e "${YELLOW}⚠️  $1${NC}"
  ((WARNINGS++))
}

print_info() {
  echo "   $1"
}

check_file_exists() {
  local file="$1"
  local description="$2"
  
  if [ -f "$REPO_DIR/$file" ]; then
    print_success "$description exists"
    return 0
  else
    print_error "$description is missing"
    return 1
  fi
}

check_dir_exists() {
  local dir="$1"
  local description="$2"
  
  if [ -d "$REPO_DIR/$dir" ]; then
    print_success "$description exists"
    return 0
  else
    print_error "$description is missing"
    return 1
  fi
}

check_file_contains() {
  local file="$1"
  local pattern="$2"
  local description="$3"
  
  if [ ! -f "$REPO_DIR/$file" ]; then
    return 1
  fi
  
  if grep -q "$pattern" "$REPO_DIR/$file"; then
    print_success "$description"
    return 0
  else
    print_error "$description - NOT FOUND"
    return 1
  fi
}

# Main validation
print_header "OpenEnv Submission Validator"

# Check 1: File Structure
print_header "File Structure"

check_file_exists "inference.py" "inference.py"
check_file_exists "environment.py" "environment.py"
check_file_exists "models.py" "models.py"
check_file_exists "openenv.yaml" "openenv.yaml"
check_file_exists "Dockerfile" "Dockerfile"
check_file_exists "requirements.txt" "requirements.txt"
check_file_exists "README.md" "README.md"

check_dir_exists "graders" "graders/ directory"
if [ -d "$REPO_DIR/graders" ]; then
  check_file_exists "graders/bug_grader.py" "  - bug_grader.py"
  check_file_exists "graders/security_grader.py" "  - security_grader.py"
  check_file_exists "graders/refactoring_grader.py" "  - refactoring_grader.py"
fi

if [ -d "$REPO_DIR/data" ]; then
  print_success "data/ directory exists"
else
  print_warning "data/ directory missing (optional but recommended)"
fi

# Check 2: inference.py Requirements
print_header "inference.py Requirements"

if [ -f "$REPO_DIR/inference.py" ]; then
  print_success "inference.py is in root directory"
  
  check_file_contains "inference.py" "from openai import OpenAI" "Uses OpenAI client"
  check_file_contains "inference.py" 'os.getenv("API_BASE_URL"' "Reads API_BASE_URL environment variable"
  check_file_contains "inference.py" 'os.getenv("MODEL_NAME"' "Reads MODEL_NAME environment variable"
  check_file_contains "inference.py" 'os.getenv("HF_TOKEN"' "Reads HF_TOKEN environment variable"
  check_file_contains "inference.py" "\[START\]" "Contains [START] output marker"
  check_file_contains "inference.py" "\[STEP\]" "Contains [STEP] output marker"
  check_file_contains "inference.py" "\[END\]" "Contains [END] output marker"
else
  print_error "inference.py not found in root directory"
fi

# Check 3: Environment Variables
print_header "Environment Variables"

if [ -f "$REPO_DIR/inference.py" ]; then
  if grep -q 'API_BASE_URL = os.getenv("API_BASE_URL".*"' "$REPO_DIR/inference.py"; then
    print_success "API_BASE_URL has default value"
  else
    print_error "API_BASE_URL missing default value"
  fi
  
  if grep -q 'MODEL_NAME = os.getenv("MODEL_NAME".*"' "$REPO_DIR/inference.py"; then
    print_success "MODEL_NAME has default value"
  else
    print_error "MODEL_NAME missing default value"
  fi
  
  if grep -q 'HF_TOKEN = os.getenv("HF_TOKEN")' "$REPO_DIR/inference.py"; then
    if grep -q "HF_TOKEN is None" "$REPO_DIR/inference.py" || grep -q "not HF_TOKEN" "$REPO_DIR/inference.py"; then
      print_success "HF_TOKEN is mandatory (no default)"
    else
      print_warning "HF_TOKEN should raise error if not provided"
    fi
  fi
fi

# Check 4: OpenEnv Compliance
print_header "OpenEnv Compliance"

if [ -f "$REPO_DIR/environment.py" ]; then
  check_file_contains "environment.py" "def reset(" "Environment has reset() method"
  check_file_contains "environment.py" "def step(" "Environment has step() method"
  check_file_contains "environment.py" "def state(" "Environment has state() method"
  check_file_contains "environment.py" "def close(" "Environment has close() method"
fi

if [ -f "$REPO_DIR/models.py" ]; then
  check_file_contains "models.py" "class Action" "Pydantic model Action defined"
  check_file_contains "models.py" "class Observation" "Pydantic model Observation defined"
  check_file_contains "models.py" "class Reward" "Pydantic model Reward defined"
fi

check_file_exists "openenv.yaml" "openenv.yaml"

# Check 5: Tasks and Graders
print_header "Tasks and Graders"

TASK_COUNT=0
if [ -f "$REPO_DIR/environment.py" ]; then
  if grep -q "bug_detection" "$REPO_DIR/environment.py"; then
    print_success "Task 'bug_detection' found"
    ((TASK_COUNT++))
  fi
  
  if grep -q "security_audit" "$REPO_DIR/environment.py"; then
    print_success "Task 'security_audit' found"
    ((TASK_COUNT++))
  fi
  
  if grep -q "refactoring_analysis" "$REPO_DIR/environment.py"; then
    print_success "Task 'refactoring_analysis' found"
    ((TASK_COUNT++))
  fi
  
  if [ $TASK_COUNT -ge 3 ]; then
    print_success "Found $TASK_COUNT tasks (requirement: 3+)"
  else
    print_error "Only found $TASK_COUNT tasks (requirement: 3+)"
  fi
fi

if [ -d "$REPO_DIR/graders" ]; then
  GRADER_COUNT=$(find "$REPO_DIR/graders" -name "*_grader.py" | wc -l)
  if [ $GRADER_COUNT -ge 3 ]; then
    print_success "Found $GRADER_COUNT graders"
  else
    print_error "Only found $GRADER_COUNT graders (requirement: 3+)"
  fi
fi

# Check 6: Output Format
print_header "Output Format"

if [ -f "$REPO_DIR/inference.py" ]; then
  check_file_contains "inference.py" "\[START\] task=" "START line format present"
  check_file_contains "inference.py" "\[STEP\] step=" "STEP line format present"
  check_file_contains "inference.py" "\[END\] success=" "END line format present"
  check_file_contains "inference.py" "reward=" "Reward formatting present"
  check_file_contains "inference.py" "done=" "Done flag present"
  check_file_contains "inference.py" "error=" "Error field present"
  check_file_contains "inference.py" ":.2f" "Reward formatted to 2 decimal places"
fi

# Check 7: Docker Configuration
print_header "Docker Configuration"

if [ -f "$REPO_DIR/Dockerfile" ]; then
  print_success "Dockerfile exists"
  check_file_contains "Dockerfile" "FROM python:" "Uses Python base image"
  check_file_contains "Dockerfile" "requirements.txt" "Installs requirements.txt"
  check_file_contains "Dockerfile" "EXPOSE" "Exposes port for Gradio"
else
  print_error "Dockerfile is missing"
fi

# Check 8: Documentation
print_header "Documentation"

if [ -f "$REPO_DIR/README.md" ]; then
  print_success "README.md exists"
  
  if grep -qi "overview" "$REPO_DIR/README.md"; then
    print_success "Contains environment overview"
  else
    print_warning "May be missing environment overview"
  fi
  
  if grep -qi "task" "$REPO_DIR/README.md"; then
    print_success "Contains task descriptions"
  else
    print_warning "May be missing task descriptions"
  fi
  
  if grep -qi "action" "$REPO_DIR/README.md"; then
    print_success "Contains action space"
  else
    print_warning "May be missing action space"
  fi
  
  if grep -qi "observation" "$REPO_DIR/README.md"; then
    print_success "Contains observation space"
  else
    print_warning "May be missing observation space"
  fi
  
  if grep -qi "setup" "$REPO_DIR/README.md"; then
    print_success "Contains setup instructions"
  else
    print_warning "May be missing setup instructions"
  fi
  
  if grep -qi "usage" "$REPO_DIR/README.md"; then
    print_success "Contains usage instructions"
  else
    print_warning "May be missing usage instructions"
  fi
else
  print_error "README.md is missing"
fi

# Summary
print_header "Validation Summary"

echo ""
echo -e "${BOLD}Passed Checks:${NC} $PASSED"

if [ $WARNINGS -gt 0 ]; then
  echo ""
  echo -e "${YELLOW}${BOLD}Warnings:${NC} $WARNINGS"
  print_info "Consider addressing warnings for best results"
fi

if [ $ERRORS -gt 0 ]; then
  echo ""
  echo -e "${RED}${BOLD}Errors:${NC} $ERRORS"
  echo ""
  echo -e "${RED}${BOLD}❌ VALIDATION FAILED${NC}"
  print_info "Fix the errors above before submitting"
  exit 1
else
  echo ""
  echo -e "${GREEN}${BOLD}✅ VALIDATION PASSED${NC}"
  print_info "Your submission is ready!"
  if [ $WARNINGS -gt 0 ]; then
    print_info "Consider addressing warnings for best results"
  fi
  exit 0
fi
