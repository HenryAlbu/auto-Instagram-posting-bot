import urllib.request
import json, html, insta, glob, os
from time import sleep
from PIL import Image

# Dictionary that stores the url,title,Id of each item into file
filesDict = {'dict': []}
# Clears filesDict on start
with open('filesDict.txt', 'w', encoding="utf8") as outfile:
    json.dump(filesDict, outfile, ensure_ascii=False)

# Variable used as a flag on if the program has been executed
initialRun = 0

# Handles removing old items from filesCheck.txt and filling the filesCheck array
count = 0
with open('filesCheck.txt', 'r') as fin:
    data = fin.read().splitlines(True)
    for line in fin:
        count += 1
    count -= 50
    print("Total number of lines is:", count)
with open('filesCheck.txt', 'w') as fout:
    fout.writelines(data[count:])
# Array that loads past used files from fileCheck.txt
with open('filesCheck.txt') as f:
    filesCheck = [line.rstrip() for line in f]


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
def printResults(data):
    global filesDict
    theJSON = json.loads(data)
    # Loops through the JSON
    for i in theJSON["data"]["posts"]:
        # Checks if its a new file or has already downloaded and if the file height is less than 2300
        if i["type"] == "Photo" and i["id"] not in filesCheck and i["images"]["image700"]["height"] < 2300:
            # calls download function and passes arg
            download(i["images"]["image700"]["url"], 'files/', i["id"])
            # Uses PIL to format image if its height is bigger than its width
            if i["images"]["image700"]["height"] > i["images"]["image700"]["width"]:
                image = Image.open('files/' + i["id"] + '.jpg')
                new_image = make_square(image)
                new_image.save('files/' + i["id"] + '.jpg')
            # print(i["images"]["image700"]["url"])
            # checks if any changes were made to the file filesDict
            try:
                with open('filesDict.txt', encoding="utf8") as data_file:
                    print(filesDict)
                    filesDict = json.load(data_file)
            except:
                pass

            # Add info into filesDict
            filesDict['dict'].append({
                'id': i["id"],
                'title': html.unescape(i["title"]),
                'url': i["images"]["image700"]["url"],
                'type': i["type"]
            })

            # appends id into fileCheck
            print(filesCheck)
            filesCheck.append(i["id"])

            # Saves fileArray to a file
            with open('filesDict.txt', 'w', encoding="utf8") as outfile:
                json.dump(filesDict, outfile, ensure_ascii=False)

        # Saves past files ids into fileCheck.txt
        with open('filesCheck.txt', 'w') as filehandle:
            for listitem in filesCheck:
                filehandle.write('%s\n' % listitem)


def getData():
    # Gets the JSON from the URL and send a header so that it looks like a legit request
    urlData = "https://9gag.com/v1/group-posts/group/default/type/fresh"
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    headers = {'User-Agent': user_agent, }

    # Opens the URL
    request = urllib.request.Request(urlData, None, headers=headers)
    webUrl = urllib.request.urlopen(request)

    # If URL is opened with success, Then run printResults function
    if webUrl.getcode() == 200:
        data = webUrl.read()
        print(data)
        print(str(webUrl.getcode()))
        printResults(data)
    else:
        print("Error")


# Runs on start
# Removes images from files if left over from previous runs
files = glob.glob('files/*')
for f in files:
    os.remove(f)

# Gets the data function
getData()
# If there are new images on start then login else wait
if filesDict['dict']:
    insta.orderedFunctions()
else:
    print("Waiting for new images")
    initialRun = 1

# Loops through at a set interval and adds another photo
while True:
    sleep(61)
    getData()
    if filesDict['dict'] != [] and initialRun == 0:
        print(len(filesDict['dict']))
        insta.add_post()
        sleep(3)
        insta.post()
    elif initialRun == 1 and filesDict['dict'] == 1:
        initialRun = 0
        insta.orderedFunctions()
    else:
        print("Waiting for new images")
