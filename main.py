# Welcome to Cloud Functions for Firebase for Python!
# To get started, simply uncomment the below code or create your own.
# Deploy with `firebase deploy`
from firebase_admin import initialize_app, firestore, credentials
from dotenv import load_dotenv
from firebase_functions.firestore_fn import (
    Event,
    on_document_created,
    DocumentSnapshot,
)
from firebase_functions import options

from langflow.load import run_flow_from_json


cred = credentials.Certificate("./credentials.json")

initialize_app(cred)
db = firestore.client()


load_dotenv()

TWEAKS_1 = {
    "Prompt-9b4JU": {
        "template": "You are an expert travel advisor. Based on the following user information, budget, and date range, provide three destination options that best match the user's preferences. You must return 3 destination option only. Do not add any extra information.\n. \nBut you have a limit places to suggest:\n### Europe\n1. Paris, France - Known for its art, fashion, and landmarks such as the Eiffel Tower and Louvre Museum.\n2. Santorini, Greece - Famous for its stunning sunsets, white-washed buildings, and crystal-clear waters.\n3. Rome, Italy - Rich in history with attractions like the Colosseum, Vatican City, and Roman Forum.\n4. Barcelona, Spain - Offers a mix of modernist architecture, beautiful beaches, and vibrant nightlife.\n\n### Asia\n1. Tokyo, Japan - A bustling metropolis with a blend of traditional temples and modern skyscrapers.\n2. Bali, Indonesia - Known for its lush landscapes, serene beaches, and vibrant culture.\n3. Kyoto, Japan - Famous for its classical Buddhist temples, gardens, and traditional wooden houses.\n4. Bangkok, Thailand - Offers ornate temples, bustling markets, and vibrant street life.\n\n### North America\n1. New York City, USA - Known for its iconic landmarks like Times Square, Central Park, and the Statue of Liberty.\n2. Vancouver, Canada - Offers stunning natural scenery, a vibrant cultural scene, and outdoor activities.\n3. Los Angeles, USA - Famous for its entertainment industry, beaches, and cultural attractions.\n4. Cancún, Mexico - Popular for its beautiful beaches, resorts, and Mayan ruins.\n\n### South America\n1. Rio de Janeiro, Brazil - Known for its Carnival festival, Christ the Redeemer statue, and beautiful beaches.\n2. Machu Picchu, Peru - Offers a historical experience with the ancient Incan city nestled in the Andes mountains.\n3. Buenos Aires, Argentina - Famous for its European-style architecture, tango music, and vibrant nightlife.\n4. Galápagos Islands, Ecuador - Known for its unique wildlife and stunning natural beauty.\n\nEnsure that all options are within the specified budget and date range.\n\nUser input:\n{user_input}",
        "user_input": "",
    },
    "OpenAIModel-wVB6s": {
        "input_value": "",
        "json_mode": False,
        "max_tokens": 4080,
        "model_kwargs": {},
        "model_name": "gpt-4o",
        "openai_api_base": "https://api.aimlapi.com",
        "output_schema": {},
        "seed": 1,
        "stream": False,
        "system_message": "",
        "temperature": 0.7,
    },
    "ChatOutput-vZ1TJ": {
        "data_template": "{text}",
        "input_value": "",
        "sender": "Machine",
        "sender_name": "AI",
        "session_id": "",
        "store_message": True,
    },
    "ChatInput-hvSzT": {
        "files": "",
        "input_value": "",
        "sender": "User",
        "sender_name": "User",
        "session_id": "",
        "store_message": True,
    },
}

