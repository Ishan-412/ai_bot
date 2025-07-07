import speech_recognition as sr
import pyttsx3
import webbrowser
import os
import google.generativeai as genai
from dotenv import load_dotenv # New: Import load_dotenv

# Load environment variables from .env file
load_dotenv() # New: Call load_dotenv at the very beginning

# Initialize recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Configure Gemini API key
try:
    # Corrected: Get the API key from the environment variable named "GEMINI_API_KEY"
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set in .env file or system.")
    genai.configure(api_key=gemini_api_key)
    print("Gemini API configured successfully.")
except Exception as e:
    print(f"Error configuring Gemini API: {e}")
    print("Please ensure 'GEMINI_API_KEY' is set in your .env file (e.g., GEMINI_API_KEY='YOUR_KEY_HERE').")
    # In a production app, you might want to exit here if the API is critical.
    # For now, it will print the error and continue, but Gemini calls will fail.

# Function to make the engine speak
def speak(text):
    """Converts text to speech using pyttsx3."""
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Error speaking: {e}")

# Function to process AI responses
def aiprocess(command):
    """Processes a command using Google's Gemini model."""
    try:
        model = genai.GenerativeModel('gemini-1.5-flash') # Using a generally stable model
        response = model.generate_content(command)
        return response.text
    except Exception as e:
        print(f"Error processing with Gemini: {e}")
        return "I encountered an error while trying to process that."

# Command processing function
def processcommand(c):
    """Processes the recognized voice command."""
    c = c.lower()

    if "open google" in c:
        speak("Opening Google.")
        webbrowser.open("https://google.com")
    elif "open youtube" in c:
        speak("Opening YouTube.")
        webbrowser.open("https://www.youtube.com/") # Corrected YouTube URL
    elif c.startswith("play"):
        song_query = c.split(" ", 1)[1]  # Extract song name
        speak(f"Searching for {song_query} on YouTube.")
        # Corrected Youtube URL
        webbrowser.open(f"https://www.youtube.com/results?search_query={song_query.replace(' ', '+')}")
    else:
        # All AI processing now goes through Gemini
        output = aiprocess(c)
        speak(output)

# Main program execution
if __name__ == '__main__':
    speak('Initializing Jarvis. How can I help you?')

    while True:
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=1)
                print("Listening...")
                audio = recognizer.listen(source, timeout=5)
                command = recognizer.recognize_google(audio)
                print(f"You said: {command}")
                processcommand(command)

        except sr.UnknownValueError:
            print("Could not understand audio")
            speak("Sorry, I did not understand that. Please try again.")
        except sr.WaitTimeoutError:
            print("Listening timed out, no speech detected.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            speak("Sorry, my speech service is currently unavailable.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            speak("An unexpected error occurred. Please try again.")