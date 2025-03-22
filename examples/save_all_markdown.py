import os
import datetime
import pytz
import json
from pathlib import Path
from dotenv import load_dotenv
from _client import get_lifelogs

"""
Limitless API - Export All Lifelogs to Markdown Files

This script exports all lifelogs from the Limitless API to individual markdown files.
Each file is named based on the lifelog's start time in America/Chicago timezone.
Files are saved in an 'export' directory with format: YYYY-MM-DD-HH-MM-SS.md

Usage:
    python export_markdown.py

Requirements:
    - LIMITLESS_API_KEY in .env file
    - Required packages in requirements.txt
"""

# Load environment variables from .env file
load_dotenv()

def export_data(lifelogs):
    """
    Export each lifelog to a separate markdown file in the export directory.
    Files are named based on the lifelog's start time in America/Chicago timezone.
    
    Args:
        lifelogs (list): List of lifelog objects from the Limitless API
    """
    # Create export directory if it doesn't exist
    export_dir = Path("export")
    export_dir.mkdir(exist_ok=True)
    
    print(f"Exporting {len(lifelogs)} lifelogs to {export_dir} directory...")
    
    # Debug: Print the structure of the first lifelog
    if lifelogs:
        print("First lifelog keys:", list(lifelogs[0].keys()))
        
        # Print the first few lifelogs to see their structure
        for i, lifelog in enumerate(lifelogs[:3], 1):
            print(f"\nLifelog {i} structure:")
            print(json.dumps(lifelog, indent=2))
    
    # Loop through all lifelogs and export them
    for i, lifelog in enumerate(lifelogs, 1):
        # Extract timestamp from the startTime field
        timestamp_str = lifelog.get("startTime")
        
        if timestamp_str:
            try:
                # Parse ISO format timestamp (e.g., "2025-03-18T15:41:44-05:00")
                start_time = datetime.datetime.fromisoformat(timestamp_str)
                
                # Convert to America/Chicago timezone
                chicago_tz = pytz.timezone("America/Chicago")
                start_time_chicago = start_time.astimezone(chicago_tz)
                
                # Format filename with date and time
                filename = start_time_chicago.strftime("%Y-%m-%d-%H-%M-%S") + ".md"
                filepath = export_dir / filename
                
                # Write markdown content to file
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(lifelog.get("markdown", ""))
                
                print(f"[{i}/{len(lifelogs)}] Exported: {filename}")
            except Exception as e:
                print(f"[{i}/{len(lifelogs)}] Error processing timestamp '{timestamp_str}': {e}")
        else:
            # Use current time with index as fallback if no timestamp is found
            now = datetime.datetime.now()
            chicago_tz = pytz.timezone("America/Chicago")
            now_chicago = now.astimezone(chicago_tz)
            filename = now_chicago.strftime("%Y-%m-%d-%H-%M-%S") + f"-{i}.md"
            filepath = export_dir / filename
            
            # Write markdown content to file
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(lifelog.get("markdown", ""))
            
            print(f"[{i}/{len(lifelogs)}] No timestamp found, using current time: {filename}")

def main():
    """
    Main function to fetch and export all lifelogs.
    """
    print("Fetching all lifelogs from beginning to now...")
    
    # Get all lifelogs (no limit) in chronological order
    lifelogs = get_lifelogs(
        api_key=os.getenv("LIMITLESS_API_KEY"),
        direction="asc",  # Chronological order (oldest first)
        limit=None,       # No limit, get all lifelogs
    )
    
    # Export data
    export_data(lifelogs)
    print("Export complete!")

if __name__ == "__main__":
    main() 
