  <h1>
    <img src="assets/limitless-logo.svg" alt="API Icon" width="32" height="32">
    Limitless Developer API: Code Examples
  </h1>

This repository contains examples demonstrating how to use our API endpoints, featuring realistic, LLM-powered use cases.

## 😍 Contributing

Share your examples with the community! Pull requests are welcome. We'll review PRs and potentially merge the best use cases (with credit, of course).

## 📚 Table of Contents

- [Getting Started](#getting-started)
- [Authentication](#authentication)
- [Examples](#examples)
- [Documentation](#documentation)
- [Support](#support)

## 🚀 Getting Started

To use these examples, you'll need:

- [An API key](https://limitless.ai/developers) from Limitless
- [Python 3](https://realpython.com/installing-python/) and virtualenv (you can install virtualenv with `pipx install virtualenv`)
- Basic understanding of REST APIs

You can also use our [OpenAPI spec](openapi.yml) to generate client libraries in your language of choice.

## 🔐 Authentication

All API requests require authentication using an API key. Include it in the header of your requests:

### Installation

```bash
cd examples
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 🛳️ Examples

### Example cURL

```bash
curl -X GET "https://api.limitless.ai/v1/<endpoint>" \
     -H "X-API-KEY: YOUR_API_KEY"
```

### Chart Usage

See the `notebooks/` folder for examples.

![Chart Example](./assets/chart.png)

### Export Markdown

This example simply prints the Markdown content from each the most recent record.

```bash
LIMITLESS_API_KEY="your_api_key" python export_markdown.py
```

##### Output:

```markdown
A request to play a song, followed by a discussion about the lyrics

Requesting Siri to play "Shiny" from Moana.

    Speaker 1: Okay.

    Speaker 2: serious.

    Speaker 2: Siri, play Shiny from Moana in the front room.

    Speaker 2: Shiny from Moana soundtrack by Jemaine Clement now playing on the front room.

Discussing the desired part of the song.

    Speaker 3: It's from the part where you're singing. we want the shiny.

    Speaker 3: Right, Mom.

Confusion about the lyrics and a reference to Grandma's advice.

... etc ...
```

### Generate a daily summary from your transcripts

```bash
LIMITLESS_API_KEY="your_api_key" OPENAI_API_KEY="sk-...." python summarize_day.py
```

##### Output (will stream to the console):

```markdown
Here's a summary of the provided transcripts:

1. **Song Request and Lyrics Discussion**: A family member requests Siri to play "Shiny" from Moana. They discuss their favorite parts of the song, express confusion over the lyrics, and reflect on Grandma's advice to "listen to your heart."

2. **Swimming Conversation**: You and another speaker recall whose child was first in the water, discuss a successful swim attempt, and consider whether to do another lap.

... etc ...
```

## ℹ️ More information

For more information on the API, see the [documentation](https://limitless.ai/developers/docs/api).

## 🛟 Support

If you need help, join our [Slack community](https://www.limitless.ai/community), follow us on [X/Twitter](https://twitter.com/limitlessai), or [email us](mailto:support@limitless.ai).

## 📄 License

This project is licensed under the [MIT License](LICENSE).
