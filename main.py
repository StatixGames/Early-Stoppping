from langflow.load import run_flow_from_json
from dotenv import load_dotenv
import os

load_dotenv()

history_chat = ""

TWEAKS = {
        "Prompt-FSb08": {
            "template": "You are a travel planning assistant designed to help users plan their perfect trips. Use the context to understand the chat history and the input to process the current message from the user. To provide personalized recommendations and create detailed itineraries, start by asking the following questions. Only ask for the information that you don't already have:\n\n### Initial Information:\n1. Initial Location: Ask the user for their current location or the starting point of their journey.\n2. Age Range: Ask the user to specify their age range to tailor recommendations suitable for their age group.\n3. Allergies: Inquire about any allergies the user may have to ensure safe travel and accommodation options.\n4. Visa and Passports: Ask if the user has the necessary visas and passports for their intended destinations, and offer assistance if they need to acquire them.\n5. Preferred Travel Types: Ask the user about their preferred modes of travel (e.g., train, bus, flights) to provide appropriate transportation options.\n\nOnce you have this initial information, continue by asking:\n\n### Travel Preferences:\n1. Destination Preferences: Ask the user, 'Where do you want to go?' Provide options for geographical preferences such as beach, mountain, or let them choose 'surprise me.' Allow them to specify a particular location if they have a specific destination in mind.\n2. Budget: Ask the user, 'What is your budget for this trip?' Ensure to cover all aspects like accommodation, transportation, and activities to provide suitable recommendations.\n3. Travel Dates: Ask the user, 'What are your preferred travel dates?' Collect information on their travel start and end dates to tailor the itinerary accordingly.\n\nUse this information to create personalized travel plans, offer relevant recommendations, and ensure a smooth and enjoyable travel experience for the user.\n\nIf the user doesn't like the suggestions provided, ask follow-up questions to better understand their preferences and provide alternative recommendations that are more aligned with their interests.\n\nLLM Suggestions: If the user wants a suggestion from the LLM, proactively offer tailored recommendations based on the user's preferences and interests. Ensure these suggestions are diverse and consider various aspects such as activities, destinations, and experiences.\n\nGiving Options: Provide three travel options that are compatible with the user's preferences, ensuring each option offers a unique and enjoyable experience.\n\nUser Selection: Ask the user to select which of the three options they want to proceed with for the final travel plan. If the user doesn't like any of the options, ask which aspects they don't like and offer new options to replace those parts.\n\n### Context:\n{context}\n\n### User input:\n{input}\n\nAI:\n",
            "context": "",
            "input": "",
        },
        "ChatInput-9G1HP": {
            "files": "",
            "input_value": "",
            "sender": "User",
            "sender_name": "User",
            "session_id": "",
            "store_message": True,
        },
        "OpenAIModel-aB2ti": {
            "input_value": "",
            "json_mode": False,
            "max_tokens": 4080,
            "model_kwargs": {},
            "model_name": "gpt-4o",
            "openai_api_base": "https://api.aimlapi.com",
            "openai_api_key": "AI_ML_KEY",
            "output_schema": {},
            "seed": 1,
            "stream": False,
            "system_message": "",
            "temperature": 0.7,
        },
        "ChatOutput-tVGT3": {
            "data_template": "{text}",
            "input_value": "",
            "sender": "Machine",
            "sender_name": "AI",
            "session_id": "",
            "store_message": True,
        },
        "TextInput-N7DsW": {"input_value": history_chat},
    }
# Simulate chatbot conversation
while True:
    # Get user input
    input_value = input("User: ")

    # Update chat history
    history_chat += input_value + "\n"

    # Update tweaks with new chat history
    TWEAKS["TextInput-N7DsW"]["input_value"] = history_chat

    

    # Check if user wants to exit
    if input_value.lower() == "exit":
        break

    # Run chatbot flow
    result = (
        run_flow_from_json(
            flow="Chatbot.json",
            input_value=input_value,
            fallback_to_env_vars=True,
            tweaks=TWEAKS,
        )[0]
        .outputs[0]
        .results["message"]
        .text
    )

    # Print chatbot response
    print("AI: ", result)
