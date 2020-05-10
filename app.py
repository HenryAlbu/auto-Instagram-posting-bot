#!/usr/bin/env Python3
import PySimpleGUI as sg
import insta
import queue
import settings
import threading


def long_operation_thread(gui_queue, post_source):
    # Launches instagram and chromedriver
    insta.launch_inst()
    # Starts posting based on selected user inputs
    insta.loop_posting()

# Makes sure everything is in order before program starts
def verifications(values):
    # if username/password is not filled out
    if "" in (values['username'], values['password']):
        print('Username/Password is empty')
        return False
    # if post source and login type are incorrect
    if values['post_source'] == "Instagram user" and values['login_type'] == "Facebook":
        print('If you are posting from an Instagram user, you need to sign in using a regular Instagram account')
        return False
    # if 9gag is chosen but no category is selected
    if values['post_source'] == "9gag" and settings.ninegag_categories == []:
        print('You have not selected any categories to post from 9gag')
        return False
    # if post source is Instagram but no user was given
    if values['post_source'] == "Instagram user" and values['scrape_user'] == "":
        print('You need to add a username to take posts from')
        return False
    return True


# The UI
def the_gui():
    # sets theme
    sg.ChangeLookAndFeel('DarkBrown1')
    gui_queue = queue.Queue()

    # Login Section
    login = [
        [sg.Frame(layout=[
            [sg.Text('Post from:', size=(17, 1), font=("Roboto", 8)),
             sg.InputCombo(('9gag', 'Instagram user'), default_value="9gag", key="post_source", size=(25, 1))],
            [sg.Text('How will you sign in:', size=(17, 1), font=("Roboto", 8)),
             sg.InputCombo(('Facebook', 'Regular Instagram Login'), default_value="Facebook", key="login_type",
                           size=(25, 1))],
            [sg.Text('Username/Email:', size=(17, 1), font=("Roboto", 8)),
             sg.InputText('', key="username", size=(27, 1))],
            [sg.Text('Password:', size=(17, 1), font=("Roboto", 8)),
             sg.InputText('', key="password", password_char='*', size=(27, 1))],
        ],
            title='Instagram Login', title_color="#ffffff")], ]

    # Output Console
    output = [
        [sg.Frame(layout=[
            [sg.Output(size=(42, 14), pad=(0, 0))],
        ], title=' ', title_color="#ffffff")], ]

    # Main Layout
    layout = [
        # Help Section
        [sg.Frame(layout=[
            [sg.Text('9gag Options:', size=(11, 1), font=("Roboto", 8), text_color="red", pad=(5, 0)),
             sg.Text('By default, it will get the most up voted posts from the selected sections and add to queue.',
                     size=(80, 1), font=("Roboto", 8), pad=(0, 0))],
            [sg.Text('_' * 210, font=("Roboto", 4), pad=(5, 0))],
            [sg.Text('Instagram Scraping Options:', size=(23, 0), font=("Roboto", 8), text_color="red", pad=(5, 0)),
             sg.Text('Copies posts from user and posts on your account (currently only supports images)', size=(80, 0),
                     font=("Roboto", 8), pad=(0, 0))],
            [sg.Text(
                'In order to use the Instagram scrapping option you will need to log in using a regular Instagram '
                'accounts. Using a facebook login will not work. PRIVATE USER SCRAPPING ONLY WORKS IF YOU ARE FOLLOWING THE USER',
                size=(105, 0), font=("Roboto", 8), pad=(5, 0))],
            [sg.Text(
                'WARNING: THIS FEATURE MIGHT NOT WORK AFTER JUNE 29/2020 - INSTAGRAM IS UPDATING ITS API',
                size=(105, 0), font=("Roboto", 8), pad=(5, 0), text_color="red")],
            [sg.Text('_' * 210, font=("Roboto", 4), pad=(5, 0))],
            [sg.Text('Login:', size=(5, 1), font=("Roboto", 8), text_color="red", pad=(5, 0)),
             sg.Text('Login details for Instagram. Allows you to choose between 9gag or Instagram scrapping as '
                     'content source for the posts.', size=(100, 0), font=("Roboto", 8), pad=(0, 0))],
            [sg.Text('_' * 210, font=("Roboto", 4), pad=(5, 0))],
            [sg.Text('General Options:', size=(13, 1), font=("Roboto", 8), text_color="red", pad=(5, 0)),
             sg.Text('Applies for both, Instagram scrapping and 9gag options.', size=(50, 1), font=("Roboto", 8),
                     pad=(0, 0))],
        ], title='Help', title_color="#ffffff")],

        # 9gag Section
        [sg.Frame(layout=[
            [sg.Checkbox('Hot', key="hot"), sg.Checkbox('Trending', key="trending"),
             sg.Checkbox('Funny', key="funny"), sg.Checkbox('Animals', key="animals"),
             sg.Checkbox('Anime/Manga', key="anime-manga"), sg.Checkbox('Anime/Waifu ', key="animewaifu"),
             sg.Checkbox('Savage', key="savage")],
            [sg.Checkbox('Awesome', key="awesome"), sg.Checkbox('Cosmic & Webtoon', key="comic-webtoon"),
             sg.Checkbox('Cosplay', key="cosplay"), sg.Checkbox('Gaming', key="gaming"),
             sg.Checkbox('WTF', key="wtf"), sg.Checkbox('Girl', key="girl"),
             sg.Checkbox('Relationship', key="relationship")],
            [sg.Checkbox('Girl/Celeb', key="girlcelebrity"), sg.Checkbox('League of Legends', key="leagueoflegends"),
             sg.Checkbox('Meme', key="meme"), sg.Checkbox('NSFW', key="nsfw"),
             sg.Checkbox('Politics', key="politics")],
        ], title='9gag Options', title_color="#ffffff")],

        # Instagram Scrapping Section
        [sg.Frame(layout=[
            [sg.Text('Username to scrape:', size=(17, 1), font=("Roboto", 8)),
             sg.InputText('', key="scrape_user", size=(26, 1))],
            [sg.Text(' ' * 210, font=("Roboto", 4), pad=(5, 0))],
            [sg.Text('# of past images to add to queue:', size=(28, 1), font=("Roboto", 8)),
             sg.Spin(values=[i for i in range(0, 1000)], key="past_images", initial_value=5, size=(6, 1))],
            [sg.Text(' ' * 210, font=("Roboto", 4), pad=(5, 0))],
            [sg.Text('Keep checking for new post? \nChecks for new post every 5 mins', size=(28, 2),
                     font=("Roboto", 8)),
             sg.InputCombo(('Yes', 'No'), default_value="Yes", key="keep_checking", size=(6, 1))],

        ], title='Instagram Scrapping Options', title_color="#ffffff"), sg.Column(login)],

        # General Options Section
        [sg.Frame(layout=[
            [sg.Text('Wait time (seconds)', size=(15, 0)),
             sg.Spin(values=[i for i in range(0, 1000)], key="wait_time", initial_value=5, size=(6, 0))],
            [sg.Text('The amount of time for an action to be done ex: closing a popup. I recommend a '
                     'min of 5. If you have slower internet, increase this value.', size=(50, 0), font=("Roboto", 8))],
            [sg.Text('_' * 100, font=("Roboto", 4))],
            [sg.Text('Next post wait time', size=(15, 1)),
             sg.Spin(values=[i for i in range(0, 1000)], key="post_time", initial_value=50, size=(6, 1))],
            [sg.Text('Delay between posts. I recommend 50 seconds or more to avoid instagram bot detection',
                     size=(40, 0), font=("Roboto", 8))],
            [sg.Text('_' * 100, font=("Roboto", 4))],
            [sg.Text('Number of posts', size=(15, 1)),
             sg.Spin(values=[i for i in range(0, 1000)], key="post_limit", initial_value=15, size=(6, 1))],
            [sg.Text('Number of posts before program stops', size=(50, 0), font=("Roboto", 8))],
        ], title='General Options', title_color="#ffffff"), sg.Column(output)],
        # Buttons
        [sg.Button('Run', size=(10, 1), key="Run"), sg.Button('Exit', size=(10, 1))]
    ]
    # Window options
    window = sg.Window('Made with love - v1.0', layout, default_element_size=(40, 1), grab_anywhere=False, location=(5, 5))

    while True:
        event, values = window.read(timeout=100)
        # If exit button is clicked
        if event in (None, 'Exit'):
            break
        # If run button is clicked
        elif event == 'Run':
            # All option for 9gag categories to loop through
            ninegagCategories = ["hot", "trending", "funny", "animals", "anime-manga", "animewaifu", "awesome",
                                 "cosmic-webtoon", "cosplay", "gaming", "girl", "girlcelebrity",
                                 "leagueoflegends", "meme", "nsfw", "politics", "relationship", "savage", "wtf"]

            # Sends selected 9gag categories to settings.py
            for key in values:
                if key in ninegagCategories and values[key]:
                    settings.ninegag_categories.append(key)
            # Checks with verification function
            if verifications(values):
                # disables the Run button when run is clicked
                window['Run'].update(disabled=True)
                print("Starting...")
                # Sends user inputs to settings.py to be set as global variables
                settings.wait_time = values['wait_time']
                settings.post_time = values['post_time']
                settings.username = values['username']
                settings.password = values['password']
                settings.login_type = values['login_type']
                settings.post_limit = values['post_limit']
                settings.scrape_user = values['scrape_user']
                settings.past_images = values['past_images']
                settings.post_source = values['post_source']
                # Converts keep_checking into a boolean
                if values['keep_checking'] == 'Yes':
                    settings.keep_checking = True
                else:
                    settings.keep_checking = False

                # Calls the long_operation_thread
                try:
                    threading.Thread(target=long_operation_thread,
                                     args=(gui_queue, values['post_source']), daemon=True).start()
                except Exception as e:
                    print('Error')

        # Checks for incoming messages from threads
        try:
            # get_nowait() will get exception when Queue is empty
            message = gui_queue.get_nowait()
        except queue.Empty:
            # break from the loop if no more messages are queued up
            message = None
        # if message received from queue, display the message in the Window
        if message:
            print('Got a message back from the thread: ', message)

    # if user exits the window, then close the window and exit the GUI
    window.close()


if __name__ == '__main__':
    the_gui()
    print('Exiting Program')
