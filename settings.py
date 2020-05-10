#!/usr/bin/env Python3
import json
import glob
import os


def init():
    global ninegag_categories, username, password, wait_time, post_time, login_type, \
        post_limit, filesDict, filesCheck, scrape_user, keep_checking, past_images, post_source, counter

    # User inputted info set as variables
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
    filesDict = {'dict': []}

    # Creates images folder if non-existent
    if not os.path.exists('images'):
        os.makedirs('images')

    # Removes images from files if left over from previous runs
    files = glob.glob('images/*')
    for f in files:
        os.remove(f)

    # Clears filesDict.JSON on start
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
    # keeps the 100 most recent downloads
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
