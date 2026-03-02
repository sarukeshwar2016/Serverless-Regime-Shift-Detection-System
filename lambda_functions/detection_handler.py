"""
AWS Lambda handler for the detection engine.
Wraps the detection engine for serverless invocation.
"""

import json
from detection.engine import DetectionEngine


engine = DetectionEngine()


def handler(event, context):
    """Lambda entry point — receives a price window and returns breakpoints."""
    body = json.loads(event.get("body", "{}"))
    prices = body.get("prices", [])

    if not prices:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "No prices provided"}),
        }

    result = engine.detect_offline(prices)
    return {
        "statusCode": 200,
        "body": json.dumps(result),
    }
