import os
from kivy.core.audio import SoundLoader

sound = SoundLoader.load('mytest.wav')
sound = SoundLoader.load('ask_again_0_m.wav')

sounds_list = os.listdir("./tablet_app/sounds/wav_tangram")

print(sounds_list)
if sound.length > 0:
    print("Sound found at %s" % sound.source)
    print("Sound is %.3f seconds" % sound.length)
    sound.play()