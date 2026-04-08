"""
Sample API code with security vulnerabilities for Task 2: Security Audit
This file contains 6 security issues that should be identified
"""

import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

# VULNERABILITY 1: Hardcoded credentials
DATABASE_PASSWORD = "admin123"
API_KEY = "sk-1234567890abcdef"


def get_db_connection():
    """Connect to database"""
    # VULNERABILITY 2: SQL Injection vulnerability
    conn = sqlite3.connect('users.db')
    return conn


@app.route('/login', methods=['POST'])
def login():
    """User login endpoint"""
    username = request.form.get('username')
    password = request.form.get('password')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # VULNERABILITY 3: SQL Injection - direct string interpolation
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    cursor.execute(query)
    user = cursor.fetchone()
    
    conn.close()
    
    if user:
        return jsonify({"status": "success", "user": user})
    return jsonify({"status": "failed"}), 401


@app.route('/search', methods=['GET'])
def search():
    """Search users endpoint"""
    query = request.args.get('q', '')
    
    # VULNERABILITY 4: XSS vulnerability - no output sanitization
    return f"<html><body><h1>Search results for: {query}</h1></body></html>"


@app.route('/user/<user_id>', methods=['GET'])
def get_user(user_id):
    """Get user by ID"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # VULNERABILITY 5: SQL Injection in parameterized route
    cursor.execute(f"SELECT * FROM users WHERE id={user_id}")
    user = cursor.fetchone()
    
    conn.close()
    
    if user:
        return jsonify({"user": user})
    return jsonify({"error": "User not found"}), 404


@app.route('/admin/delete', methods=['POST'])
def delete_user():
    """Delete user endpoint"""
    # VULNERABILITY 6: Missing authentication/authorization check
    user_id = request.form.get('user_id')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM users WHERE id={user_id}")
    conn.commit()
    conn.close()
    
    return jsonify({"status": "deleted"})


if __name__ == '__main__':
    # VULNERABILITY 7: Debug mode enabled in production
    app.run(debug=True, host='0.0.0.0')
