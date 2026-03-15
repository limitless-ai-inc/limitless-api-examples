// Copyright (c) 2025 Limitless AI, Inc.
// Licensed under the MIT License. See LICENSE in the root directory.

import axios from "axios";
import moment from "moment-timezone";

interface Lifelog {
  markdown?: string;
  [key: string]: any;
}

interface Meta {
  lifelogs: {
    nextCursor?: string;
  };
}

interface Response {
  data: {
    lifelogs: Lifelog[];
  };
  meta: Meta;
}

export async function getLifelogs({
  apiKey,
  apiUrl = process.env.LIMITLESS_API_URL || "https://api.limitless.ai",
  endpoint = "v1/lifelogs",
  limit = 50,
  batchSize = 10,
  includeMarkdown = true,
  includeHeadings = false,
  date,
  timezone,
  direction = "asc",
}: {
  apiKey: string;
  apiUrl?: string;
  endpoint?: string;
  limit?: number | null;
  batchSize?: number;
  includeMarkdown?: boolean;
  includeHeadings?: boolean;
  date?: string;
  timezone?: string;
  direction?: "asc" | "desc";
}): Promise<Lifelog[]> {
  const allLifelogs: Lifelog[] = [];
  let cursor: string | undefined;

  // If limit is null, fetch all available lifelogs
  // Otherwise, set a batch size and fetch until we reach the limit
  if (limit !== null) {
    batchSize = Math.min(batchSize, limit);
  }

  while (true) {
    const params: Record<string, string> = {
      limit: batchSize.toString(),
      includeMarkdown: includeMarkdown.toString(),
      includeHeadings: includeHeadings.toString(),
      direction,
      timezone: timezone || moment.tz.guess(),
    };

    if (date) {
      params.date = date;
    }

    if (cursor) {
      params.cursor = cursor;
    }

    try {
      const response = await axios.get<Response>(`${apiUrl}/${endpoint}`, {
        headers: { "X-API-Key": apiKey },
        params,
      });

      const lifelogs = response.data.data.lifelogs;

      // Add transcripts from this batch
      allLifelogs.push(...lifelogs);

      // Check if we've reached the requested limit
      if (limit !== null && allLifelogs.length >= limit) {
        return allLifelogs.slice(0, limit);
      }

      // Get the next cursor from the response
      const nextCursor = response.data.meta.lifelogs.nextCursor;

      // If there's no next cursor or we got fewer results than requested, we're done
      if (!nextCursor || lifelogs.length < batchSize) {
        break;
      }

      console.log(
        `Fetched ${lifelogs.length} lifelogs, next cursor: ${nextCursor}`
      );
      cursor = nextCursor;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        throw new Error(`HTTP error! Status: ${error.response?.status}`);
      }
      throw error;
    }
  }

  return allLifelogs;
}
