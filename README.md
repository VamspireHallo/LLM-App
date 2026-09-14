# AI Email Rewriter

This application rewrites draft emails using Duke's AI Gateway and the GPT 4.1 model.

## Features

- Rewrites a draft email in Professional, Friendly, Concise, or Formal tone
- Shows the generated email beside the original draft
- Keeps temporary session history while the app is open
- Does not store API keys in source code

## Local Setup

1. Install Python and `uv`.

2. Run:

   ```bash
   uv sync

## Network Access Note

The application connects to Duke's AI Gateway. If the Gateway connection times out while you are off campus, connect to Duke VPN and run the application again.

## AI Assistance Disclosure

I used OpenAI Codex (GPT-5) through ChatGPT Work between September 3 and September 14, 2026. It assisted with drafting the Gradio interface, configuring the Duke AI Gateway connection, creating the Dockerfile, and troubleshooting `uv`, Docker, VPN, and network-connection issues I had through out the project's developement.

I chose the AI Email Rewriter concept, wrote the AI prompts for the LiteLLM, created the Duke AI Gateway key, selected the GPT 4.1 model, configured and tested the application locally and with Docker, reviewed the generated code, and chose the prompt behavior and interface features.