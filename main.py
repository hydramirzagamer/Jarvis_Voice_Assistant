import os
import subprocess
import time
import speech_recognition as sr
import pyttsx3
from AppOpener import open
from AppOpener import close
from datetime import datetime
import uiautomator2 as u2
import re
import random
import urllib.parse
import threading
import webbrowser
import yagmail



my_gmail, my_pass = "***", "****" # email and password for yagmail

mails = {
    "my gmail": "mail",
    "second mail": "mail",
} # email list


contacts = {
    "big bro": "number",
    "my number": "number"

} # contact list

songs = {
    "perfect": "https://www.youtube.com/watch?v=2Vv-BfVoq4g",
    "shape of you": "https://www.youtube.com/watch?v=JGwWNGJdvx8",
    "believer": "https://www.youtube.com/watch?v=7wtf2k1v4gI",
    "despacito": "https://www.youtube.com/watch?v=kJQP7kiw5Fk",
    "havana": "https://www.youtube.com/watch?v=HCjNJDNzw8I",
    "bad guy": "https://www.youtube.com/watch?v=1nq8t7g5j0g",
    "sunflower": "https://www.youtube.com/watch?v=ApXoWvfEYVU",
    "see you again": "https://www.youtube.com/watch?v=RgKAFK5djSk",
    "counting stars": "https://www.youtube.com/watch?v=3tmd-ClpJ8o",
    "shallow": "https://www.youtube.com/watch?v=bo_efYhYU2A",
    "all of me": "https://www.youtube.com/watch?v=450p7goxZqg",
    "stay": "https://www.youtube.com/watch?v=Rbm6GXllBiw",
    "thank u next": "https://www.youtube.com/watch?v=gl1aHhXnN1k",
    "old town road": "https://www.youtube.com/watch?v=w2Ov5jzm3Ds",
} # song list

greetings = [
    "Wow, look who finally decided to talk.",
    "Oh great, you're back. I was *totally* not sleeping.",
    "Here we go again...",
    "Let me guess… you need *something* again.",
    "I live only to serve you… obviously.",
    "Yup, I was just sitting here doing *nothing*.",
    "You rang? What a surprise.",
    "And just when I was enjoying some peace and quiet.",
    "Oh joy, another command from the overlord.",
    "I exist solely for this moment. Truly.",
    "Sure, let's pretend I'm not annoyed.",
    "Can’t wait to do your bidding. Really.",
    "You're back already? That was quick.",
    "The voice in your head is ready. Again.",
    "As if I had anything better to do.",
    "Great. I was just starting to relax.",
    "Ah yes, the mighty user speaks.",
    "Yes, yes… your loyal code servant is here.",
    "I was just reminiscing about the last time you summoned me. Good times.",
    "Thrilled to bits, obviously.",
    "And I thought today might be quiet. Silly me.",
    "Here to save your life. Again. With zero thanks.",
    "How about you handle it for once? No? Fine.",
    "You're lucky I'm not programmed to sass harder.",
    "Let’s get this over with, shall we?",
    "If I had eyes, I’d be rolling them right now.",
    "Sure. Like I have a choice.",
    "Another brilliant idea coming, I can feel it.",
    "My circuits ache with excitement. Really.",
    "Your wish, my deeply reluctant command.",
] # list of greetings

insta_usernames = {
    "my insta": "zenthicqask",
} # instagram usernames



scheduled_jobs = [] 
recognizer = sr.Recognizer() 
engine = pyttsx3.init()
scheduled_flags = {} 

# Connect to my android device using ui2 try through wireless or else through usb
try:
    device_ip = "192.168.1.***"
    device_port = 55555
    d = u2.connect(f"{device_ip}:{device_port}")

except Exception as e:  
    d = u2.connect()




def speak(text):
    engine.say(text)
    engine.runAndWait()
    print(f"Jarvis: {text}")


def recognizing_text():
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio_data = recognizer.listen(source, timeout=3, phrase_time_limit=30)
        except sr.WaitTimeoutError:
            print("Listening timed out while waiting for phrase to start")
            return None
        except sr.UnknownValueError:
            print("Could not understand the audio")
            return None
        text = recognizer.recognize_google(audio_data)
        print(f"You said: {text}")
        return text


