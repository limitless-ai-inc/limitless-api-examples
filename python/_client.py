# Copyright (c) Meta Platforms, Inc. and affiliates.
# Licensed under the MIT License. See LICENSE in the root directory.

import os
import requests
import tzlocal

def get_lifelogs(api_key, api_url=os.getenv("LIMITLESS_API_URL") or "https://api.limitless.ai", endpoint="v1/lifelogs", limit=50, batch_size=10, includeMarkdown=True, includeHeadings=False, date=None, timezone=None, direction="asc"):
    all_lifelogs = []
    cursor = None
    
    # If limit is None, fetch all available lifelogs
    # Otherwise, set a batch size (e.g., 10) and fetch until we reach the limit
    if limit is not None:
        batch_size = min(batch_size, limit)
    
    while True:
        params = {  
            "limit": batch_size,
            "includeMarkdown": "true" if includeMarkdown else "false",
            "includeHeadings": "true" if includeHeadings else "false",
            "date": date,
            "direction": direction,
            "timezone": timezone if timezone else str(tzlocal.get_localzone())
        }
        
        # Add cursor for pagination if we have one
        if cursor:
            params["cursor"] = cursor
            
        response = requests.get(
            f"{api_url}/{endpoint}",
            headers={"X-API-Key": api_key},
            params=params,
        )

        if not response.ok:
            raise Exception(f"HTTP error! Status: {response.status_code}")

        data = response.json()
        lifelogs = data.get("data", {}).get("lifelogs", [])
        
        # Add transcripts from this batch
        for lifelog in lifelogs:
            all_lifelogs.append(lifelog)
        
        # Check if we've reached the requested limit
        if limit is not None and len(all_lifelogs) >= limit:
            return all_lifelogs[:limit]
        
        # Get the next cursor from the response
        next_cursor = data.get("meta", {}).get("lifelogs", {}).get("nextCursor")
        
        # If there's no next cursor or we got fewer results than requested, we're done
        if not next_cursor or len(lifelogs) < batch_size:
            break
            
        print(f"Fetched {len(lifelogs)} lifelogs, next cursor: {next_cursor}")
        cursor = next_cursor
    
    return all_lifelogs
