import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
import pickle
import os
import re

# --------------------------
# Helper: convert total_sqft to number
# --------------------------
def clean_sqft(x):
    try:
        x = str(x).lower().strip()

        # Case 1: Range like "2100 - 2850"
        if "-" in x:
            parts = x.split("-")
            low = float(parts[0])
            high = float(parts[1])
            return (low + high) / 2

        # Case 2: Sq. Meter
        if "meter" in x:
            val = float(re.findall(r"[\d\.]+", x)[0])
            return val * 10.7639  # convert to sq.ft.

        # Case 3: Ground (Tamil Nadu unit)
        if "ground" in x:
            val = float(re.findall(r"[\d\.]+", x)[0])
            return val * 2400  # approx

        # Case 4: Pure number
        return float(re.findall(r"[\d\.]+", x)[0])
    except:
        return np.nan

# --------------------------
# Helper: extract BHK
# --------------------------
def extract_bhk(x):
    try:
        x = str(x).lower()
        nums = re.findall(r'\d+', x)
        return int(nums[0]) if nums else np.nan
    except:
        return np.nan

# --------------------------
# Load & clean data
# --------------------------
df = pd.read_csv("data/bengaluru_house_prices.csv")

df["total_sqft"] = df["total_sqft"].apply(clean_sqft)
df["bhk"] = df["size"].apply(extract_bhk)

# Remove unusable rows
df = df.dropna(subset=["total_sqft", "bhk", "bath", "price"])

# --------------------------
# Features & model
# --------------------------
X = df[["total_sqft", "bath", "bhk", "location"]]
y = df["price"]

pre = ColumnTransformer(
    [("loc", OneHotEncoder(handle_unknown="ignore"), ["location"])],
    remainder="passthrough"
)

model = Pipeline([
    ("prep", pre),
    ("reg", LinearRegression())
])

# Train
model.fit(X, y)

# Save model
os.makedirs("models", exist_ok=True)
with open("models/house_price_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("SUCCESS: Model trained & saved at models/house_price_model.pkl")