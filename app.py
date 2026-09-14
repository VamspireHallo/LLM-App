import os

import gradio as gr
from dotenv import load_dotenv
from openai import OpenAI

# Loads LITELLM_TOKEN from the local .env file.
load_dotenv()

API_KEY = os.getenv("LITELLM_TOKEN")
BASE_URL = "https://litellm.oit.duke.edu/v1"
MODEL = "GPT 4.1"

if not API_KEY:
    raise ValueError(
        "LITELLM_TOKEN is missing. Add it to your local .env file."
    )

client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL,
)


def rewrite_email(email_text: str, tone: str, history: list):
    """Rewrite an email and add it to the current session's history."""
    history = history or []

    if not email_text or not email_text.strip():
        message = "Please paste an email draft before clicking Rewrite My Email."
        return message, history, history

    tone_guidance = {
        "Friendly": (
            "Use a warm, approachable, conversational style. "
            "Use natural everyday language and contractions when appropriate. "
            "Sound helpful and personable, not stiff or corporate."
        ),
        "Concise": (
            "Use the fewest words possible while preserving the request. "
            "Write no more than two short sentences after the subject line. "
            "Remove greetings, filler, explanations, and unnecessary politeness."
        ),
        "Professional": (
            "Use a polished workplace or academic style. "
            "Be respectful, clear, and organized. "
            "Use complete sentences and polite wording without sounding overly formal."
        ),
        "Formal": (
            "Use a highly formal and respectful style. "
            "Avoid contractions and casual wording. "
            "Use elevated, courteous language appropriate for an official request."
        ),
    }

    prompt = f"""
Rewrite the email below in a {tone.lower()} tone.

Tone instructions:
{tone_guidance[tone]}

Rules:
- Preserve the sender's intent and factual information.
- Do not invent names, dates, attachments, promises, or details.
- Make the selected tone noticeably different from the other available tones.
- Do not use nearly identical wording across tones.
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
            temperature=0.8,
        )

        rewritten_email = response.choices[0].message.content

        # Adds the newest result at the top of the history table.
        updated_history = [
            [tone, email_text, rewritten_email],
            *history,
        ]

        return rewritten_email, updated_history, updated_history

    except Exception as error:
        message = (
            "Unable to generate a rewrite.\n\n"
            "Check your Duke API key, model name, and network connection.\n\n"
            f"Technical message: {error}"
        )
        return message, history, history


def clear_history():
    """Clear the current browser session's generation history."""
    return [], []


with gr.Blocks(title="AI Email Rewriter") as demo:
    gr.Markdown("# AI Email Rewriter")
    gr.Markdown(
        "Paste your email draft below, select a tone, and receive a clearer "
        "rewritten email. Always review the result before sending."
    )

    history_state = gr.State([])

    with gr.Row():
        email_text = gr.Textbox(
            label="Your Draft Email",
            lines=12,
            placeholder=(
                "Example: hey professor I missed class yesterday and wanted "
                "to know what I need to catch up on thanks"
            ),
        )

        rewritten_output = gr.Textbox(
            label="Generated New Email",
            lines=12,
            interactive=False,
            placeholder="Your generated email will show up here.",
        )

    tone = gr.Dropdown(
        choices=["Professional", "Friendly", "Concise", "Formal"],
        value="Professional",
        label="Desired Tone",
    )

    generate_button = gr.Button("Rewrite My Email", variant="primary")

    gr.Markdown("## Session History")

    history_table = gr.Dataframe(
        headers=["Tone", "Original Draft", "Generated Email"],
        value=[],
        interactive=False,
        label="Your Previous Email Generations",
    )

    clear_button = gr.Button("Clear History")

    generate_button.click(
        fn=rewrite_email,
        inputs=[email_text, tone, history_state],
        outputs=[rewritten_output, history_state, history_table],
    )

    clear_button.click(
        fn=clear_history,
        outputs=[history_state, history_table],
    )

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        inbrowser=False,
    )