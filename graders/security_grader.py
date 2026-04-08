"""
Grader for Task 2: Security Vulnerability Assessment
Evaluates security issue detection with severity weighting
"""

from typing import List, Dict, Tuple


class SecurityGrader:
    """Grader for security vulnerability assessment task"""
    
    def __init__(self):
        # Ground truth vulnerabilities in api.py
        self.ground_truth_vulnerabilities = [
            {
                "line": 12,
                "type": "hardcoded_credentials",
                "description": "Hardcoded database password",
                "severity": "critical",
                "weight": 1.0
            },
            {
                "line": 13,
                "type": "hardcoded_credentials",
                "description": "Hardcoded API key",
                "severity": "critical",
                "weight": 1.0
            },
            {
                "line": 33,
                "type": "sql_injection",
                "description": "SQL injection via string interpolation",
                "severity": "critical",
                "weight": 1.0
            },
            {
                "line": 48,
                "type": "xss",
                "description": "XSS vulnerability - no output sanitization",
                "severity": "high",
                "weight": 0.7
            },
            {
                "line": 58,
                "type": "sql_injection",
                "description": "SQL injection in user_id parameter",
                "severity": "critical",
                "weight": 1.0
            },
            {
                "line": 69,
                "type": "missing_auth",
                "description": "Missing authentication/authorization check",
                "severity": "critical",
                "weight": 1.0
            },
            {
                "line": 82,
                "type": "debug_mode",
                "description": "Debug mode enabled in production",
                "severity": "medium",
                "weight": 0.4
            }
        ]
        
        self.total_weight = sum(v['weight'] for v in self.ground_truth_vulnerabilities)
    
    def grade(self, findings: List[Dict]) -> Tuple[float, Dict]:
        """
        Grade the security vulnerability findings
        
        Args:
            findings: List of security findings from the agent
            
        Returns:
            Tuple of (score, breakdown) where score is 0.0-1.0
        """
        weighted_score = 0.0
        found_vulnerabilities = set()
        false_positives = 0
        
        # Evaluate each finding
        for finding in findings:
            if finding.get('action_type') != 'flag_security_issue':
                continue
                
            line_num = finding.get('line_number')
            matched = False
            
            # Check if this finding matches a ground truth vulnerability
            for i, vuln in enumerate(self.ground_truth_vulnerabilities):
                if i in found_vulnerabilities:
                    continue
                    
                # Allow +/- 3 lines tolerance for security issues
                if abs(vuln['line'] - line_num) <= 3:
                    weighted_score += vuln['weight']
                    found_vulnerabilities.add(i)
                    matched = True
                    
                    # Bonus for suggesting a fix
                    if finding.get('suggested_fix'):
                        weighted_score += 0.1
                    
                    break
            
            if not matched:
                false_positives += 1
                # Penalty for false positives
                weighted_score -= 0.1
        
        # Normalize score
        score = max(0.0, min(1.0, weighted_score / self.total_weight))
        
        breakdown = {
            "found_vulnerabilities": len(found_vulnerabilities),
            "total_vulnerabilities": len(self.ground_truth_vulnerabilities),
            "false_positives": false_positives,
            "weighted_score": round(weighted_score, 2),
            "max_weight": round(self.total_weight, 2),
            "critical_found": sum(1 for i in found_vulnerabilities 
                                 if self.ground_truth_vulnerabilities[i]['severity'] == 'critical'),
            "critical_total": sum(1 for v in self.ground_truth_vulnerabilities 
                                 if v['severity'] == 'critical')
        }
        
        return score, breakdown
    
    def get_feedback(self, breakdown: Dict) -> str:
        """Generate feedback message based on grading breakdown"""
        found = breakdown['found_vulnerabilities']
        total = breakdown['total_vulnerabilities']
        fp = breakdown['false_positives']
        critical_found = breakdown['critical_found']
        critical_total = breakdown['critical_total']
        
        feedback = f"Found {found}/{total} vulnerabilities. "
        feedback += f"Critical issues: {critical_found}/{critical_total}. "
        
        if fp > 0:
            feedback += f"{fp} false positives. "
        
        if critical_found == critical_total:
            feedback += "All critical vulnerabilities identified! "
        
        return feedback
