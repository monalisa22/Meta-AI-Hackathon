"""
Test script to verify the Code Review Environment works correctly
"""

import sys
from environment import CodeReviewEnv
from models import Action


def test_bug_detection():
    """Test bug detection task"""
    print("Testing Bug Detection Task...")
    env = CodeReviewEnv(task_id="bug_detection")
    
    # Reset environment
    obs = env.reset()
    assert obs.task_id == "bug_detection"
    assert len(obs.files) > 0
    print(f"✓ Environment reset successful")
    print(f"  - Files: {list(obs.files.keys())}")
    print(f"  - Max steps: {obs.max_steps}")
    
    # Test action
    action = Action(
        action_type="identify_bug",
        file_path="task1_sample.py",
        line_number=10,
        description="Division by zero when list is empty",
        severity="high"
    )
    
    obs, reward, done, info = env.step(action)
    print(f"✓ Step executed successfully")
    print(f"  - Reward: {reward}")
    print(f"  - Done: {done}")
    print(f"  - Step count: {obs.step_count}")
    
    # Submit review
    submit_action = Action(
        action_type="submit_review",
        file_path="task1_sample.py",
        description="Review complete",
        severity="info"
    )
    
    obs, reward, done, info = env.step(submit_action)
    print(f"✓ Review submitted")
    print(f"  - Final reward: {reward:.2f}")
    print(f"  - Done: {done}")
    
    score = env.get_final_score()
    print(f"✓ Final score: {score:.2f}")
    
    env.close()
    print("✓ Bug Detection Task: PASSED\n")


def test_security_audit():
    """Test security audit task"""
    print("Testing Security Audit Task...")
    env = CodeReviewEnv(task_id="security_audit")
    
    obs = env.reset()
    assert obs.task_id == "security_audit"
    print(f"✓ Environment reset successful")
    print(f"  - Files: {list(obs.files.keys())}")
    
    # Test security finding
    action = Action(
        action_type="flag_security_issue",
        file_path="api.py",
        line_number=12,
        description="Hardcoded credentials detected",
        severity="critical"
    )
    
    obs, reward, done, info = env.step(action)
    print(f"✓ Security issue flagged")
    print(f"  - Reward: {reward}")
    
    env.close()
    print("✓ Security Audit Task: PASSED\n")


def test_refactoring_analysis():
    """Test refactoring analysis task"""
    print("Testing Refactoring Analysis Task...")
    env = CodeReviewEnv(task_id="refactoring_analysis")
    
    obs = env.reset()
    assert obs.task_id == "refactoring_analysis"
    print(f"✓ Environment reset successful")
    print(f"  - Files: {list(obs.files.keys())}")
    
    # Test refactoring suggestion
    action = Action(
        action_type="suggest_refactor",
        file_path="user_service.py",
        line_number=12,
        description="Extract validation logic to separate validator classes",
        severity="medium"
    )
    
    obs, reward, done, info = env.step(action)
    print(f"✓ Refactoring suggested")
    print(f"  - Reward: {reward}")
    
    env.close()
    print("✓ Refactoring Analysis Task: PASSED\n")


def test_state_method():
    """Test state method"""
    print("Testing state() method...")
    env = CodeReviewEnv(task_id="bug_detection")
    env.reset()
    
    state = env.state()
    assert "task_id" in state
    assert "current_step" in state
    assert "done" in state
    print(f"✓ state() method works")
    print(f"  - State: {state}")
    
    env.close()
    print("✓ State Method: PASSED\n")


def main():
    """Run all tests"""
    print("="*60)
    print("Code Review Environment Test Suite")
    print("="*60 + "\n")
    
    try:
        test_bug_detection()
        test_security_audit()
        test_refactoring_analysis()
        test_state_method()
        
        print("="*60)
        print("✅ ALL TESTS PASSED!")
        print("="*60)
        return 0
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
