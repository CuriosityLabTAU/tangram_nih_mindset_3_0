from kivy.core.audio import SoundLoader

sound = SoundLoader.load('mytest.wav')
sound = SoundLoader.load('ask_again_0_m.wav')
if sound.length > 0:
    print("Sound found at %s" % sound.source)
    print("Sound is %.3f seconds" % sound.length)
    sound.play()