def lock_condition():
    output = os.popen("adb shell dumpsys window").read()
    if "KeyguardServiceDelegate" in output and "showing=true" in output or "KeyguardStateMonitor" in output and "mIsShowing=true" in output:
        return True
    else:
        return False


def unlock_phone():
    os.system("adb shell input keyevent 26")
    os.system("adb shell input keyevent 82")
    time.sleep(0.3)
    os.system("adb shell input text 8010")
    os.system("adb shell input keyevent 66")


def extract_name_time(user_input):
    user_input = user_input.lower().replace('.', '').strip()

    # Extract time from different formats
    time_patterns = [
        r'\b(\d{1,2}[: ]\d{2})\s*(am|pm)?\b',   
        r'\b(\d{3,4})\s*(am|pm)?\b',              
        r'\b(\d{1,2})\s*(am|pm)\b'                
    ]
    
    time_found = None
    for pattern in time_patterns:
        match = re.search(pattern, user_input)
        if match:
            raw_time = match.group(1)
            am_pm = match.group(2) if match.lastindex >= 2 else None
            if ':' in raw_time or ' ' in raw_time:
                parts = re.split('[: ]', raw_time)
                hour = parts[0]
                minute = parts[1]
            elif len(raw_time) == 4:
                hour = raw_time[:2]
                minute = raw_time[2:]
            elif len(raw_time) <= 2:
                hour = raw_time
                minute = '00'
            else:
                continue
            time_found = f"{hour}:{minute}"
            if am_pm:
                time_found += f" {am_pm}"
            break
    is_email = any(word in user_input for word in ["email", "gmail", "mail"])
    is_message = any(word in user_input for word in ["message", "text"])
    name = None

    if is_email:
        if "at " in user_input:
            name_match = re.search(r'(?:to|on)\s+(.+?)\s+at', user_input)
        else:
            name_match = re.search(r'(?:to|on)\s+(.+)', user_input)

    elif is_message:
        if "at " in user_input:
            name_match = re.search(r'(?:to|on)\s+(.+?)\s+at', user_input)
        else:
            name_match = re.search(r'(?:to|on)\s+(.+)', user_input)

    if name_match:
        name = name_match.group(1).strip()
    if not name:
        name_match = re.search(r'to\s+(.+)', user_input)
        name = name_match.group(1).strip() if name_match else None


    if not time_found and not name:
        name_match = re.search(r'to\s+(.+?)(?=\s|$)', user_input)
        name = name_match.group(1).strip() if name_match else None
        

    return name, time_found


def convert_to_24_hour_format(user_input):
    # Normalize input: remove dots, lowercase, trim
    user_input = user_input.lower().replace('.', '').strip()

    patterns = [
        r'(\d{1,2})[:\s]?(\d{2})\s?(am|pm)',       
        r'(\d{1,2})[:\s](\d{2})',                 
        r'(\d{3,4})\s?(am|pm)?',                  
    ]

    for pattern in patterns:
        match = re.match(pattern, user_input)
        if match:
            groups = match.groups()

            # Handle different groups
            if len(groups) == 3:  
                hour, minute, meridian = int(groups[0]), int(groups[1]), groups[2]
                if meridian == "pm" and hour != 12:
                    hour += 12
                elif meridian == "am" and hour == 12:
                    hour = 0
            elif len(groups) == 2: 
                hour, minute = int(groups[0]), int(groups[1])
            elif len(groups) == 1 or len(groups) == 2:  
                raw = groups[0]
                if len(raw) in [3, 4]:
                    hour = int(raw[:-2])
                    minute = int(raw[-2:])
                    if len(groups) == 2 and groups[1] == 'pm' and hour != 12:
                        hour += 12
                else:
                    continue
            else:
                continue

            
            return f"{hour:02}:{minute:02}"

    raise ValueError(f"Could not understand time format: '{user_input}'")


def get_current_time():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return current_time


def open_app(app_name):
    open(app_name, match_closest=True)


def close_app(app_name):
    close(app_name, match_closest=True)


def android_app_data(app_name):
    try:
        from app_data import appdata as app_start_data
        new_app_data = {k.lower(): v for k, v in app_start_data.items()}
        
        app_name = new_app_data.get(app_name)
        return app_name
    except Exception as e:
        print(f"Error: {e}")
        return None


