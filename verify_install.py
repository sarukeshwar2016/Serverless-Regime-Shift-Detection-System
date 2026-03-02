"""
Verification script - imports every required library and prints OK or FAILED.
Run: python verify_install.py
"""

libraries = [
    ("boto3", "boto3"),
    ("redis", "redis"),
    ("river", "river"),
    ("ruptures", "ruptures"),
    ("websocket-client", "websocket"),
    ("python-dotenv", "dotenv"),
    ("fastapi", "fastapi"),
    ("uvicorn", "uvicorn"),
    ("pandas", "pandas"),
    ("numpy", "numpy"),
    ("mangum", "mangum"),
    ("yfinance", "yfinance"),
    ("stripe", "stripe"),
    ("requests", "requests"),
    ("threading (built-in)", "threading"),
]

print("=" * 50)
print("  Library Verification")
print("=" * 50)

all_ok = True
results = []
for name, module in libraries:
    try:
        __import__(module)
        status = "OK"
        results.append((name, "OK"))
        print(f"  [OK]     {name}")
    except ImportError as e:
        status = f"FAILED - {e}"
        results.append((name, "FAILED"))
        print(f"  [FAILED] {name} - {e}")
        all_ok = False

print("=" * 50)
if all_ok:
    print("  ALL LIBRARIES INSTALLED SUCCESSFULLY!")
else:
    print("  SOME LIBRARIES FAILED. See above.")
print("=" * 50)
