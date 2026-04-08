"""
Grader for Task 3: Cross-File Refactoring Analysis
Evaluates refactoring suggestions based on actionability, correctness, and impact
"""

from typing import List, Dict, Tuple


class RefactoringGrader:
    """Grader for refactoring analysis task"""
    
    def __init__(self):
        # Ground truth refactoring opportunities
        self.ground_truth_refactorings = [
            {
                "file": "user_service.py",
                "type": "long_method",
                "description": "create_user method has too many responsibilities",
                "impact": "high",
                "weight": 0.25,
                "keywords": ["create_user", "validation", "extract", "separate"]
            },
            {
                "file": "user_service.py",
                "type": "code_duplication",
                "description": "Duplicated filtering logic in get_*_users methods",
                "impact": "medium",
                "weight": 0.20,
                "keywords": ["duplication", "filter", "get_active", "get_premium", "get_verified"]
            },
            {
                "file": "notification_service.py",
                "type": "god_class",
                "description": "NotificationService has too many responsibilities",
                "impact": "high",
                "weight": 0.25,
                "keywords": ["god class", "single responsibility", "separate", "email", "sms", "push"]
            },
            {
                "file": "user_service.py",
                "type": "validation_extraction",
                "description": "Validation logic should be extracted to separate validators",
                "impact": "medium",
                "weight": 0.15,
                "keywords": ["validation", "validator", "extract", "username", "email", "password"]
            },
            {
                "file": "notification_service.py",
                "type": "template_pattern",
                "description": "Template loading could use a template pattern",
                "impact": "low",
                "weight": 0.15,
                "keywords": ["template", "pattern", "load_email_template", "load_sms_template"]
            }
        ]
        
        self.total_weight = sum(r['weight'] for r in self.ground_truth_refactorings)
    
    def grade(self, findings: List[Dict]) -> Tuple[float, Dict]:
        """
        Grade the refactoring suggestions
        
        Args:
            findings: List of refactoring suggestions from the agent
            
        Returns:
            Tuple of (score, breakdown) where score is 0.0-1.0
        """
        weighted_score = 0.0
        found_refactorings = set()
        false_positives = 0
        suggestions_with_fixes = 0
        
        # Evaluate each finding
        for finding in findings:
            if finding.get('action_type') != 'suggest_refactor':
                continue
                
            description = finding.get('description', '').lower()
            file_path = finding.get('file_path', '')
            matched = False
            
            # Check if this finding matches a ground truth refactoring
            for i, refactor in enumerate(self.ground_truth_refactorings):
                if i in found_refactorings:
                    continue
                
                # Check if file matches
                if refactor['file'] not in file_path:
                    continue
                
                # Check if description contains relevant keywords
                keyword_matches = sum(1 for keyword in refactor['keywords'] 
                                     if keyword.lower() in description)
                
                if keyword_matches >= 2:  # At least 2 keywords must match
                    weighted_score += refactor['weight']
                    found_refactorings.add(i)
                    matched = True
                    
                    # Bonus for providing suggested fix
                    if finding.get('suggested_fix'):
                        weighted_score += 0.05
                        suggestions_with_fixes += 1
                    
                    break
            
            if not matched:
                false_positives += 1
                # Small penalty for irrelevant suggestions
                weighted_score -= 0.05
        
        # Normalize score
        score = max(0.0, min(1.0, weighted_score / self.total_weight))
        
        # Calculate impact distribution
        high_impact_found = sum(1 for i in found_refactorings 
                               if self.ground_truth_refactorings[i]['impact'] == 'high')
        high_impact_total = sum(1 for r in self.ground_truth_refactorings 
                               if r['impact'] == 'high')
        
        breakdown = {
            "found_refactorings": len(found_refactorings),
            "total_refactorings": len(self.ground_truth_refactorings),
            "false_positives": false_positives,
            "suggestions_with_fixes": suggestions_with_fixes,
            "weighted_score": round(weighted_score, 2),
            "max_weight": round(self.total_weight, 2),
            "high_impact_found": high_impact_found,
            "high_impact_total": high_impact_total
        }
        
        return score, breakdown
    
    def get_feedback(self, breakdown: Dict) -> str:
        """Generate feedback message based on grading breakdown"""
        found = breakdown['found_refactorings']
        total = breakdown['total_refactorings']
        fp = breakdown['false_positives']
        with_fixes = breakdown['suggestions_with_fixes']
        high_impact = breakdown['high_impact_found']
        
        feedback = f"Identified {found}/{total} refactoring opportunities. "
        feedback += f"High-impact suggestions: {high_impact}. "
        
        if with_fixes > 0:
            feedback += f"{with_fixes} suggestions included fixes. "
        
        if fp > 0:
            feedback += f"{fp} irrelevant suggestions. "
        
        if found == total:
            feedback += "Comprehensive analysis! "
        
        return feedback
