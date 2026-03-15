// Copyright (c) 2025 Limitless AI, Inc.
// Licensed under the MIT License. See LICENSE in the root directory.

import dotenv from "dotenv";
import { getLifelogs } from "./_client";

// Load environment variables
dotenv.config();

// Define a function to export the most recent lifelog
// Customize the export function to your needs!
function exportData(lifelogs: any[]): void {
  for (const lifelog of lifelogs) {
    console.log(lifelog.markdown || "", "\n");
  }
}

// Run the script
async function main(): Promise<void> {
  try {
    // NOTE: Increase limit to get more lifelogs
    const lifelogs = await getLifelogs({
      apiKey: process.env.LIMITLESS_API_KEY || "",
      limit: 1,
      direction: "desc",
    });

    // Export data
    exportData(lifelogs);
  } catch (error) {
    console.error("Error:", error);
    process.exit(1);
  }
}

// Run the main function
main();
