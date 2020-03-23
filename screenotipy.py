#!/usr/bin/env python

from queue import Queue
import os
import time
from PIL import Image, ImageChops
from pyscreenshot import grab
from pydub import AudioSegment
from pydub import playback
import configparser


def starting():
    print("Starting in...", end=' ')
    for i in range(_initial_delay, 0, -1):
        if i == 1:
            print(i)
        else:
            print(i, end=' ')
        time.sleep(1)


def strtobool(s):
    if s.lower() == "true":
        return True
    else:
        return False


config = configparser.ConfigParser()
config.read('config.ini')
_audio_wav_name = config['config']['audio_wav_name']
_capture_delay = int(config['config']['capture_delay'])
_initial_delay = int(config['config']['initial_delay'])
_non_stop_audio = strtobool(config['config']['non_stop_audio'])
_delete_images = strtobool(config['config']['delete_images'])

print(_non_stop_audio)
print(_delete_images)

starting()

# storing this image and the previous image
q = Queue(maxsize=2)

audio = AudioSegment.from_wav(_audio_wav_name)

print("Audio duration: ", audio.duration_seconds)

while True:
    if q.qsize() == 2:
        image1 = q.get()
        image2 = q.get()
        result = ImageChops.difference(Image.open(image1), Image.open(image2))

        if _delete_images:
            print("deleting...", _delete_images)
            os.remove(image1)
            os.remove(image2)

        if result.getbbox() is not None:
            print(result.getbbox())

            playback.play(audio)
            print("Press any key to continue:")
            input()
            starting()
        else:
            pass
    else:
        im = grab()
        fileName = 'screenshot-' + str(int(time.time())) + '.png'
        im.save(fileName)
        q.put(fileName)
        if q.qsize() == 1:
            print("Waiting for next screenshot...")
            time.sleep(_capture_delay)