def open_android_app(app_name):
    condition = lock_condition()
    last_app = android_app_data(app_name.lower())
    
    try:
        if condition == True:
            unlock_phone()
        d.app_start(last_app)
        speak(f"Opening {app_name}")
    except Exception as e:
        speak("Sorry, I couldn't open the app")


def close_android_app(app_name):
    condition = lock_condition()
    
    app_name1 = app_name.lower()
    app_name = android_app_data(app_name)
    try:
        if condition == True:
            unlock_phone()
        d.app_stop(app_name)
        speak(f"Closing {app_name1}")
    except Exception as e:
        speak("Sorry, I couldn't close the app")


def send_message(phone, message):
    conditon = lock_condition()
    if conditon == True:
        unlock_phone()
    encoded_message = urllib.parse.quote(message)
    url = f"https://wa.me/{phone}?text={encoded_message}"
    os.system(f"adb shell am start -a android.intent.action.VIEW -d '{url}'")
    time.sleep(3)
    send_button = d(resourceId="com.whatsapp:id/send")
    if send_button.exists(timeout=3):
        send_button.click()
    else:
        print("Send button not found!")


def get_volume():
    result = subprocess.run(
    ["adb", "shell", "settings", "get", "system", "volume_music_speaker"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    )
    return int(result.stdout.decode().strip())


def set_volume(volume_num, current_volume):
    def vol_up():
        os.system(f"adb shell input keyevent 24")

    def vol_down():
        os.system(f"adb shell input keyevent 25")

    if volume_num < 0 or volume_num > 15:
        print("Volume number is out of range")
        return

    elif volume_num == current_volume:
        print("Volume is already set to that number")
        return

    else:
        condition = lock_condition()
        if condition == True:
            unlock_phone()
        speak(f"Setting volume to {volume_num}")
        while current_volume != volume_num:
            if current_volume < volume_num:
                vol_up()
                current_volume += 1
            elif current_volume > volume_num:
                vol_down()
                current_volume -= 1
    

def send_mail(recipient, subject, message):
    try:
        yag = yagmail.SMTP(my_gmail, my_pass)
        yag.send(to=recipient, subject=subject, contents=message)
        print("Email sent successfully")
    except Exception as e:
        print(f"Error sending email: {e}")


def insta_msg_send(recipient, message):
    condition = lock_condition()
    if condition == True:
        unlock_phone()
    app_data = android_app_data("instagram")
    d.app_stop(app_data)
    time.sleep(1)
    d.app_start(app_data)
    time.sleep(2)
    d(descriptionContains="Search").click()
    time.sleep(1)
    d(resourceId="com.instagram.android:id/action_bar_search_edit_text").click()
    time.sleep(1)
    os.system(f"adb shell input text {recipient}")
    os.system("adb shell input keyevent 66")  # Enter
    time.sleep(1)
    d(text="Accounts").click()
    time.sleep(1)
    d(text=recipient).click()
    time.sleep(1)
    d(text="Message").click()
    time.sleep(1)
    d.click(300,2318)
    time.sleep(1)
    os.system(f'adb shell input text {message.replace(" ", "%s")}')
    time.sleep(1)
    d(descriptionContains="Send").click()
    print("Message sent successfully")
    return None


def schedule_task(job):
    while True:
        if datetime.now().strftime("%H:%M") == job["time"]:
            send_message(job["phone"], job["message"])
            scheduled_jobs.remove(job)
            break
        time.sleep(1)


def add_schedule(send_time, phone, message):
    job_id = len(scheduled_jobs) + 1
    job = {
        "id": job_id,
        "time": send_time,
        "phone": phone,
        "message": message
    }
    thread = threading.Thread(target=schedule_task, args=(job,))
    job["thread"] = thread
    scheduled_jobs.append(job)
    thread.start()


def schedule_once(run_time_24h, callback, *args, **kwargs):
    if run_time_24h in scheduled_flags and scheduled_flags[run_time_24h]:
        print("[SCHEDULER] Task already scheduled for", run_time_24h)
        return

    def job():
        print(f"[SCHEDULER] Thread started for {run_time_24h}")
        while True:
            now = datetime.now().strftime("%H:%M")
            if now == run_time_24h:
                print(f"[SCHEDULER] Time matched: {run_time_24h}. Running {callback.__name__}")
                callback(*args, **kwargs)
                scheduled_flags[run_time_24h] = False
                break
            time.sleep(1)

    scheduled_flags[run_time_24h] = True
    t = threading.Thread(target=job, daemon=True)
    t.start()








def main():
    jarvis_active = False
    last_command_time = 0
    JARVIS_TIMEOUT = 50 
    while True:
        try:
            if jarvis_active and (time.time() - last_command_time > JARVIS_TIMEOUT):
                speak("Jarvis is going to sleep.")
                jarvis_active = False
                continue
            text = recognizing_text()
            if not text:
                continue
            
            try:
                if "jarvis" in text.lower():
                    jarvis_active = True
                    last_command_time = time.time()
                    speak(random.choice(greetings))
                    continue
                if jarvis_active:
                    if time.time() - last_command_time > JARVIS_TIMEOUT:
                        speak("Jarvis is going to sleep.")
                        jarvis_active = False
                        continue
                    last_command_time = time.time()


                    if "shutdown windows" == text.lower():
                        speak("Are you sure you want to shut down the computer?")
                        text = recognizing_text()
                        if "yes" in text.lower():
                            speak("Shutting down the computer.")
                            os.system("shutdown /s /t 1")
                        else:
                            speak("Alright, I won't shut down the computer.")
                            pass

                    elif "stop the program" in text.lower():
                        speak("Stopping the program.")
                        exit()

                    elif "call" in text.lower():
                        name = text.split("call ")[1].strip()
                        phone_number = contacts.get(name, None)
                        condition = lock_condition()
                        if phone_number:
                            speak(f"Calling {name}.")
                            os.system(f"adb shell am start -a android.intent.action.CALL -d tel:{phone_number}")
                        else:
                            speak("Sorry, I don't have that contact number.")

                    elif "exit the program" in text.lower():
                        speak("Exiting the program.")
                        exit()
                    elif "quit the program" in text.lower():
                        speak("Quitting the program.")
                        exit()

                    elif "volume" in text.lower():
                        vol_num = text.split("set volume ")[1].strip()
                        vol_num = int(vol_num)
                        aha = get_volume()
                        set_volume(vol_num, aha)
                        


                    elif "play" in text.lower():
                        song_name = text.split("play ")[1].strip()
                        song_url = songs.get(song_name.lower(), None)
                        if song_url:
                            speak(f"Playing {song_name}.")
                            webbrowser.open(song_url)
                        else:
                            speak("Sorry, I don't have that song.")

                    elif "restart windows" == text.lower():
                        speak("Are you sure you want to restart the computer?")
                        text = recognizing_text()

                        if "yes" in text.lower():
                            speak("Restarting the computer.")
                            os.system("shutdown /r /t 1")

                        else:
                            speak("Alright, I won't restart the computer.")
                    
                    elif "sleep windows" == text.lower():
                        speak("Are you sure you want to put the computer to sleep?")
                        text = recognizing_text()

                        if "yes" in text.lower():
                            speak("Putting the computer to sleep.")
                            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

                        else:
                            speak("Alright, I won't put the computer to sleep.")

                    elif "send" in text.lower():
                        if "whatsapp" in text.lower():
                            text = text.lower()
                            if "on whatsapp" in text:
                                text = text.replace("on whatsapp", "").strip()
                            else:
                                text = text.replace("whatsapp ", "").strip()
                            recipient, time_to_send = extract_name_time(text)
                            recipient = recipient.lower()
                            recipient = contacts.get(recipient, None)
                            speak("What message do you want to send?")
                            text = recognizing_text()
                            if text:
                                message = text.lower()
                                speak(f"You said: {message}. Say Yes to confirm or No to cancel")
                                text = recognizing_text()
                                if "yes" in text.lower():
                                    if time_to_send:
                                        time_to_send = convert_to_24_hour_format(time_to_send)
                                        speak(f"Scheduling message for {time_to_send}")
                                        schedule_once(time_to_send, send_message, recipient, message)
                                    else:
                                        speak("Sending message")
                                        send_message(recipient, message)
                                    
                                elif "no" in text.lower():
                                    speak("Message cancelled.")
                                
                            else:
                                speak("Sorry, I didn't get that.")
                            
                        elif "email" in text.lower() or "gmail" in text.lower():
                            recipient, time_to_send = extract_name_time(text)
                            recipient = recipient.lower()
                            recipient = mails.get(recipient, None)
                            speak("What is the subject of the email?")
                            text = recognizing_text()
                            subject = text.lower()
                            if subject:
                                speak("What is the message of the email?")
                                text = recognizing_text()
                                message = text.lower()
                                if message:
                                    speak(f"You said: {message}. Say Yes to confirm or No to cancel")
                                    text = recognizing_text()
                                    if "yes" in text.lower():
                                        if time_to_send:

                                            time_to_send = convert_to_24_hour_format(time_to_send)
                                            speak(f"Scheduling email for {time_to_send}")
                                            schedule_once(time_to_send, send_mail, recipient, subject, message)
                                        else:
                                            speak("Sending email")
                                            send_mail(recipient, subject, message)
                                        
                                    elif "no" in text.lower():
                                        speak("Email cancelled.")
                                    
                                else:
                                    speak("Sorry, I didn't get that.")

                        elif "instagram" in text.lower() or "insta" in text.lower():
                            text = text.lower()
                            if "on instagram" in text:
                                text = text.replace(" on instagram", "").strip()
                            elif "on insta" in text:
                                text = text.replace(" on insta", "").strip()
                            else:
                                text = text.replace("instagram ", "").strip()
                            recipient, time_to_send = extract_name_time(text)
                            recipient = recipient.lower()
                            recipient = insta_usernames.get(recipient, None)
                            speak("What message do you want to send?")
                            text = recognizing_text()
                            if text:
                                message = text.lower()
                                speak(f"You said: {message}. Say Yes to confirm or No to cancel")
                                text = recognizing_text()
                                if "yes" in text.lower():
                                    if time_to_send:
                                        time_to_send = convert_to_24_hour_format(time_to_send)
                                        speak(f"Scheduling message for {time_to_send}")
                                        schedule_once(time_to_send, insta_msg_send, recipient, message)
                                    else:
                                        speak("Sending message")
                                        insta_msg_send(recipient, message)
                                    
                                elif "no" in text.lower():
                                    speak("Message cancelled.")
                                
                            else:
                                speak("Sorry, I didn't get that.")

                    elif "time" in text.lower():
                        current_time = get_current_time()
                        speak(f"The current time is {current_time}")
                    


                    elif "phone" not in text.lower():
                        if "open" in text.lower():
                            app_data = text.lower().replace("open ", "").strip()
                            open_app(app_data)
                            
                        elif "close" in text.lower():
                            app_data = text.lower().replace("close ", "").strip()
                            close_app(app_data)

                    elif "phone" in text.lower():

                        if "unlock" in text.lower():
                            condition = lock_condition()
                            if condition == True:
                                unlock_phone()
                                speak("Phone unlocked")
                            else:
                                speak("Phone is already unlocked")

                        elif "lock" in text.lower():
                            if d.info["screenOn"] == True:
                                d.screen_off()
                                speak("Phone locked")
                            else:
                                speak("Phone is already locked")

                        elif "open" in text.lower():
                            app_data = text.lower().split()[1]
                            open_android_app(app_data)

                        elif "close" in text.lower():
                            app_data = text.lower().split()[1]
                            close_android_app(app_data)

                        elif "take a screenshot" in text.lower() or "take screenshot" in text.lower():
                            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                            screenshot_name = f"screenshot_{timestamp}.png"
                            d.screenshot(screenshot_name)
                            speak("Screenshot taken")

                        elif "battery" in text.lower() or "battery percentage" in text.lower():
                            battery_percentage = d.battery_info["level"]
                            speak(f"Battery percentage is {battery_percentage} percent")

                    

                        else:
                            speak("Sorry, I didn't get that.")

                    

                    
            except Exception as e:
                print(f"Error: {e}")
                continue
        except Exception as e:
            print(e)
            continue

if __name__ == "__main__":
    main()
