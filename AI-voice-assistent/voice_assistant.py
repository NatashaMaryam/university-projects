import speech_recognition as sr
import pyttsx3
import os
import requests
import pyjokes
import psutil
import signal
import webbrowser

# Initialize recognizer and engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Function to speak text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to take voice input
def take_command():
    try:
        with sr.Microphone() as source:
            print("Listening...")
            voice = recognizer.listen(source)
            command = recognizer.recognize_google(voice)
            command = command.lower()
            print(f"You said: {command}")
            return command
    except Exception as e:
        print("Sorry, I could not understand. Please try again.")
        return ""

# Function to get weather updates
def get_weather(city):
    api_key = "d54f1f9fc10de47e94e0f394473fa528"  # Replace with your actual API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    
    if data["cod"] == "404":
        return "City not found!"
    
    main = data["main"]
    weather_desc = data["weather"][0]["description"]
    temp = main["temp"]
    return f"The weather in {city} is {weather_desc} with a temperature of {temp}°C."

# Function to close a process
def close_application(app_name):
    for proc in psutil.process_iter(attrs=['pid', 'name']):
        if app_name.lower() in proc.info['name'].lower():
            proc.send_signal(signal.SIGTERM)  # Send the termination signal
            print(f"Closing {app_name}...")
            speak(f"Closing {app_name}.")
            break

# Function to play music
def play_music(song_name):
    speak(f"Playing {song_name}.")
    # Example for playing music file (change the path to your music file location)
    music_file = f"C:\\Users\\YourUsername\\Music\\{song_name}.mp3"  # Update with the correct path
    if os.path.exists(music_file):
        os.startfile(music_file)  # This will open the file with the default music player
    else:
        speak("Sorry, I couldn't find that song. Let's try playing from YouTube.")
        search_youtube(song_name)

# Function to search on YouTube
def search_youtube(query):
    url = f"https://www.youtube.com/results?search_query={query}"
    webbrowser.open(url)
    speak(f"Searching YouTube for {query}")

# Function to open a website
def open_website(website):
    url = f"https://{website}.com"
    webbrowser.open(url)
    speak(f"Opening {website}.")

# Main function to run assistant
def run_assistant():
    speak("Hello! How can I assist you today?")
    
    while True:
        command = take_command()
        
        # Exit command
        if 'exit' in command or 'stop' in command:
            speak("Goodbye! Have a great day.")
            break

        # Open Notepad
        elif 'open notepad' in command:
            speak("Opening Notepad.")
            os.system("notepad")

        # Open Chrome
        elif 'open chrome' in command:
            speak("Opening Google Chrome.")
            os.system("start chrome")

        # Open MS Word
        elif 'open word' in command:
            speak("Opening Microsoft Word.")
            os.system("start winword")

        # Open MS Excel
        elif 'open excel' in command:
            speak("Opening Microsoft Excel.")
            os.system("start excel")

        # Open MS PowerPoint
        elif 'open powerpoint' in command:
            speak("Opening Microsoft PowerPoint.")
            os.system("start powerpnt")

        # Open YouTube
        elif 'open youtube' in command:
            speak("Opening YouTube.")
            os.system("start chrome www.youtube.com")

        # Open File Explorer
        elif 'open explorer' in command:
            speak("Opening File Explorer.")
            os.system("start explorer")

        # Close Notepad
        elif 'close notepad' in command:
            close_application("notepad")

        # Close Chrome
        elif 'close chrome' in command:
            close_application("chrome")

        # Close MS Word
        elif 'close word' in command:
            close_application("winword")

        # Close MS Excel
        elif 'close excel' in command:
            close_application("excel")

        # Close MS PowerPoint
        elif 'close powerpoint' in command:
            close_application("powerpnt")

        # Close YouTube
        elif 'close youtube' in command:
            
            close_application("chrome")  # Closes Chrome; make sure it's only YouTube tab

        # Weather updates
        elif 'weather in' in command:
            city = command.replace("weather in", "").strip()
            weather_info = get_weather(city)
            speak(weather_info)

        # Telling a joke
        elif 'tell me a joke' in command:
            joke = pyjokes.get_joke()
            speak(joke)

        # Play Music
        elif 'play' in command:
            song_name = command.replace("play", "").strip()
            play_music(song_name)

        # Search a website or open it
        elif 'search for' in command:
            search_query = command.replace("search for", "").strip()
            search_youtube(search_query)
        
        # Open a website directly
        elif 'open' in command:
            website_name = command.replace("open", "").strip()
            open_website(website_name)

        # Default response
        else:
            speak("Sorry, I don't understand that command.")

# Run the assistant
if __name__ == "__main__":
    run_assistant()
