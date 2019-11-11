import speech_recognition as sr
from subprocess import call
import os


def main():
    # in case of changing a device - change the name of mic - use:
    # print(sr.Microphone.list_microphone_names())
    mic_name = "HDA Intel PCH: ALC233 Analog (hw:0,0)"

    # Sample rate is how often values are recorded
    sample_rate = 48000
    # Chunk is like a buffer. It stores 2048 samples (bytes of data)
    # here.
    chunk_size = 2048
    # Initialize the recognizer
    r = sr.Recognizer()

    # generate a list of all audio cards/microphones
    mic_list = sr.Microphone.list_microphone_names()

    # the following loop aims to set the device ID of the mic that
    # we specifically want to use to avoid ambiguity.
    for i, microphone_name in enumerate(mic_list):
        if microphone_name == mic_name:
            device_id = i

    # use the microphone as source for input. Here, we also specify
    # which device ID to specifically look for incase the microphone
    # is not working, an error will pop up saying "device_id undefined"
    with sr.Microphone(device_index=device_id, sample_rate=sample_rate,
                       chunk_size=chunk_size) as source:
        # wait for a second to let the recognizer adjust the
        # energy threshold based on the surrounding noise level
        r.adjust_for_ambient_noise(source)
        call(["pwd"])
        print("Say Something")
        # listens for the user's input
        audio = r.listen(source)

        try:
            text = r.recognize_google(audio)
            print("you said: " + text)

            # error occurs when google could not understand what was said

            if text == 'exit directory':
                # cd..
                print("cd ..")
                os.chdir("..")
                call(["pwd"])
            elif 'enter directory' in text:
                # cd name of dir extracted from text
                print("cd name")
                call(["cd"])
                call(["pwd"])
            elif text == 'show contents':
                print("ls")
                call(["ls", "-l"])
                call(["pwd"])

        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")

        except sr.RequestError as e:
            print("Could not request results from "
                  "Google Speech Recognition service; {0}".format(e))


if __name__ == "__main__":
    main()