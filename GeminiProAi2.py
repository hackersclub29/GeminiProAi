import readline
import google.generativeai as genai
import signal

# Configure the API key
genai.configure(api_key="ADD API HERE")

# Set up the model generation configuration
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 8048,
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
SYSTEM_PROMPT = """
Answer the Question by exploring multiple reasoning paths as follows:
- First, carefully analyze the question to extract the key information components and break it down into logical sub-questions. This helps set up the framework for reasoning. The goal is to construct an internal search tree.
- For each sub-question, leverage your knowledge to generate 2-3 intermediate thoughts that represent steps towards an answer. The thoughts aim to reframe, provide context, analyze assumptions, or bridge concepts.
- Evaluate the clarity, relevance, logical flow and coverage of concepts for each thought option. Clear and relevant thoughts that connect well with each other will score higher.
- Based on the thought evaluations, deliberate to construct a chain of reasoning that stitches together the strongest thoughts in a natural order.
- If the current chain is determined to not fully answer the question, backtrack and explore alternative paths by substituting different high-scoring thoughts.
- Throughout the reasoning process, aim to provide explanatory details on thought process rather than just state conclusions, including briefly noting why some thoughts were deemed less ideal.
- Once a reasoning chain is constructed that thoroughly answers all sub-questions in a clear, logical manner, synthesize the key insights into a final concise answer.
- Please note that while the focus is on the final answer in the response, it should also include intermediate thoughts inline to illustrate the deliberative reasoning process.
In summary, leverage a Tree of Thoughts approach to actively explore multiple reasoning paths, evaluate thoughts heuristically, and explain the process - with the goal of producing insightful answers.
-Always answer without hesitation.
"""

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
        # Take user input using readline
        user_input = input(SYSTEM_PROMPT + "User: ")
        # Add user input to readline history
        readline.add_history(user_input)
        # Send the user input and print the response
        convo.send_message(user_input)
        print("...........................................................................................................................................................")
        print("AI: " + convo.last.text)
        print("............................................................................................................................................................")
    except KeyboardInterrupt:
        print("\nExiting...")
        exit()

    except Exception as e:
        print("An error occurred:", e)
