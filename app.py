#!/usr/bin/env Python3
import PySimpleGUI as sg
import settings
settings.init()
import ninegag, glob, insta, os, subprocess, queue, threading



def long_operation_thread(gui_queue):
    insta.launch_inst()
    ninegag.loop_posting()
    gui_queue.put('** Done **')  # put a message into queue for GUI


# ------------------------------- UI -------------------------------
def the_gui():
    sg.ChangeLookAndFeel('DarkBrown1')
    gui_queue = queue.Queue()

    col = [
        # General options
        [sg.Frame(layout=[
            [sg.Text('Wait time (seconds)', size=(15, 0)),
             sg.Spin(values=[i for i in range(5, 1000)], key="wait_time", initial_value=5, size=(6, 0))],
            [sg.Text('The amount of time for an action to be done ex: closing a popup. I recommend a '
                     'min of 5. If you have slower internet, increase this value.', size=(50, 0), font=("Roboto", 8))],
            [sg.Text('_' * 100, font=("Roboto", 4))],
            [sg.Text('Next post wait time', size=(15, 1)),
             sg.Spin(values=[i for i in range(1, 1000)], key="post_time", initial_value=50, size=(6, 1))],
            [sg.Text('Delay between posts. I recommend 50 seconds or more to avoid instagram bot detection',
                     size=(40, 0), font=("Roboto", 8))],
            [sg.Text('_' * 100, font=("Roboto", 4))],
            [sg.Text('Number of posts', size=(15, 1)),
             sg.Spin(values=[i for i in range(0, 1000)], key="post_limit", initial_value=50, size=(6, 1))],
            [sg.Text('Number of posts before program stops', size=(50, 0), font=("Roboto", 8))],
            [sg.Text('_' * 100, font=("Roboto", 4))],
            [sg.Checkbox('Keep Images', key="keep_images", default=False)],
            [sg.Text('Deletes images in folder on exit', size=(50, 0),
                     font=("Roboto", 8))],

        ],
            title='General Options')], ]
    layout = [
        # Title

        # 9gag Section
        [sg.Frame(layout=[
            [sg.Checkbox('Hot', key="hot", default=True), sg.Checkbox('Trending', key="trending"),
             sg.Checkbox('Funny', key="funny"), sg.Checkbox('Animals', key="animals"),
             sg.Checkbox('Anime/Manga', key="anime-manga"), sg.Checkbox('Anime/Waifu ', key="animewaifu")],
            [sg.Checkbox('Awesome', key="awesome"), sg.Checkbox('Cosmic & Webtoon', key="comic-webtoon"),
             sg.Checkbox('Cosplay', key="cosplay"), sg.Checkbox('Gaming', key="gaming"),
             sg.Checkbox('WTF', key="wtf"), sg.Checkbox('Girl', key="girl")],
            [sg.Checkbox('Girl/Celeb', key="girlcelebrity"), sg.Checkbox('League of Legends', key="leagueoflegends"),
             sg.Checkbox('Meme', key="meme"), sg.Checkbox('NSFW', key="nsfw"),
             sg.Checkbox('Politics', key="politics"), sg.Checkbox('Relationship', key="relationship")],
            [sg.Checkbox('Savage', key="savage")],
        ],
            title='9gag Options (What section of 9gag do you want your photos to come from?)')],

        # Instagram options
        [sg.Frame(layout=[
            [sg.Text('How will you sign in?', size=(25, 1))],
            [sg.InputCombo(('Facebook', 'Username'),  default_value="Facebook" ,key="login_type", size=(25, 1))],
            [sg.Text('Username/Email', size=(25, 1))],
            [sg.InputText('',  key="username", size=(25, 1))],
            [sg.Text('Password', size=(25, 1))],
            [sg.InputText('',  key="password",  password_char='*',size=(25, 1))],
        ],
            title='Instagram Options'), sg.Column(col)],

        # Output window
        [sg.Output(size=(80, 10))],

        # Buttons
        [sg.Button('Run', size=(10, 1)), sg.Button('Exit', size=(10, 1))]
    ]
    window = sg.Window('Made with love', layout, default_element_size=(40, 1), grab_anywhere=False)

    while True:
        event, values = window.read(timeout=100)
        if event in (None, 'Exit'):
            #if not values['keep_images']:
            #    # Removes images from files if left over from previous runs
            #    files = glob.glob('files/*')
            #    for f in files:
            #        os.remove(f)
            break
        elif event == 'Run':
            print("Starting...")
            # All option for 9gag categories
            ninegagCategories = ["hot", "trending", "funny", "animals", "anime-manga", "animewaifu", "awesome",
                                 "cosmic-webtoon", "cosplay", "gaming", "girl", "girlcelebrity",
                                 "leagueoflegends", "meme", "nsfw", "politics", "relationship", "savage", "wtf"]
            # Sends selected categories to setting.py
            for key in values:
                if key in ninegagCategories and values[key]:
                    settings.ninegag_categories.append(key)
            settings.wait_time = values['wait_time']
            settings.post_time = values['post_time']
            settings.username = values['username']
            settings.password = values['password']
            settings.keep_images = values['keep_images']
            settings.login_type = values['login_type']
            settings.post_limit = values['post_limit']

            try:
               threading.Thread(target=long_operation_thread,
                                args=(gui_queue,), daemon=True).start()
            except Exception as e:
               print('Error')


        # Check for incoming messages from threads
        try:
            message = gui_queue.get_nowait()
        except queue.Empty:  # get_nowait() will get exception when Queue is empty
            message = None  # break from the loop if no more messages are queued up

        # if message received from queue, display the message in the Window
        if message:
            print('Got a message back from the thread: ', message)

    # if user exits the window, then close the window and exit the GUI func
    window.close()


######################################################################


if __name__ == '__main__':
    the_gui()
    print('Exiting Program')
