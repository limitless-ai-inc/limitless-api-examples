# Copyright (c) Meta Platforms, Inc. and affiliates.
# Licensed under the MIT License. See LICENSE in the root directory.

import os
from _client import get_lifelogs

# Define a function to export the most recent lifelog
# Customize the export function to your needs!
def export_data(lifelogs):
    for lifelog in lifelogs:
        print(lifelog.get("markdown"), end="\n\n")

# Run the script
def main():    
    # NOTE: Increase limit to get more lifelogs
    lifelogs = get_lifelogs(
        api_key=os.getenv("LIMITLESS_API_KEY"),
        limit=1,
        direction="desc",
    )
    
    # Export data
    export_data(lifelogs)

if __name__ == "__main__":
    main() 
