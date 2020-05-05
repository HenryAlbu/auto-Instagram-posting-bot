import autoit, json, os
from time import sleep
from selenium import webdriver

# Variables
username = ""
password = ""
minimizeWindow = False  # True or False

# Chrome browser options
mobile_emulation = {"deviceMetrics": {"width": 360, "height": 640, "pixelRatio": 3.0},
                    "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19"}
opts = webdriver.ChromeOptions()
opts.add_argument("window-size=1,765")
opts.add_experimental_option("mobileEmulation", mobile_emulation)
driver = webdriver.Chrome(executable_path=r"chromedriver.exe", options=opts)  # you must enter the path to your driver

# Opens Instagram
main_url = "https://www.instagram.com"
driver.get(main_url)
sleep(4)


def login():
    print("In login")
    login_button = driver.find_element_by_xpath("//button[contains(text(),'Log In')]")
    login_button.click()
    sleep(2)
    username_input = driver.find_element_by_xpath("//input[@name='username']")
    username_input.send_keys(username)
    password_input = driver.find_element_by_xpath("//input[@name='password']")
    password_input.send_keys(password)
    sleep(1)
    password_input.submit()


def remove_popups():
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


def close_save_info():
    print("Close Save Info")
    try:
        driver.find_element_by_xpath("//a[contains(text(),'Not Now')]").click()
    except:
        pass


def close_get_notification():
    print("Close get notification")
    try:
        driver.find_element_by_xpath("//button[contains(text(),'Not Now')]").click()
    except:
        pass


def close_add_to_home():
    try:
        print("close add to home")
        driver.find_element_by_xpath("//button[contains(text(),'Cancel')]").click()
    except:
        print("passed")
        pass


def add_post():
    try:
        print("add post")
        driver.find_element_by_xpath("//div[@role='menuitem']").click()
    except:
        print("passed")
        pass


def post():
    # Readies the content for instagram
    with open('filesDict.txt', encoding="utf8") as json_file:
        data = json.load(json_file)
        print("Instagram" + str(data))
        if bool(data):
            # gets first item in filesDict and sets it as the next instagram upload
            image_path = os.getcwd() + "\\files\\" + data['dict'][0]['id'] + ".jpg"
            caption = data['dict'][0]['title']
            # Loops and removes the first item since it has been uploaded
            for i in range(len(data)):
                if data['dict'][i]["id"] == data['dict'][0]['id']:
                    del data['dict'][i]
                    break

            # saves file without first item
            with open('filesDict.txt', 'w', encoding="utf8") as outfile:
                json.dump(data, outfile)

            print(image_path)
            print(caption)

    # Opens File Explore window
    print("Starting open")
    autoit.win_active("Open")
    print("Starting open Edit 1")
    autoit.control_send("Open", "Edit1", image_path)
    autoit.control_send("Open", "Edit1", "{ENTER}")
    sleep(2)

    # Clicks through options and adds caption after file is added
    try:
        driver.find_element_by_xpath("//span[contains(text(),'Expand')]").click()
    except:
        pass
    sleep(5)
    driver.find_element_by_xpath("//button[contains(text(),'Next')]").click()
    sleep(5)
    caption_field = driver.find_element_by_xpath("//textarea[@aria-label='Write a caption…']")
    caption_field.send_keys(caption)
    driver.find_element_by_xpath("//button[contains(text(),'Share')]").click()
    os.remove(image_path)


# Executes functions in order
def orderedFunctions():
    login()
    sleep(5)
    remove_popups()
    sleep(5)
    remove_popups()
    sleep(5)
    remove_popups()
    sleep(5)
    sleep(5)
    add_post()
    sleep(5)
    post()
    sleep(5)
    remove_popups()
    # Minimizes window if variable = True
    if minimizeWindow:
        driver.minimize_window()