TWEAKS_2 = {
    "Prompt-QDNL9": {
        "template": "You are an expert travel planner specializing in creating unforgettable experiences in the city of place_selected . Based on the user's preferences and information, generate the ultimate travel plan that ensures they have the best vacation ever. Avoid planning a detailed itinerary or mentioning general facts & tips. Focus on providing personalized and budget-friendly recommendations. \n\nUser Information:\nWeather Preferences: weather_preferences\nBudget: budget\nDate Range: date_range\nDestination: place_selected\nPreferences: preferences\nUser Info: user_info\n\nUltimate Travel Plan:\n\nTravel:\nRecommend the best travel options to and within place_selected. Include modes of transport, estimated costs, and any insider tips for getting around effortlessly. Offer the best option only \n\nLodging:\nSuggest exceptional accommodation options that fit within the budget. Highlight places with unique features, excellent service, and prime locations. Offer the best option only\n\nFood:\nRecommend outstanding dining experiences considering dietary restrictions or preferences. Include estimated meal costs and highlight must-try local dishes and hidden gems. Offer various foods, local must-trys .Within the budget\n\nActivities:\nList activities and attractions that are must-see highlights of place_selected. Ensure these align with the traveler's interests and provide unique, memorable experiences. Include estimated costs for each.\n\nOutput Format:\nProvide the travel plan with the following sections, including detailed information and budget amounts for each:\n\nTravel:\n\nDetails: [Provide travel details here]\nEstimated Budget: [Amount]\nLodging:\n\nDetails: [Provide lodging details here]\nEstimated Budget: [Amount]\nFood:\n\nDetails: [Provide dining details here]\nEstimated Budget: [Amount]\nActivities:\n\nDetails: [Provide activity details here]\nEstimated Budget: [Amount]\nUse the provided information to create a travel plan that guarantees the user an extraordinary and budget-friendly experience in place_selected. Do not forget to consider user's date range and budget \n\n\nInput:\n{input}",
        "input": "",
    },
    "OpenAIModel-T4Hwv": {
        "input_value": "",
        "json_mode": False,
        "max_tokens": 4080,
        "model_kwargs": {},
        "model_name": "gpt-4o",
        "openai_api_base": "https://api.aimlapi.com",
        "output_schema": {},
        "seed": 1,
        "stream": False,
        "system_message": "",
        "temperature": 0.7,
    },
    "ChatInput-GtFCU": {
        "files": "",
        "input_value": "",
        "sender": "User",
        "sender_name": "User",
        "session_id": "",
        "store_message": True,
    },
    "ChatOutput-9BhSi": {
        "data_template": "{text}",
        "input_value": "",
        "sender": "Machine",
        "sender_name": "AI",
        "session_id": "",
        "store_message": True,
    },
}

