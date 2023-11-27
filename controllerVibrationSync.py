import sounddevice as sd
import numpy as np
import mouse
from statistics import mean
import time
from selenium import webdriver
import os

def analyze_continuous_real_time_audio():
    # Set parameters for audio input
    sample_rate = 441  # adjust as needed #add or remove a 0 to increase refresh rate # also adjust the decibels lower sample_rate = lower db 44100 default
    mean1 = 0
    threshold = 4
    thresholdDB = 66
    driver = webdriver.Chrome()
    driver.get("file:///C:/Users/dani_/OneDrive/%D0%94%D0%BE%D0%BA%D1%83%D0%BC%D0%B5%D0%BD%D1%82%D0%B8/OneDrive/Documents_and_code/code/html-random-bs/controller-vibrate/dist/index.html")#put here the adress of your page
    disconnected = True
    stop = True
    clicked = False

    # Infinite loop for continuous real-time analysis
    while True:
        # Record real-time audio
        audio_data = sd.rec(2 * sample_rate, channels=2, dtype=np.int16)  # Record 2 seconds of audio
        sd.wait()
        while disconnected:
            time.sleep(3)
            disconnected = False

        # Convert audio to numpy array
        audio_array = np.array(audio_data.flatten())

        # Perform Fourier Transform to get frequencies
        frequencies = np.fft.fftfreq(len(audio_array), 1 / sample_rate)

        # Calculate the magnitude of each frequency component
        magnitudes = np.abs(np.fft.fft(audio_array))

        # Convert magnitude to dB
        magnitudes_db = 20 * np.log10(magnitudes)
        # magnitudes_db = 20 * np.log10(magnitudes)

        # Print the loudness of each frequency in dB
        # for freq, mag_db in zip(frequencies, magnitudes_db):
        #     if(mag_db > 125):
        #         print(f"Frequency: {freq} Hz, Loudness (dB): {mag_db}")
        # print(mean(magnitudes_db[100:300]))
        # np.mean(magnitudes_db[])
        # print(frequencies[50], magnitudes_db[50])
        # print(np.log10(sample_rate))
        meanOld = mean1
        # mean1 = mean(magnitudes_db[50:300])
        mean1 = mean(magnitudes_db[50:1750])
        if(stop):
            meanOld = mean1
            stop = False
        # if(magnitudes_db[100] > 90 or magnitudes_db[125] > 100):
        # if(mean(magnitudes_db[0:800])):
        # print(abs(mean1 - meanOld))
        print(mean(magnitudes_db[50:300]))
        if(abs(mean1 - meanOld) > threshold and disconnected == False): #based on sudden changes in the sound
        # if(mean(magnitudes_db[50:300]) > thresholdDB and disconnected == False): #activates when you reach a cerain volume level
            # mouse.drag(35, 285, 35, 285, absolute=True, duration=0) #scr 1
            if(clicked == False):
                driver.find_element("xpath", "//button[contains(text(),'Go')]").click()#put here the content you have put in Notepad, ie the XPath
                clicked = True
        if(abs(mean1 - meanOld) < threshold and clicked == True): #based on sudden changes in the sound but to turn it off
        # if(mean(magnitudes_db[50:300]) < thresholdDB and clicked == True): #deactivates when you reach a ceratin volume level
            driver.find_element("xpath", "//button[contains(text(),'Stop')]").click()#put here the content you have put in Notepad, ie the XPath
            clicked = False
            # os.popen("curl https://trigger.macrodroid.com/cfbe1ca8-0398-4df3-8d46-25f1bae001ae/vibrate")
            # print("done?")
            stop = True
            # mouse.drag(1635, 285, 1635, 285, absolute=True, duration=0) #scr 2
            # time.sleep(0.05)
            # mouse.click("left")

# Run continuous real-time analysis
analyze_continuous_real_time_audio()