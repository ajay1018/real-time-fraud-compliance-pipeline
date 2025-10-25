# Rules (demo)
- High value threshold: amount >= 1000 → flag_high_value
- Sanctioned / risky countries: {"RU"} → flag_country_risk
- Rapid-fire (same account >= 2 txns within 7 minutes totaling >= 1500) → flag_rapid_fire
- Channel anomaly (api over 5000) → flag_channel_anomaly
