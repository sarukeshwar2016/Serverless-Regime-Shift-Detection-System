import csv
import random
import os

def generate_black_friday():
    """Generates a CSV of typical payment volumes with a massive Black Friday spike."""
    path = os.path.join(os.path.dirname(__file__), 'datasets', 'stripe_black_friday.csv')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    
    with open(path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['timestamp', 'amount', 'currency'])
        
        # 300 normal $10-$50 payments
        for i in range(300):
            writer.writerow([1700000000 + (i*10), random.uniform(10.0, 50.0), 'usd'])
            
        # 100 massive $500-$2000 payments (Black Friday rush)
        for i in range(300, 400):
            writer.writerow([1700000000 + (i*10), random.uniform(500.0, 2000.0), 'usd'])
            
        # 100 normal payments returning
        for i in range(400, 500):
            writer.writerow([1700000000 + (i*10), random.uniform(10.0, 50.0), 'usd'])
            
    print(f"Generated {path}")

def generate_fraud_wave():
    """Generates a CSV of normal payments interrupted by a wave of identical small fraudulent charges."""
    path = os.path.join(os.path.dirname(__file__), 'datasets', 'stripe_fraud_wave.csv')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    
    with open(path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['timestamp', 'amount', 'currency'])
        
        # 300 normal random payments
        for i in range(300):
            writer.writerow([1700000000 + (i*10), random.uniform(15.0, 150.0), 'usd'])
            
        # 100 identical $1.99 charges quickly (Fraud bot testing stolen cards)
        for i in range(300, 400):
            writer.writerow([1700000000 + (i*1), 1.99, 'usd'])
            
        # 100 normal payments returning
        for i in range(400, 500):
            writer.writerow([1700000000 + (i*10), random.uniform(15.0, 150.0), 'usd'])
            
    print(f"Generated {path}")


if __name__ == "__main__":
    generate_black_friday()
    generate_fraud_wave()
