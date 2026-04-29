# fraud_detector.py
import random
import pandas as pd

def fraud_score(row):
    """
    Lightweight fraud scoring for demo.
    Generates variety: VERIFIED / SUSPICIOUS / FRAUD
    """

    issues = 0

    # 1️⃣ Missing basic details → suspicious
    risky_columns = ["total_sqft", "bath", "size", "price", "location"]
    for col in risky_columns:
        if col not in row or pd.isna(row[col]):
            issues += 1

    # 2️⃣ Price anomaly (simple logic)
    try:
        sqft = float(row.get("total_sqft", 0))
        price = float(row.get("price", 0))

        if sqft > 0:
            price_per_sqft = price / sqft

            if price_per_sqft < 50:     # too cheap
                issues += 1
            elif price_per_sqft > 400:  # too expensive
                issues += 1
    except:
        pass

    # 3️⃣ Small randomness for realistic demo
    randomness = random.randint(0, 10)
    if randomness > 7:
        issues += 1  # ~30% chance to add suspicion

    # 4️⃣ Assign label
    if issues == 0:
        return "VERIFIED"
    elif issues == 1:
        return "SUSPICIOUS"
    else:
        return "FRAUD"