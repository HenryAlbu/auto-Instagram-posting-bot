#!/usr/bin/env Python3
import urllib.request
import json, html, settings
from PIL import Image


# Downloads images/videos
def download(url, file_path, file_name):
    full_path = file_path + file_name + '.jpg'
    urllib.request.urlretrieve(url, full_path)


# Function that makes the resizes images be able to fit instagram
def make_square(im, min_size=256, fill_color=(0, 0, 0, 0)):
    x, y = im.size
    size = max(min_size, x, y)
    new_im = Image.new('RGB', (size, size), fill_color)
    new_im.paste(im, (int((size - x) / 2), int((size - y) / 2)))
    return new_im

# Print section of JSON
def print_results(data):
    theJSON = json.loads(data)
    # Loops through the JSON
    for i in theJSON["data"]["posts"]:

        # Checks if its a new file or has already downloaded and if the file height is less than 2000
        if i["type"] == "Photo" and i["id"] not in settings.filesCheck and i["images"]["image700"]["height"] < 2000:

            # calls download function and passes arg
            download(i["images"]["image700"]["url"], 'images/', i["id"])

            # Uses PIL to format image if its height is bigger than its width
            if i["images"]["image700"]["height"] > i["images"]["image700"]["width"]:
                image = Image.open('images/' + i["id"] + '.jpg')
                new_image = make_square(image)
                new_image.save('images/' + i["id"] + '.jpg')
            print("Downloading image: \n" + i["images"]["image700"]["url"])

            # checks if any changes were made to the file filesDict
            try:
                with open('filesDict.json', encoding="utf8") as data_file:
                    settings.filesDict = json.load(data_file)
            except:
                pass

            # Add info into filesDict array
            settings.filesDict['dict'].append({
                'id': i["id"],
                'title': html.unescape(i["title"]).encode('ascii', 'ignore').decode('ascii'),
                'url': i["images"]["image700"]["url"],
                'type': i["type"]
            })

            # appends id into fileCheck
            settings.filesCheck.append(i["id"])

            # saves fileDict array into fileDict.json
            with open('filesDict.json', 'w+', encoding="utf8") as outfile:
                json.dump(settings.filesDict, outfile, ensure_ascii=False)

        # saves ids in fileCheck array into fileCheck.txt
        with open('filesCheck.txt', 'w') as filehandle:
            for listitem in settings.filesCheck:
                filehandle.write('%s\n' % listitem)


def get_data():
    # loops through 9gag section user chose
    for x in settings.ninegag_categories:
        try:
            if x in ("hot","trending"):
                urlData = "https://9gag.com/v1/group-posts/group/default/type/" + x
            else:
                urlData = "https://9gag.com/v1/group-posts/group/" + x

            # Gets the JSON from the URL and sends a header so that it looks like a legit request
            user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
            headers = {'User-Agent': user_agent, }
            print("Getting images from category: " + x)

            # Opens the URL
            request = urllib.request.Request(urlData, None, headers=headers)
            webUrl = urllib.request.urlopen(request)

            # If URL is opened with success, Then run printResults function
            if webUrl.getcode() == 200:
                data = webUrl.read()
                print_results(data)
            else:
                print("Error")
        except:
            pass