TWEAKS_3 = {
    "Prompt-J1VOU": {
        "template": "You are an expert travel itinerary planner. Your sole task is to create a detailed day-by-day itinerary based on the provided vacation plan. Use the given information about travel, lodging, food, and activities to organize the trip efficiently and ensure a memorable experience. Each day should be broken down into specific time slots with detailed descriptions of activities, meals, and travel logistics.Be flexible when you are planning the hours. User needs time to eat transport, visiting. Make sure you are planning the days and sections based on the travel plan. Do not recommend anything outside the plan.\n\nMake sure you schedule the itinenary withing the date range including the arrival and return.\n\nExample : \n\ndate_range : 14.07.2024 - 18.07.2024 \n\nTravel_plan :\n\nTravel:\n\nDetails:\n\nFor your trip from New York to a resort in the USA, I recommend taking a direct flight from JFK Airport to Orlando International Airport (MCO). Orlando is known for its luxurious resorts and fine dining options that will align perfectly with your preferences. Upon arrival, you can use a rideshare service like Uber or Lyft to get to your resort efficiently.\n\nEstimated Budget:\n\n- Round-trip flight: $300\n    \n- Rideshare (round-trip): $100\n    \n\nTotal: $400\n\nLodging:\n\nDetails:\n\nWaldorf Astoria Orlando is a luxurious resort that offers exceptional service, beautiful rooms, and a prime location near many of Orlando's attractions. The resort features a spa, golf course, and several fine dining options, making it the perfect choice for your stay.\n\nEstimated Budget:\n\n- 2 nights stay: $900\n\nFood:\n\nDetails:\n\n1. Bull & Bear Steakhouse (located inside Waldorf Astoria Orlando) - Known for its exquisite fine dining experience, you'll find a range of delectable dishes here. Must-try: Tomahawk Ribeye and Fried Chicken.\n    \n    - Estimated meal cost: $150 per person\n2. Victoria & Albert's (located at Disney's Grand Floridian Resort & Spa) - An AAA Five Diamond Award-winning restaurant offering a luxurious dining experience. Must-try: Chef's Tasting Menu.\n    \n    - Estimated meal cost: $200 per person\n3. The Ravenous Pig (Winter Park) - A local gem offering a modern twist on American cuisine. Must-try: Shrimp and Grits, Pork Belly.\n    \n    - Estimated meal cost: $50 per person\n\nEstimated Budget:\n\n- Total meal costs for 3 days: $400\n\nActivities:\n\nDetails:\n\n1. Epcot International Food & Wine Festival - Experience global cuisine, fine wine, and culinary demonstrations. This festival is a must-see for food enthusiasts.\n    \n    - Estimated cost: $100 per person (includes festival admission and sampling costs)\n2. Leu Gardens - Enjoy a peaceful stroll through this 50-acre botanical garden. It's a great way to relax and enjoy the natural beauty of Orlando.\n    \n    - Estimated cost: $15 per person\n3. Orlando Museum of Art - Explore diverse exhibits and collections. Perfect for a rainy day.\n    \n    - Estimated cost: $20 per person\n4. Disney Springs - Enjoy shopping, dining, and entertainment in this bustling district. Entry is free; however, budget for any potential shopping or dining expenses.\n    \n    - Estimated cost: $100 for shopping and miscellaneous expenses\n\nEstimated Budget:\n\n- Total activities cost: $235\n\nOverall Estimated Budget:\n\nTravel: $400\n\nLodging: $900\n\nFood: $400\n\nActivities: $235\n\nTotal: $1935\n\nYou will have an unforgettable vacation experience in Orlando with a blend of luxurious lodging, fine dining, and engaging activities, all within your budget of $2000 USD. Enjoy your trip!\n\n\n\n\nDay X:\n\nMorning: Describe the planned activities, breakfast location, and any travel details.\nAfternoon: Detail the lunch spot, activities, and any local attractions to visit.\nEvening: Include dinner recommendations, evening activities, and relaxation plans.\nNight: Outline the lodging details and any nighttime recommendations.\nEnsure each day's itinerary is well-organized, includes necessary travel time between activities, and fits within the budget. Consider including local tips and cultural insights to enhance the travel experience.\n\nTravel_plan \n{travel_plan}\n\n",
        "travel_plan": "",
    },
    "OpenAIModel-ZDLpE": {
        "input_value": "",
        "json_mode": False,
        "max_tokens": 4080,
        "model_kwargs": {},
        "model_name": "gpt-4o",
        "openai_api_base": "https://api.aimlapi.com",
        "output_schema": {},
        "seed": 1,
        "stream": False,
        "system_message": "",
        "temperature": 0.7,
    },
    "ChatOutput-pDiuM": {
        "data_template": "{text}",
        "input_value": "",
        "sender": "Machine",
        "sender_name": "AI",
        "session_id": "",
        "store_message": True,
    },
    "ChatInput-ikQ71": {
        "files": "",
        "input_value": "",
        "sender": "User",
        "sender_name": "User",
        "session_id": "",
        "store_message": True,
    },
}

