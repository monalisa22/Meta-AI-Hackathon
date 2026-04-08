"""
User service with code smells for Task 3: Refactoring Analysis
This file contains multiple refactoring opportunities
"""

class UserService:
    def __init__(self):
        self.users = []
    
    # CODE SMELL 1: Long method with multiple responsibilities
    def create_user(self, username, email, password, age, address, phone):
        """Create a new user with validation"""
        # Validate username
        if not username or len(username) < 3:
            return {"error": "Username too short"}
        if len(username) > 20:
            return {"error": "Username too long"}
        
        # Validate email
        if not email or '@' not in email:
            return {"error": "Invalid email"}
        if not '.' in email:
            return {"error": "Invalid email domain"}
        
        # Validate password
        if not password or len(password) < 8:
            return {"error": "Password too short"}
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        if not (has_upper and has_lower and has_digit):
            return {"error": "Password must contain upper, lower, and digit"}
        
        # Validate age
        if age < 18:
            return {"error": "User must be 18 or older"}
        if age > 120:
            return {"error": "Invalid age"}
        
        # Create user
        user = {
            'username': username,
            'email': email,
            'password': password,
            'age': age,
            'address': address,
            'phone': phone
        }
        self.users.append(user)
        return {"success": True, "user": user}
    
    # CODE SMELL 2: Duplicated code
    def get_active_users(self):
        """Get all active users"""
        active_users = []
        for user in self.users:
            if user.get('status') == 'active':
                active_users.append(user)
        return active_users
    
    def get_premium_users(self):
        """Get all premium users"""
        premium_users = []
        for user in self.users:
            if user.get('subscription') == 'premium':
                premium_users.append(user)
        return premium_users
    
    def get_verified_users(self):
        """Get all verified users"""
        verified_users = []
        for user in self.users:
            if user.get('verified') == True:
                verified_users.append(user)
        return verified_users
