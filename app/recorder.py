import time
import requests
import sounddevice as sd
import soundfile as sf
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pygame
import io

# Check bot muted or not and then execute audio
def monitor_mute_status():
    driver = webdriver.Chrome()
    while True:
        if bot_is_muted(driver):
            # start recording
            audio_data = record_audio()

            # send data to the server
            processed_audio = process_audio(audio_data)
            play_audio(processed_audio,driver)


def bot_is_muted(driver):
    # find mute/unmute button
    mute_button = driver.find_element_by_xpath("//button[@aria-label='Mute microphone']")

    is_muted = mute_button.get_attribute("aria-pressed") == "true"

    return is_muted

def record_audio():
    duration = 60
    fs = 44100
    audio_data = sd.rec(int(duration* fs),samplerate=fs,channels=2,dtype='float64')
    sd.wait()
    return audio_data

def process_audio(audio_data):
    url = 'http://remote-server.com/process-audio'
    response = requests.post(url,data=audio_data)
    processed_audio = response.content
    return processed_audio

def play_audio(audio_data,driver):
    chat_box = driver.find_element_by_xpath("//textarea[@class='chat-box']")
    chat_box.send_keys("Playing processed audio....")
    time.sleep(5)

    pygame.mixer.init()

    audio_stream = io.BytesIO(audio_data)
    sound = pygame.mixer.Sound(audio_stream)

    sound.play()

    pygame.time.wait(int(sound.get_length) * 1000)

    # clean
    pygame.mixer.quit()


monitor_mute_status()


    

