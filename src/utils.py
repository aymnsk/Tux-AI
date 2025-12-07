"""
Utility functions for MLOps showcase
"""

import json
import time
from datetime import datetime
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class MetricsCollector:
    """Collect metrics for MLOps showcase"""
    
    def __init__(self):
        self.metrics = {
            "api_calls": 0,
            "tokens_processed": 0,
            "response_times": [],
            "fallback_activations": 0,
            "errors": 0
        }
    
    def record_api_call(self, tokens: int, response_time: float):
        """Record API call metrics"""
        self.metrics["api_calls"] += 1
        self.metrics["tokens_processed"] += tokens
        self.metrics["response_times"].append(response_time)
    
    def record_fallback(self):
        """Record fallback activation"""
        self.metrics["fallback_activations"] += 1
    
    def record_error(self):
        """Record error"""
        self.metrics["errors"] += 1
    
    def get_summary(self) -> Dict[str, Any]:
        """Get metrics summary"""
        return {
            "total_api_calls": self.metrics["api_calls"],
            "total_tokens": self.metrics["tokens_processed"],
            "avg_response_time": sum(self.metrics["response_times"]) / len(self.metrics["response_times"]) if self.metrics["response_times"] else 0,
            "fallback_rate": self.metrics["fallback_activations"] / self.metrics["api_calls"] if self.metrics["api_calls"] > 0 else 0,
            "error_rate": self.metrics["errors"] / self.metrics["api_calls"] if self.metrics["api_calls"] > 0 else 0,
            "timestamp": datetime.now().isoformat()
        }

class ConversationExporter:
    """Export conversations for analysis"""
    
    @staticmethod
    def export_to_json(conversation_history: list, filename: str):
        """Export conversation to JSON"""
        data = {
            "exported_at": datetime.now().isoformat(),
            "total_messages": len(conversation_history),
            "conversation": conversation_history
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        logger.info(f"Conversation exported to {filename}")
    
    @staticmethod
    def generate_report(conversation_history: list) -> dict:
        """Generate conversation analysis report"""
        user_messages = [msg for msg in conversation_history if msg["role"] == "user"]
        assistant_messages = [msg for msg in conversation_history if msg["role"] == "assistant"]
        
        return {
            "analysis_date": datetime.now().isoformat(),
            "total_interactions": len(conversation_history),
            "user_messages": len(user_messages),
            "assistant_messages": len(assistant_messages),
            "topics_covered": ConversationExporter._extract_topics(conversation_history)
        }
    
    @staticmethod
    def _extract_topics(conversation_history: list) -> list:
        """Extract main topics from conversation"""
        topics = []
        mlops_keywords = ["docker", "kubernetes", "deployment", "model", "mlops", "ci/cd", "rust", "c++", "architecture"]
        
        for msg in conversation_history:
            content = msg["content"].lower()
            found_topics = [topic for topic in mlops_keywords if topic in content]
            topics.extend(found_topics)
        
        return list(set(topics))