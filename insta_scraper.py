#!/usr/bin/env Python3
import html
import settings
import json
import os
import re
import time

# variable used to track time
oldtime = time.time()

def get_data():
    global oldtime
    # Waits 5 min if not first run to get instagram posts from selected user
    # this limits the amount of request and makes it not seem like a bot
    if time.time() - oldtime > 300 or settings.counter == 0:
        print("Please wait, getting images from user... \nThis might take a few mins")
        # gets images and sends it to the images folder
        args = 'instagram-scraper ' + settings.scrape_user + ' -u ' + settings.username + ' -p ' + settings.password + \
               ' -t image -m '+ str(settings.past_images) +' --latest --media-metadata -d images'
        os.system(args)
        get_contents()
        # resets the time var
        oldtime = time.time()

# takes images and JSON file from images and breaks it down into the queue
def get_contents():
    # opens the content from the JSON file created by get_data
    with open('images/' + settings.scrape_user + '.json', encoding="utf8") as json_file:
        data = json.load(json_file)

        # grabs only image data from JSON file
        for i in data["GraphImages"]:

            # checks image has already been downloaded and avoids multi-pic posts
            if i["id"] not in settings.filesCheck and i["__typename"] == "GraphImage":
                print("YAY! Found a new image")
                regex = re.findall('\w+.jpg', i["display_url"])

                # sometimes captions are empty, this avoids an error if it is
                try:
                    title = html.unescape(i["edge_media_to_caption"]["edges"][0]["node"]["text"]).encode('ascii','ignore').decode('ascii')
                except:
                    title = ""

                # checks if any changes were made to the file filesDict
                try:
                    with open('filesDict.json', encoding="utf8") as data_file:
                        settings.filesDict = json.load(data_file)
                except:
                    pass

                # appends new info to the queue
                settings.filesDict['dict'].append({
                    'id': os.path.splitext(regex[0])[0],
                    'title': title,
                    'url': i["id"],
                    'type': "Photo"
                })

                # appends id into fileCheck array
                settings.filesCheck.append(i["id"])

                # Saves fileArray to a file
                with open('filesDict.json', 'w+', encoding="utf8") as outfile:
                    json.dump(settings.filesDict, outfile, ensure_ascii=False)

            # Saves ids from fileCheck array to fileCheck.txt
            with open('filesCheck.txt', 'w') as filehandle:
                for listitem in settings.filesCheck:
                    filehandle.write('%s\n' % listitem)