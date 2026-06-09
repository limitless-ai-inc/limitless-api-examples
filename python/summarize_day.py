# Copyright (c) Meta Platforms, Inc. and affiliates.
# Licensed under the MIT License. See LICENSE in the root directory.

import os
from openai import OpenAI
from _client import get_lifelogs

def summarize_lifelogs(lifelogs, should_stream=True):
  client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
  response = client.chat.completions.create(
      model="gpt-4o-mini",
      messages=[
          {"role": "system", "content": "You are a helpful assistant that summarizes transcripts."},
          {"role": "user", "content": f"Summarize the following transcripts: {lifelogs}"}
      ],
      stream=should_stream
  )
  if should_stream:
    for chunk in response:
      if chunk.choices[0].finish_reason is None:
        print(chunk.choices[0].delta.content, end='')
  else:
    return response.choices[0].message.content

def main():
    # Get transcripts, limiting size because OpenAI has a 128k context window
    lifelogs = get_lifelogs(
        api_key=os.getenv("LIMITLESS_API_KEY"),
        limit=10
    )

    # Summarize transcripts
    summarize_lifelogs(lifelogs)

if __name__ == "__main__":
    main() 
