#!/usr/bin/env python3
"""
Validation Learning Mixin - Non-Intrusive Integration Interface

This module provides the mixin pattern for adding learning capabilities to existing
validation systems without modifying their core logic.

Key Features:
- Drop-in integration for existing validation systems
- Zero impact on validation logic
- Safe failure handling
- Optional learning enhancement
- Backward compatibility guarantee

Usage Example:
```python
class EnhancedValidationSystem(ExistingValidationSystem, ValidationSystemLearningMixin):
    def enhanced_validation_method(self, *args, **kwargs):
        # Standard validation (unchanged)
        result = super().standard_validation_method(*args, **kwargs)
        
        # Learning integration (non-intrusive)
        self._learn_from_validation_result(result, *args, **kwargs)
        
        # Optional: enhance with insights
        insights = self._get_validation_insights(self._extract_learning_context(*args, **kwargs))
        enhanced_result = self._enhance_validation_with_insights(result, insights)
        
        return enhanced_result
```

Author: AI Systems Suite / Claude Test Generator Framework
Version: 1.0.0
"""

import time
import uuid
import hashlib
from datetime import datetime
from typing import Dict, Optional, List, Any, Union, Callable
from abc import ABC, abstractmethod

from .validation_learning_core import get_learning_core, ValidationEvent, ValidationInsights