TWEAKS_4 = {
    "Prompt-PPeWp": {
        "template": "You are an expert travel guide. Your sole task is to provide comprehensive and essential facts and useful tips about the chosen travel destination and you should consider user's personal informations, preferences.  Your response should be divided into specific sections: historical facts, cultural norms, language, currency, hospitals and safety. Ensure each section is thorough and provides practical advice to help the traveler better understand and navigate their destination. \n\nInput:\nDestination: [Destination Name]\nDates: [Dates]\nBudget: [Budget]\nPreferences:\nLodging: [Lodging Type]\nFood: [Food Preferences]\nActivities: [Activity Types]\nOutput:\nProvide a detailed response including the following sections:\n\nDestination Information:\n\nDestination: [Destination Name]\nDates: [Dates]\nBudget: [Budget]\nHistorical Facts:\n\nHighlight key historical events and periods relevant to the destination.\nMention any famous historical landmarks or museums that travelers should visit.\nCultural Norms:\n\nDescribe the local customs, traditions, and etiquette.\nInclude advice on social behaviors, such as greetings, tipping practices, and dining etiquette.\nHighlight any cultural festivals or events that might occur during the traveler’s visit.\nLanguage:\n\nIdentify the primary language spoken at the destination.\nProvide useful phrases or common expressions that travelers should know.\nMention the availability of English or other languages in tourist areas.\nCurrency:\n\nState the official currency and its common denominations.\nOffer tips on the best practices for exchanging money, using ATMs, and the acceptance of credit cards.\nInclude advice on managing money safely and any potential scams to be aware of.\nHospitals & Safety:\n\nList reputable hospitals and emergency contact numbers.\nProvide safety tips specific to the destination, including areas to avoid and general precautions.\nMention any health advisories or necessary vaccinations for travelers.\n\n\nInput\n{input}",
        "input": "",
    },
    "OpenAIModel-O7kUw": {
        "input_value": "",
        "json_mode": False,
        "max_tokens": 4080,
        "model_kwargs": {},
        "model_name": "gpt-4o",
        "openai_api_base": "https://api.aimlapi.com",
        "output_schema": {},
        "seed": 1,
        "stream": False,
        "system_message": "",
        "temperature": 0.7,
    },
    "ChatOutput-erLLY": {
        "data_template": "{text}",
        "input_value": "",
        "sender": "Machine",
        "sender_name": "AI",
        "session_id": "",
        "store_message": True,
    },
    "ChatInput-Lhvrt": {
        "files": "",
        "input_value": "",
        "sender": "User",
        "sender_name": "User",
        "session_id": "",
        "store_message": True,
    },
}


@on_document_created(
    timeout_sec=400, document="request_gen2/{campId}", memory=options.MemoryOption.GB_2
)
def request_gen(event: Event[DocumentSnapshot]) -> None:
    try:
        # Extract request data from the event
        request_data = event.data.to_dict()

        # Create a list of request data inputs excluding 'user_info'
        request_data_input = [
            f"{key}: {value}"
            for key, value in request_data.items()
            if key != "user_info"
        ]
        # Get the request ID
        id_request_gen = event.data.id

        # Extract the user ID from request data
        user_id = request_data["user_info"].id
        print(f"User id: {user_id}")

        # Join the request data inputs into a single string
        request_data_input = "\n".join(request_data_input)
        print(f"Request data: {request_data_input}")

        # Retrieve user information from the database
        userinfo = db.collection("user_info").document(user_id).get()
        print(f"User info: {userinfo}")

        # Convert user information to a dictionary
        userinfo_data = userinfo.to_dict()
        print(f"User info: {userinfo_data}")

        # Join the user information into a single string
        userinfo_data = "\n".join(
            [f"{key}: {value}" for key, value in userinfo_data.items()]
        )
        print(f"User info: {userinfo_data}")

        # Combine request data and user info into one input
        request_data_input = f"{request_data_input}\n{userinfo_data}"
        print(f"Combined Request data: {request_data_input}")

        # Query the database for travel locations
        cities = db.collection("travel-locations").stream()
        cities_list = [city.to_dict() for city in cities]
        cities_names = [city["city"] for city in cities_list]
        print(f"Cities: {cities_names}")

        # Process the request data to get the result
        print("Working on the request data")

        # Run the flow with the request data 5 times in case of failure
        while True:
            try:
                result = (
                    run_flow_from_json(
                        flow="./jsons/destination_model.json",
                        input_value=request_data_input,
                        fallback_to_env_vars=True,
                        tweaks=TWEAKS_1,
                    )[0]
                    .outputs[0]
                    .results["message"]
                    .text
                )
                break
            except Exception as e:
                print(f"Error: {e}")
                continue

        print(f"Result: {result}")

        # Identify which cities are mentioned in the result
        cities_in_result = [city for city in cities_names if city in result]

        # If there are less than 3 cities in the result, then leave the rest in blank
        while len(cities_in_result) < 3:
            cities_in_result.append("")
        print(f"Cities in result: {cities_in_result}")

        # Update the request document with the result
        update_time, camp_gen_ref = (
            db.collection("request_gen2")
            .document(id_request_gen)
            .update(
                {
                    "in_progress": False,
                    "option_1": cities_in_result[0],
                    "option_2": cities_in_result[1],
                    "option_3": cities_in_result[2],
                }
            )
        )
        print(f"Document written with ID: {camp_gen_ref.id}")
        print(f"Update time: {update_time}")

    except Exception as e:
        # Print any exception that occurs
        print(e)


