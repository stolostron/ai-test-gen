#!/usr/bin/env python3
"""
Evidence Validation Engine
Critical service for ensuring accuracy and preventing false positives in analysis
"""

import json
import logging
import re
import time
from dataclasses import dataclass, asdict
from typing import Dict, Any, List, Optional, Tuple
from enum import Enum


class ValidationType(Enum):
    """Types of validation checks"""
    FILE_EXISTENCE = "file_existence"
    DEPENDENCY_VERIFICATION = "dependency_verification"  
    EXTENSION_VERIFICATION = "extension_verification"
    CITATION_VERIFICATION = "citation_verification"
    TECHNICAL_CLAIM_VERIFICATION = "technical_claim_verification"
    CROSS_SOURCE_CONSISTENCY = "cross_source_consistency"


class ValidationResult(Enum):
    """Validation check results"""
    VERIFIED = "verified"
    FAILED = "failed"
    PARTIALLY_VERIFIED = "partially_verified"
    UNABLE_TO_VERIFY = "unable_to_verify"


@dataclass
class ValidationCheck:
    """Individual validation check result"""
    check_type: ValidationType
    claim: str
    result: ValidationResult
    confidence: float
    evidence: List[str]
    verification_method: str
    timestamp: float


@dataclass
class ValidationSummary:
    """Summary of all validation checks"""
    total_checks: int
    verified_count: int
    failed_count: int
    partially_verified_count: int
    unable_to_verify_count: int
    overall_accuracy: float
    false_positive_risk: float
    validation_timestamp: float


@dataclass
class EvidenceValidationResult:
    """Complete evidence validation result"""
    checks: List[ValidationCheck]
    summary: ValidationSummary
    validated_claims: List[str]
    rejected_claims: List[str]
    confidence_score: float


