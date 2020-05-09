# Initializes setting files
import json
import glob
import os


def init():
    global ninegag_categories, username, password, wait_time, post_time, login_type, \
        post_limit, filesDict, filesCheck, scrape_user, keep_checking, past_images, post_source, counter
    ninegag_categories = []
    username = ""
    password = ""
    wait_time = 5
    post_time = 50
    login_type = ""
    post_limit = 0
    scrape_user = ""
    past_images = 0
    post_source = ""
    counter = 0
    keep_checking = True
    # Creates assets folder if non-existent
    if not os.path.exists('assets'):
        os.makedirs('assets')
    # Removes images from files if left over from previous runs
    files = glob.glob('assets/*')
    for f in files:
        os.remove(f)
    filesDict = {'dict': []}
    # Clears filesDict on start
    with open('filesDict.json', 'w+', encoding="utf8") as outfile:
        json.dump(filesDict, outfile, ensure_ascii=False)
    # Creates filesCheck if not existent
    try:
        file = open('filesCheck.txt', 'r')
        file.close()
    except IOError:
        file = open('filesCheck.txt', 'w')
        file.close()
    # Handles removing old items from filesCheck.txt and filling the filesCheck array
    count = 0
    with open('filesCheck.txt', 'r') as f:
        data = f.read().splitlines(True)
        for line in f:
            count += 1
        count -= 100
    with open('filesCheck.txt', 'w') as fout:
        fout.writelines(data[count:])
    # Array that loads past used files from fileCheck.txt
    with open('filesCheck.txt') as f:
        filesCheck = [line.rstrip() for line in f]


init()
