import sys
import os
import time
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Fallback basket of core companies to pre-cache if API discovery fails
FALLBACK_BASKET = [
    "MSFT", "AAPL", "NVDA", "AVGO", "GOOGL", 
    "META", "AMZN", "TSLA", "JPM", "LLY", 
    "UNH", "ABBV", "XOM", "GE", "COST", 
    "WMT", "HD", "MA", "V", "NFLX"
]

def get_daily_target_tickers():
    api_key = os.environ.get("FMP_API_KEY")
    
    if not api_key or api_key == "YOUR_KEY":
        print("⚠️ No valid FMP_API_KEY found in environment variables. Using default core basket.")
        return FALLBACK_BASKET[:10]
        
    try:
        # Query FMP API to find the most active stocks of the day
        print("🔍 Querying FMP API to discover the top 10 most active stocks today...")
        url = f"https://financialmodelingprep.com/stable/most-active?apikey={api_key}"
        res = requests.get(url, timeout=5)
        
        if res.ok:
            data = res.json()
            discovered = []
            for item in data:
                symbol = item.get("symbol", "").upper().strip()
                # Keep only clean equity ticker symbols (e.g. no dots, no indices, standard lengths)
                if symbol.isalpha() and len(symbol) <= 4:
                    discovered.append(symbol)
                    
            if len(discovered) >= 10:
                target_list = discovered[:10]
                print(f"📈 Discovered 10 most active stocks dynamically: {', '.join(target_list)}")
                return target_list
            else:
                print(f"⚠️ Only found {len(discovered)} active symbols. Falling back to core basket.")
        else:
            print(f"⚠️ FMP API returned error {res.status_code}. Falling back to core basket.")
    except Exception as e:
        print(f"⚠️ Error occurred during ticker discovery: {str(e)}. Falling back to core basket.")
        
    return FALLBACK_BASKET[:10]

def run_ingestion():
    print("🚀 Starting TurtleVest Quant Dynamic Overnight Ingestion Script...")
    
    # 1. Identify daily tickers
    target_tickers = get_daily_target_tickers()
    
    # 2. Check if local Node.js scraper API is online
    api_base = os.environ.get("SCRAPER_API_URL", "")
    try:
        if api_base:
            res = requests.get(api_base, timeout=5)
            print("✅ Node.js backend parser is online.")
        else:
            print("⚠️ Warning: SCRAPER_API_URL environment variable is not set.")
    except Exception:
        print("⚠️ Warning: Could not verify root Node.js server. Attempting connections anyway...")
        
    ollama_url = os.environ.get("OLLAMA_URL", "")
    for index, ticker in enumerate(target_tickers, 1):
        print(f"\n[{index}/{len(target_tickers)}] Processing ticker: {ticker}...")
        
        # Trigger SEC Filing Insight (Postgres Cache populates on Node server side)
        try:
            print(f"  👉 Triggering SEC Filing Scrape & Ollama NLP analysis for {ticker}...")
            payload = {"ticker": ticker, "force": True, "ollamaUrl": ollama_url, "model": "qwen-32k"}
            res_insights = requests.post(f"{api_base}/api/sec/insights", json=payload, timeout=120)
            
            if res_insights.ok:
                print(f"  ✅ Successfully processed and cached SEC filing insights for {ticker}.")
            else:
                print(f"  ❌ Backend returned error {res_insights.status_code} for {ticker} insights.")
        except Exception as e:
            print(f"  ❌ Connection failure during SEC insights parsing for {ticker}: {str(e)}")
            
        # Trigger SEC Form 4 Insider Trades Sync
        try:
            print(f"  👉 Triggering Form 4 Insider Trade Scrape for {ticker}...")
            res_insider = requests.get(f"{api_base}/api/sec/insider/{ticker}", timeout=60)
            
            if res_insider.ok:
                print(f"  ✅ Successfully synced and cached insider transactions for {ticker}.")
            else:
                print(f"  ❌ Backend returned error {res_insider.status_code} for {ticker} insider trades.")
        except Exception as e:
            print(f"  ❌ Connection failure during insider trade sync for {ticker}: {str(e)}")
            
        # Add a delay between companies to protect local hardware and comply with SEC rate limit guidelines
        print("  ⏳ Resting for 5 seconds...")
        time.sleep(5)
        
    print("\n🏁 Daily ingestion successfully completed!")

if __name__ == "__main__":
    run_ingestion()
