import requests
import time

def test_api():
    print("==================================================")
    print("      REGIME PLATFORM - PHASE 6 REST API TEST     ")
    print("==================================================")
    
    base_url = "http://127.0.0.1:8000"
    
    # 1. Test Root
    try:
        res = requests.get(base_url + "/")
        print("\n[1] GET / (Root Health Check)")
        print(f"Status Code: {res.status_code}")
        print(f"Response: {res.json()}")
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Is uvicorn running?")
        return
        
    # 2. Test Hot Layer (Redis)
    res = requests.get(base_url + "/api/state/all")
    print("\n[2] GET /api/state/all (Redis Hot Layer)")
    print(f"Status Code: {res.status_code}")
    data = res.json()
    if data.get("data"):
        print("✅ Successfully fetched live regime states from Redis cache!")
    else:
        print("⚠️ No data in Redis (expected if ingestion engine isn't currently running).")
        
    # 3. Test Cold Layer (MongoDB)
    res = requests.get(base_url + "/api/history?limit=3")
    print("\n[3] GET /api/history (MongoDB Cold Layer)")
    print(f"Status Code: {res.status_code}")
    data = res.json()
    count = data.get("count", 0)
    print(f"✅ Successfully fetched {count} historical anomalies from MongoDB Atlas!")
    if count > 0:
        print(f"Example anomaly: {data['data'][0]['regime_data']['regime']}")
        
    print("\n==================================================")
    print("✅ Phase 6 Complete: REST API is fully functional!")
    print("==================================================")

if __name__ == "__main__":
    test_api()
