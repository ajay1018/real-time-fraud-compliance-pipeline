from pathlib import Path
import pandas as pd

RAW = Path("data/raw")
PROC = Path("data/processed"); PROC.mkdir(parents=True, exist_ok=True)

df = pd.read_json(RAW / "transactions.json")

# Flags
df["flag_high_value"] = (df["amount"] >= 1000).astype(int)
df["flag_country_risk"] = df["country"].isin(["RU"]).astype(int)
df["flag_channel_anomaly"] = ((df["channel"] == "api") & (df["amount"] > 5000)).astype(int)

# Rapid-fire per account (rolling window proxy)
df["ts"] = pd.to_datetime(df["ts"], utc=True)
df = df.sort_values(["account_id", "ts"])
df["prev_ts"] = df.groupby("account_id")["ts"].shift(1)
df["delta_min"] = (df["ts"] - df["prev_ts"]).dt.total_seconds()/60
df["prev_amount"] = df.groupby("account_id")["amount"].shift(1)
df["flag_rapid_fire"] = ((df["delta_min"] <= 7) & ((df["amount"] + df["prev_amount"].fillna(0)) >= 1500)).astype(int)

# Overall fraud flag
flag_cols = ["flag_high_value","flag_country_risk","flag_channel_anomaly","flag_rapid_fire"]
df["is_flagged"] = (df[flag_cols].sum(axis=1) > 0).astype(int)

# KPIs
kpi_overall = pd.DataFrame({
    "transactions": [len(df)],
    "flagged": [int(df["is_flagged"].sum())],
    "flag_rate": [df["is_flagged"].mean()]
})
kpi_by_country = df.groupby("country", as_index=False)["is_flagged"].mean().rename(columns={"is_flagged":"flag_rate"}).sort_values("flag_rate", ascending=False)
kpi_by_channel = df.groupby("channel", as_index=False)["is_flagged"].mean().rename(columns={"is_flagged":"flag_rate"}).sort_values("flag_rate", ascending=False)

# Write outputs
df.to_csv(PROC / "transactions_enriched.csv", index=False)
kpi_overall.to_csv(PROC / "kpi_overall.csv", index=False)
kpi_by_country.to_csv(PROC / "kpi_by_country.csv", index=False)
kpi_by_channel.to_csv(PROC / "kpi_by_channel.csv", index=False)

print("[transform] wrote:", PROC / "transactions_enriched.csv")
