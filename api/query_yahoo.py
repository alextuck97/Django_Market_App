import yfinance as yf

def get_ticker_history(ticker, period="1d", interval="1d"):
    '''
    Scrape the requested data
    '''
    t = yf.Ticker(ticker)
    h = t.history(period=period, interval=interval)
    h = h.fillna("NaN")
    if period == "1d" and interval == "1d":
        data = h.iloc[0].to_dict()
        datetime = str(h.iloc[0].name)
        date, time = datetime.split(" ")
        data["date"] = date
        data["time"] = time
        data = [data]
    else:
        data = []
        for name, row in h.iterrows():
            entry = row.to_dict()
            date, time = str(name).split(" ")
            entry["date"] = date
            entry["time"] = time
            data.append(entry)
    
    return data


