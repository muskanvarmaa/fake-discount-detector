import re

def chatbot_response(user_input):
    user_input = user_input.lower()
    
    # Keyword : Response
    rules = {
        r'hello|hi|hey': "Hello! Welcome to RedBus. How can I help you?",
        r'book|ticket|bus': "Sure! Please provide your source and destination.",
        r'price|fare|cost': "Bus fares start from 500 INR depending on the route.",
        r'cancel': "You can cancel tickets in the 'My Bookings' section.",
        r'support|help': "You can call us at 1800-123-4567 for support.",
        r'bye|exit': "Goodbye! Have a safe journey!"
    }

    for pattern, response in rules.items():
        if re.search(pattern, user_input):
            return response
            
    return "I'm sorry, I don't understand. Can you rephrase?"

# The Interaction Loop
print("--- Bus Booking Chatbot ---")
while True:
    message = input("You: ")
    res = chatbot_response(message)
    print("Chatbot:", res)
    if "goodbye" in res.lower():
        break