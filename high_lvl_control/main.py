import subprocess
import speech_recognition as sr
from subprocess import call
import os

manual = {
    "pomoc": "pomoc - wyświetla dostępne komendy",
    "informacje": "informacje \'nazwa komendy\' - wyświetla informacje jak działa dana komenda",
    "pokaż ścieżkę": "pokaż ścieżkę - podaje ścieżkę do aktualnego katalogu",
    "pokaż pliki": "pokaż pliki - listuje pliki w katalogu",
    "stwórz folder": "stwórz katalog \'nazwa\' - tworzy katalog o podanej nazwie",
    "usuń folder": "usuń folder \'nazwa\' - usuwa katalog o podanej nazwie, jeśli istnieje",
    "wyjdź z folderu": "wyjdź z folderu - wychodzi z katalogu na wyższy poziom",
    "wejdż do folder": "wejdź do \'nazwa\' - wchodzi do katalogu o podanej nazwie",
    "otwórz": "otwórz \'nazwa\' - otwiera katalog o podanej nazwie, jeśli istnieje",
    "wyjdź z terminala": "wyjdź z terminala - kończy działanie programu",
    "wyloguj": "wyloguj - wylogowuje użytkownika",
    "wyłącz komputer": "wyłącz komputer - wyłącza komputer",
    "restartuj komputer": ""
}


def get_input(recognizer, microphone):
    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        response["transcription"] = recognizer.recognize_google(audio, language="pl-PL")
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API nieosiągalne."
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = True
        response["error"] = "Nie rozpoznaję komendy."

    return response


def process_command(text, wd):
    print("Zrozumiałem: " + text)
    if 'pomoc' in text:
        for key, val in manual.items():
            print(val)
    else:
        if text == "pokaż ścieżkę":
            print(wd)
        elif text == "pokaż pliki":
            for file in [f for f in os.listdir(wd)]:
                print(file)
        elif text == "wyjdź z terminala":
            return False, wd
        elif text == "wyjdź z folderu":
            wd = os.path.dirname(wd)
            os.chdir(wd)
        elif text == "wyloguj":
            os.system("shutdown -l")
        elif text == "wyłącz koputer":
            os.system("shutdown /s /t 1")
        elif text == "restartuj komputer":
            os.system("shutdown /r /t 1")

        words = text.split()
        if words[0] == "informacje":
            command_name = ' '.join(words[1:])
            try:
                print(manual[command_name])
            except:
                print("Nie ma komendy " + command_name + " spróbuj ponownie.")
        elif words[0] == "otwórz":
            dir_name = ' '.join(words[1:])
            try:
                os.chdir(os.path.join(wd, dir_name))
                wd = os.path.join(wd, dir_name)
            except:
                print(dir_name + " nie istnieje, możesz go utorzyć komendą stwórz folder.")
        elif len(words) > 1 and words[1] == "folder":
            dir_name = ' '.join(words[2:])
            dir_path = os.path.join(wd, dir_name)
            if words[0] == "stwórz":
                os.makedirs(dir_path)
            elif words[0] == "usuń":
                os.removedirs(dir_path)
    return True, wd


def main():
    # in case of changing a device - change the name of mic - use:
    # print(sr.Microphone.list_microphone_names())
    mic_name = "HDA Intel PCH: ALC233 Analog (hw:0,0)"

    # create recognizer and mic instances
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    working_directory = os.getcwd()

    call(["clear"])
    running = True
    print("Komenda \'Pomoc\' listuje wszystkied dostępne komendy. Miłej zabawy!")
    while running:
        print("/")
        voice_input = get_input(recognizer, microphone)
        if not voice_input["error"]:
            text = voice_input["transcription"].lower()
            running, working_directory = process_command(text, working_directory)


if __name__ == "__main__":
    main()