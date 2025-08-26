#!/usr/bin/env python3
"""
Pre-Generation Format Hook
Validates format requirements before test generation
"""

from .pattern_extension_format_enforcer import PatternExtensionFormatEnforcer

def pre_generation_format_check():
    """Check format requirements before generation"""
    enforcer = PatternExtensionFormatEnforcer()
    format_prompt = enforcer.generate_format_enforcement_prompt()
    
    return {
        'format_requirements': format_prompt,
        'enforcement_active': True,
        'target_score': 85
    }

def get_format_enforcement_prompt():
    """Get format enforcement prompt for agents"""
    return """
MANDATORY FORMAT REQUIREMENTS (TARGET: 85+ POINTS):

1. **EXACT Login Format Required:**
   **Step 1: Log into the ACM hub cluster** - Access the hub cluster using credentials: `oc login <CLUSTER_CONSOLE_URL>`

2. **Single-Line Table Format Only:**
   | Step | Expected Result |
   |------|-----------------|
   | **Step description** - Command: `oc command` | Expected output: `sample output` |

3. **Mandatory Elements:**
   - NO HTML tags (<br/>, <b>, <i>) - use markdown
   - Sample outputs in backticks for every step
   - NO internal script references (setup_clc, login_oc)
   - **Description:** and **Setup:** sections required
   - Minimum 3 test cases

4. **Validation:** Automatic format validation applied (target compliances required)
"""
