"""Security utilities"""

import hashlib
from datetime import datetime, timedelta
import streamlit as st
from src.utils.logger import logger
from config.settings import Config

class SecurityManager:
    """Handle security-related operations"""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        """Verify password against hash"""
        return SecurityManager.hash_password(password) == hashed
    
    @staticmethod
    def sanitize_input(user_input: str) -> str:
        """Sanitize user input to prevent XSS"""
        dangerous_chars = ['<', '>', '"', "'", '&', ';']
        sanitized = user_input
        for char in dangerous_chars:
            sanitized = sanitized.replace(char, '')
        return sanitized.strip()
    
    @staticmethod
    def hash_sensitive_data(data: str) -> str:
        """Hash sensitive data"""
        return hashlib.sha256(data.encode()).hexdigest()
    
    @staticmethod
    def validate_session(username: str) -> bool:
        """Validate user session"""
        if 'login_time' not in st.session_state:
            return False
        
        elapsed = datetime.now() - st.session_state.login_time
        timeout = timedelta(minutes=Config.security.SESSION_TIMEOUT_MINUTES)
        
        if elapsed > timeout:
            logger.warning(f"Session timeout for user: {username}")
            return False
        
        return True
    
    @staticmethod
    def validate_password_strength(password: str) -> tuple[bool, str]:
        """Validate password strength"""
        if len(password) < Config.security.PASSWORD_MIN_LENGTH:
            return False, f"Password must be at least {Config.security.PASSWORD_MIN_LENGTH} characters"
        
        if Config.security.PASSWORD_REQUIRE_NUMBERS and not any(c.isdigit() for c in password):
            return False, "Password must contain at least one number"
        
        if Config.security.PASSWORD_REQUIRE_SPECIAL_CHARS and not any(c in "!@#$%^&*" for c in password):
            return False, "Password must contain at least one special character"
        
        return True, "Password is strong"

class AuthenticationManager:
    """Handle user authentication"""
    
    # In production, this should be loaded from a secure database
    VALID_USERS = {
        "admin": SecurityManager.hash_password("admin123"),
        "user": SecurityManager.hash_password("user123")
    }
    
    @staticmethod
    def authenticate(username: str, password: str) -> bool:
        """Authenticate user credentials"""
        if username not in AuthenticationManager.VALID_USERS:
            logger.warning(f"Login attempt with invalid username: {username}")
            return False
        
        if not SecurityManager.verify_password(password, AuthenticationManager.VALID_USERS[username]):
            logger.warning(f"Login attempt with invalid password for user: {username}")
            return False
        
        logger.info(f"User authenticated: {username}")
        return True
    
    @staticmethod
    def initialize_session(username: str):
        """Initialize user session"""
        st.session_state.authenticated = True
        st.session_state.username = username
        st.session_state.login_time = datetime.now()
        logger.info(f"Session initialized for user: {username}")
    
    @staticmethod
    def logout():
        """Logout user"""
        username = st.session_state.get('username', 'Unknown')
        st.session_state.authenticated = False
        st.session_state.username = None
        st.session_state.login_time = None
        logger.info(f"User logged out: {username}")