class ValidationSystemLearningMixin:
    """
    Mixin for adding learning capabilities to existing validation systems
    
    This mixin provides a standard interface for integrating learning capabilities
    into any validation system while maintaining complete backward compatibility.
    
    Integration Steps:
    1. Inherit from this mixin: class MySystem(ExistingSystem, ValidationSystemLearningMixin)
    2. Call _learn_from_validation_result() after validation operations
    3. Optionally call _get_validation_insights() for enhanced capabilities
    4. Optionally call _enhance_validation_with_insights() to add insights to results
    
    The mixin handles all learning core communication and ensures safe operation.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Get shared learning core instance
        self.learning_core = get_learning_core()
        
        # Learning configuration
        self.learning_enabled = self.learning_core.is_enabled()
        self.learning_event_id_prefix = self.__class__.__name__.lower()
        
        # Performance tracking for learning
        self._learning_stats = {
            'events_submitted': 0,
            'insights_requested': 0,
            'insights_received': 0,
            'learning_errors': 0
        }
    
    def _learn_from_validation_result(self, result: Any, *args, **kwargs) -> None:
        """
        Learn from validation result (non-intrusive)
        
        This method should be called after any validation operation to enable learning.
        It extracts learning data from the validation context and result, then submits
        it to the learning core for processing.
        
        Args:
            result: The validation result to learn from
            *args, **kwargs: Original validation method arguments
        """
        if not self.learning_enabled:
            return
        
        try:
            start_time = time.time()
            
            # Create learning event
            event = self._create_validation_event(result, *args, **kwargs)
            if event:
                # Submit for learning (non-blocking)
                self.learning_core.learn_from_validation(event)
                self._learning_stats['events_submitted'] += 1
            
            # Track performance
            learning_time = (time.time() - start_time) * 1000  # Convert to ms
            if learning_time > 10:  # Log if learning takes more than 10ms
                self._log_learning_performance(f"Learning event creation took {learning_time:.1f}ms")
            
        except Exception as e:
            # Silent failure - learning never impacts validation
            self._handle_learning_error('learn_from_validation_result', e)
    
    def _get_validation_insights(self, context: Dict[str, Any]) -> Optional[ValidationInsights]:
        """
        Get learning insights for validation context
        
        This method requests insights from the learning core based on the current
        validation context. Insights can help predict outcomes or suggest optimizations.
        
        Args:
            context: Validation context dictionary
            
        Returns:
            ValidationInsights if available, None otherwise
        """
        if not self.learning_enabled:
            return None
        
        try:
            self._learning_stats['insights_requested'] += 1
            insights = self.learning_core.get_validation_insights(context)
            
            if insights:
                self._learning_stats['insights_received'] += 1
            
            return insights
            
        except Exception as e:
            self._handle_learning_error('get_validation_insights', e)
            return None
    
    def _enhance_validation_with_insights(self, standard_result: Any, insights: Optional[ValidationInsights]) -> Any:
        """
        Enhance validation result with learning insights
        
        This method adds learning insights to the validation result without modifying
        the core result structure. The enhancement is additive and optional.
        
        Args:
            standard_result: Original validation result
            insights: Learning insights to add (can be None)
            
        Returns:
            Enhanced result with insights added (if available)
        """
        if not insights:
            return standard_result
        
        try:
            # Add insights to result without modifying core structure
            enhanced_result = self._add_insights_to_result(standard_result, insights)
            return enhanced_result
            
        except Exception as e:
            self._handle_learning_error('enhance_validation_with_insights', e)
            # Return original result on any error
            return standard_result
    
    def _create_validation_event(self, result: Any, *args, **kwargs) -> Optional[ValidationEvent]:
        """
        Create validation event from result and arguments
        
        This method extracts learning data from the validation operation and creates
        a ValidationEvent for the learning core. Override this method to customize
        learning data extraction for specific validation systems.
        
        Args:
            result: Validation result
            *args, **kwargs: Original validation method arguments
            
        Returns:
            ValidationEvent if data extraction successful, None otherwise
        """
        try:
            # Generate unique event ID
            event_id = self._generate_event_id()
            
            # Extract learning context
            context = self._extract_learning_context(*args, **kwargs)
            
            # Extract learning result
            learning_result = self._extract_learning_result(result)
            
            # Determine success and confidence
            success = self._is_validation_successful(result)
            confidence = self._extract_confidence(result)
            
            # Extract metadata
            metadata = self._extract_metadata(*args, **kwargs)
            
            return ValidationEvent(
                event_id=event_id,
                event_type=self._get_validation_type(),
                context=context,
                result=learning_result,
                timestamp=datetime.utcnow(),
                source_system=self.__class__.__name__,
                success=success,
                confidence=confidence,
                metadata=metadata
            )
            
        except Exception as e:
            self._handle_learning_error('create_validation_event', e)
            return None
    
    def _generate_event_id(self) -> str:
        """Generate unique event ID"""
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S_%f')
        random_part = str(uuid.uuid4())[:8]
        return f"{self.learning_event_id_prefix}_{timestamp}_{random_part}"
    
    def _extract_learning_context(self, *args, **kwargs) -> Dict[str, Any]:
        """
        Extract learning context from validation arguments
        
        Override this method to customize context extraction for specific validation systems.
        The context should contain information that helps identify similar validations.
        """
        context = {
            'validation_type': self._get_validation_type(),
            'source_system': self.__class__.__name__,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        # Add argument information (safely)
        try:
            if args:
                context['args_count'] = len(args)
                context['args_types'] = [type(arg).__name__ for arg in args[:3]]  # First 3 args only
            
            if kwargs:
                context['kwargs_keys'] = list(kwargs.keys())
                # Add some safe kwargs values
                for key, value in kwargs.items():
                    if isinstance(value, (str, int, float, bool)) and len(str(value)) < 100:
                        context[f'kwargs_{key}'] = value
                        
        except Exception:
            # Continue with basic context if argument extraction fails
            pass
        
        return context
    
    def _extract_learning_result(self, result: Any) -> Dict[str, Any]:
        """
        Extract learning result from validation result
        
        Override this method to customize result extraction for specific validation systems.
        """
        learning_result = {
            'result_type': type(result).__name__,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        try:
            # Extract result information safely
            if hasattr(result, '__dict__'):
                # Object with attributes
                attrs = {k: v for k, v in result.__dict__.items() 
                        if not k.startswith('_') and isinstance(v, (str, int, float, bool, list, dict))}
                learning_result['attributes'] = attrs
                
            elif isinstance(result, dict):
                # Dictionary result
                safe_dict = {k: v for k, v in result.items() 
                           if isinstance(v, (str, int, float, bool, list, dict)) and len(str(v)) < 1000}
                learning_result['dict_data'] = safe_dict
                
            elif isinstance(result, (list, tuple)):
                # List/tuple result
                learning_result['collection_length'] = len(result)
                learning_result['collection_types'] = [type(item).__name__ for item in result[:5]]
                
            elif isinstance(result, (str, int, float, bool)):
                # Simple result
                learning_result['simple_value'] = result
                
        except Exception:
            # Continue with basic result if extraction fails
            pass
        
        return learning_result
    
    def _is_validation_successful(self, result: Any) -> bool:
        """
        Determine if validation was successful
        
        Override this method to customize success determination for specific validation systems.
        """
        try:
            # Check common success indicators
            if hasattr(result, 'success'):
                return bool(result.success)
            
            if hasattr(result, 'is_valid'):
                return bool(result.is_valid)
            
            if hasattr(result, 'passed'):
                return bool(result.passed)
            
            if isinstance(result, dict):
                if 'success' in result:
                    return bool(result['success'])
                if 'valid' in result:
                    return bool(result['valid'])
                if 'passed' in result:
                    return bool(result['passed'])
                if 'errors' in result:
                    return len(result['errors']) == 0
            
            if isinstance(result, bool):
                return result
            
            # Default: assume successful if no errors occurred
            return True
            
        except Exception:
            # Default to successful if we can't determine
            return True
    
    def _extract_confidence(self, result: Any) -> float:
        """
        Extract confidence level from validation result
        
        Override this method to customize confidence extraction for specific validation systems.
        """
        try:
            # Check common confidence indicators
            if hasattr(result, 'confidence'):
                return float(result.confidence)
            
            if hasattr(result, 'score'):
                return float(result.score)
            
            if isinstance(result, dict):
                if 'confidence' in result:
                    return float(result['confidence'])
                if 'score' in result:
                    return float(result['score'])
                if 'quality' in result:
                    return float(result['quality'])
            
            # Default confidence based on success
            return 0.8 if self._is_validation_successful(result) else 0.2
            
        except Exception:
            # Default confidence
            return 0.5
    
    def _extract_metadata(self, *args, **kwargs) -> Dict[str, Any]:
        """
        Extract metadata from validation arguments
        
        Override this method to add system-specific metadata for learning.
        """
        metadata = {
            'method_name': self._get_validation_type(),
            'args_provided': len(args) > 0,
            'kwargs_provided': len(kwargs) > 0,
            'extraction_timestamp': datetime.utcnow().isoformat()
        }
        
        try:
            # Add some method-specific metadata
            if hasattr(self, '_get_validation_metadata'):
                custom_metadata = self._get_validation_metadata(*args, **kwargs)
                if isinstance(custom_metadata, dict):
                    metadata.update(custom_metadata)
                    
        except Exception:
            # Continue with basic metadata if custom extraction fails
            pass
        
        return metadata
    
    def _get_validation_type(self) -> str:
        """
        Get validation type identifier
        
        Override this method to provide a specific validation type for learning categorization.
        """
        # Use class name as default validation type
        return self.__class__.__name__.replace('Validation', '').replace('Engine', '').lower()
    
    def _add_insights_to_result(self, result: Any, insights: ValidationInsights) -> Any:
        """
        Add insights to validation result
        
        This method adds learning insights to the result in a non-intrusive way.
        Override this method to customize how insights are added for specific result types.
        """
        try:
            # Handle different result types
            if hasattr(result, '__dict__'):
                # Object with attributes - add insights as new attribute
                setattr(result, 'learning_insights', insights)
                return result
                
            elif isinstance(result, dict):
                # Dictionary - add insights as new key
                enhanced_result = result.copy()
                enhanced_result['learning_insights'] = insights.to_dict()
                return enhanced_result
                
            elif isinstance(result, tuple):
                # Tuple - return new tuple with insights
                return (*result, insights)
                
            elif isinstance(result, list):
                # List - return new list with insights appended
                enhanced_result = result.copy()
                enhanced_result.append({'learning_insights': insights.to_dict()})
                return enhanced_result
                
            else:
                # Other types - return tuple with original result and insights
                return (result, insights)
                
        except Exception:
            # Return original result if enhancement fails
            return result
    
    def _handle_learning_error(self, operation: str, error: Exception) -> None:
        """Handle learning errors safely"""
        try:
            self._learning_stats['learning_errors'] += 1
            
            # Log error at debug level to avoid spam
            if hasattr(self, 'logger'):
                self.logger.debug(f"Learning error in {operation}: {str(error)}")
            
        except Exception:
            # Even error handling should not fail
            pass
    
    def _log_learning_performance(self, message: str) -> None:
        """Log learning performance information"""
        try:
            if hasattr(self, 'logger'):
                self.logger.debug(f"Learning performance: {message}")
        except Exception:
            pass
    
    def get_learning_statistics(self) -> Dict[str, Any]:
        """Get learning integration statistics"""
        try:
            base_stats = self._learning_stats.copy()
            base_stats['learning_enabled'] = self.learning_enabled
            base_stats['learning_core_health'] = self.learning_core.get_health_status()
            return base_stats
        except Exception:
            return {'error': 'Statistics unavailable'}


class ValidationSystemLearningInterface(ABC):
    """
    Abstract interface for validation systems that want standardized learning integration
    
    Implementing this interface ensures consistent learning behavior across different
    validation systems while allowing customization of learning data extraction.
    """
    
    @abstractmethod
    def _get_validation_metadata(self, *args, **kwargs) -> Dict[str, Any]:
        """Extract system-specific metadata for learning"""
        pass
    
    @abstractmethod  
    def _get_validation_context_signature(self, *args, **kwargs) -> str:
        """Generate context signature for pattern matching"""
        pass
    
    @abstractmethod
    def _should_learn_from_result(self, result: Any) -> bool:
        """Determine if this result should be used for learning"""
        pass


# Convenience functions for direct integration without inheritance

def learn_from_validation(validation_system_name: str, 
                         validation_type: str,
                         context: Dict[str, Any], 
                         result: Any, 
                         success: bool = True, 
                         confidence: float = 0.8,
                         metadata: Optional[Dict[str, Any]] = None) -> None:
    """
    Learn from validation without using the mixin pattern
    
    This function allows direct integration with the learning system for cases
    where the mixin pattern is not suitable.
    
    Args:
        validation_system_name: Name of the validation system
        validation_type: Type of validation performed
        context: Validation context dictionary
        result: Validation result
        success: Whether validation was successful
        confidence: Confidence level (0.0 to 1.0)
        metadata: Optional metadata dictionary
    """
    try:
        learning_core = get_learning_core()
        if not learning_core.is_enabled():
            return
        
        event = ValidationEvent(
            event_id=f"direct_{validation_system_name}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S_%f')}",
            event_type=validation_type,
            context=context,
            result={'result_data': result} if not isinstance(result, dict) else result,
            timestamp=datetime.utcnow(),
            source_system=validation_system_name,
            success=success,
            confidence=confidence,
            metadata=metadata or {}
        )
        
        learning_core.learn_from_validation(event)
        
    except Exception:
        # Silent failure - learning never impacts validation
        pass


def get_validation_insights(validation_type: str, context: Dict[str, Any]) -> Optional[ValidationInsights]:
    """
    Get validation insights without using the mixin pattern
    
    Args:
        validation_type: Type of validation
        context: Validation context dictionary
        
    Returns:
        ValidationInsights if available, None otherwise
    """
    try:
        learning_core = get_learning_core()
        if not learning_core.is_enabled():
            return None
        
        enhanced_context = context.copy()
        enhanced_context['validation_type'] = validation_type
        
        return learning_core.get_validation_insights(enhanced_context)
        
    except Exception:
        return None


# Decorator for automatic learning integration

def with_learning(validation_type: str = None, 
                 learn_on_success: bool = True,
                 learn_on_failure: bool = True):
    """
    Decorator for automatic learning integration
    
    This decorator can be applied to validation methods to automatically
    integrate learning without modifying the method code.
    
    Args:
        validation_type: Type of validation (defaults to method name)
        learn_on_success: Whether to learn from successful validations
        learn_on_failure: Whether to learn from failed validations
    
    Example:
    ```python
    class MyValidationSystem:
        @with_learning(validation_type='evidence_validation')
        def validate_evidence(self, evidence_data):
            # Original validation logic
            result = self._perform_validation(evidence_data)
            return result
    ```
    """
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            # Execute original method
            result = func(self, *args, **kwargs)
            
            try:
                # Determine validation success
                success = True
                if hasattr(result, 'success'):
                    success = result.success
                elif isinstance(result, dict) and 'success' in result:
                    success = result['success']
                elif isinstance(result, bool):
                    success = result
                
                # Check if we should learn from this result
                should_learn = (success and learn_on_success) or (not success and learn_on_failure)
                
                if should_learn:
                    # Extract learning data
                    val_type = validation_type or func.__name__
                    context = {
                        'validation_type': val_type,
                        'method_name': func.__name__,
                        'class_name': self.__class__.__name__,
                        'args_count': len(args),
                        'kwargs_keys': list(kwargs.keys())
                    }
                    
                    # Add safe argument data
                    for i, arg in enumerate(args[:3]):  # First 3 args
                        if isinstance(arg, (str, int, float, bool)) and len(str(arg)) < 100:
                            context[f'arg_{i}'] = arg
                    
                    confidence = 0.8 if success else 0.2
                    if hasattr(result, 'confidence'):
                        confidence = result.confidence
                    elif isinstance(result, dict) and 'confidence' in result:
                        confidence = result['confidence']
                    
                    # Submit for learning
                    learn_from_validation(
                        validation_system_name=self.__class__.__name__,
                        validation_type=val_type,
                        context=context,
                        result=result,
                        success=success,
                        confidence=confidence
                    )
                
            except Exception:
                # Silent failure - learning never impacts validation
                pass
            
            return result
            
        wrapper.__name__ = func.__name__
        wrapper.__doc__ = func.__doc__
        return wrapper
    return decorator