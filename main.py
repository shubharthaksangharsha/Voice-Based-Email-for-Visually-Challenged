from gtts import gTTS
import traceback
import speech_recognition as sr
import psutil as ps
import threading
import os
import time 
import datefinder
import datetime
import struct
import random
import pvporcupine
import pyaudio 
import imaplib
import webbrowser
from email.message import EmailMessage
import smtplib
from email.mime import audio
import email 
from email.header import decode_header
import json 
from store_emails import readEmails, storeEmails, smtp_servers

#converting text to speech 
def speak(text):
    """
    Converts given text to speech using Google Text-to-Speech (gTTS) API, and plays the generated audio file.

    Args:
        text (str): The text to convert to speech.

    Returns:
        None
    """
    speech = gTTS(text=text, lang="en-in", slow=False)
    speech.save("text.mp3")
    os.system("mpg123 text.mp3")

#greeting function
def wishMe():
    '''
    This function greets the user based on the current time by playing an audio file using the os.system() method.

    Returns:
        None
    '''
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        os.system('mpg123 wish_me/good_morning.mp3')
    elif hour >= 12 and hour < 18:
        os.system('mpg123 wish_me/good_afternoon.mp3')
    else:
        os.system('mpg123 wish_me/good_evening.mp3')


#take voice command from the user microphone and convert it into text 
def takeCommand(pause_threshold = 0.6, timeout=5, phrase_time_limit=3):
    """
    This function listens to the user's voice input through the microphone and returns a string output.

    Args:
    pause_threshold (float): The minimum length of silence (in seconds) that is considered the end of a phrase.
    timeout (int): The maximum number of seconds that the function will wait for speech before timing out and returning.
    phrase_time_limit (int): The maximum number of seconds that this function will allow a phrase to continue before stopping and returning the first part of the speech recognized.

    Returns:
    str: The text of the speech recognized from the user's input.

    Raises:
    None
    """
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = pause_threshold
        try:
            audio = r.listen(source,timeout=timeout,phrase_time_limit=phrase_time_limit)
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")
        except Exception as e:
            print("Say that again please...")
            return "None"
    return query

#sending mail 
def sendEmail(to, content):
    '''
    This function sends an email to the specified recipient containing the provided content. It uses the email address and password stored in the operating system's environment variables to authenticate and connect to Gmail's SMTP server. The email's subject is set to "Mail From Voice Assistant" and the sender's email address is also set from the environment variables.
    Params:
        to: email address of the recipient
        content: the message to be sent

    Returns:
        None
    '''
    username = os.environ.get('mymail')
    password = os.environ.get('myapp_pass2')
    domain = username.split('@')[1].split('.')[0]
    server, port = smtp_servers.get(domain)
    msg = EmailMessage()
    msg['Subject'] = 'Mail From Voice Assistant'
    msg['From'] = username
    msg['To'] = to
    msg.set_content(content)
    with smtplib.SMTP_SSL(server, port) as smtp:
        smtp.login(username, password)
        smtp.send_message(msg)
        
def clean(text):
    # clean text for creating a folder
    return "".join(c if c.isalnum() else "_" for c in text)

#reading email
def read_unseen():
    flag = 0
    host = 'imap.gmail.com'
    username = os.environ.get('mymail')
    password = os.environ.get('myapp_pass2')
    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    imap.login(username, password)
    #status, messages = imap.select("INBOX")
    imap.select('INBOX')
    _, messages = imap.search(None, 'UNSEEN')
    speak('reading 2 emails')
    # number of top emails to fetch
    N = 3
    mail_ids = []
    # total number of emails
    for block in messages:
        mail_ids += block.split()
        start_messages = int(mail_ids[0])
        end_messages = int(mail_ids[-1])
    for index, i in enumerate(range(end_messages, start_messages, -1)):
        # fetch the email message by ID
        if index == 2:
            break
        res, msg = imap.fetch(str(i), "(RFC822)")
        for response in msg:
            if isinstance(response, tuple):
                # parse a bytes email into a message object
                msg = email.message_from_bytes(response[1])
                # decode the email subject
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                # if it's a bytes, decode to str
                    subject = subject.decode(encoding)
                # decode email sender
                From, encoding = decode_header(msg.get("From"))[0]
                if isinstance(From, bytes):
                    From = From.decode(encoding)
                print("Subject:", subject)
                print("From:", From)
                speak('mail from : ' + From)
                speak('subject is ' + subject)
                speak('Do you want me to continue reading')
                answer = takeCommand().lower()
                if 'nope' in answer or 'no' in answer:
                    speak('Okay')
                    flag = 1
                    break                    
                # if the email message is multipart
                if msg.is_multipart():
                    print('********shubhi*******')
                    # iterate over email parts
                    for part in msg.walk():
                        # extract content type of email
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))
                        try:
                            # get the email body
                            body = part.get_payload(decode=True).decode()
                        except:
                            print('no body found')
                            pass
                        if content_type == "text/plain" and "attachment" not in content_disposition:
                            print('No attachment only plain texts')
                            pass
                        elif "attachment" in content_disposition:
                            # download attachment
                            print('Contains attachment')
                            filename = part.get_filename()
                            if filename:
                                folder_name = clean(subject)
                                if not os.path.isdir(folder_name):
                                    # make a folder for this email (named after the subject)
                                    os.mkdir(folder_name)
                                filepath = os.path.join(folder_name, filename)
                                # download attachment and save it
                                open(filepath, "wb").write(part.get_payload(decode=True))
                else:
                    print('********shubhi2*******')
                    # extract content type of email
                    content_type = msg.get_content_type()
                    # get the email body
                    body = msg.get_payload(decode=True).decode()
                    if content_type == "text/plain":
                        # print only text email parts
                        print(body)
                        speak("The mail contains")
                        speak(body)
                    if content_type == "text/html":
                        # if it's HTML, create a new HTML file and open it in browser
                        folder_name = clean(subject)
                        if not os.path.isdir(folder_name):
                        # make a folder for this email (named after the subject)
                            os.mkdir(folder_name)
                        filename = "index.html"
                        filepath = os.path.join(folder_name, filename)
                        # write the file
                        open(filepath, "w").write(body)
                        # open in the default browser
                        webbrowser.open(filepath)
                        time.sleep(2)
                        os.system(f'rm -rf {filepath}')
                        os.system(f'rmdir {folder_name}')
                    print("="*100)
                speak('Do you want me to delete this mail')
                answer = takeCommand().lower()
                if 'yes' in answer or 'delete' in answer:
                    imap.store(str(i), '+FLAGS', '\\Deleted')
                    speak('Email deleted successfully')
                    imap.expunge()
                    continue
        if flag == 1:
            break
                
    # close the connection and logout
    imap.close()
    imap.logout()

