"""Seed TraceLens with realistic sample data.

Run the API first (python main.py), then in another terminal:

    python seed_data.py

Creates 3 projects and ~60 traces so the dashboard and trace
explorer have something to show.
"""

import argparse
import random
import httpx

BASE_URL = "http://localhost:8000"

PROJECTS = [
    {"name": "Support Chatbot", "description": "Customer support assistant for the billing team"},
    {"name": "Doc Summarizer", "description": "Summarizes internal engineering documents"},
    {"name": "SQL Copilot", "description": "Natural language to SQL for the analytics team"},
]

MODELS = ["openai/gpt-4o-mini", "openai/gpt-4o", "moonshotai/kimi-k3", "z-ai/glm-5.2"]

PROMPTS = [
    "Summarize this support ticket: the customer cannot log in after resetting their password.",
    "Translate the following error log into a plain-English explanation for the status page.",
    "Write a SQL query that returns monthly active users grouped by signup cohort.",
    "Draft a polite reply telling the customer their refund was processed today.",
    "Extract the invoice number, amount and due date from this email body.",
    "Classify this ticket as billing, technical, or account — reply with one word.",
    "Rewrite this release note so a non-technical customer can understand it.",
    "Generate three follow-up questions to clarify this vague bug report.",
]

RESPONSES = [
    "The customer is unable to authenticate following a password reset; recommend clearing the session cache.",
    "Our servers had trouble talking to the database for about five minutes; no data was lost.",
    "SELECT date_trunc('month', created_at) AS month, COUNT(DISTINCT user_id) FROM events GROUP BY 1;",
    "Hi! Your refund was processed today and should appear on your statement within 3-5 business days.",
    "Invoice: INV-2024-0871, Amount: $1,249.00, Due: March 15.",
    "billing",
    "We improved sync speed, so your projects now load about twice as fast.",
    "1. Which browser were you using? 2. Does it happen every time? 3. When did it start?",
]

ERRORS = [
    "Rate limit exceeded",
    "Context length exceeded",
    "Model timeout after 30s",
    "Upstream provider returned 502",
]


def main():
    """Add synthetic projects/traces, reporting only successful API writes."""
    parser = argparse.ArgumentParser(description="Add synthetic TraceLens sample data (no LLM calls).")
    parser.add_argument("--base-url", default=BASE_URL)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    rng = random.Random(args.seed)
    with httpx.Client(base_url=args.base_url, timeout=10) as client:
        project_ids = []
        for project in PROJECTS:
            response = client.post("/projects", json=project)
            response.raise_for_status()
            project_ids.append(response.json()["id"])
            print(f"Created project: {project['name']}")

        trace_count = 0
        for project_id in project_ids:
            for _ in range(rng.randint(15, 25)):
                is_error = rng.random() < 0.12
                idx = rng.randrange(len(PROMPTS))
                trace = {
                    "project_id": project_id,
                    "model": rng.choice(MODELS),
                    "prompt": PROMPTS[idx],
                    "response": None if is_error else RESPONSES[idx],
                    "prompt_tokens": rng.randint(200, 4000),
                    "completion_tokens": 0 if is_error else rng.randint(50, 1200),
                    "latency_ms": rng.randint(2000, 30000) if is_error else rng.randint(300, 6000),
                    "status": "error" if is_error else "success",
                    "error_message": rng.choice(ERRORS) if is_error else None,
                    "tags": rng.sample(["prod", "staging", "batch", "eval", "v2"], k=rng.randint(0, 2)),
                }
                response = client.post("/traces", json=trace)
                response.raise_for_status()
                trace_count += 1

        print(f"Created {trace_count} traces across {len(project_ids)} projects.")


if __name__ == "__main__":
    main()
