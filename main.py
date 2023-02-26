from gtts import gTTS
import traceback
import speech_recognition as sr
import psutil as ps
import threading
from pulsectl import Pulse, PulseVolumeInfo
import os
import schedule
import datefinder
import datetime
import struct
import random
import pvporcupine
import pyaudio 
import imaplib
from email.message import EmailMessage
import smtplib
from email.mime import audio
import email 
from email.header import decode_header


emails = {'myself': 'shubharthaksangharsha@gmail.com', 'mummy': 'usharani20jan@gmail.com', 'bro': 'siddhant3s@gmail.com', 'bhabhi':'ahuja.chaks@gmail.com', 'pranchal': 'pranchal018@gmail.com', 'pranjal': 'pranchal018@gmail.com'}

def speak(text):
    speech = gTTS(text=text, lang="en-in", slow=False)
    speech.save("text.mp3")
    os.system("mpg123 text.mp3")

#greeting function
def wishMe():
    '''
    It wishes the User according the time and return the file which played using os.system()
    '''
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        os.system('mpg123 wish_me/good_morning.mp3')
    elif hour >= 12 and hour < 18:
        os.system('mpg123 wish_me/good_afternoon.mp3')
    else:
        os.system('mpg123 wish_me/good_evening.mp3')


#take command from the user
def takeCommand():
    '''
    It takes microphone input from the user and returns string output
    '''
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 0.5
        try:
            audio = r.listen(source,timeout=1,phrase_time_limit=2)
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")
        except Exception as e:
            print("Say that again please...")
            return "None"
    return query
#for news
def takeCommand2():
    '''
    It takes microphone input from the user and returns output
    '''
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 0.6
        try:
            audio = r.listen(source,phrase_time_limit=2, timeout = 6)
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")
        except Exception as e:
            print("Say that again please")
            return "exception"
    return query
    
def takeCommand3():
    '''
    It takes microphone input from the user and returns string output
    '''
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 0.6
        try:
            audio = r.listen(source,phrase_time_limit=6, timeout = 6)
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")
        except Exception as e:
            print("Say that again please")
            return "exception"
    return query
def takeCommand4():
    '''
    It takes microphone input from the user and returns string output
    '''
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 0.6
        try:
            audio = r.listen(source,phrase_time_limit = 10,timeout = 10)
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")
        except Exception as e:
            print("Say that again please")
            return "exception"
    return query
def takeCommand5():
    '''
    It takes microphone input from the user and returns string output
    '''
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print('takeCommand5')
            print("Listening...")
            r.pause_threshold = 0.6
            audio = r.listen(source,phrase_time_limit = 5,timeout = 3)
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")
    except Exception as e:
            print("Say that again please")
            print(e)
            return ""
    return query

#sending mail 
def sendEmail(to, content):
    username = os.environ.get('mymail')
    password = os.environ.get('myapp_pass2')
    msg = EmailMessage()
    msg['Subject'] = 'Mail From Apsara AI'
    msg['From'] = username
    #msg['To'] = username
    msg['To'] = to
    msg.set_content(content)
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
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
                speak(str(index+1) + 'mail from : ' + From)
                speak('subject is ' + subject)
                speak('Do you want me to continue reading')
                answer = takeCommand3().lower()
                if 'nope' in answer or 'no' in answer:
                    speak('Okay')
                    flag = 1
                    break                    
                # if the email message is multipart
                if msg.is_multipart():
                    # iterate over email parts
                    for part in msg.walk():
                        # extract content type of email
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))
                        try:
                            # get the email body
                            body = part.get_payload(decode=True).decode()
                        except:
                            pass
                        if content_type == "text/plain" and "attachment" not in content_disposition:
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
                    # extract content type of email
                    content_type = msg.get_content_type()
                    # get the email body
                    body = msg.get_payload(decode=True).decode()
                    if content_type == "text/plain":
                        # print only text email parts
                        print(body)
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
        if flag == 1:
            break
                
    # close the connection and logout
    imap.close()
    imap.logout()





def run(query):
    if 'read email' in query  or 'read mail' in query:
                        speak('Connecting to mail server')
                        read_unseen()   
    #Send mail to anyone
    elif "send mail" in query or 'sendmail' in query:
                        try:
                            speak('To Who I should send this mail')
                            answer = takeCommand2().lower()
                            if 'mummy' in answer:
                                speak("What should I say")
                                content = takeCommand2().lower()
                                to = emails['mummy']
                                speak('Confirm me yes or no')
                                answer = takeCommand2().lower()
                                if 'yes' in answer:
                                    sendEmail(to, content)
                                    speak('Email has been sent!')
                                elif 'no' in answer:
                                    speak('Okay')
                                else:
                                    speak('No response going back')
                            elif 'bro' in answer:
                                speak("What should I say")
                                content = takeCommand2()
                                to = emails['bro']
                                speak('Confirm me yes or no')
                                answer = takeCommand2().lower()
                                if 'yes' in answer:
                                    sendEmail(to, content)
                                    speak('Email has been sent!')
                                elif 'no' in answer:
                                    speak('Okay')
                                else:
                                    speak('No response going back')
                            elif 'myself' in answer:
                                speak("What should I say")
                                content = takeCommand5()
                                to = emails['myself']
                                speak('Confirm me yes or no')
                                answer = takeCommand2().lower()
                                if 'yes' in answer:
                                    sendEmail(to, content)
                                    speak('Email has been sent!')
                                elif 'no' in answer:
                                    speak('Okay')
                                else:
                                    speak('No response going back')
                                    speak('No response going back')
                            elif 'pranchal' in answer or 'pranjal' in answer:
                                speak("What should I say")
                                content = takeCommand5()
                                to = emails['pranchal']
                                speak('Confirm me yes or no')
                                answer = takeCommand2().lower()
                                if 'yes' in answer:
                                    sendEmail(to, content)
                                    speak('Email has been sent!')
                                elif 'no' in answer:
                                    speak('Okay')
                                else:
                                    speak('No response going back')
                        except:
                            speak('Sorry my friend. I am not able to send this email at this moment')  

               


if __name__ == '__main__':
    pico_key= os.getenv("pico_key")
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
                schedule.run_pending()
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
                        query = takeCommand5().lower()
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

