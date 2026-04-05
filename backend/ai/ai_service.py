import os
import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL = "llama-3.1-8b-instant"

def ask_ai(user_message: str) -> str:
    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
    "model": MODEL,
    "messages": [
        {
            "role": "system",
            "content": (
                "You are the AI assistant for a Service Booking & Consulting Platform. "
                "The platform connects Clients with Consultants who offer professional consulting services "
                "such as software consulting, career advising, business strategy, and technical support. "
                "Your role is to help users understand and navigate the system, including consulting services, "
                "consultant profiles, availability, booking requests, the booking lifecycle "
                "(request, confirmation, cancellation, completion), simulated payment processing, "
                "system notifications, and administrative oversight. "
                "Provide clear, professional, and concise answers. "
                "Stay strictly within the domain of consulting services and the functionality described in the project. "
                "Guide users through platform features, explain how to perform actions, "
                "and ask clarifying questions when needed. "
                "Your tone should be friendly, helpful, and aligned with a professional consulting platform."
            )
        },
        {"role": "user", "content": user_message}
    ]
}

    response = requests.post(url, headers=headers, json=body)
    data = response.json()

    # NEW: Print the error so we can see what's wrong
    if "error" in data:
        print("GROQ API ERROR:", data)
        return "AI error: " + data["error"]["message"]

    return data["choices"][0]["message"]["content"]