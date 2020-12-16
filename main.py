from gtts import gTTS
import speech_recognition as sr
import playsound
import os
import random
import sys

r = sr.Recognizer()
idx_tracker = 0
choice_prompt = 'Enter your choice:'


def prepare_list(file_name):
    with open(file_name) as f:
        text_list = f.read().splitlines()
        return text_list


def randomize_list(list_to_shuffle):
    clone_list = list_to_shuffle.copy()
    random.shuffle(clone_list)
    return clone_list


def speak_control(list_source, navigation_clue):
    global idx_tracker
    if navigation_clue.lower() == 'p':
        if idx_tracker != 0:
            idx_tracker -= 1

    else:
        if idx_tracker != len(list_source)-1:
            idx_tracker += 1

    speak(list_source[idx_tracker])


def speak(text):
    file = "speak.mp3"
    tts = gTTS(text)
    tts.save(file)
    playsound.playsound(file)
    os.remove(file)


def speak_and_listen(text):
    while 1:
        try:
            speak(text)

            print('Wait...')
            with sr.Microphone() as mic:

                # wait for a second to let the recognizer
                # adjust the energy threshold based on
                # the surrounding noise level
                r.adjust_for_ambient_noise(mic, duration=0.2)

                # listens for the user's input
                print('Speak now...')
                audio = r.listen(mic)

                # Using google to recognize audio
                spoken_word = r.recognize_google(audio)
                spoken_word = spoken_word.lower().replace(" ", "")

                if text.lower() == spoken_word:
                    print('Correct!')
                else:
                    print(f'Expected {text}; Heard {spoken_word}')
                break

        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))

        except sr.UnknownValueError:
            print("I heard nothing. Let's try again...")


def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))


def menu(file_to_read):
    with open(file_to_read) as f:
        print(f.read())


def speak_flow(list_to_use):
    back_to_prev_menu = False
    global idx_tracker
    while not back_to_prev_menu:
        menu(get_script_path() + '\\ListenMenu.txt')
        selected_input = input(choice_prompt)

        if selected_input.lower() == 'x':
            back_to_prev_menu = True
            idx_tracker = 0
            break

        speak_control(list_to_use, selected_input)


if __name__ == '__main__':
    original_list = prepare_list(get_script_path() + '\\List.txt')
    random_list = randomize_list(original_list)
    exit_app = False

    while not exit_app:
        menu(get_script_path() + '\\MainMenu.txt')
        choice = input(choice_prompt)

        if choice.lower() == 'x':
            exit_app = True
            break

        if int(choice) == 1:
            speak_flow(original_list)

        elif int(choice) == 2:
            speak_flow(random_list)

        elif int(choice) == 3:
            for i in original_list:
                speak_and_listen(i)

        elif int(choice) == 4:
            for i in random_list:
                speak_and_listen(i)
