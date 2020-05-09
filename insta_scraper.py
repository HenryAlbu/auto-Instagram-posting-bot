import html
import settings
import json
import os
import re
import time

oldtime = time.time()

def get_data():
    global oldtime
    # Waits 5 min if not first run to get instagram posts
    if time.time() - oldtime > 300 or settings.counter == 0:
        print("Please wait, getting images from user... \nThis might take a few mins")
        args = 'instagram-scraper ' + settings.scrape_user + ' -u ' + settings.username + ' -p ' + settings.password + \
               ' -t image -m '+ str(settings.past_images) +' --latest --media-metadata -d assets'
        os.system(args)
        get_contents()
        oldtime = time.time()


def get_contents():
    # Readies the content for instagram
    with open('assets/' + settings.scrape_user + '.json', encoding="utf8") as json_file:
        data = json.load(json_file)
        for i in data["GraphImages"]:
            if i["id"] not in settings.filesCheck and i["__typename"] == "GraphImage":
                print("YAY! Found a new image")
                regex = re.findall('\w+.jpg', i["display_url"])
                # checks if any changes were made to the file filesDict
                try:
                    with open('filesDict.json', encoding="utf8") as data_file:
                        settings.filesDict = json.load(data_file)
                except:
                    pass
                settings.filesDict['dict'].append({
                    'id': os.path.splitext(regex[0])[0],
                    'title': html.unescape(i["edge_media_to_caption"]["edges"][0]["node"]["text"]).encode('ascii','ignore').decode('ascii'),
                    'url': i["id"],
                    'type': "Photo"
                })

                # appends id into fileCheck
                settings.filesCheck.append(i["id"])

                # Saves fileArray to a file
                with open('filesDict.json', 'w+', encoding="utf8") as outfile:
                    json.dump(settings.filesDict, outfile, ensure_ascii=False)

                # Saves past files ids into fileCheck.txt
            with open('filesCheck.txt', 'w') as filehandle:
                for listitem in settings.filesCheck:
                    filehandle.write('%s\n' % listitem)