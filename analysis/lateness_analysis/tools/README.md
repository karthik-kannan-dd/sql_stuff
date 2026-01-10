# Lateness Analysis Tools

Streamlit apps for analyzing dasher lateness patterns.

![Screenshot](screenshot.png)

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Tools

### 1. Dasher Lateness Lookup

Look up lateness patterns for individual dashers.

```bash
streamlit run app.py
```

**Features:**
- Summary stats (total deliveries, median lateness, tier classification)
- Pattern detection (pickup-heavy, dropoff-heavy, mixed)
- Distribution histogram and scatter plots
- Time series of daily average lateness
- Delivery detail table with CSV export

### 2. Delivery Store Wait Analysis

Compare a delivery's store wait time against other dashers at the same store.

```bash
streamlit run delivery_analysis_app.py
```

**Features:**
- Delivery details (store, wait time, lateness)
- Comparison against dashers who arrived 10/30/60 min before
- Gap interpretation (supports/refutes "slow store" claims)
- Wait time distribution histogram
- Store historical statistics
