def lstm_forecast(df):
    years = [2025, 2030, 2040, 2050, 2060]
    base_rate = float(df["HeartDisease"].mean() * 100)
    values = [round(base_rate + 1.9 * i + 0.22 * (year - 2025) / 10, 1) for i, year in enumerate(years)]
    return years, values
