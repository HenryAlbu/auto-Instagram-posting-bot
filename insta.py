#!/usr/bin/env Python3
from time import sleep
import json
import os
import autoit
import settings
import insta_scraper
import ninegag
from selenium import webdriver

# Variables
driver = ""


def launch_inst():
    global driver
    print("Opening instagram")

    # Chrome browser options
    mobile_emulation = {"deviceMetrics": {"width": 360, "height": 640, "pixelRatio": 3.0},
                        "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19"}
    opts = webdriver.ChromeOptions()
    opts.add_argument("window-size=1,765")
    opts.add_experimental_option("mobileEmulation", mobile_emulation)
    driver = webdriver.Chrome(executable_path=r"chromedriver.exe", options=opts)


    # Opens Instagram
    main_url = "https://www.instagram.com"
    driver.get(main_url)
    sleep(10)
    ordered_functions()


def login():
    # Logs into instagram
    print("Logging into Instagram")
    driver.find_element_by_xpath("//button[contains(text(),'Log In')]").click()
    # checks if user selected to login through facebook or regular method
    if settings.login_type == "Facebook":
        print("Going through Facebook")
        driver.find_element_by_xpath("//button[contains(text(),'Continue with Facebook')]").click()
        sleep(settings.wait_time)
        driver.find_element_by_xpath("//input[@name='email']").send_keys(settings.username)
        driver.find_element_by_xpath("//input[@name='pass']").send_keys(settings.password)
        sleep(settings.wait_time)
        driver.find_element_by_xpath("//button[@name='login']").click()
    else:
        sleep(settings.wait_time)
        driver.find_element_by_xpath("//input[@name='username']").send_keys(settings.username)
        driver.find_element_by_xpath("//input[@name='password']").send_keys(settings.password)
        sleep(settings.wait_time)
        driver.find_element_by_xpath("//button[@type='submit']").click()


def remove_popups():
    print("Removing any popups")
    try:
        driver.find_element_by_xpath("//a[contains(text(),'Not Now')]").click()
    except:
        try:
            driver.find_element_by_xpath("//button[contains(text(),'Not Now')]").click()
        except:
            try:
                driver.find_element_by_xpath("//button[contains(text(),'Cancel')]").click()
            except:
                pass


def add_post():
    # clicks add post button
    try:
        driver.find_element_by_xpath("//div[@role='menuitem']").click()
    except:
        pass


def post():
    print("Adding post")

    # Readies the content for instagram
    with open('filesDict.json', encoding="utf8") as json_file:

        # loads the data from the queue (filesDict.json)
        data = json.load(json_file)

        # if not empty
        if bool(data):

            # gets first item in filesDict.json and sets it as the next instagram upload
            # also sets the image path and caption
            image_path = os.getcwd() + "\\images\\" + data['dict'][0]['id'] + ".jpg"
            caption = data['dict'][0]['title']

            # Loops and removes the first item since it has just been uploaded
            for i in range(len(data)):
                if data['dict'][i]["id"] == data['dict'][0]['id']:
                    del data['dict'][i]
                    break

            # saves file without first item
            with open('filesDict.json', 'w', encoding="utf8") as outfile:
                json.dump(data, outfile)

    # Opens File Explore window
    print("Opening file explorer")
    autoit.win_active("Open")
    autoit.control_set_text("Open", "Edit1", image_path)
    autoit.control_send("Open", "Edit1", "{ENTER}")
    sleep(settings.wait_time)

    # depending on aspect ratio, sometimes this button does not exist
    try:
        driver.find_element_by_xpath("//span[contains(text(),'Expand')]").click()
    except:
        pass
    sleep(settings.wait_time)

    # clicks through options and adds caption after file is added
    driver.find_element_by_xpath("//button[contains(text(),'Next')]").click()
    sleep(settings.wait_time)
    caption_field = driver.find_element_by_xpath("//textarea[@aria-label='Write a caption…']")
    caption_field.send_keys(caption)
    driver.find_element_by_xpath("//button[contains(text(),'Share')]").click()


# Executes initial login and removing pop ups functions in order
def ordered_functions():
    login()
    sleep(settings.wait_time)
    remove_popups()
    sleep(settings.wait_time)
    remove_popups()
    sleep(settings.wait_time)
    remove_popups()



def loop_posting():
    while True:
        # Loops through at a set interval and adds another photo depending on the method the user chose
        if settings.post_source == "9gag":
            ninegag.get_data()
        else:
            # if keep_checking is true it will keep checking for new images else it will stop the program
            if settings.keep_checking or settings.counter == 0:
                insta_scraper.get_data()
            else:
                print("Program is done getting and posting previous user posts")
                break

        with open('filesDict.json', encoding="utf8") as data_file:
            settings.filesDict = json.load(data_file)
        # checks if post limit has been reached and queue is not empty
        if settings.filesDict['dict'] and settings.counter < settings.post_limit:
            remove_popups()
            sleep(settings.wait_time)
            add_post()
            sleep(settings.wait_time)
            post()
            sleep(settings.wait_time)
            remove_popups()
            settings.counter += 1
            print("Posting again in: " + str(settings.post_time))
        # if max post limit has been reached
        elif settings.counter >= settings.post_limit:
            print("The program has reached the max post limit of: " + str(settings.post_limit))
            break
        # if max post limit has not been reached but there are no new images
        else:
            print("Waiting for new images")
        sleep(settings.post_time)
