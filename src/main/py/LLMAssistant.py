import tkinter as tk
import threading
import speech_recognition as sr
import time
import pyttsx3
from openai import OpenAI
import sys
import random

global talking
global count
count = 1
talking = False

# Initialize OpenAI with your API key
openai = OpenAI(api_key="sk-proj-qFtAPWc457lOM9emeNXfT3BlbkFJCSHj9Pd74lZeMfubjFaN")

# Initialize speech recognizer and text-to-speech engine
r = sr.Recognizer()
speaker = pyttsx3.init()
listening = False

def record_text():
    while listening:
        try:
            with sr.Microphone() as source2:
                r.adjust_for_ambient_noise(source2, duration=1)
                audio2 = r.listen(source2)
                myText = r.recognize_google(audio2)
                return myText
        except sr.RequestError as e:
            print("unknownRequest")
            continue
        except sr.UnknownValueError:
            print("unknown language")
            display_text("Unknown Language")
            continue
        except sr.WaitTimeoutError:
            print("Listening timed out while waiting for phrase to start")
            time.sleep(1)
            continue
    return

def generate_response():
    global talking
    while listening:
        print("INPUT AVAILABLE")
        hellotext = record_text()
        if hellotext and listening:
            print("INPUT: " + hellotext)
            display_text("INPUT: " + hellotext)
            messages.append({'role': 'user', 'content': hellotext})
            response = openai.chat.completions.create(
                model='gpt-3.5-turbo',
                messages=messages
            )
            messages.append({'role': 'assistant', 'content': response.choices[0].message.content})
            LLMresponse = response.choices[0].message.content
            print("Output: " + LLMresponse)
            talking = True
            talking_animation()
            speaker.say(LLMresponse)
            speaker.runAndWait()
            talking = False
            display_text(" ")
            status_update("(っ ͡ ͡º - ͡ ͡º ς)")
            display_text("LISTENING...")
            sys.stdout.write("\r" + " " * 40 + "\r")  # Clear the line

def start_listening():
    global count, listening
    count += 1
    if count % 2 == 0:
        button_update(0)
        status_update("(..◜ᴗ◝..)")
        listening = True
        threading.Thread(target=generate_response).start()
    else:
        print("listening stopped")
        listening = False
        sleeping_animation(0)
        button_update(1)

def sleeping_animation(num):
    global listening
    if not listening:
        sleepers = ["(っ˕ -｡)     ", "(っ˕ -｡)ᶻ    ","(っ˕ -｡)ᶻ 𝗓  ", "(っ˕ -｡)ᶻ 𝗓 𐰁"]
        status_update(sleepers[num % len(sleepers)])
        root.after(500, lambda: sleeping_animation(num + 1))
        
def talking_animation():
    if talking:
        num = random.randint(0, 4)
        statuses = ["৻( •̀ ᗜ •́ ৻)", "ദ്ദി(˵ •̀ ᴗ - ˵ ) ✧", "( ˶ˆᗜˆ˵ )", "( ˶°ㅁ°)⁭", "( ❛▿❛ )"]
        status_update(statuses[num])
        root.after((num+1)*2400, talking_animation)

def status_update(status):
    status_label.config(text=status)

def display_text(text):
    text_display.config(text=text)

def button_update(num):
    if num == 0:
        start_button.config(text="LISTENING ON", bg="green")
    else:
        start_button.config(text="LISTENING OFF", bg="red")

def exit_program():
    global listening
    listening = False
    root.destroy()
    sys.exit(0)
    quit()

# GUI setup
root = tk.Tk()
root.title("Voice Assistant")

root.attributes('-fullscreen', True)

status_label_font = ("TkFixedFont", 40)
text_font = ("Hack", 25)

exit_button = tk.Button(root, text="Exit", command=exit_program, bg='red')
exit_button.pack(pady=10)


status_label = tk.Label(root, text="(˶ᵔ ᵕ ᵔ˶)", font=status_label_font, anchor='center', justify='center')
status_label.pack(pady=10, fill='x', expand=True)

text_display = tk.Label(root, text=" ", font=text_font)
text_display.pack(pady=10)

start_button = tk.Button(root, text="LISTENING OFF", command=start_listening, bg="red")
start_button.pack(pady=20)

print("BEGIN")
messages = [{'role': 'system', 'content': 'You are a helpful AI assistant, and are interacting with the user over a microphone.'}]
hellotext = "foo"

root.mainloop()
