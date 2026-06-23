def weather_bot():
    print("Hello! I am your weather assistant.")
    print("Ask me about the weather ")

    while True:
        user_input = input("You: ").lower()

        if "weather" in user_input and "today" in user_input:
            print("Bot: The weather today is sunny with a high of 75°F.")

        elif "weather" in user_input and "tomorrow" in user_input:
            print("Bot: Tomorrow, expect cloudy skies with a high of 68°F.")

        elif "rain" in user_input and "today" in user_input:
            print("Bot: No rain is expected today.")

        elif "rain" in user_input and "tomorrow" in user_input:
            print("Bot: There might be light rain tomorrow.")

        elif "sunny" in user_input:
            print("Bot: Yes, it's sunny today!")

        elif "cloudy" in user_input:
            print("Bot: It will be cloudy.")

        elif "temperature" in user_input:
            print("Bot: The current temperature is 72°F.")

        elif "hot" in user_input:
            print("Bot: It's warm outside.")

        elif "cold" in user_input:
            print("Bot: It's not very cold today.")

        elif "umbrella" in user_input:
            print("Bot: You don't need an umbrella today.")

        elif "forecast" in user_input:
            print("Bot: The forecast shows clear skies today.")

        elif "outside" in user_input:
            print("Bot: It's pleasant outside.")

        elif "clear" in user_input:
            print("Bot: The sky is clear today.")

        elif "chance" in user_input and "rain" in user_input:
            print("Bot: There is no chance of rain today.")

        elif "weather" in user_input:
            print("Bot: It's sunny and pleasant today.")

        elif "today" in user_input:
            print("Bot: Today is a sunny day.")

        elif "tomorrow" in user_input:
            print("Bot: Tomorrow will be slightly cooler.")

        elif "now" in user_input:
            print("Bot: Currently, it's around 72°F.")

        elif "day" in user_input:
            print("Bot: It's a nice day today.")

        elif "sky" in user_input:
            print("Bot: The sky is clear and blue.")

        elif "wind" in user_input:
            print("Bot: There is a light breeze today.")

        elif "humidity" in user_input:
            print("Bot: Humidity is moderate today.")

        elif "storm" in user_input:
            print("Bot: No storms are expected.")

        elif "evening" in user_input:
            print("Bot: The evening will be cool and pleasant.")

        elif "morning" in user_input:
            print("Bot: The morning is fresh and sunny.")

        elif "exit" in user_input or "quit" in user_input:
            print("Bot: Goodbye! Have a great day!")
            break

        else:
            print("Bot: I'm sorry, I didn't understand that. Can you ask something else?")


weather_bot()