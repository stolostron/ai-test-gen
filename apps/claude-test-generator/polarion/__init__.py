#!/usr/bin/env python3
"""
AI-Powered Polarion Integration for Claude Test Generator
Complete replacement of manual scripts with intelligent AI services
"""

# Import the main AI service
from .ai_polarion_service import (
    AIPolarionService,
    get_ai_polarion_service,
    post_test_cases_if_enabled,
    get_polarion_status_for_framework,
    integrate_polarion_with_framework,
    ai_setup_credentials,
    ai_credential_status,
    ai_test_connection,
    ai_post_test_cases
)

# All integration functionality now handled by AI service

__version__ = "2.0.0"
__all__ = [
    # Main AI Service
    "AIPolarionService",
    "get_ai_polarion_service",
    
    # Framework Integration Functions
    "post_test_cases_if_enabled",
    "get_polarion_status_for_framework", 
    "integrate_polarion_with_framework",
    
    # AI CLI Functions
    "ai_setup_credentials",
    "ai_credential_status",
    "ai_test_connection",
    "ai_post_test_cases"
]
