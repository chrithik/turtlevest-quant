import time
from datetime import datetime, timedelta
from generate_reports import run_ingestion

print("⏰ Background Ingestion Scheduler is active.")
print("The scheduler will trigger run_ingestion() once every 7 days (weekly).")

# Initial run delay (to allow databases/networks to boot up completely in Docker)
print("⏳ Initial startup delay: waiting 30 seconds before starting schedule loop...")
time.sleep(30)

while True:
    now = datetime.now()
    # Calculate target time: midnight (00:00) of the next week (e.g. 7 days from now)
    target = now.replace(hour=0, minute=0, second=0, microsecond=0)
    if target <= now:
        target += timedelta(days=7)
        
    wait_seconds = (target - now).total_seconds()
    print(f"Next ingestion scheduled at: {target.strftime('%Y-%m-%d %H:%M:%S')} (waiting {round(wait_seconds/3600, 2)} hours)...")
    
    # Sleep until target time
    time.sleep(wait_seconds)
    
    # Trigger ingestion
    try:
        run_ingestion()
    except Exception as e:
        print(f"❌ Error occurred during scheduled ingestion: {str(e)}")
