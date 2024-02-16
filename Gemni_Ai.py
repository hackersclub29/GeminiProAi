import google.generativeai as genai
import signal

# Configure the API key
genai.configure(api_key="AIzaSyA4TRH7gtEmH_KU0TetZBT7iAcMrrui_tM")

# Set up the model generation configuration
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 4048,
}

# Set up safety settings
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_LOW_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_LOW_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_LOW_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_ONLY_HIGH"},
]


# Initialize the generative model
model = genai.GenerativeModel(
    model_name="gemini-1.0-pro",
    generation_config=generation_config,
    safety_settings=safety_settings,
)

# Predefined system prompt
print("Welcome to gemini-1-pro")

# Start a conversation
convo = model.start_chat(history=[])

# Define a signal handler to catch Ctrl+C
def signal_handler(sig, frame):
    print("\nExiting...")
    exit()

# Catch Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

# Loop for conversation
while True:
    try:
        # Take user input
        user_input = input("Enter your Promte (Ctrl+Q to quit): ")

        # Check for quit command
        if user_input == "Ctrl+Q":
            print("\nExiting...")
            exit()

        # Send the user input and print the response
        convo.send_message(user_input)
        print(convo.last.text)
        print("-------------------------------------------------------------------------------------------------------------------------------------------------")

    except KeyboardInterrupt:
        print("\nExiting...")
        exit()

    except Exception as e:
        print("An error occurred:", e)
