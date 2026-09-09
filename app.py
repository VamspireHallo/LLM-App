import os
import sys

import gradio as gr
from dotenv import load_dotenv
from openai import OpenAI

# Loads values from .env when running locally or in Docker.
load_dotenv()

# In Google Colab, load only the API key from Colab Secrets.
if not os.getenv("API_KEY"):
    try:
        from google.colab import userdata

        api_key = userdata.get("API_KEY")
        if api_key:
            os.environ["API_KEY"] = api_key
    except ImportError:
        pass

API_KEY = os.getenv("API_KEY")

# These values are not secrets.
BASE_URL = "https://litellm.oit.duke.edu/v1"

# Replace this with the exact model name you used in CYBERSEC 520
# or one available in your Duke AI Dashboard.
MODEL = "gpt-4.1"

if not API_KEY:
    raise ValueError(
        "API_KEY is missing. Add it to Colab Secrets "
        "or your local .env file."
    )

client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL,
)


def rewrite_email(email_text: str, tone: str) -> str:
    """Rewrite an email through the Duke AI Gateway."""
    if not email_text or not email_text.strip():
        return "Please paste an email draft before clicking **Rewrite Email**."

    prompt = f"""
Rewrite the email below in a {tone.lower()} tone.

Rules:
- Preserve the sender's intent and factual information.
- Do not invent names, dates, attachments, promises, or details.
- Make the message clear, natural, and ready to send.
- Begin with a suggested subject line.
- Then provide the rewritten email.
- Do not explain your changes.

Original email:
{email_text}
"""

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a careful email-writing assistant. "
                        "Improve clarity and tone while preserving the user's meaning."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.5,
        )

        return response.choices[0].message.content

    except Exception as error:
        return (
            "### Unable to generate a rewrite\n"
            "Check your Duke API key, model name, and network connection.\n\n"
            f"Technical message: `{error}`"
        )


demo = gr.Interface(
    fn=rewrite_email,
    inputs=[
        gr.Textbox(
            label="Your draft email",
            lines=10,
            placeholder=(
                "Example: hey professor i missed class yesterday and wanted "
                "to know what i need to catch up on thanks"
            ),
        ),
        gr.Dropdown(
            choices=["Professional", "Friendly", "Concise", "Formal"],
            value="Professional",
            label="Desired tone",
        ),
    ],
    outputs=gr.Markdown(label="Rewritten email"),
    title="ClearMail: AI Email Rewriter",
    description=(
        "Paste a draft, select a tone, and receive a clearer rewritten email. "
        "Always review the result before sending."
    ),
    examples=[
        [
            "hey professor i missed class yesterday and wanted to know "
            "what i need to catch up on thanks",
            "Professional",
        ]
    ],
)

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
    )
