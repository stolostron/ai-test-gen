#!/usr/bin/env python3
"""
Foundation Context Data Structure for Progressive Context Architecture
Provides the core data model for Phase 0 and agent inheritance
"""

import json
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum


class ContextValidationLevel(Enum):
    """Context validation levels for quality assurance"""
    MINIMAL = "minimal"
    STANDARD = "standard"
    COMPREHENSIVE = "comprehensive"


@dataclass
class JiraTicketInfo:
    """JIRA ticket information extracted from API"""
    jira_id: str
    title: str
    status: str
    fix_version: Optional[str]
    priority: str
    component: str
    detection_timestamp: str
    confidence: float = 0.9


@dataclass
class VersionContext:
    """Version analysis context for gap assessment"""
    target_version: str
    environment_version: str
    comparison_result: str  # "newer", "same", "older", "unknown"
    detection_method: str
    confidence: float = 0.9
    version_gap_details: Optional[Dict[str, Any]] = None


@dataclass
class EnvironmentBaseline:
    """Environment assessment baseline information"""
    cluster_name: str
    api_url: str
    console_url: str
    platform: str
    region: str
    health_status: str
    connectivity_confirmed: bool
    assessment_timestamp: str
    confidence: float = 0.9


@dataclass
class ContextMetadata:
    """Metadata for context tracking and validation"""
    context_version: str = "1.0.0"
    creation_timestamp: str = ""
    last_updated: str = ""
    consistency_score: float = 1.0
    validation_level: ContextValidationLevel = ContextValidationLevel.STANDARD
    
    def __post_init__(self):
        if not self.creation_timestamp:
            self.creation_timestamp = datetime.utcnow().isoformat()
        if not self.last_updated:
            self.last_updated = self.creation_timestamp


