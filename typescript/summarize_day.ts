// Copyright (c) 2025 Limitless AI, Inc.
// Licensed under the MIT License. See LICENSE in the root directory.

import dotenv from "dotenv";
import OpenAI from "openai";
import { getLifelogs } from "./_client";

// Load environment variables
dotenv.config();

async function summarizeLifelogs(
  lifelogs: any[],
  shouldStream = true
): Promise<void | string> {
  const client = new OpenAI({
    apiKey: process.env.OPENAI_API_KEY,
  });

  if (shouldStream) {
    const stream = await client.chat.completions.create({
      model: "gpt-4.1",
      messages: [
        {
          role: "system",
          content: "You are a helpful assistant that summarizes transcripts.",
        },
        {
          role: "user",
          content: `Summarize the following transcripts: ${JSON.stringify(
            lifelogs
          )}`,
        },
      ],
      stream: true,
    });

    for await (const chunk of stream) {
      if (chunk.choices[0]?.finish_reason === null) {
        process.stdout.write(chunk.choices[0]?.delta?.content || "");
      }
    }
  } else {
    const response = await client.chat.completions.create({
      model: "gpt-4.1",
      messages: [
        {
          role: "system",
          content: "You are a helpful assistant that summarizes transcripts.",
        },
        {
          role: "user",
          content: `Summarize the following transcripts: ${JSON.stringify(
            lifelogs
          )}`,
        },
      ],
      stream: false,
    });

    const content = response.choices[0]?.message?.content;
    return content || "";
  }
}

async function main(): Promise<void> {
  try {
    // Get transcripts, limiting size because OpenAI has a 128k context window
    const lifelogs = await getLifelogs({
      apiKey: process.env.LIMITLESS_API_KEY || "",
      limit: 10,
    });

    // Summarize transcripts
    await summarizeLifelogs(lifelogs);
  } catch (error) {
    console.error("Error:", error);
    process.exit(1);
  }
}

// Run the main function
main();