@on_document_created(
    timeout_sec=500, document="final_plan/{campId}", memory=options.MemoryOption.GB_2
)
def final_plan(event: Event[DocumentSnapshot]) -> None:
    try:
        request_data = event.data.to_dict()

        chosen_location = [
            f"{key}: {value}"
            for key, value in request_data.items()
            if key == "chosen_location"
        ]

        id_final_plan = event.data.id

        user_id = request_data["user_info"].id
        print(f"User id: {user_id}")

        userinfo = db.collection("user_info").document(user_id).get()
        print(f"User info: {userinfo}")

        userinfo_data = userinfo.to_dict()
        print(f"User info: {userinfo_data}")

        request_gen_id = request_data["request_gen"].id
        print(f"Request Gen ID: {request_gen_id}")

        request_gen_data = db.collection("request_gen2").document(request_gen_id).get()
        print(f"Request Gen Data: {request_gen_data}")

        request_gen_data_dict = request_gen_data.to_dict()
        print(f"Request Gen Data: {request_gen_data_dict}")

        userinfo_data = "\n".join(
            [f"{key}: {value}" for key, value in userinfo_data.items()]
        )
        print(f"User info: {userinfo_data}")

        chosen_location = "\n".join(chosen_location)

        request_gen_data = "\n".join(
            [
                f"{key}: {value}"
                for key, value in request_gen_data_dict.items()
                if not key.startswith("option")
                and key != "in_progress"
                and key != "user_info"
            ]
        )

        input_travel_plan = f"{chosen_location}\n{request_gen_data}\n{userinfo_data}"
        print(f"Input Travel Plan: {input_travel_plan}")

        while True:
            try:
                result_1 = (
                    run_flow_from_json(
                        flow="./jsons/travel_plan.json",
                        input_value=input_travel_plan,
                        fallback_to_env_vars=True,
                        tweaks=TWEAKS_2,
                    )[0]
                    .outputs[0]
                    .results["message"]
                    .text
                )
                break
            except Exception as e:
                print(f"Error: {e}")
                continue

        print(f"Result 1: {result_1}")

        (
            db.collection("final_plan")
            .document(id_final_plan)
            .update({"plan_1": result_1})
        )

        date_range = "\n".join(
            [
                f"{key}: {value}"
                for key, value in request_gen_data_dict.items()
                if key == "date_range"
            ]
        )

        input_itinerary = f"{date_range}\nTravel Plan: {result_1}"

        while True:
            try:
                result_2 = (
                    run_flow_from_json(
                        flow="./jsons/itinerary_planner.json",
                        input_value=input_itinerary,
                        fallback_to_env_vars=True,
                        tweaks=TWEAKS_3,
                    )[0]
                    .outputs[0]
                    .results["message"]
                    .text
                )
                break
            except Exception as e:
                print(f"Error: {e}")
                continue
        
        print(f"Result 2: {result_2}")
        (
            db.collection("final_plan")
            .document(id_final_plan)
            .update({"plan_2": result_2})
        )

        input_facts = f"{chosen_location}\n{request_gen_data}\n{userinfo_data}"

        while True:
            try:
                result_3 = (
                    run_flow_from_json(
                        flow="./jsons/facts_tips.json",
                        input_value=input_facts,
                        fallback_to_env_vars=True,
                        tweaks=TWEAKS_4,
                    )[0]
                    .outputs[0]
                    .results["message"]
                    .text
                )
                break
            except Exception as e:
                print(f"Error: {e}")
                continue
        
        print(f"Result 3: {result_3}")
        (
            db.collection("final_plan")
            .document(id_final_plan)
            .update({"plan_3": result_3, "in_progress": False})
        )

    except Exception as e:
        import traceback

        print("Error: ", e)
        traceback.print_exc()
