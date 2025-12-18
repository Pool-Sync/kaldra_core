"""
Protobuf adapters for KALDRA Explainability (v3.4 Phase 3).

Converts between Explanation objects and Protobuf messages.

Note: This module provides adapters without requiring protoc-generated stubs.
For production use with actual protobuf serialization, generate stubs via:
    protoc --python_out=src/explainability/proto -I proto proto/explainability/explanation.proto
"""
from typing import Dict, Any
import json
import logging

logger = logging.getLogger(__name__)


# Mock proto classes for testing without protoc
class MockProtoMessage:
    """Base mock for protobuf messages."""
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
    
    def SerializeToString(self) -> bytes:
        return json.dumps(self.__dict__).encode('utf-8')
    
    @classmethod
    def FromString(cls, data: bytes):
        obj_dict = json.loads(data.decode('utf-8'))
        return cls(**obj_dict)


class ComponentConfidenceProto(MockProtoMessage):
    """Mock ComponentConfidence protobuf message."""
    pass


class DecisionStepProto(MockProtoMessage):
    """Mock DecisionStep protobuf message."""
    pass


class ExplanationConfidenceProto(MockProtoMessage):
    """Mock ExplanationConfidence protobuf message."""
    pass


class ExplanationProto(MockProtoMessage):
    """Mock Explanation protobuf message."""
    pass


def explanation_to_proto(explanation: Any) -> ExplanationProto:
    """
    Convert Explanation to Protobuf message.
    
    Args:
        explanation: Explanation instance
    
    Returns:
        ExplanationProto message
    """
    # Convert details and raw_facts to string maps
    details_map = {k: json.dumps(v) if not isinstance(v, str) else v
                   for k, v in explanation.details.items()}
    raw_facts_map = {k: json.dumps(v) if not isinstance(v, str) else v
                     for k, v in explanation.raw_facts.items()}
    
    proto_msg = ExplanationProto(
        summary=explanation.summary,
        details=details_map,
        raw_facts=raw_facts_map
    )
    
    # Add confidence if present
    if explanation.confidence:
        conf = explanation.confidence
        
        # Convert components
        components = []
        for comp in conf.components:
            comp_proto = ComponentConfidenceProto(
                name=comp.name,
                score=comp.score,
                reason=comp.reason,
                metadata={k: str(v) for k, v in comp.metadata.items()}
            )
            components.append(comp_proto)
        
        # Convert trace
        trace = []
        for step in conf.trace:
            step_proto = DecisionStepProto(
                step=step.step,
                description=step.description,
                weight=step.weight,
                source=step.source,
                metadata={k: str(v) for k, v in step.metadata.items()}
            )
            trace.append(step_proto)
        
        # Create confidence proto
        conf_proto = ExplanationConfidenceProto(
            overall=conf.overall,
            components=components,
            trace=trace,
            metadata={k: str(v) for k, v in conf.metadata.items()}
        )
        
        proto_msg.confidence = conf_proto
    
    return proto_msg


def explanation_from_proto(proto_msg: ExplanationProto) -> Dict[str, Any]:
    """
    Convert Protobuf message to Explanation-compatible dict.
    
    Args:
        proto_msg: ExplanationProto message
    
    Returns:
        Dictionary compatible with Explanation constructor
    """
    # Parse details and raw_facts
    details = {}
    for k, v in proto_msg.details.items():
        try:
            details[k] = json.loads(v)
        except:
            details[k] = v
    
    raw_facts = {}
    for k, v in proto_msg.raw_facts.items():
        try:
            raw_facts[k] = json.loads(v)
        except:
            raw_facts[k] = v
    
    result = {
        "summary": proto_msg.summary,
        "details": details,
        "raw_facts": raw_facts
    }
    
    # Parse confidence if present
    if hasattr(proto_msg, 'confidence') and proto_msg.confidence:
        conf = proto_msg.confidence
        
        result["confidence"] = {
            "overall": conf.overall,
            "components": [
                {
                    "name": comp.name,
                    "score": comp.score,
                    "reason": comp.reason,
                    "metadata": dict(comp.metadata)
                }
                for comp in conf.components
            ],
            "trace": [
                {
                    "step": step.step,
                    "description": step.description,
                    "weight": step.weight,
                    "source": step.source,
                    "metadata": dict(step.metadata)
                }
                for step in conf.trace
            ],
            "metadata": dict(conf.metadata)
        }
    
    return result
