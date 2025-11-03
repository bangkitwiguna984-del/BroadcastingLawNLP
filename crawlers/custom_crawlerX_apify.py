# Libraries

import os
import pandas as pd
from apify_client import ApifyClient
from datetime import datetime

# API dan aktor

APIFY_TOKEN = "API_KEY"
client = ApifyClient(APIFY_TOKEN)

# Searh parameter and time configuration

search_term = "RUU Penyiaran"  # customized with the preferred queries

# Generate a list of start and end dates for each month in the desired range
date_range = pd.date_range(start="2024-05-01", end="2025-05-30", freq='MS')
all_collected_tweets = []

# Scraping

print(f"🚀 Starting tweet collection for the query: '{search_term}'")
print("-" * 30)

for i in range(len(date_range) - 1):
    # This actor requires the date format to be YYYY-MM-DD_HH:MM:SS_UTC
    start_date_utc = date_range[i].strftime('%Y-%m-%d') + "_00:00:00_UTC"
    end_date_utc = date_range[i+1].strftime('%Y-%m-%d') + "_00:00:00_UTC"

    print(
        f"➡️  Fetching tweets from {date_range[i].strftime('%Y-%m-%d')} to {date_range[i+1].strftime('%Y-%m-%d')}...")

    # Prepare the Actor Input (Corrected as per your instruction)
    # We now use the separate fields for content, start date, and end date.
    run_input = {
        "twitterContent": search_term,
        "since": start_date_utc,
        "until": end_date_utc,
        "maxItems": 5000,
        "lang": "in",
        "queryType": "Latest",
    }

    # Run the Actor and Wait for It to Finish
    try:
        # Actor ID: 'CJdippxWmn9uRfooo'
        run = client.actor("CJdippxWmn9uRfooo").call(run_input=run_input)

        # Fetch and Store the Results ---
        print(f"   ✅ Run finished. Fetching results from dataset...")

        monthly_tweets = [item for item in client.dataset(
            run["defaultDatasetId"]).iterate_items()]
        all_collected_tweets.extend(monthly_tweets)

        print(f"   👍 Collected {len(monthly_tweets)} tweets this month.")
        print(f"   Total collected so far: {len(all_collected_tweets)}")
        print("-" * 30)

    except Exception as e:
        print(f"   ❌ An error occurred during the run: {e}")
        print("-" * 30)

    # Final Output and Save to File
    print("\n🎉 Collection complete!")
    print(f"Total number of tweets collected: {len(all_collected_tweets)}")

    if all_collected_tweets:
        df = pd.DataFrame(all_collected_tweets)
        output_filename = "ruu_penyiaran_tweets.csv"
        df.to_csv(output_filename, index=False, encoding='utf-8-sig')
        print(f"💾 Data saved successfully to '{output_filename}'")
