from pathlib import Path
from urllib.request import urlopen

URL = "https://raw.githubusercontent.com/hsmanik/Student_performance_factors/main/StudentPerformanceFactors.csv"
DEST = Path("data/StudentPerformanceFactors.csv")

DEST.parent.mkdir(parents=True, exist_ok=True)

if DEST.exists() and DEST.stat().st_size > 1000:
    print(f"Dataset already exists: {DEST}")
else:
    print("Downloading Student Performance Factors dataset...")
    with urlopen(URL, timeout=30) as response:
        DEST.write_bytes(response.read())
    print(f"Saved dataset to {DEST} ({DEST.stat().st_size:,} bytes)")