@dataclass
class FoundationContext:
    """
    Core Foundation Context for Progressive Context Architecture
    This is the base context that all agents inherit and enhance
    """
    
    # Metadata
    metadata: ContextMetadata
    
    # Core foundation data
    jira_info: JiraTicketInfo
    version_context: VersionContext
    environment_baseline: EnvironmentBaseline
    
    # Deployment instruction
    deployment_instruction: str
    
    # Progressive context preparation
    agent_inheritance_ready: bool = False
    
    # Validation tracking
    validation_results: Optional[Dict[str, bool]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        data = asdict(self)
        # Convert enums to strings for JSON serialization
        if 'metadata' in data and 'validation_level' in data['metadata']:
            data['metadata']['validation_level'] = data['metadata']['validation_level'].value
        return data
    
    def to_json(self) -> str:
        """Convert to JSON string"""
        return json.dumps(self.to_dict(), indent=2)
    
    def save_to_file(self, file_path: str) -> bool:
        """Save foundation context to file"""
        try:
            with open(file_path, 'w') as f:
                f.write(self.to_json())
            return True
        except Exception as e:
            print(f"Error saving foundation context: {e}")
            return False
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FoundationContext':
        """Create FoundationContext from dictionary"""
        # Handle enum conversion for metadata
        metadata_data = data['metadata'].copy()
        if 'validation_level' in metadata_data and isinstance(metadata_data['validation_level'], str):
            metadata_data['validation_level'] = ContextValidationLevel(metadata_data['validation_level'])
        
        return cls(
            metadata=ContextMetadata(**metadata_data),
            jira_info=JiraTicketInfo(**data['jira_info']),
            version_context=VersionContext(**data['version_context']),
            environment_baseline=EnvironmentBaseline(**data['environment_baseline']),
            deployment_instruction=data['deployment_instruction'],
            agent_inheritance_ready=data.get('agent_inheritance_ready', False),
            validation_results=data.get('validation_results')
        )
    
    @classmethod
    def from_json_file(cls, file_path: str) -> 'FoundationContext':
        """Load FoundationContext from JSON file"""
        with open(file_path, 'r') as f:
            data = json.load(f)
        return cls.from_dict(data)
    
    def validate_completeness(self) -> Dict[str, bool]:
        """Validate that all required fields are properly populated"""
        validation_results = {
            'jira_id_present': bool(self.jira_info.jira_id),
            'target_version_present': bool(self.version_context.target_version),
            'environment_version_present': bool(self.version_context.environment_version),
            'version_gap_analyzed': bool(self.version_context.comparison_result != "unknown"),
            'environment_assessed': bool(self.environment_baseline.health_status),
            'deployment_instruction_generated': bool(self.deployment_instruction),
            'connectivity_confirmed': self.environment_baseline.connectivity_confirmed,
            'metadata_complete': bool(self.metadata.creation_timestamp)
        }
        
        # Update validation results
        self.validation_results = validation_results
        
        # Calculate overall completeness score
        completeness_score = sum(validation_results.values()) / len(validation_results)
        self.metadata.consistency_score = completeness_score
        
        # Update last modified timestamp
        self.metadata.last_updated = datetime.utcnow().isoformat()
        
        return validation_results
    
    def is_ready_for_agent_inheritance(self) -> bool:
        """Check if foundation context is ready for agent inheritance"""
        validation_results = self.validate_completeness()
        
        # Require all critical fields to be present
        critical_requirements = [
            'jira_id_present',
            'target_version_present',
            'environment_version_present',
            'version_gap_analyzed',
            'deployment_instruction_generated'
        ]
        
        all_critical_met = all(validation_results.get(req, False) for req in critical_requirements)
        
        self.agent_inheritance_ready = all_critical_met
        return all_critical_met
    
    def get_agent_context_summary(self) -> Dict[str, Any]:
        """Get summary suitable for agent context inheritance"""
        return {
            'jira_id': self.jira_info.jira_id,
            'jira_title': self.jira_info.title,
            'jira_status': self.jira_info.status,
            'target_version': self.version_context.target_version,
            'environment_version': self.version_context.environment_version,
            'version_gap': self.version_context.comparison_result,
            'environment': {
                'cluster': self.environment_baseline.cluster_name,
                'platform': self.environment_baseline.platform,
                'health': self.environment_baseline.health_status
            },
            'deployment_instruction': self.deployment_instruction,
            'context_quality': self.metadata.consistency_score,
            'ready_for_agents': self.agent_inheritance_ready
        }


class FoundationContextBuilder:
    """Builder pattern for creating FoundationContext instances"""
    
    def __init__(self):
        self.reset()
    
    def reset(self):
        """Reset builder to initial state"""
        self._jira_info = None
        self._version_context = None
        self._environment_baseline = None
        self._deployment_instruction = ""
        self._metadata = ContextMetadata()
    
    def with_jira_info(self, jira_id: str, title: str, status: str, 
                      fix_version: Optional[str] = None, priority: str = "Medium",
                      component: str = "Unknown") -> 'FoundationContextBuilder':
        """Add JIRA information"""
        self._jira_info = JiraTicketInfo(
            jira_id=jira_id,
            title=title,
            status=status,
            fix_version=fix_version,
            priority=priority,
            component=component,
            detection_timestamp=datetime.utcnow().isoformat()
        )
        return self
    
    def with_version_context(self, target_version: str, environment_version: str,
                           comparison_result: str, detection_method: str) -> 'FoundationContextBuilder':
        """Add version context"""
        self._version_context = VersionContext(
            target_version=target_version,
            environment_version=environment_version,
            comparison_result=comparison_result,
            detection_method=detection_method
        )
        return self
    
    def with_environment_baseline(self, cluster_name: str, api_url: str, console_url: str,
                                platform: str, region: str, health_status: str,
                                connectivity_confirmed: bool) -> 'FoundationContextBuilder':
        """Add environment baseline"""
        self._environment_baseline = EnvironmentBaseline(
            cluster_name=cluster_name,
            api_url=api_url,
            console_url=console_url,
            platform=platform,
            region=region,
            health_status=health_status,
            connectivity_confirmed=connectivity_confirmed,
            assessment_timestamp=datetime.utcnow().isoformat()
        )
        return self
    
    def with_deployment_instruction(self, instruction: str) -> 'FoundationContextBuilder':
        """Add deployment instruction"""
        self._deployment_instruction = instruction
        return self
    
    def build(self) -> FoundationContext:
        """Build the FoundationContext instance"""
        if not all([self._jira_info, self._version_context, self._environment_baseline]):
            raise ValueError("Missing required components for FoundationContext")
        
        context = FoundationContext(
            metadata=self._metadata,
            jira_info=self._jira_info,
            version_context=self._version_context,
            environment_baseline=self._environment_baseline,
            deployment_instruction=self._deployment_instruction
        )
        
        # Validate and prepare for agent inheritance
        context.validate_completeness()
        context.is_ready_for_agent_inheritance()
        
        return context


# Convenience function for quick context creation
def create_foundation_context(jira_id: str, jira_title: str, jira_status: str,
                            target_version: str, environment_version: str,
                            cluster_name: str, environment_health: str,
                            deployment_instruction: str = "") -> FoundationContext:
    """Quick creation of foundation context with minimal required fields"""
    
    builder = FoundationContextBuilder()
    
    # Determine version comparison
    comparison_result = "unknown"
    if target_version and environment_version:
        if target_version == environment_version:
            comparison_result = "same"
        elif target_version > environment_version:
            comparison_result = "newer"
        else:
            comparison_result = "older"
    
    # Generate deployment instruction if not provided
    if not deployment_instruction and comparison_result != "unknown":
        if comparison_result == "newer":
            deployment_instruction = f"Upgrade from {environment_version} to {target_version}"
        elif comparison_result == "same":
            deployment_instruction = f"Environment already at target version {target_version}"
        else:
            deployment_instruction = f"Target version {target_version} is older than environment {environment_version}"
    
    return (builder
            .with_jira_info(jira_id, jira_title, jira_status)
            .with_version_context(target_version, environment_version, comparison_result, "api_detection")
            .with_environment_baseline(cluster_name, "api-detected", "console-detected", 
                                     "kubernetes", "detected", environment_health, True)
            .with_deployment_instruction(deployment_instruction)
            .build())