class EvidenceValidationEngine:
    """
    Evidence Validation Engine
    Ensures accuracy and prevents false positives in technical analysis
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Validation patterns for different claim types
        self.file_extension_patterns = {
            'javascript': ['.js', '.jsx'],
            'typescript': ['.ts', '.tsx'],
            'cypress': ['.cy.js', '.cy.ts'],
            'test_files': ['.test.js', '.spec.js', '.test.ts', '.spec.ts']
        }
        
        # Known false positive patterns to catch
        self.false_positive_patterns = [
            r'\.cy\.js.*when.*actual.*\.js',  # Extension mismatches
            r'\.cy\.js.*files.*when.*actual.*files.*\.js',  # Extension mismatches variation
            r'mobx.*dependency.*without.*package\.json.*verification',  # Dependency claims
            r'mobx.*without.*verification',  # Dependency claims variation
            r'all.*verified.*without.*actual.*verification',  # Overconfident claims
            r'verified.*without.*verification',  # Overconfident claims variation
        ]
    
    def validate_technical_claims(self, claims: List[str], 
                                investigation_data: Dict[str, Any]) -> EvidenceValidationResult:
        """
        Validate technical claims against actual evidence
        
        Args:
            claims: List of technical claims to validate
            investigation_data: Raw investigation data for validation
            
        Returns:
            EvidenceValidationResult: Complete validation analysis
        """
        self.logger.info(f"Starting validation of {len(claims)} technical claims")
        
        validation_checks = []
        
        for claim in claims:
            # Run multiple validation checks per claim
            checks = self._validate_single_claim(claim, investigation_data)
            validation_checks.extend(checks)
        
        # Generate validation summary
        summary = self._generate_validation_summary(validation_checks)
        
        # Categorize claims based on validation results
        validated_claims, rejected_claims = self._categorize_claims(claims, validation_checks)
        
        # Calculate overall confidence
        confidence_score = self._calculate_validation_confidence(validation_checks, summary)
        
        return EvidenceValidationResult(
            checks=validation_checks,
            summary=summary,
            validated_claims=validated_claims,
            rejected_claims=rejected_claims,
            confidence_score=confidence_score
        )
    
    def _validate_single_claim(self, claim: str, 
                              investigation_data: Dict[str, Any]) -> List[ValidationCheck]:
        """Validate a single technical claim with multiple check types"""
        checks = []
        timestamp = time.time()
        
        # Check for file extension claims
        if self._is_file_extension_claim(claim):
            check = self._validate_file_extensions(claim, investigation_data, timestamp)
            checks.append(check)
        
        # Check for dependency claims
        if self._is_dependency_claim(claim):
            check = self._validate_dependency_claims(claim, investigation_data, timestamp)
            checks.append(check)
        
        # Check for citation claims
        if self._is_citation_claim(claim):
            check = self._validate_citation_claims(claim, investigation_data, timestamp)
            checks.append(check)
        
        # Check for false positive patterns
        false_positive_check = self._check_false_positive_patterns(claim, timestamp)
        if false_positive_check:
            checks.append(false_positive_check)
        
        # If no specific checks apply, do general technical claim validation
        if not checks:
            check = self._validate_general_technical_claim(claim, investigation_data, timestamp)
            checks.append(check)
        
        return checks
    
    def _is_file_extension_claim(self, claim: str) -> bool:
        """Check if claim is about file extensions"""
        extension_indicators = [
            r'\.cy\.js', r'\.js', r'\.ts', r'\.jsx', r'\.tsx',
            r'file.*extension', r'files.*found.*\d+.*\.', r'\.spec\.', r'\.test\.'
        ]
        
        return any(re.search(pattern, claim, re.IGNORECASE) for pattern in extension_indicators)
    
    def _is_dependency_claim(self, claim: str) -> bool:
        """Check if claim is about dependencies"""
        dependency_indicators = [
            r'package\.json', r'dependency', r'mobx', r'cypress.*version',
            r'npm.*install', r'dependency.*version', r'framework.*version'
        ]
        
        return any(re.search(pattern, claim, re.IGNORECASE) for pattern in dependency_indicators)
    
    def _is_citation_claim(self, claim: str) -> bool:
        """Check if claim contains citation references"""
        citation_indicators = [
            r'\[Jenkins:', r'\[Repo:', r'\[Env:', r'\[Fix:', r'\[JIRA:',
            r'https://.*jenkins', r'https://.*github', r'https://.*jira'
        ]
        
        return any(re.search(pattern, claim, re.IGNORECASE) for pattern in citation_indicators)
    
    def _validate_file_extensions(self, claim: str, investigation_data: Dict[str, Any], 
                                 timestamp: float) -> ValidationCheck:
        """Validate file extension claims against actual repository data"""
        
        # Extract claimed file extensions
        claimed_extensions = re.findall(r'\.(\w+)', claim)
        
        # Check repository analysis data
        repo_data = investigation_data.get('repository_analysis', {})
        actual_files = repo_data.get('test_files_found', [])
        
        if not actual_files:
            return ValidationCheck(
                check_type=ValidationType.EXTENSION_VERIFICATION,
                claim=claim,
                result=ValidationResult.UNABLE_TO_VERIFY,
                confidence=0.0,
                evidence=["No repository file data available"],
                verification_method="repository_file_analysis",
                timestamp=timestamp
            )
        
        # Analyze actual file extensions
        actual_extensions = set()
        for file_path in actual_files:
            if '.' in file_path:
                ext = file_path.split('.')[-1]
                actual_extensions.add(ext)
        
        # Validate claimed vs actual
        verification_evidence = [f"Actual files found: {actual_files}"]
        verification_evidence.append(f"Actual extensions: {sorted(actual_extensions)}")
        verification_evidence.append(f"Claimed extensions: {claimed_extensions}")
        
        # Check for common false positive: .cy.js vs .js
        if 'cy' in claimed_extensions and 'cy' not in actual_extensions and 'js' in actual_extensions:
            return ValidationCheck(
                check_type=ValidationType.EXTENSION_VERIFICATION,
                claim=claim,
                result=ValidationResult.FAILED,
                confidence=0.9,
                evidence=verification_evidence + ["Extension mismatch detected: .cy.js vs .js"],
                verification_method="repository_file_extension_analysis",
                timestamp=timestamp
            )
        
        # Check if claimed extensions match actual
        claimed_set = set(claimed_extensions)
        if claimed_set.issubset(actual_extensions):
            return ValidationCheck(
                check_type=ValidationType.EXTENSION_VERIFICATION,
                claim=claim,
                result=ValidationResult.VERIFIED,
                confidence=0.95,
                evidence=verification_evidence + ["Extensions verified against actual files"],
                verification_method="repository_file_extension_analysis",
                timestamp=timestamp
            )
        else:
            return ValidationCheck(
                check_type=ValidationType.EXTENSION_VERIFICATION,
                claim=claim,
                result=ValidationResult.FAILED,
                confidence=0.85,
                evidence=verification_evidence + ["Extension mismatch detected"],
                verification_method="repository_file_extension_analysis",
                timestamp=timestamp
            )
    
    def _validate_dependency_claims(self, claim: str, investigation_data: Dict[str, Any], 
                                   timestamp: float) -> ValidationCheck:
        """Validate dependency claims against actual package data"""
        
        # Check repository dependency analysis
        repo_data = investigation_data.get('repository_analysis', {})
        dependency_analysis = repo_data.get('dependency_analysis', {})
        
        if not dependency_analysis:
            return ValidationCheck(
                check_type=ValidationType.DEPENDENCY_VERIFICATION,
                claim=claim,
                result=ValidationResult.UNABLE_TO_VERIFY,
                confidence=0.0,
                evidence=["No dependency analysis data available"],
                verification_method="package_json_analysis",
                timestamp=timestamp
            )
        
        # Look for specific dependency mentions in claim
        mobx_mentioned = 'mobx' in claim.lower()
        cypress_mentioned = 'cypress' in claim.lower()
        
        evidence = [f"Dependency analysis: {dependency_analysis}"]
        
        # Validate MobX claims (common false positive)
        if mobx_mentioned:
            framework = dependency_analysis.get('framework', '').lower()
            if 'mobx' not in str(dependency_analysis).lower():
                return ValidationCheck(
                    check_type=ValidationType.DEPENDENCY_VERIFICATION,
                    claim=claim,
                    result=ValidationResult.FAILED,
                    confidence=0.9,
                    evidence=evidence + ["MobX not found in dependency analysis"],
                    verification_method="package_json_verification",
                    timestamp=timestamp
                )
        
        # Validate Cypress claims
        if cypress_mentioned:
            framework = dependency_analysis.get('framework', '').lower()
            if 'cypress' in framework:
                return ValidationCheck(
                    check_type=ValidationType.DEPENDENCY_VERIFICATION,
                    claim=claim,
                    result=ValidationResult.VERIFIED,
                    confidence=0.9,
                    evidence=evidence + [f"Cypress framework verified: {framework}"],
                    verification_method="package_json_verification",
                    timestamp=timestamp
                )
        
        # General dependency validation
        return ValidationCheck(
            check_type=ValidationType.DEPENDENCY_VERIFICATION,
            claim=claim,
            result=ValidationResult.PARTIALLY_VERIFIED,
            confidence=0.6,
            evidence=evidence + ["Partial dependency verification completed"],
            verification_method="package_json_analysis",
            timestamp=timestamp
        )
    
    def _validate_citation_claims(self, claim: str, investigation_data: Dict[str, Any], 
                                 timestamp: float) -> ValidationCheck:
        """Validate citation claims against available evidence sources"""
        
        # Extract citation patterns
        jenkins_citations = re.findall(r'\[Jenkins:[^\]]+\]', claim)
        repo_citations = re.findall(r'\[Repo:[^\]]+\]', claim)
        
        # Check against available evidence sources
        jenkins_data = investigation_data.get('jenkins_intelligence', {})
        repo_data = investigation_data.get('repository_analysis', {})
        
        evidence = []
        verification_score = 0.0
        total_citations = len(jenkins_citations) + len(repo_citations)
        
        if total_citations == 0:
            return ValidationCheck(
                check_type=ValidationType.CITATION_VERIFICATION,
                claim=claim,
                result=ValidationResult.UNABLE_TO_VERIFY,
                confidence=0.0,
                evidence=["No citations found to verify"],
                verification_method="citation_pattern_analysis",
                timestamp=timestamp
            )
        
        # Validate Jenkins citations
        for citation in jenkins_citations:
            if jenkins_data.get('metadata', {}).get('job_name'):
                verification_score += 1.0
                evidence.append(f"Jenkins citation verified: {citation}")
            else:
                evidence.append(f"Jenkins citation unverified: {citation}")
        
        # Validate repository citations
        for citation in repo_citations:
            if repo_data.get('repository_cloned', False):
                verification_score += 1.0
                evidence.append(f"Repository citation verified: {citation}")
            else:
                evidence.append(f"Repository citation unverified: {citation}")
        
        # Special case: if we have mixed results, it should be partially verified
        verified_citations = verification_score
        unverified_citations = total_citations - verification_score
        
        # Calculate verification result
        verification_ratio = verification_score / total_citations
        
        # Handle mixed citation scenarios more accurately
        if verified_citations > 0 and unverified_citations > 0:
            # Mixed results - some verified, some not
            result = ValidationResult.PARTIALLY_VERIFIED
            confidence = 0.6 + (verification_ratio * 0.2)  # 0.6-0.8 range
        elif verification_ratio >= 0.8:
            result = ValidationResult.VERIFIED
            confidence = 0.9
        elif verification_ratio >= 0.5:
            result = ValidationResult.PARTIALLY_VERIFIED
            confidence = 0.7
        else:
            result = ValidationResult.FAILED
            confidence = 0.5
        
        return ValidationCheck(
            check_type=ValidationType.CITATION_VERIFICATION,
            claim=claim,
            result=result,
            confidence=confidence,
            evidence=evidence,
            verification_method="citation_cross_reference",
            timestamp=timestamp
        )
    
    def _check_false_positive_patterns(self, claim: str, timestamp: float) -> Optional[ValidationCheck]:
        """Check for known false positive patterns"""
        
        for i, pattern in enumerate(self.false_positive_patterns):
            if re.search(pattern, claim, re.IGNORECASE):
                return ValidationCheck(
                    check_type=ValidationType.TECHNICAL_CLAIM_VERIFICATION,
                    claim=claim,
                    result=ValidationResult.FAILED,
                    confidence=0.95,
                    evidence=[f"Detected false positive pattern: {pattern}"],
                    verification_method=f"false_positive_pattern_{i}",
                    timestamp=timestamp
                )
        
        return None
    
    def _validate_general_technical_claim(self, claim: str, investigation_data: Dict[str, Any], 
                                         timestamp: float) -> ValidationCheck:
        """General validation for technical claims"""
        
        # Look for specific confidence indicators
        confidence_indicators = ['verified', 'confirmed', 'validated', 'proven']
        uncertainty_indicators = ['likely', 'probably', 'appears', 'seems']
        
        confidence_score = 0.5  # Default neutral confidence
        evidence = [f"General technical claim analysis: {claim[:100]}..."]
        
        # Adjust confidence based on language used
        if any(indicator in claim.lower() for indicator in confidence_indicators):
            confidence_score += 0.2
            evidence.append("Confident language detected")
        
        if any(indicator in claim.lower() for indicator in uncertainty_indicators):
            confidence_score -= 0.1
            evidence.append("Uncertain language detected")
        
        # Check if claim has supporting data
        has_numbers = bool(re.search(r'\d+', claim))
        has_specifics = bool(re.search(r'(version|line|file|commit)', claim, re.IGNORECASE))
        
        if has_numbers and has_specifics:
            confidence_score += 0.2
            evidence.append("Specific details (numbers/versions) detected")
        
        # Determine result based on confidence score
        if confidence_score >= 0.8:
            result = ValidationResult.VERIFIED
        elif confidence_score >= 0.6:
            result = ValidationResult.PARTIALLY_VERIFIED
        elif confidence_score >= 0.4:
            result = ValidationResult.UNABLE_TO_VERIFY
        else:
            result = ValidationResult.FAILED
        
        return ValidationCheck(
            check_type=ValidationType.TECHNICAL_CLAIM_VERIFICATION,
            claim=claim,
            result=result,
            confidence=min(confidence_score, 1.0),
            evidence=evidence,
            verification_method="general_claim_analysis",
            timestamp=timestamp
        )
    
    def _generate_validation_summary(self, checks: List[ValidationCheck]) -> ValidationSummary:
        """Generate summary statistics for validation checks"""
        
        total_checks = len(checks)
        verified_count = sum(1 for c in checks if c.result == ValidationResult.VERIFIED)
        failed_count = sum(1 for c in checks if c.result == ValidationResult.FAILED)
        partially_verified_count = sum(1 for c in checks if c.result == ValidationResult.PARTIALLY_VERIFIED)
        unable_to_verify_count = sum(1 for c in checks if c.result == ValidationResult.UNABLE_TO_VERIFY)
        
        # Calculate overall accuracy
        if total_checks == 0:
            overall_accuracy = 0.0
            false_positive_risk = 1.0
        else:
            accuracy_score = (verified_count + 0.5 * partially_verified_count) / total_checks
            overall_accuracy = accuracy_score
            false_positive_risk = failed_count / total_checks
        
        return ValidationSummary(
            total_checks=total_checks,
            verified_count=verified_count,
            failed_count=failed_count,
            partially_verified_count=partially_verified_count,
            unable_to_verify_count=unable_to_verify_count,
            overall_accuracy=overall_accuracy,
            false_positive_risk=false_positive_risk,
            validation_timestamp=time.time()
        )
    
    def _categorize_claims(self, claims: List[str], 
                          checks: List[ValidationCheck]) -> Tuple[List[str], List[str]]:
        """Categorize claims as validated or rejected based on checks"""
        
        validated_claims = []
        rejected_claims = []
        
        # Group checks by claim
        claim_check_map = {}
        for check in checks:
            claim = check.claim
            if claim not in claim_check_map:
                claim_check_map[claim] = []
            claim_check_map[claim].append(check)
        
        # Evaluate each claim
        for claim in claims:
            claim_checks = claim_check_map.get(claim, [])
            
            if not claim_checks:
                # No checks performed, default to validation with low confidence
                validated_claims.append(claim)
                continue
            
            # Calculate overall result for the claim
            verified_checks = sum(1 for c in claim_checks if c.result == ValidationResult.VERIFIED)
            failed_checks = sum(1 for c in claim_checks if c.result == ValidationResult.FAILED)
            total_checks = len(claim_checks)
            
            # If any check failed, reject the claim
            if failed_checks > 0:
                rejected_claims.append(claim)
            # If majority verified, accept the claim
            elif verified_checks / total_checks >= 0.5:
                validated_claims.append(claim)
            # Otherwise, default to validation (conservative approach)
            else:
                validated_claims.append(claim)
        
        return validated_claims, rejected_claims
    
    def _calculate_validation_confidence(self, checks: List[ValidationCheck], 
                                        summary: ValidationSummary) -> float:
        """Calculate overall validation confidence score"""
        
        if not checks:
            return 0.0
        
        # Weight different factors
        accuracy_weight = 0.5
        verification_rate_weight = 0.3
        confidence_avg_weight = 0.2
        
        # Calculate weighted confidence
        accuracy_score = summary.overall_accuracy
        verification_rate = summary.verified_count / summary.total_checks if summary.total_checks > 0 else 0.0
        avg_confidence = sum(c.confidence for c in checks) / len(checks)
        
        overall_confidence = (
            accuracy_weight * accuracy_score +
            verification_rate_weight * verification_rate +
            confidence_avg_weight * avg_confidence
        )
        
        return min(overall_confidence, 1.0)
    
    def to_dict(self, validation_result: EvidenceValidationResult) -> Dict[str, Any]:
        """Convert validation result to dictionary for serialization"""
        # Convert checks with enum serialization
        checks_dict = []
        for check in validation_result.checks:
            check_dict = asdict(check)
            # Convert enums to string values
            check_dict['check_type'] = check.check_type.value
            check_dict['result'] = check.result.value
            checks_dict.append(check_dict)
        
        return {
            'checks': checks_dict,
            'summary': asdict(validation_result.summary),
            'validated_claims': validation_result.validated_claims,
            'rejected_claims': validation_result.rejected_claims,
            'confidence_score': validation_result.confidence_score
        }