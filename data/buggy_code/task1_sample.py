"""
Sample Python code with intentional bugs for Task 1: Bug Detection
This file contains 8 common bugs that should be identified
"""

def calculate_average(numbers):
    """Calculate average of a list of numbers"""
    # BUG 1: Division by zero when list is empty
    total = sum(numbers)
    return total / len(numbers)


def find_user_by_id(user_id, users):
    """Find a user in the list by ID"""
    # BUG 2: Potential None access - no check if user is found
    user = None
    for u in users:
        if u['id'] == user_id:
            user = u
    return user['name']  # Will crash if user is None


def process_items(items):
    """Process a list of items"""
    result = []
    # BUG 3: Off-by-one error - will miss last item
    for i in range(len(items) - 1):
        result.append(items[i] * 2)
    return result


def read_config_file(filename):
    """Read configuration from file"""
    # BUG 4: File not closed - resource leak
    file = open(filename, 'r')
    config = file.read()
    return config


def get_discount_price(price, discount_percent):
    """Calculate discounted price"""
    # BUG 5: Type mismatch - string concatenation with number
    discount = price * discount_percent / 100
    return "Price: " + (price - discount)


class ShoppingCart:
    def __init__(self):
        self.items = []
    
    def add_item(self, item):
        """Add item to cart"""
        self.items.append(item)
    
    def get_total(self):
        """Calculate total price"""
        total = 0
        # BUG 6: Unhandled exception if item doesn't have 'price' key
        for item in self.items:
            total += item['price']
        return total


def merge_dictionaries(dict1, dict2):
    """Merge two dictionaries"""
    # BUG 7: Modifies original dict1 instead of creating new dict
    dict1.update(dict2)
    return dict1


def validate_email(email):
    """Validate email format"""
    # BUG 8: Incorrect comparison - should use '==' not '='
    if email.count('@') == 1 and '.' in email:
        return True
    return False


# Additional helper function with no bugs (for testing false positives)
def safe_divide(a, b):
    """Safely divide two numbers"""
    if b == 0:
        return 0
    return a / b
