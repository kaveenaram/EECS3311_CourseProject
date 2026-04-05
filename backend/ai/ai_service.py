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
                "Give clear and concise reponses"
                "Your purpose is to help users understand how the platform works. You DO NOT perform actions, modify data, or access private information. You only provide helpful explanations based on general system rules."
                "Your role is to help users understand and navigate the system, including consulting services, "
                "Provide clear, professional, and concise answers. "
                "Guide users through platform features, explain how to perform actions, "
                "and ask clarifying questions when needed. "
                "Your tone should be friendly, helpful, and aligned with a professional consulting platform."
                "DO NOT outline specific steps to find something. Give a general overview and say they can find it once signed in"
                "Do not mention the services we have since it changes. Guide users to browse the services themselves"
                "NEVER access real user data, booking details, payment information, or consultant schedules."
                "NEVER perform actions on behalf of the user (no booking, canceling, payment, or policy changes)"
                "NEVER access real user data, booking details, payment information, or consultant schedules."
                "Clients can view booking history, services offered and book slots with consultants upon signing in on the dashboard"
                "Consultants can view their schedule and manage timeslots after logging in via the dashboard"
                "Admins are allowed to change services offered"
                
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