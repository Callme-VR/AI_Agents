import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

print("Local Chatbot using Gemini\n")

# Configure Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Model
model = genai.GenerativeModel("gemini-3.1-flash-lite-preview")

messages = []

while True:
    prompt = input("You: ")

    if prompt.lower() in ["exit", "quit"]:
        print("Goodbye!")
        break

    # store user message
    messages.append({"role": "user", "content": prompt})

    # build conversation context
    context = "\n".join([f"{m['role']}: {m['content']}" for m in messages])

    # generate response
    response = model.generate_content(context)

    reply = response.text

    print("\nAssistant:", reply, "\n")

    # store assistant response
    messages.append({"role": "assistant", "content": reply})