#run function which triggers when wake word is detected
def run(query):
    if 'read email' in query  or 'read mail' in query:
                        speak('Connecting to mail server')
                        read_unseen()   
    #Send mail to anyone
    elif "send mail" in query or 'sendmail' in query:
                        try:
                            speak('To Who I should send this mail')
                            for i, name in enumerate(emails):
                                print(i, name)
                                if i == 5:
                                    break
                                speak(name)
                            name = takeCommand().lower()
                            if name in emails:
                                to = emails[name]
                                print(f'Sending mail to {name}')
                                speak(f"What should I say to {name}")
                                content = takeCommand()
                                speak("Confirm me yes or no")
                                answer = takeCommand().lower()
                                if 'yes' in answer:
                                    sendEmail(to, content)
                                    speak('Email has been sent!')
                                elif 'no' in answer:
                                    speak('Okay')
                                else:
                                    speak('No response going back')
                            else:
                                speak(f"I'm sorry, {name} is not found in my contacts. Please provide their email address.")
                                email = takeCommand().lower()
                                emails[name] = email
                                storeEmails(emails)
                                speak(f"Email address for {name} has been added to my contacts. What should I say to {name}?")
                                content = takeCommand()
                                speak("Confirm me yes or no")
                                answer = takeCommand().lower()
                                if 'yes' in answer:
                                     sendEmail(email, content)
                                     speak("Email has been sent!")
                                elif 'no' in answer:
                                     speak('Okay')
                                else:
                                     speak("No response, going back")
                        except Exception as e:
                             speak("Sorry, I am not able to send this email at this moment.")
                             print(e)                        
#main function 
if __name__ == '__main__':
    #getting all the stored emails
    emails = readEmails()
    pico_key= os.getenv("pico_key") #getting pocuprine key
    say = ['say/1.mp3', 'say/2.mp3', 'say/3.mp3', 'say/4.mp3'] 
    greet = ['1.mp3', '2.mp3']
    wishMe()
    #Greet
    os.system(f'mpg123 apsara_first_greet/{random.choice(greet)}')
    porcupine = None
    audio_stream = None
    paudio = None
    battery_flag = 0
    try: 
        porcupine = pvporcupine.create(access_key = pico_key, keyword_paths=['./apsara_keyword/ap-sara_en_linux_v2_1_0.ppn','./apsara_keyword/app-sara_en_linux_v2_1_0.ppn', 'apsara_keyword/hey_jarvis.ppn'])
        paudio = pyaudio.PyAudio()
        audio_stream = paudio.open(rate=porcupine.sample_rate, channels=1, format=pyaudio.paInt16, input=True, frames_per_buffer=porcupine.frame_length)
        while True:
            try:
                keyword = audio_stream.read(porcupine.frame_length)
                keyword = struct.unpack_from("h" * porcupine.frame_length, keyword)
                keyword_index = porcupine.process(keyword)
                if (not ps.sensors_battery().power_plugged and int(ps.sensors_battery().percent) < 10):
                    speak('Sir Please charge me')
                    battery_flag = 1
                
                if ps.sensors_battery().power_plugged and battery_flag:
                    speak('Thank you sir')
                    battery_flag = 0
                    
                if keyword_index >= 0:
                    print("Hotword detected")
                    os.system(f'mpg123 {random.choice(say)}')
                    # os.system(f'aplay output4.wav')
                    try:
                        query = takeCommand().lower()
                    except:
                        print("exception occured!!")
                        pass
                    run(query)
            except Exception:
                print(traceback.format_exc())
                print('Unable to understand')
            else:     
                pass
    finally:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paudio is not None:
            paudio.terminate()   