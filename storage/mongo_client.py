import os
import time
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

load_dotenv()

class MongoStorageClient:
    """
    Handles permanent cloud storage for the Regime Platform using MongoDB Atlas.
    Replaces the AWS DynamoDB phase to ensure a 100% free serverless architecture.
    """
    def __init__(self):
        self.uri = os.getenv("MONGO_URI")
        if not self.uri or "<db_password>" in self.uri:
            print("⚠️ MongoDB URI missing or <db_password> not replaced in .env")
            self.client = None
            return
            
        try:
            # Create a new client and connect to the server
            self.client = MongoClient(self.uri, server_api=ServerApi('1'), serverSelectionTimeoutMS=5000)
            # Send a ping to confirm a successful connection
            self.client.admin.command('ping')
            self.db = self.client["regime_platform"]
            self.collection = self.db["anomaly_logs"]
            print("✅ Successfully connected to MongoDB Atlas Cloud Database!")
        except Exception as e:
            print(f"⚠️ MongoDB connection failed: {e}")
            self.client = None

    def log_anomaly(self, source: str, asset: str, anomaly_data: dict) -> bool:
        """
        Saves a permanently confirmed anomaly/regime to the cloud Database.
        Unlike Redis (which only stores the latest 1 record per asset), 
        MongoDB acts as our historical ledger for the dashboard history table.
        """
        if not self.client:
            return False
            
        try:
            document = {
                "source": source,
                "asset": asset,
                "regime_data": anomaly_data,
                "timestamp": anomaly_data.get("updated_at", time.time())
            }
            self.collection.insert_one(document)
            return True
        except Exception as e:
            print(f"MongoDB save error: {e}")
            return False
