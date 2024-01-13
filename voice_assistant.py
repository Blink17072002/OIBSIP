import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import webbrowser
import pyjokes
from ecapture import ecapture as ec
import smtplib
import wolframalpha
from urllib.request import urlopen
import json
import requests



listener = sr.Recognizer()
engine = pyttsx3.init()
# Set the voice to that of a female
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id) # This changes this voice to female

def talk(text):
    engine.say(text)
    engine.runAndWait() # This makes the virtual assistant to speak

def take_command():
    try:
        with sr.Microphone() as source:
            print('listening...')
            voice = listener.listen(source)
            command = listener.recognize_google(voice).lower()
            
            if 'sophia' in command:
                command = command.replace('sophia', '')
                print(command)


    except Exception as e:
        print(e)
        print('Unable to recognize your voice.')
        return 'None'
    
    return command


def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
     
    # Enable low security in gmail
    server.login('your email', 'password')
    server.sendmail('email', to, content)
    server.close()


def run_sophia():
    while True:
        command = take_command()
        if 'exit' in command or 'stop' in command or 'goodbye' in command:
            print("Goodbye!")
            talk("Goodbye!")
            break

        elif 'play' in command:
            song = command.replace('play', '')
            talk('playing' + song)
            pywhatkit.playonyt(song)

        elif 'the time' in command:
            time = datetime.datetime.now().strftime('%I:%M %p')
            print(time)
            talk('The time is ' + time)
            
        elif 'search' in command or 'wikipedia' in command:
            try:
                talk('Searching Wikipedia...')
                # Removing the trigger word 'search' or 'wikipedia' from the command
                if 'search' in command:
                    command = command.replace('search', '')
                elif 'wikipedia' in command:
                    command = command.replace('wikipedia', '')
                # Searching Wikipedia for the query
                results = wikipedia.summary(command, sentences=3)
                talk('According to Wikipedia')
                print(results)
                talk(results)
            except wikipedia.exceptions.DisambiguationError as e:
                talk('Your search query led to a disambiguation page. Please be more specific.')
            except wikipedia.exceptions.PageError:
                talk('Sorry, I could not find any Wikipedia page for that query.')
            except Exception as e:
                talk('An error occurred while trying to search Wikipedia.')


        elif 'open youtube' in command:
            talk("Here's Youtube\n")
            webbrowser.open('youtube.com')

        elif 'open google' in command:
            talk("Here's Google\n")
            webbrowser.open('google.com')

        elif 'send an email' in command:
            try:
                talk("Sure! What's the content of the email?")
                email_content = take_command()
                receipient = 'your_email_address'    
                sendEmail(receipient, email_content)
                talk("Email sent successfully!")
            except Exception as e:
                print(e)
                talk("I am not able to send this email")

        elif 'open youtube' in command:
            talk("Here you go to Youtube\n")
            webbrowser.open("youtube.com")

        elif 'open google' in command:
            talk("Here you go to Google\n")
            webbrowser.open("google.com")

        elif "calculate" in command:  
            try:          
                app_id = "Wolframalpha api id"
                client = wolframalpha.Client(app_id)
                indx = command.lower().split().index('calculate') 
                command = command.split()[indx + 1:] 
                res = client.query(' '.join(command)) 
                answer = next(res.results).text
                print("The answer is " + answer) 
                command("The answer is " + answer) 
            except Exception as e:
                print(e)
                talk("I am not able to calculate it.")

        elif 'news' in command:
            try:
                jsonObj = urlopen('''https://newsapi.org/v2/everything?domains=wsj.com&apiKey=api_key''')
                data = json.load(jsonObj)
                i = 1

                talk('Here are the top 10 news in the US')

                # Modify the loop condition to iterate through the first 10 articles
                for item in data['articles'][:10]:
                    print(str(i) + '. ' + item['title'] + '\n')
                    print(item['description'] + '\n')
                    talk(str(i) + '. ' + item['title'] + '\n')
                    i += 1

                talk('Do you want more news?')
                more_news_command = take_command()

                if 'yes' in more_news_command:
                    talk('How many more news articles do you want?')
                    try:
                        additional_news_count = int(take_command())
                    except ValueError:
                        talk('Invalid number. Please try again.')
                        return

                    for item in data['articles'][10:10+additional_news_count]:
                        print(str(i) + '. ' + item['title'] + '\n')
                        print(item['description'] + '\n')
                        talk(str(i) + '. ' + item['title'] + '\n')
                        i += 1
                else:
                    talk('Alright, thank you for your time.')

            except Exception as e:
                talk('Sorry, I cannot process that!')
                print(str(e))

        
        elif "don't listen" in command or "stop listening" in command:
            talk("for how much time you want to stop jarvis from listening commands")
            a = int(take_command())
            time.sleep(a)
            print(a)

        elif "camera" in command or "take a photo" in command or 'take a picture' in command:
            talk('taking photo')
            ec.capture(0, "Sophia Camera ", "img.jpg")
            talk('photo taken')

        elif "write a note" in command:
            talk("What should i write, sir")
            note = take_command()
            file = open('sophia.txt', 'w')
            talk("Sir, Should i include date and time")
            snfm = take_command()
            if 'yes' in snfm or 'sure' in snfm:
                strTime = datetime.datetime.now().strftime("% H:% M:% S")
                file.write(strTime)
                file.write(" :- ")
                file.write(note)
            else:
                file.write(note)
            
        elif "show note" in command:
            talk("Showing Notes")
            file = open("sophia.txt", "r") 
            print(file.read())
            talk(file.read(6))


        elif "weather" in command:
            api_key = 'your_api_key'
            base_url = "http://api.openweathermap.org/data/2.5/weather?"
            talk("City name:")
            print("City name:")
            city_name = take_command()
            complete_url = base_url + "appid=" + api_key + "&q=" + city_name
            response = requests.get(complete_url)
            
            if response.status_code == 200:
                weather_data = response.json()
                if weather_data["cod"] != "404":
                    main_data = weather_data["main"]
                    current_temperature = main_data["temp"]
                    current_pressure = main_data["pressure"]
                    current_humidity = main_data["humidity"]
                    weather_description = weather_data["weather"][0]["description"]
                    print('Here is the weather report of ' + city_name)
                    talk('Here is the weather report of ' + city_name)
                    print("Temperature (in kelvin unit) = " + str(current_temperature) + "\nAtmospheric pressure (in hPa unit) = " + str(current_pressure) + "\nHumidity (in percentage) = " + str(current_humidity) + "\nDescription = " + str(weather_description))
                    talk("Temperature (in kelvin unit) = " + str(current_temperature) + "\nAtmospheric pressure (in hPa unit) = " + str(current_pressure) + "\nHumidity (in percentage) = " + str(current_humidity) + "\nDescription = " + str(weather_description))
                else:
                    talk("City not found.")
            else:
                talk("Unable to fetch weather data. Please try again later.")

        elif 'joke' in command:
            joke = pyjokes.get_joke()
            print(joke)
            talk(joke)

        elif 'what is your name' in command or 'your name' in command or 'what are you called' in command or 'what should I call you' in command:
            response = 'You can call me Sophia. I am your personal voice assistant!'
            print(response)
            talk(response)

        talk("Is there anything else you want me to do?")
        
        # Wait for the user's response
        response = take_command().lower()
        if 'no' in response or 'nothing' in response or "that's all" in response:
            print("Thank you for the time. See you soon!.")
            talk("Thank you for the time. See you soon!.")
            break

        

run_sophia()