#!/usr/bin/env python3
"""
Pre-Submission Validation Script for Meta OpenEnv Hackathon
Validates all requirements before submission
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple
import importlib.util


class Colors:
    """ANSI color codes"""
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    BOLD = '\033[1m'
    NC = '\033[0m'  # No Color


def print_header(text: str):
    """Print section header"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.NC}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text}{Colors.NC}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.NC}\n")


def print_success(text: str):
    """Print success message"""
    print(f"{Colors.GREEN}✅ {text}{Colors.NC}")


def print_error(text: str):
    """Print error message"""
    print(f"{Colors.RED}❌ {text}{Colors.NC}")


def print_warning(text: str):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.NC}")


def print_info(text: str):
    """Print info message"""
    print(f"   {text}")


class SubmissionValidator:
    """Validates OpenEnv submission requirements"""
    
    def __init__(self, repo_dir: str = "."):
        self.repo_dir = Path(repo_dir)
        self.errors = []
        self.warnings = []
        self.passed = []
    
    def validate_all(self) -> bool:
        """Run all validation checks"""
        print_header("OpenEnv Submission Validator")
        
        checks = [
            ("File Structure", self.check_file_structure),
            ("inference.py Requirements", self.check_inference_script),
            ("Environment Variables", self.check_environment_variables),
            ("OpenEnv Compliance", self.check_openenv_compliance),
            ("Tasks and Graders", self.check_tasks_and_graders),
            ("Output Format", self.check_output_format),
            ("Docker Configuration", self.check_docker),
            ("Documentation", self.check_documentation),
        ]
        
        for check_name, check_func in checks:
            print_header(check_name)
            try:
                check_func()
            except Exception as e:
                print_error(f"Check failed with exception: {str(e)}")
                self.errors.append(f"{check_name}: {str(e)}")
        
        # Print summary
        self.print_summary()
        
        return len(self.errors) == 0
    
    def check_file_structure(self):
        """Validate required files exist"""
        required_files = [
            "inference.py",
            "environment.py",
            "models.py",
            "openenv.yaml",
            "Dockerfile",
            "requirements.txt",
            "README.md",
        ]
        
        for file in required_files:
            file_path = self.repo_dir / file
            if file_path.exists():
                print_success(f"{file} exists")
                self.passed.append(f"File: {file}")
            else:
                print_error(f"{file} is missing")
                self.errors.append(f"Missing required file: {file}")
        
        # Check graders directory
        graders_dir = self.repo_dir / "graders"
        if graders_dir.exists() and graders_dir.is_dir():
            print_success("graders/ directory exists")
            grader_files = ["bug_grader.py", "security_grader.py", "refactoring_grader.py"]
            for grader in grader_files:
                if (graders_dir / grader).exists():
                    print_success(f"  - {grader} exists")
                else:
                    print_error(f"  - {grader} is missing")
                    self.errors.append(f"Missing grader: {grader}")
        else:
            print_error("graders/ directory is missing")
            self.errors.append("Missing graders directory")
        
        # Check data directory
        data_dir = self.repo_dir / "data"
        if data_dir.exists() and data_dir.is_dir():
            print_success("data/ directory exists")
        else:
            print_warning("data/ directory is missing (optional but recommended)")
    
    def check_inference_script(self):
        """Validate inference.py requirements"""
        inference_path = self.repo_dir / "inference.py"
        
        if not inference_path.exists():
            print_error("inference.py not found in root directory")
            self.errors.append("inference.py must be in root directory")
            return
        
        print_success("inference.py is in root directory")
        
        # Read and check content
        with open(inference_path, 'r') as f:
            content = f.read()
        
        # Check for OpenAI client usage
        if "from openai import OpenAI" in content:
            print_success("Uses OpenAI client")
            self.passed.append("OpenAI client usage")
        else:
            print_error("Does not use OpenAI client")
            self.errors.append("Must use 'from openai import OpenAI'")
        
        # Check for environment variables
        required_vars = ["API_BASE_URL", "MODEL_NAME", "HF_TOKEN"]
        for var in required_vars:
            if f'os.getenv("{var}"' in content or f"os.getenv('{var}'" in content:
                print_success(f"Reads {var} environment variable")
            else:
                print_error(f"Does not read {var} environment variable")
                self.errors.append(f"Must read {var} from environment")
        
        # Check for output format
        if "[START]" in content and "[STEP]" in content and "[END]" in content:
            print_success("Contains required output format markers")
            self.passed.append("Output format markers present")
        else:
            print_error("Missing required output format markers")
            self.errors.append("Must emit [START], [STEP], and [END] lines")
    
    def check_environment_variables(self):
        """Check environment variable configuration"""
        inference_path = self.repo_dir / "inference.py"
        
        if not inference_path.exists():
            return
        
        with open(inference_path, 'r') as f:
            content = f.read()
        
        # Check API_BASE_URL has default
        if 'API_BASE_URL = os.getenv("API_BASE_URL"' in content:
            if ', "' in content.split('API_BASE_URL = os.getenv("API_BASE_URL"')[1].split('\n')[0]:
                print_success("API_BASE_URL has default value")
                self.passed.append("API_BASE_URL default")
            else:
                print_error("API_BASE_URL missing default value")
                self.errors.append("API_BASE_URL must have default value")
        
        # Check MODEL_NAME has default
        if 'MODEL_NAME = os.getenv("MODEL_NAME"' in content:
            if ', "' in content.split('MODEL_NAME = os.getenv("MODEL_NAME"')[1].split('\n')[0]:
                print_success("MODEL_NAME has default value")
                self.passed.append("MODEL_NAME default")
            else:
                print_error("MODEL_NAME missing default value")
                self.errors.append("MODEL_NAME must have default value")
        
        # Check HF_TOKEN is mandatory (no default)
        if 'HF_TOKEN = os.getenv("HF_TOKEN")' in content:
            # Check if there's a validation
            if "HF_TOKEN is None" in content or "not HF_TOKEN" in content:
                print_success("HF_TOKEN is mandatory (no default)")
                self.passed.append("HF_TOKEN mandatory")
            else:
                print_warning("HF_TOKEN should raise error if not provided")
                self.warnings.append("Add validation for HF_TOKEN")
    
    def check_openenv_compliance(self):
        """Check OpenEnv specification compliance"""
        env_path = self.repo_dir / "environment.py"
        models_path = self.repo_dir / "models.py"
        yaml_path = self.repo_dir / "openenv.yaml"
        
        # Check environment.py
        if env_path.exists():
            with open(env_path, 'r') as f:
                env_content = f.read()
            
            required_methods = ["reset", "step", "state", "close"]
            for method in required_methods:
                if f"def {method}(" in env_content:
                    print_success(f"Environment has {method}() method")
                else:
                    print_error(f"Environment missing {method}() method")
                    self.errors.append(f"Environment must implement {method}()")
        
        # Check models.py
        if models_path.exists():
            with open(models_path, 'r') as f:
                models_content = f.read()
            
            required_models = ["Action", "Observation", "Reward"]
            for model in required_models:
                if f"class {model}" in models_content:
                    print_success(f"Pydantic model {model} defined")
                else:
                    print_error(f"Missing Pydantic model: {model}")
                    self.errors.append(f"Must define {model} model")
        
        # Check openenv.yaml
        if yaml_path.exists():
            print_success("openenv.yaml exists")
            self.passed.append("openenv.yaml present")
        else:
            print_error("openenv.yaml is missing")
            self.errors.append("Must include openenv.yaml")
    
    def check_tasks_and_graders(self):
        """Verify 3+ tasks with graders"""
        env_path = self.repo_dir / "environment.py"
        
        if not env_path.exists():
            return
        
        with open(env_path, 'r') as f:
            content = f.read()
        
        # Look for task definitions
        task_count = 0
        tasks = ["bug_detection", "security_audit", "refactoring_analysis"]
        
        for task in tasks:
            if f'"{task}"' in content or f"'{task}'" in content:
                print_success(f"Task '{task}' found")
                task_count += 1
        
        if task_count >= 3:
            print_success(f"Found {task_count} tasks (requirement: 3+)")
            self.passed.append(f"{task_count} tasks")
        else:
            print_error(f"Only found {task_count} tasks (requirement: 3+)")
            self.errors.append("Must have at least 3 tasks")
        
        # Check graders
        graders_dir = self.repo_dir / "graders"
        if graders_dir.exists():
            grader_count = len(list(graders_dir.glob("*_grader.py")))
            if grader_count >= 3:
                print_success(f"Found {grader_count} graders")
                self.passed.append(f"{grader_count} graders")
            else:
                print_error(f"Only found {grader_count} graders (requirement: 3+)")
                self.errors.append("Must have at least 3 graders")
    
    def check_output_format(self):
        """Validate output format compliance"""
        inference_path = self.repo_dir / "inference.py"
        
        if not inference_path.exists():
            return
        
        with open(inference_path, 'r') as f:
            content = f.read()
        
        # Check for proper format strings
        checks = [
            ("[START] task=", "START line format"),
            ("[STEP] step=", "STEP line format"),
            ("[END] success=", "END line format"),
            ("reward={", "Reward formatting"),
            ("done=", "Done flag"),
            ("error=", "Error field"),
        ]
        
        for pattern, description in checks:
            if pattern in content:
                print_success(f"{description} present")
            else:
                print_warning(f"{description} may be missing")
                self.warnings.append(f"Verify {description}")
        
        # Check for 2 decimal place formatting
        if ":.2f" in content:
            print_success("Reward formatted to 2 decimal places")
            self.passed.append("Reward formatting")
        else:
            print_warning("Verify rewards are formatted to 2 decimal places")
    
    def check_docker(self):
        """Check Docker configuration"""
        dockerfile_path = self.repo_dir / "Dockerfile"
        
        if not dockerfile_path.exists():
            print_error("Dockerfile is missing")
            self.errors.append("Must include Dockerfile")
            return
        
        print_success("Dockerfile exists")
        
        with open(dockerfile_path, 'r') as f:
            content = f.read()
        
        # Check for Python base image
        if "FROM python:" in content:
            print_success("Uses Python base image")
        else:
            print_warning("Verify Python base image is used")
        
        # Check for requirements installation
        if "requirements.txt" in content:
            print_success("Installs requirements.txt")
        else:
            print_warning("Verify requirements.txt is installed")
        
        # Check for port exposure
        if "EXPOSE" in content:
            print_success("Exposes port for Gradio")
        else:
            print_warning("Consider exposing port 7860 for Gradio")
    
    def check_documentation(self):
        """Check documentation completeness"""
        readme_path = self.repo_dir / "README.md"
        
        if not readme_path.exists():
            print_error("README.md is missing")
            self.errors.append("Must include README.md")
            return
        
        print_success("README.md exists")
        
        try:
            with open(readme_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            with open(readme_path, 'r', encoding='latin-1') as f:
                content = f.read()
        
        required_sections = [
            ("Overview", "environment overview"),
            ("Task", "task descriptions"),
            ("Action", "action space"),
            ("Observation", "observation space"),
            ("Setup", "setup instructions"),
            ("Usage", "usage instructions"),
        ]
        
        for keyword, description in required_sections:
            if keyword.lower() in content.lower():
                print_success(f"Contains {description}")
            else:
                print_warning(f"May be missing {description}")
                self.warnings.append(f"Add {description} to README")
    
    def print_summary(self):
        """Print validation summary"""
        print_header("Validation Summary")
        
        print(f"\n{Colors.BOLD}Passed Checks:{Colors.NC} {len(self.passed)}")
        for item in self.passed[:5]:  # Show first 5
            print_info(f"✓ {item}")
        if len(self.passed) > 5:
            print_info(f"  ... and {len(self.passed) - 5} more")
        
        if self.warnings:
            print(f"\n{Colors.YELLOW}{Colors.BOLD}Warnings:{Colors.NC} {len(self.warnings)}")
            for warning in self.warnings:
                print_warning(warning)
        
        if self.errors:
            print(f"\n{Colors.RED}{Colors.BOLD}Errors:{Colors.NC} {len(self.errors)}")
            for error in self.errors:
                print_error(error)
            print(f"\n{Colors.RED}{Colors.BOLD}❌ VALIDATION FAILED{Colors.NC}")
            print_info("Fix the errors above before submitting")
        else:
            print(f"\n{Colors.GREEN}{Colors.BOLD}✅ VALIDATION PASSED{Colors.NC}")
            print_info("Your submission is ready!")
            if self.warnings:
                print_info("Consider addressing warnings for best results")


def main():
    """Main entry point"""
    repo_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    
    validator = SubmissionValidator(repo_dir)
    success = validator.validate_all()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
