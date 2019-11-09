import speech_recognition as sr
import random
import time
import speech_recognition as sr


def recognize_speech_from_mic(recognizer, microphone):
    """Transcribe speech from recorded from `microphone`.
    Returns a dictionary with three keys:
    "success": a boolean indicating whether or not the API request was
    successful
    "error": `None` if no error occured, otherwise a string containing
    an error message if the API could not be reached or
    speech was unrecognizable
    "transcription": `None` if speech could not be transcribed,
    otherwise a string containing the transcribed text
    """
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")
    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }
    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    # update the response object accordingly
    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"
    return response

#1: recognision from a file
#2: recognision from a mic using google api
#3: points 1 and 2 combined
#4: listing connected devices and checking their indexes
#5: a fun game!
#6: the Google Maps Control project

task = 6

if task == 1:
    r = sr.Recognizer()
    harvard = sr.AudioFile('harvard.wav')
    with harvard as source:
        audio = r.record(source)
if task == 2:
    print("Wpisz w konsolę komendę.")
    # wpisz na konsolę:
    # python -m speech_recognition
if task == 3:
    r = sr.Recognizer()
    mic = sr.Microphone(device_index=0)
    with mic as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        v = r.recognize_google(audio)
        print(v)

    harvard = sr.AudioFile('harvard.wav')
    with harvard as source1:
        audio1 = r.record(source1)
        u = r.recognize_google(audio1)
        print(u)
if task == 4:
    print(sr.Microphone.list_microphone_names())
    mic = sr.Microphone(device_index=0)
if task == 5:

    # set the list of words, maxnumber of guesses, and prompt limit
    WORDS = ["apple", "banana", "grape", "orange", "mango", "lemon"]
    NUM_GUESSES = 3
    PROMPT_LIMIT = 5
    # create recognizer and mic instances
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    # get a random word from the list
    word = random.choice(WORDS)
    # format the instructions string
    instructions = (
        "I'm thinking of one of these words:\n"
        "{words}\n"
        "You have {n} tries to guess which one.\n"
    ).format(words=', '.join(WORDS), n=NUM_GUESSES)
    # show instructions and wait 3 seconds before starting the game
    print(instructions)
    time.sleep(3)
    for i in range(NUM_GUESSES):
        # get the guess from the user
        # if a transcription is returned, break out of the loop and
        # continue
        # if no transcription returned and API request failed, break
        # loop and continue
        # if API request succeeded but no transcription was returned,
        # re-prompt the user to say their guess again. Do this up
        # to PROMPT_LIMIT times
        for j in range(PROMPT_LIMIT):
            print('Guess {}. Speak!'.format(i + 1))
            guess = recognize_speech_from_mic(recognizer, microphone)
            if guess["transcription"]:
                break
            if not guess["success"]:
                break
            print("I didn't catch that. What did you say?\n")
        # if there was an error, stop the game
        if guess["error"]:
            print("ERROR: {}".format(guess["error"]))
            break
        # show the user the transcription
        print("You said: {}".format(guess["transcription"]))
        # determine if guess is correct and if any attempts remain
        guess_is_correct = guess["transcription"].lower() == word.lower()
        user_has_more_attempts = i < NUM_GUESSES - 1
        # determine if the user has won the game
        # if not, repeat the loop if user has more attempts
        # if no attempts left, the user loses the game
        if guess_is_correct:
            print("Correct! You win!".format(word))
            break
        elif user_has_more_attempts:
            print("Incorrect. Try again.\n")

        else:
            print("Sorry, you lose!\nI was thinking of '{}'.".format(word))
            break
if task == 6:
    #in case of changing a device - change the name of mic - use:
    #print(sr.Microphone.list_microphone_names())
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
        print("Say Something")
        # listens for the user's input
        audio = r.listen(source)

        try:
            text = r.recognize_google(audio)
            print("you said: " + text)

            # error occurs when google could not understand what was said

        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")

        except sr.RequestError as e:
            print("Could not request results from "
                  "Google Speech Recognition service; {0}".format(e))




