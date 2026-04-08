"""
Grader for Task 1: Bug Detection
Evaluates bug identification accuracy with precision and recall
"""

from typing import List, Dict, Tuple


class BugGrader:
    """Grader for bug detection task"""
    
    def __init__(self):
        # Ground truth bugs in task1_sample.py
        self.ground_truth_bugs = [
            {
                "line": 10,
                "type": "division_by_zero",
                "description": "Division by zero when list is empty",
                "severity": "high"
            },
            {
                "line": 20,
                "type": "null_pointer",
                "description": "Potential None access without check",
                "severity": "high"
            },
            {
                "line": 27,
                "type": "off_by_one",
                "description": "Off-by-one error - misses last item",
                "severity": "medium"
            },
            {
                "line": 34,
                "type": "resource_leak",
                "description": "File not closed - resource leak",
                "severity": "medium"
            },
            {
                "line": 42,
                "type": "type_error",
                "description": "Type mismatch - string concatenation with number",
                "severity": "high"
            },
            {
                "line": 56,
                "type": "key_error",
                "description": "Unhandled KeyError if 'price' key missing",
                "severity": "medium"
            },
            {
                "line": 63,
                "type": "side_effect",
                "description": "Modifies original dict1 instead of creating new",
                "severity": "low"
            }
        ]
    
    def grade(self, findings: List[Dict]) -> Tuple[float, Dict]:
        """
        Grade the bug detection findings
        
        Args:
            findings: List of bug findings from the agent
            
        Returns:
            Tuple of (score, breakdown) where score is 0.0-1.0
        """
        true_positives = 0
        false_positives = 0
        false_negatives = 0
        
        # Track which ground truth bugs were found
        found_bugs = set()
        
        # Evaluate each finding
        for finding in findings:
            if finding.get('action_type') != 'identify_bug':
                continue
                
            line_num = finding.get('line_number')
            matched = False
            
            # Check if this finding matches a ground truth bug
            for i, bug in enumerate(self.ground_truth_bugs):
                if i in found_bugs:
                    continue
                    
                # Allow +/- 2 lines tolerance
                if abs(bug['line'] - line_num) <= 2:
                    true_positives += 1
                    found_bugs.add(i)
                    matched = True
                    break
            
            if not matched:
                false_positives += 1
        
        # Calculate false negatives
        false_negatives = len(self.ground_truth_bugs) - true_positives
        
        # Calculate metrics
        precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
        recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
        f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        
        # Bonus for perfect recall
        bonus = 0.1 if recall == 1.0 else 0
        
        # Final score (F1 score + bonus, capped at 1.0)
        score = min(f1_score + bonus, 1.0)
        
        breakdown = {
            "true_positives": true_positives,
            "false_positives": false_positives,
            "false_negatives": false_negatives,
            "precision": round(precision, 2),
            "recall": round(recall, 2),
            "f1_score": round(f1_score, 2),
            "bonus": round(bonus, 2),
            "total_bugs": len(self.ground_truth_bugs)
        }
        
        return score, breakdown
    
    def get_feedback(self, breakdown: Dict) -> str:
        """Generate feedback message based on grading breakdown"""
        tp = breakdown['true_positives']
        fp = breakdown['false_positives']
        fn = breakdown['false_negatives']
        
        feedback = f"Found {tp}/{breakdown['total_bugs']} bugs correctly. "
        
        if fp > 0:
            feedback += f"{fp} false positives. "
        
        if fn > 0:
            feedback += f"Missed {fn} bugs. "
        
        if breakdown['recall'] == 1.0:
            feedback += "Perfect recall! "
        
        return feedback
