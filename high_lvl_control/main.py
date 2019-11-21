import speech_recognition as sr
import shutil
import os

manual = {
    "pomoc": "pomoc - wyświetla dostępne komendy",
    "informacje": "informacje \'nazwa komendy\' - wyświetla informacje jak działa dana komenda",
    "pokaż ścieżkę": "pokaż ścieżkę - podaje ścieżkę do aktualnego katalogu",
    "pokaż pliki": "pokaż pliki - listuje pliki w katalogu",
    "stwórz folder": "stwórz folder \'nazwa\' - tworzy katalog o podanej nazwie",
    "usuń folder": "usuń folder \'nazwa\' - usuwa katalog o podanej nazwie, jeśli istnieje",
    "otwórz": "otwórz \'nazwa\' - otwiera katalog o podanej nazwie, jeśli istnieje",
    "wyjdź z folderu": "wyjdź z folderu - wychodzi z katalogu na wyższy poziom",
    "stwórz dokument": "stwórz dokument \'nazwa\' - tworzy dokument tekstowy o podanej nazwie",
    "edytuj dokument": "edytuj dokument \'nazwa\' - edyuje dokument tekstowy o podanej nazwie, o ile istnieje",
    "usuń dokument": "usuń dokument \'nazwa\' - usuwa dokument tekstowy o podanej nazwie, o ile istnieje",
    "zakończ program": "zakończ program - kończy działanie programu"
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


def edit_file(file, r, m):
    voice_input = get_input(r, m)
    if voice_input:
        if voice_input["transcription"]:
            voice_input = voice_input["transcription"].lower()
        else: voice_input = ""
    else: voice_input = ""
    print("Zrozumiałem:\n" + voice_input + "\nCzy dopisać? Powiedz: Dopisz/Nie dopisuj.")
    tak_nie = get_input(r, m)
    if tak_nie:
        if tak_nie["transcription"]:
            tak_nie = tak_nie["transcription"].lower()
        else: tak_nie = ""
    else: tak_nie = ""

    while not (tak_nie == "dopisz" or tak_nie == "nie dopisuj"):
        print("Zrozumiałem:\n" + tak_nie + "\nPowiedz czy dopisać? Dopisz/Nie dopisuj.")
        tak_nie = get_input(r, m)
        if tak_nie:
            if tak_nie["transcription"]:
                tak_nie = tak_nie["transcription"].lower()
            else:
                tak_nie = ""
        else:
            tak_nie = ""
    if tak_nie == "dopisz":
        file.write("\n" + voice_input)
        print("Dopisałem:\n" + voice_input + ".\nZamykam dokument.")
    else: print("Nie dopisałem nic. Zamykam dokument.")


def process_command(text, wd, r, m):
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
        elif text == "zakończ program":
            return False, wd
        elif text == "wyjdź z folderu":
            wd = os.path.dirname(wd)
            os.chdir(wd)
            print("Wyszedłem z folderu.")

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
                print("Otworzyłem folder " + dir_name + ".")
            except:
                print(dir_name + " nie istnieje, możesz go utorzyć komendą stwórz folder.")
        elif len(words) > 1 and words[1] == "folder":
            dir_name = ' '.join(words[2:])
            dir_path = os.path.join(wd, dir_name)
            if words[0] == "stwórz" or words[0] == "utwórz":
                os.makedirs(dir_path)
                print("Stworzyłem folder " + dir_name + ".")
            elif words[0] == "usuń":
                if not os.path.isdir(dir_path):
                    print("Katalog nie istnieje, nie mogę go więc usunąć.")
                else:
                    if not os.listdir(dir_path):
                        os.removedirs(dir_path)
                    else:
                        shutil.rmtree(dir_path)
        elif len(words) > 1 and words[1] == "dokument":
            file_name = ' '.join(words[2:])
            file_path = os.path.join(wd, file_name + ".txt")
            if words[0] == "stwórz" or words[0] == "utwórz":
                file = open(file_path, "w")
                file.close()
                print("Stworzyłem dokument " + file_name + ".")
            elif words[0] == "usuń":
                if os.path.exists(file_path):
                    os.remove(file_path)
                    print("Usunąłem dokument " + file_name + ".")
                else:
                    print("Podany dokument nie istnieje, więc nie może zostać usunięty.")
            elif words[0] == "edytuj":
                if os.path.exists(file_path):
                    file = open(file_path, "r")
                    print("Zawartość dokumentu:")
                    print(file.read())
                    file.close()
                    end = words[0]
                    print("Powiedz, co dopisać w pliku. Słucham.")
                    file = open(file_path, "a")
                    edit_file(file, r, m)
                    file.close()
                else:
                    print("Podany dokument nie istnieje, więc nie może zostać edytowany.")
    return True, wd


def main():
    # in case of changing a device - change the name of mic - use:
    # print(sr.Microphone.list_microphone_names())

    # create recognizer and mic instances
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    working_directory = os.getcwd()

    running = True
    print("Komenda \'Pomoc\' listuje wszystkie dostępne komendy. Miłej zabawy!")
    while running:
        print("/")
        voice_input = get_input(recognizer, microphone)
        if not voice_input["error"]:
            text = voice_input["transcription"].lower()
            running, working_directory = process_command(text, working_directory, recognizer, microphone)


if __name__ == "__main__":
    main()