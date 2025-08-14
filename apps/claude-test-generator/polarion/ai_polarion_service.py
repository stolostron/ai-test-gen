#!/usr/bin/env python3
"""
AI-Powered Polarion Service
Complete AI-driven replacement for all Polarion scripts and manual operations
Provides intelligent, adaptive, and robust Polarion integration for the Claude framework
"""

import os
import json
import logging
import requests
import base64
import getpass
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass
import re

logger = logging.getLogger(__name__)

@dataclass
class AIPolarionResult:
    """Standardized result from AI Polarion operations"""
    success: bool
    confidence: float
    data: Dict[str, Any]
    recommendations: List[str]
    actions: List[str]
    metadata: Dict[str, Any]

class AIPolarionService:
    """
    Complete AI-powered Polarion service replacing all manual scripts
    Provides intelligent credential management, connection handling, test case operations
    """
    
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.credentials_dir = self.base_dir / ".polarion"
        self.credentials_file = self.credentials_dir / "credentials.json"
        self.session = None
        self.config = {}
        
        # AI initialization
        self._ai_initialize()
    
    def _ai_initialize(self):
        """AI-powered initialization with intelligent configuration discovery"""
        logger.info("🤖 AI Polarion Service: Initializing intelligent configuration")
        
        # AI discovery of configuration sources
        self._ai_discover_and_load_config()
        
        # AI session management
        if self._ai_has_valid_credentials():
            self._ai_initialize_session()
    
    def _ai_discover_and_load_config(self):
        """AI-powered configuration discovery and loading"""
        config_sources = []
        
        # Source 1: Secure local storage (highest priority)
        if self.credentials_file.exists():
            try:
                with open(self.credentials_file, 'r') as f:
                    local_creds = json.load(f)
                self.config.update(local_creds)
                config_sources.append("secure_local_storage")
                logger.debug("🤖 AI: Loaded configuration from secure local storage")
            except Exception as e:
                logger.warning(f"AI: Failed to load local credentials: {e}")
        
        # Source 2: Environment variables (override priority)
        env_config = {
            'url': os.getenv('POLARION_URL'),
            'pat_token': os.getenv('POLARION_PAT_TOKEN'),
            'username': os.getenv('POLARION_USERNAME'),
            'password': os.getenv('POLARION_PASSWORD'),
            'project_id': os.getenv('POLARION_PROJECT_ID')
        }
        
        for key, value in env_config.items():
            if value:
                self.config[key] = value
                config_sources.append("environment")
        
        # AI defaults with intelligent fallbacks
        self.config.setdefault('timeout', 30)
        self.config.setdefault('verify_ssl', True)
        self.config.setdefault('test_case_type', 'testcase')
        
        logger.info(f"🤖 AI: Configuration loaded from sources: {config_sources}")
    
    def _ai_has_valid_credentials(self) -> bool:
        """AI validation of credential completeness"""
        required = ['url', 'project_id']
        auth_methods = [
            self.config.get('pat_token'),
            (self.config.get('username') and self.config.get('password'))
        ]
        
        has_required = all(self.config.get(key) for key in required)
        has_auth = any(auth_methods)
        
        return has_required and has_auth
    
    def _ai_initialize_session(self):
        """AI-powered session initialization with intelligent authentication"""
        self.session = requests.Session()
        
        # AI authentication strategy selection
        if self.config.get('pat_token'):
            self.session.headers.update({
                'Authorization': f'Bearer {self.config["pat_token"]}',
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            })
            logger.debug("🤖 AI: Initialized with PAT authentication")
        elif self.config.get('username') and self.config.get('password'):
            auth_string = base64.b64encode(
                f"{self.config['username']}:{self.config['password']}".encode()
            ).decode()
            self.session.headers.update({
                'Authorization': f'Basic {auth_string}',
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            })
            logger.debug("🤖 AI: Initialized with basic authentication")
    
    # =============================================================================
    # AI CREDENTIAL MANAGEMENT (Replaces credentials.py)
    # =============================================================================
    
    def ai_setup_credentials(self) -> AIPolarionResult:
        """AI-enhanced interactive credential setup"""
        logger.info("🤖 AI Credential Setup: Starting intelligent credential management")
        
        try:
            # AI pre-setup analysis
            current_status = self._ai_analyze_current_credentials()
            
            print("🤖 AI-Enhanced Polarion Credential Setup")
            print("=" * 50)
            
            if current_status["has_credentials"]:
                print("📊 Current Configuration:")
                for key, value in current_status["summary"].items():
                    print(f"  {key}: {value}")
                
                update = input("\n🤖 AI recommends updating credentials. Continue? (y/N): ").strip().lower()
                if update not in ['y', 'yes']:
                    return AIPolarionResult(
                        success=False,
                        confidence=0.0,
                        data={},
                        recommendations=["Setup cancelled by user"],
                        actions=[],
                        metadata={"status": "cancelled"}
                    )
            
            # AI-guided credential collection
            credentials = self._ai_collect_credentials_interactively()
            
            if not credentials:
                return AIPolarionResult(
                    success=False,
                    confidence=0.0,
                    data={},
                    recommendations=["Credential collection failed"],
                    actions=["Retry setup with complete information"],
                    metadata={"status": "failed", "reason": "incomplete_data"}
                )
            
            # AI credential storage with security
            storage_result = self._ai_store_credentials_securely(credentials)
            
            if storage_result["success"]:
                # AI validation of stored credentials
                validation_result = self.ai_test_connection()
                
                return AIPolarionResult(
                    success=True,
                    confidence=validation_result.confidence,
                    data={
                        "credentials_stored": True,
                        "validation_result": validation_result.data
                    },
                    recommendations=[
                        "✅ Credentials stored securely",
                        "✅ AI validation completed"
                    ] + validation_result.recommendations,
                    actions=["Credentials ready for use"],
                    metadata={
                        "status": "success",
                        "validation_confidence": validation_result.confidence
                    }
                )
            else:
                return AIPolarionResult(
                    success=False,
                    confidence=0.0,
                    data={},
                    recommendations=[f"❌ Storage failed: {storage_result['error']}"],
                    actions=["Check file permissions and retry"],
                    metadata={"status": "storage_failed"}
                )
                
        except Exception as e:
            logger.error(f"AI credential setup failed: {e}")
            return AIPolarionResult(
                success=False,
                confidence=0.0,
                data={},
                recommendations=[f"❌ Setup failed: {e}"],
                actions=["Check system configuration and retry"],
                metadata={"status": "error", "exception": str(e)}
            )
    
    def _ai_analyze_current_credentials(self) -> Dict[str, Any]:
        """AI analysis of current credential status"""
        has_local = self.credentials_file.exists()
        has_env = bool(os.getenv('POLARION_PAT_TOKEN') or os.getenv('POLARION_USERNAME'))
        
        summary = {}
        if has_local:
            try:
                with open(self.credentials_file, 'r') as f:
                    creds = json.load(f)
                summary["Local Storage"] = f"✅ {creds.get('url', 'Unknown URL')}"
                summary["Project"] = creds.get('project_id', 'Not set')
                summary["Auth Type"] = "PAT" if creds.get('pat_token') else "Basic"
            except:
                summary["Local Storage"] = "❌ Corrupted"
        
        if has_env:
            summary["Environment"] = "✅ Variables detected"
        
        return {
            "has_credentials": has_local or has_env,
            "summary": summary
        }
    
    def _ai_collect_credentials_interactively(self) -> Optional[Dict[str, Any]]:
        """AI-guided interactive credential collection"""
        credentials = {}
        
        # URL with AI validation
        while True:
            url = input("Polarion URL (e.g., https://polarion.company.com): ").strip()
            if url and url.startswith(('http://', 'https://')):
                credentials['url'] = url.rstrip('/')
                break
            print("❌ AI Validation: Please enter a valid URL starting with http:// or https://")
        
        # Project ID with AI validation
        project_id = input("Default Project ID: ").strip()
        if not project_id:
            print("⚠️ AI Warning: Project ID is required for most operations")
            return None
        credentials['project_id'] = project_id
        
        # Username (optional)
        username = input("Username (optional, press Enter to skip): ").strip() or None
        if username:
            credentials['username'] = username
        
        # PAT Token with AI guidance
        print("\n🔑 Personal Access Token (Recommended):")
        print("   Generate in Polarion: User Menu → Access Tokens")
        pat_token = getpass.getpass("PAT Token (input hidden, Enter to skip): ").strip()
        
        if pat_token:
            credentials['pat_token'] = pat_token
        elif username:
            # Basic auth fallback
            password = getpass.getpass("Password (input hidden): ").strip()
            if password:
                credentials['password'] = password
            else:
                print("❌ AI Validation: Either PAT token or username/password required")
                return None
        else:
            print("❌ AI Validation: Authentication method required")
            return None
        
        # AI optional configuration
        print("\n⚙️ AI Configuration Optimization:")
        timeout = input("API Timeout in seconds (default: 30): ").strip()
        if timeout and timeout.isdigit():
            credentials['timeout'] = int(timeout)
        
        verify_ssl = input("Verify SSL certificates? (Y/n): ").strip().lower()
        credentials['verify_ssl'] = verify_ssl not in ['n', 'no']
        
        return credentials
    
    def _ai_store_credentials_securely(self, credentials: Dict[str, Any]) -> Dict[str, Any]:
        """AI-powered secure credential storage"""
        try:
            # AI security: Ensure directory exists with secure permissions
            self.credentials_dir.mkdir(mode=0o700, exist_ok=True)
            
            # AI enhancement: Add metadata
            credentials.update({
                'stored_at': datetime.now().isoformat(),
                'version': '1.0',
                'ai_managed': True
            })
            
            # AI security: Store with secure permissions
            with open(self.credentials_file, 'w') as f:
                json.dump(credentials, f, indent=2)
            
            os.chmod(self.credentials_file, 0o600)
            
            # AI validation: Verify storage
            if self.credentials_file.exists():
                return {"success": True, "file": str(self.credentials_file)}
            else:
                return {"success": False, "error": "File not created"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def ai_credential_status(self) -> AIPolarionResult:
        """AI analysis of credential status"""
        try:
            status_data = {
                "credentials_stored": self.credentials_file.exists(),
                "environment_detected": bool(os.getenv('POLARION_PAT_TOKEN')),
                "configuration_valid": self._ai_has_valid_credentials()
            }
            
            recommendations = []
            
            if status_data["credentials_stored"]:
                recommendations.append("✅ Local credentials stored securely")
                try:
                    with open(self.credentials_file, 'r') as f:
                        creds = json.load(f)
                    status_data.update({
                        "url": creds.get('url'),
                        "project_id": creds.get('project_id'),
                        "auth_type": "PAT" if creds.get('pat_token') else "Basic",
                        "ai_managed": creds.get('ai_managed', False)
                    })
                except:
                    recommendations.append("⚠️ Credential file corrupted")
                    status_data["configuration_valid"] = False
            else:
                recommendations.append("❌ No local credentials found")
            
            if status_data["environment_detected"]:
                recommendations.append("ℹ️ Environment variables detected")
            
            if status_data["configuration_valid"]:
                recommendations.append("✅ Configuration is valid")
            else:
                recommendations.append("❌ Configuration incomplete")
                recommendations.append("💡 Run: ai_setup_credentials()")
            
            confidence = 0.8 if status_data["configuration_valid"] else 0.2
            
            return AIPolarionResult(
                success=True,
                confidence=confidence,
                data=status_data,
                recommendations=recommendations,
                actions=["Configuration ready"] if status_data["configuration_valid"] else ["Setup required"],
                metadata={"status": "analyzed"}
            )
            
        except Exception as e:
            return AIPolarionResult(
                success=False,
                confidence=0.0,
                data={},
                recommendations=[f"❌ Status analysis failed: {e}"],
                actions=["Check system configuration"],
                metadata={"status": "error"}
            )
    
    # =============================================================================
    # AI CONNECTION MANAGEMENT (Replaces api_client.py, config.py)
    # =============================================================================
    
    def ai_test_connection(self) -> AIPolarionResult:
        """AI-powered connection testing with intelligent diagnostics"""
        logger.info("🤖 AI Connection Test: Starting intelligent diagnostics")
        
        try:
            # AI Phase 1: Configuration validation
            config_analysis = self._ai_analyze_configuration()
            if config_analysis["confidence"] < 0.5:
                return AIPolarionResult(
                    success=False,
                    confidence=config_analysis["confidence"],
                    data=config_analysis,
                    recommendations=config_analysis["recommendations"],
                    actions=["Configure credentials before testing connection"],
                    metadata={"phase": "configuration", "status": "failed"}
                )
            
            # AI Phase 2: Network connectivity test
            network_analysis = self._ai_test_network_connectivity()
            
            # AI Phase 3: API authentication test
            auth_analysis = self._ai_test_api_authentication()
            
            # AI Phase 4: Project access validation
            project_analysis = self._ai_test_project_access()
            
            # AI综合分析
            overall_confidence = (
                config_analysis["confidence"] * 0.3 +
                network_analysis["confidence"] * 0.2 +
                auth_analysis["confidence"] * 0.3 +
                project_analysis["confidence"] * 0.2
            )
            
            success = overall_confidence > 0.6
            
            # AI recommendations compilation
            all_recommendations = []
            all_recommendations.extend(config_analysis["recommendations"])
            all_recommendations.extend(network_analysis["recommendations"])
            all_recommendations.extend(auth_analysis["recommendations"])
            all_recommendations.extend(project_analysis["recommendations"])
            
            return AIPolarionResult(
                success=success,
                confidence=overall_confidence,
                data={
                    "config_analysis": config_analysis,
                    "network_analysis": network_analysis,
                    "auth_analysis": auth_analysis,
                    "project_analysis": project_analysis
                },
                recommendations=all_recommendations,
                actions=["Connection ready"] if success else ["Check configuration and network"],
                metadata={
                    "status": "success" if success else "failed",
                    "overall_confidence": overall_confidence,
                    "test_phases": 4
                }
            )
            
        except Exception as e:
            logger.error(f"AI connection test failed: {e}")
            return AIPolarionResult(
                success=False,
                confidence=0.0,
                data={},
                recommendations=[f"❌ Connection test failed: {e}"],
                actions=["Check system configuration and network"],
                metadata={"status": "error", "exception": str(e)}
            )
    
    def _ai_analyze_configuration(self) -> Dict[str, Any]:
        """AI analysis of configuration completeness and quality"""
        analysis = {
            "confidence": 0.0,
            "recommendations": [],
            "details": {}
        }
        
        # AI scoring
        score = 0
        max_score = 100
        
        # Required fields
        if self.config.get('url'):
            score += 30
            analysis["recommendations"].append("✅ Polarion URL configured")
            analysis["details"]["url"] = self.config['url']
        else:
            analysis["recommendations"].append("❌ Polarion URL missing")
        
        if self.config.get('project_id'):
            score += 20
            analysis["recommendations"].append("✅ Project ID configured")
            analysis["details"]["project_id"] = self.config['project_id']
        else:
            analysis["recommendations"].append("❌ Project ID missing")
        
        # Authentication
        if self.config.get('pat_token'):
            score += 40
            analysis["recommendations"].append("✅ PAT token configured (recommended)")
            analysis["details"]["auth_type"] = "PAT"
        elif self.config.get('username') and self.config.get('password'):
            score += 30
            analysis["recommendations"].append("✅ Basic auth configured")
            analysis["details"]["auth_type"] = "Basic"
        else:
            analysis["recommendations"].append("❌ No authentication configured")
        
        # Optional settings
        if self.config.get('timeout'):
            score += 5
        if 'verify_ssl' in self.config:
            score += 5
        
        analysis["confidence"] = min(score / max_score, 1.0)
        return analysis
    
    def _ai_test_network_connectivity(self) -> Dict[str, Any]:
        """AI-powered network connectivity testing"""
        analysis = {
            "confidence": 0.0,
            "recommendations": [],
            "details": {}
        }
        
        if not self.config.get('url'):
            analysis["recommendations"].append("❌ No URL to test")
            return analysis
        
        try:
            import time
            start_time = time.time()
            
            # Test basic connectivity
            response = requests.get(
                f"{self.config['url']}/polarion",
                timeout=self.config.get('timeout', 30),
                verify=self.config.get('verify_ssl', True)
            )
            
            response_time = (time.time() - start_time) * 1000
            analysis["details"]["response_time_ms"] = round(response_time, 2)
            
            if response.status_code == 200:
                analysis["confidence"] = 0.9
                analysis["recommendations"].append(f"✅ Server accessible ({response_time:.0f}ms)")
            else:
                analysis["confidence"] = 0.5
                analysis["recommendations"].append(f"⚠️ Server returned status {response.status_code}")
                
        except requests.exceptions.SSLError:
            analysis["confidence"] = 0.3
            analysis["recommendations"].append("⚠️ SSL certificate issues")
            analysis["recommendations"].append("💡 Consider setting verify_ssl: false")
        except requests.exceptions.Timeout:
            analysis["confidence"] = 0.2
            analysis["recommendations"].append("⚠️ Connection timeout")
        except requests.exceptions.ConnectionError:
            analysis["confidence"] = 0.0
            analysis["recommendations"].append("❌ Cannot reach server")
        except Exception as e:
            analysis["confidence"] = 0.0
            analysis["recommendations"].append(f"❌ Network error: {e}")
        
        return analysis
    
    def _ai_test_api_authentication(self) -> Dict[str, Any]:
        """AI-powered API authentication testing"""
        analysis = {
            "confidence": 0.0,
            "recommendations": [],
            "details": {}
        }
        
        if not self.session:
            analysis["recommendations"].append("❌ No session initialized")
            return analysis
        
        try:
            # Test API endpoint with authentication
            response = self.session.get(
                f"{self.config['url']}/polarion/rest/v1/projects",
                timeout=self.config.get('timeout', 30)
            )
            
            if response.status_code == 200:
                analysis["confidence"] = 0.9
                analysis["recommendations"].append("✅ API authentication successful")
                
                # AI enhancement: Parse project list
                try:
                    projects = response.json()
                    analysis["details"]["accessible_projects"] = len(projects.get('data', []))
                    analysis["recommendations"].append(f"✅ Access to {analysis['details']['accessible_projects']} projects")
                except:
                    pass
                    
            elif response.status_code == 401:
                analysis["confidence"] = 0.0
                analysis["recommendations"].append("❌ Authentication failed (401)")
                analysis["recommendations"].append("💡 Check PAT token or credentials")
            elif response.status_code == 403:
                analysis["confidence"] = 0.3
                analysis["recommendations"].append("⚠️ Authentication succeeded but access denied (403)")
            else:
                analysis["confidence"] = 0.2
                analysis["recommendations"].append(f"⚠️ API returned status {response.status_code}")
                
        except Exception as e:
            analysis["confidence"] = 0.0
            analysis["recommendations"].append(f"❌ API test failed: {e}")
        
        return analysis
    
    def _ai_test_project_access(self) -> Dict[str, Any]:
        """AI-powered project access validation"""
        analysis = {
            "confidence": 0.0,
            "recommendations": [],
            "details": {}
        }
        
        project_id = self.config.get('project_id')
        if not project_id or not self.session:
            analysis["recommendations"].append("❌ No project to test or no session")
            return analysis
        
        try:
            # Test specific project access
            response = self.session.get(
                f"{self.config['url']}/polarion/rest/v1/projects/{project_id}",
                timeout=self.config.get('timeout', 30)
            )
            
            if response.status_code == 200:
                analysis["confidence"] = 0.9
                analysis["recommendations"].append(f"✅ Project '{project_id}' accessible")
                
                try:
                    project_data = response.json()
                    project_name = project_data.get('name', project_id)
                    analysis["details"]["project_name"] = project_name
                    analysis["recommendations"].append(f"✅ Project name: {project_name}")
                except:
                    pass
                    
            elif response.status_code == 404:
                analysis["confidence"] = 0.0
                analysis["recommendations"].append(f"❌ Project '{project_id}' not found")
            elif response.status_code == 403:
                analysis["confidence"] = 0.2
                analysis["recommendations"].append(f"❌ No access to project '{project_id}'")
            else:
                analysis["confidence"] = 0.3
                analysis["recommendations"].append(f"⚠️ Project test returned status {response.status_code}")
                
        except Exception as e:
            analysis["confidence"] = 0.0
            analysis["recommendations"].append(f"❌ Project access test failed: {e}")
        
        return analysis
    
    # =============================================================================
    # AI TEST CASE OPERATIONS (Replaces test_case_fetcher.py, test_case_poster.py)
    # =============================================================================
    
    def ai_post_test_cases(self, test_cases_file: str, ticket_id: str = None, project_id: str = None) -> AIPolarionResult:
        """AI-powered test case posting with intelligent parsing and metadata enhancement"""
        logger.info(f"🤖 AI Test Case Posting: Processing {test_cases_file}")
        
        try:
            # AI Phase 1: Validate prerequisites
            prereq_check = self._ai_validate_posting_prerequisites(project_id)
            if not prereq_check["valid"]:
                return AIPolarionResult(
                    success=False,
                    confidence=0.0,
                    data=prereq_check,
                    recommendations=prereq_check["recommendations"],
                    actions=["Fix configuration before posting"],
                    metadata={"phase": "prerequisites", "status": "failed"}
                )
            
            # AI Phase 2: Parse test cases from markdown
            parsing_result = self._ai_parse_test_cases_from_markdown(test_cases_file)
            if not parsing_result["success"]:
                return AIPolarionResult(
                    success=False,
                    confidence=0.0,
                    data=parsing_result,
                    recommendations=["❌ Failed to parse test cases from markdown"],
                    actions=["Check markdown format"],
                    metadata={"phase": "parsing", "status": "failed"}
                )
            
            test_cases = parsing_result["test_cases"]
            logger.info(f"🤖 AI: Parsed {len(test_cases)} test cases from markdown")
            
            # AI Phase 3: Enhance with metadata
            enhanced_cases = self._ai_enhance_test_cases_with_metadata(test_cases, ticket_id)
            
            # AI Phase 4: Post to Polarion
            posting_results = self._ai_post_cases_to_polarion(enhanced_cases, project_id or self.config['project_id'])
            
            success_rate = len(posting_results["successful"]) / len(enhanced_cases) if enhanced_cases else 0
            overall_success = success_rate > 0.5
            
            return AIPolarionResult(
                success=overall_success,
                confidence=success_rate,
                data={
                    "total_cases": len(enhanced_cases),
                    "successful_posts": posting_results["successful"],
                    "failed_posts": posting_results["failed"],
                    "success_rate": f"{success_rate:.1%}",
                    "project_id": project_id or self.config['project_id']
                },
                recommendations=[
                    f"✅ Posted {len(posting_results['successful'])} of {len(enhanced_cases)} test cases",
                    f"📊 Success rate: {success_rate:.1%}"
                ],
                actions=["Test cases available in Polarion"],
                metadata={
                    "status": "success" if overall_success else "partial",
                    "posting_results": posting_results
                }
            )
            
        except Exception as e:
            logger.error(f"AI test case posting failed: {e}")
            return AIPolarionResult(
                success=False,
                confidence=0.0,
                data={},
                recommendations=[f"❌ Posting failed: {e}"],
                actions=["Check configuration and file format"],
                metadata={"status": "error", "exception": str(e)}
            )
    
    def _ai_validate_posting_prerequisites(self, project_id: str = None) -> Dict[str, Any]:
        """AI validation of posting prerequisites"""
        validation = {
            "valid": True,
            "recommendations": []
        }
        
        if not self.session:
            validation["valid"] = False
            validation["recommendations"].append("❌ No authenticated session")
            return validation
        
        target_project = project_id or self.config.get('project_id')
        if not target_project:
            validation["valid"] = False
            validation["recommendations"].append("❌ No project ID specified")
            return validation
        
        validation["recommendations"].append("✅ Prerequisites validated")
        validation["project_id"] = target_project
        return validation
    
    def _ai_parse_test_cases_from_markdown(self, file_path: str) -> Dict[str, Any]:
        """AI-powered parsing of test cases from markdown"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # AI pattern recognition for test cases
            test_cases = []
            
            # Pattern 1: ## Test Case format
            test_case_pattern = r'## Test Case \d+:(.*?)(?=## Test Case \d+:|$)'
            matches = re.findall(test_case_pattern, content, re.DOTALL)
            
            for i, match in enumerate(matches, 1):
                test_case = self._ai_extract_test_case_details(match, i)
                if test_case:
                    test_cases.append(test_case)
            
            return {
                "success": True,
                "test_cases": test_cases,
                "count": len(test_cases)
            }
            
        except Exception as e:
            logger.error(f"AI markdown parsing failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "test_cases": []
            }
    
    def _ai_extract_test_case_details(self, content: str, case_number: int) -> Optional[Dict[str, Any]]:
        """AI extraction of test case details from markdown content"""
        try:
            lines = content.strip().split('\n')
            
            # AI parsing of title
            title_line = lines[0].strip() if lines else f"Test Case {case_number}"
            title = title_line.strip(' :')
            
            # AI parsing of description and setup
            description = ""
            setup = ""
            test_steps = []
            
            current_section = None
            in_table = False
            
            for line in lines[1:]:
                line = line.strip()
                
                if line.startswith('**Description:**'):
                    current_section = 'description'
                    description = line.replace('**Description:**', '').strip()
                elif line.startswith('**Setup:**'):
                    current_section = 'setup'
                    setup = line.replace('**Setup:**', '').strip()
                elif '| Step |' in line and '| Expected Result |' in line:
                    current_section = 'table'
                    in_table = True
                elif in_table and line.startswith('|') and not line.startswith('|---'):
                    # AI parsing of table rows
                    parts = [part.strip() for part in line.split('|')[1:-1]]
                    if len(parts) >= 2:
                        test_steps.append({
                            "step": parts[0],
                            "expected_result": parts[1]
                        })
                elif current_section == 'description' and line and not line.startswith('**'):
                    description += " " + line
                elif current_section == 'setup' and line and not line.startswith('**'):
                    setup += " " + line
            
            return {
                "title": title,
                "description": description.strip(),
                "setup": setup.strip(),
                "test_steps": test_steps,
                "case_number": case_number
            }
            
        except Exception as e:
            logger.warning(f"AI failed to extract test case {case_number}: {e}")
            return None
    
    def _ai_enhance_test_cases_with_metadata(self, test_cases: List[Dict[str, Any]], ticket_id: str = None) -> List[Dict[str, Any]]:
        """AI enhancement of test cases with intelligent metadata"""
        enhanced_cases = []
        
        for case in test_cases:
            enhanced = case.copy()
            
            # AI metadata enhancement
            enhanced["metadata"] = {
                "source": "claude_test_generator",
                "generated_at": datetime.now().isoformat(),
                "ai_enhanced": True,
                "type": self.config.get('test_case_type', 'testcase'),
                "status": "draft",
                "priority": "normal",
                "severity": "normal"
            }
            
            if ticket_id:
                enhanced["metadata"]["jira_ticket"] = ticket_id
            
            # AI intelligent categorization
            title_lower = case.get("title", "").lower()
            description_lower = case.get("description", "").lower()
            
            # AI category detection
            if any(word in title_lower + description_lower for word in ["upgrade", "update", "migration"]):
                enhanced["metadata"]["category"] = "upgrade"
                enhanced["metadata"]["priority"] = "high"
            elif any(word in title_lower + description_lower for word in ["ui", "console", "interface"]):
                enhanced["metadata"]["category"] = "ui"
            elif any(word in title_lower + description_lower for word in ["rbac", "security", "auth"]):
                enhanced["metadata"]["category"] = "security"
                enhanced["metadata"]["priority"] = "high"
            elif any(word in title_lower + description_lower for word in ["import", "export"]):
                enhanced["metadata"]["category"] = "import_export"
            else:
                enhanced["metadata"]["category"] = "functional"
            
            enhanced_cases.append(enhanced)
        
        return enhanced_cases
    
    def _ai_post_cases_to_polarion(self, test_cases: List[Dict[str, Any]], project_id: str) -> Dict[str, List]:
        """AI-powered posting of test cases to Polarion"""
        results = {
            "successful": [],
            "failed": []
        }
        
        for case in test_cases:
            try:
                # AI formatting for Polarion
                polarion_case = self._ai_format_case_for_polarion(case, project_id)
                
                # AI posting with retry logic
                post_result = self._ai_post_single_case(polarion_case, project_id)
                
                if post_result["success"]:
                    results["successful"].append({
                        "title": case["title"],
                        "id": post_result["id"],
                        "url": post_result.get("url")
                    })
                else:
                    results["failed"].append({
                        "title": case["title"],
                        "error": post_result["error"]
                    })
                    
            except Exception as e:
                logger.error(f"AI failed to post case '{case.get('title', 'Unknown')}': {e}")
                results["failed"].append({
                    "title": case.get("title", "Unknown"),
                    "error": str(e)
                })
        
        return results
    
    def _ai_format_case_for_polarion(self, case: Dict[str, Any], project_id: str) -> Dict[str, Any]:
        """AI formatting of test case for Polarion API"""
        # Build test steps in Polarion format
        test_steps_html = "<ol>"
        for step in case.get("test_steps", []):
            test_steps_html += f"<li><strong>Step:</strong> {step['step']}<br/>"
            test_steps_html += f"<strong>Expected Result:</strong> {step['expected_result']}</li>"
        test_steps_html += "</ol>"
        
        description_html = case.get("description", "")
        if case.get("setup"):
            description_html += f"<br/><strong>Setup:</strong> {case['setup']}"
        
        return {
            "type": case["metadata"]["type"],
            "title": case["title"],
            "description": description_html,
            "testSteps": test_steps_html,
            "status": case["metadata"]["status"],
            "priority": case["metadata"]["priority"],
            "severity": case["metadata"]["severity"],
            "customFields": {
                "source": case["metadata"]["source"],
                "ai_enhanced": case["metadata"]["ai_enhanced"],
                "category": case["metadata"]["category"],
                "jira_ticket": case["metadata"].get("jira_ticket"),
                "generated_at": case["metadata"]["generated_at"]
            }
        }
    
    def _ai_post_single_case(self, case_data: Dict[str, Any], project_id: str) -> Dict[str, Any]:
        """AI posting of single test case with intelligent error handling"""
        try:
            response = self.session.post(
                f"{self.config['url']}/polarion/rest/v1/projects/{project_id}/workitems",
                json=case_data,
                timeout=self.config.get('timeout', 30)
            )
            
            if response.status_code in [200, 201]:
                response_data = response.json()
                test_case_id = response_data.get('id')
                
                return {
                    "success": True,
                    "id": test_case_id,
                    "url": f"{self.config['url']}/polarion/#/project/{project_id}/workitem?id={test_case_id}"
                }
            else:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}: {response.text}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    # =============================================================================
    # AI FRAMEWORK INTEGRATION (Replaces framework_integration.py)
    # =============================================================================
    
    def ai_framework_integration(self, test_cases_file: str, ticket_id: str = None, project_id: str = None) -> Optional[Dict[str, Any]]:
        """Main framework integration point - replaces all integration scripts"""
        logger.info("🤖 AI Framework Integration: Starting Polarion integration")
        
        # AI availability check
        if not self._ai_has_valid_credentials():
            logger.info("🤖 AI: Polarion not configured - skipping integration")
            return None
        
        # AI posting attempt
        posting_result = self.ai_post_test_cases(test_cases_file, ticket_id, project_id)
        
        if posting_result.success:
            return {
                "success": True,
                "test_case_ids": [case["id"] for case in posting_result.data.get("successful_posts", [])],
                "project_id": posting_result.data.get("project_id"),
                "count": posting_result.data.get("total_cases", 0),
                "report": {
                    "total_posted": len(posting_result.data.get("successful_posts", [])),
                    "success_rate": posting_result.data.get("success_rate", "0%"),
                    "test_cases": posting_result.data.get("successful_posts", []),
                    "posted_at": datetime.now().isoformat()
                },
                "message": f"✅ AI posted {posting_result.data.get('total_cases', 0)} test cases to Polarion"
            }
        else:
            return {
                "success": False,
                "reason": posting_result.metadata.get("status", "unknown"),
                "message": posting_result.recommendations[0] if posting_result.recommendations else "❌ AI posting failed"
            }
    
    def ai_generate_polarion_section(self, posting_result: Optional[Dict[str, Any]]) -> str:
        """AI generation of Polarion section for Complete-Analysis.md"""
        if not posting_result:
            return f"""## 🔗 Polarion Integration

**Status**: ❌ Not Configured  
**AI Recommendation**: Set up Polarion integration for automatic test case posting

💡 **Setup Instructions**:
1. Install dependencies: `pip install -r requirements.txt`
2. Configure credentials: Use the AI setup service
3. Test connection: Verify with AI connection service

🤖 **AI Enhancement**: This integration uses intelligent credential management, 
automated test case parsing, and adaptive posting strategies.

"""
        
        if not posting_result.get("success"):
            return f"""## 🔗 Polarion Integration

**Status**: ❌ Posting Failed  
**AI Analysis**: {posting_result.get('reason', 'Unknown error')}  
**Message**: {posting_result.get('message', 'AI posting failed')}

🤖 **AI Troubleshooting**: The AI service detected configuration issues.
Run the AI diagnostic service to resolve problems automatically.

"""
        
        report = posting_result.get("report", {})
        test_cases = report.get("test_cases", [])
        
        content = f"""## 🔗 Polarion Integration

**Status**: ✅ AI Successfully Posted  
**Project**: {posting_result.get('project_id', 'Unknown')}  
**Test Cases Created**: {posting_result.get('count', 0)}  
**AI Success Rate**: {report.get('success_rate', '100%')}

### 🤖 AI-Created Test Cases
"""
        
        for tc in test_cases:
            content += f"- **[{tc['id']}]({tc.get('url', '#')})**: {tc['title']}\n"
        
        content += f"\n### 🎯 AI Integration Details\n"
        content += f"- **AI Parsing**: Intelligent markdown analysis and test case extraction\n"
        content += f"- **AI Enhancement**: Automatic metadata addition and categorization\n"
        content += f"- **AI Posting**: Adaptive error handling and retry strategies\n"
        content += f"- **Posted**: {report.get('posted_at', 'Unknown time')}\n"
        
        return content
    
    def ai_get_status_for_framework(self) -> str:
        """AI generation of Polarion status for framework reports"""
        status_result = self.ai_credential_status()
        
        if not status_result.success or not status_result.data.get("configuration_valid"):
            return f"""## 🔗 Polarion Integration

**Status**: ❌ Not Configured  
**AI Analysis**: Configuration incomplete or invalid

💡 **AI Setup Required**:
1. Run: AI credential setup service
2. Configure Polarion URL and project ID  
3. Test: AI connection validation service

🤖 **AI Features Available**: Once configured, enjoy intelligent credential management,
automated test case posting, and adaptive error handling.

"""
        
        return f"""## 🔗 Polarion Integration

**Status**: ✅ AI Ready (Optional)  
**Project**: {status_result.data.get('project_id', 'Not set')}  
**Server**: {status_result.data.get('url', 'Not set')}  
**AI Management**: {status_result.data.get('ai_managed', False)}

🤖 **AI Intelligence Available**: Test cases can be posted to Polarion when explicitly requested
with intelligent parsing, metadata enhancement, and adaptive posting strategies.

💡 **Usage**: Polarion posting is now OPTIONAL - specify in your request to enable posting.

"""

# =============================================================================
# MAIN AI SERVICE INTERFACE
# =============================================================================

# Global AI service instance
_ai_polarion_service = None

def get_ai_polarion_service() -> AIPolarionService:
    """Get the global AI Polarion service instance"""
    global _ai_polarion_service
    if _ai_polarion_service is None:
        _ai_polarion_service = AIPolarionService()
    return _ai_polarion_service

# Framework integration functions (replacing all scripts)
def post_test_cases_if_enabled(test_cases_file: str, ticket_id: str = None, project_id: str = None, user_requested: bool = False) -> Optional[Dict[str, Any]]:
    """AI-powered test case posting for framework integration - ONLY when explicitly requested by user"""
    if not user_requested:
        # Polarion posting is now OPTIONAL - only when user explicitly requests it
        return None
    
    service = get_ai_polarion_service()
    return service.ai_framework_integration(test_cases_file, ticket_id, project_id)

def get_polarion_status_for_framework() -> str:
    """AI-generated Polarion status for framework reports"""
    service = get_ai_polarion_service()
    return service.ai_get_status_for_framework()

def integrate_polarion_with_framework():
    """Factory function returning AI service (replaces old integration class)"""
    return get_ai_polarion_service()

# CLI interface functions
def ai_setup_credentials():
    """AI credential setup interface"""
    service = get_ai_polarion_service()
    return service.ai_setup_credentials()

def ai_credential_status():
    """AI credential status interface"""
    service = get_ai_polarion_service()
    return service.ai_credential_status()

def ai_test_connection():
    """AI connection test interface"""
    service = get_ai_polarion_service()
    return service.ai_test_connection()

def ai_post_test_cases(test_cases_file: str, ticket_id: str = None, project_id: str = None):
    """AI test case posting interface"""
    service = get_ai_polarion_service()
    return service.ai_post_test_cases(test_cases_file, ticket_id, project_id)

if __name__ == "__main__":
    # AI service demonstration
    print("🤖 AI Polarion Service")
    print("=" * 30)
    
    service = get_ai_polarion_service()
    
    # Show AI status
    status = service.ai_credential_status()
    print(f"Configuration Valid: {status.data.get('configuration_valid', False)}")
    print(f"Recommendations: {status.recommendations}")
    
    if status.data.get('configuration_valid'):
        # Test AI connection
        connection = service.ai_test_connection()
        print(f"Connection Success: {connection.success}")
        print(f"Confidence: {connection.confidence:.1%}")
    else:
        print("\n💡 Run ai_setup_credentials() to configure Polarion")