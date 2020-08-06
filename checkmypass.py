import requests
import hashlib
import sys
import pyttsx3  #pip install pyttsx3
import speech_recognition as sr


engine = pyttsx3.init()
engine.setProperty('rate', 190)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('volume', 1)


def voice_change(v):
    x = int(v)
    engine.setProperty('voice', voices[x].id)
    speak("done sir")


#speak function
def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def request_api_data(query_char):
    url="https://api.pwnedpasswords.com/range/"+ query_char
    res=requests.get(url)
    if res.status_code !=200:
        raise RuntimeError(f'Error fetching:{res.status_code},check the api and try again')
    return res

def get_password_leaks_count(hashes,hash_to_check):
    hashes = (line.split(':')for line in hashes.text.splitlines())
    for h,count in hashes:
        if h== hash_to_check:
            return count
    return 0
    
def pwned_api_check(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char,tail = sha1password[:5],sha1password[5:]
    response = request_api_data(first5_char)
    return get_password_leaks_count(response,tail)

def main(args):
    
    password=input ("enter your password:")
    count = pwned_api_check(password)
        # password=input ("enter your password:")
    if count:
        speak(f'{password} was fount  {count} times...you should probably change your password' )
        print(f'{password} was fount  {count} times...you should probably change your password')
    else:
        speak(f"{password} was NOT found.Carrty on !")
        print(f"{password} was NOT found.Carrty on !")
    return 'done!'


if __name__=="__main__":

    sys.exit(main(sys.argv[1:]))

