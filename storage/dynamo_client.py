"""
DynamoDB client — stores and retrieves regime-shift results in AWS DynamoDB.
"""

import os
from typing import Any, Dict, List, Optional

import boto3
from dotenv import load_dotenv

load_dotenv()


class DynamoClient:
    """Thin wrapper around AWS DynamoDB for regime-shift data."""

    def __init__(self, table_name: str = "regime_shifts"):
        self.table_name = table_name
        self._dynamodb = boto3.resource(
            "dynamodb",
            region_name=os.getenv("AWS_REGION", "us-east-1"),
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        )
        self._table = self._dynamodb.Table(table_name)

    def save_result(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """Save a detection result to DynamoDB."""
        response = self._table.put_item(Item=item)
        return response

    def get_results(self, source: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Query recent results for a data source."""
        response = self._table.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key("source").eq(source),
            Limit=limit,
            ScanIndexForward=False,
        )
        return response.get("Items", [])

    def get_all(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Scan the entire table (use sparingly)."""
        response = self._table.scan(Limit=limit)
        return response.get("Items", [])
