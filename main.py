import urllib.request
import json, html
import insta
from time import sleep


# Dictionary that stores the url,title,Id of each item into file
filesDict = {'dict': []}
# Array that loads past used files from fileCheck.txt
with open('filesCheck.txt') as f:
    filesCheck = [line.rstrip() for line in f]

# Downloads images/videos
def download(url, file_path, file_name, type):
    if type == "Photo":
        full_path = file_path + file_name + '.jpg'
    else:
        full_path = file_path + file_name + '.mp4'
    urllib.request.urlretrieve(url, full_path)

# Print section of JSON
def printResults(data):
    global filesDict
    theJSON = json.loads(data)
    # Loops through the JSON
    for i in theJSON["data"]["posts"]:
        # Checks if its a new file or has already downloaded
        if i["type"] == "Photo" and i["id"] not in filesCheck:
            # calls download function and passes arg
            download(i["images"]["image700"]["url"], 'files/', i["id"], "Photo")
            #print(i["images"]["image700"]["url"])
            # checks if any changes were made to the file filesDict
            try:
                with open('filesDict.txt', encoding="utf8") as data_file:
                    filesDict = json.load(data_file)
                    print(filesDict)
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
            filesCheck.append(i["id"])
            # Saves fileArray to a file

            with open('filesDict.txt', 'w', encoding="utf-8") as outfile:
                json.dump(filesDict, outfile, ensure_ascii=False)

        # Saves past files ids into fileCheck.txt
        with open('filesCheck.txt', 'w') as filehandle:
            for listitem in filesCheck:
                filehandle.write('%s\n' % listitem)

def getData():
    # Gets the JSON from the URL and send a header so that it looks like a legit request
    urlData = "https://9gag.com/v1/group-posts/group/default/type/fresh"
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    headers={'User-Agent':user_agent,}
    # Opens the URL
    request = urllib.request.Request(urlData,None,headers=headers)
    webUrl = urllib.request.urlopen(request)

    # If URL is opened with success, Then run printResults function
    if (webUrl.getcode()==200):
        data = webUrl.read()
        print(data)
        print(str(webUrl.getcode()))
        printResults(data)
    else:
        print("Error")

getData()

if filesDict['dict'] != []:
    insta.orderedFunctions()

while True:
    print("innnnn")
    sleep(50)
    getData()
    if filesDict['dict'] != []:
        insta.add_post()
        sleep(3)
        insta.post()

