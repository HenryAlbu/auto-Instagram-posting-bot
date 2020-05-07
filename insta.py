import autoit, json, os, settings, platform
from time import sleep
from selenium import webdriver

# Variables
minimizeWindow = False  # True or False
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
    # Checks if on Mac or Windows
    if platform.system() == "Windows":
        driver = webdriver.Chrome(executable_path=r"chromedriver.exe", options=opts)
    else:
        driver = webdriver.Chrome(options=opts)

    # Opens Instagram
    main_url = "https://www.instagram.com"
    driver.get(main_url)
    sleep(10)
    ordered_functions()

def login():
    print("Logging into Instagram")
    driver.find_element_by_xpath("//button[contains(text(),'Log In')]").click()
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
    try:
        driver.find_element_by_xpath("//div[@role='menuitem']").click()
    except:
        pass


def post():
    print("Adding post")
    # Readies the content for instagram
    with open('filesDict.txt', encoding="utf8") as json_file:
        data = json.load(json_file)
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


    # Opens File Explore window
    print("Opening file explorer")
    autoit.win_active("Open")
    sleep(0)
    autoit.control_set_text("Open", "Edit1", image_path)
    autoit.control_send("Open", "Edit1", "{ENTER}")
    sleep(settings.wait_time)

    # Clicks through options and adds caption after file is added
    try:
        driver.find_element_by_xpath("//span[contains(text(),'Expand')]").click()
    except:
        pass
    sleep(settings.wait_time)
    driver.find_element_by_xpath("//button[contains(text(),'Next')]").click()
    sleep(settings.wait_time)
    caption_field = driver.find_element_by_xpath("//textarea[@aria-label='Write a caption…']")
    caption_field.send_keys(caption)
    driver.find_element_by_xpath("//button[contains(text(),'Share')]").click()
    if not settings.keep_images:
        os.remove(image_path)


# Executes functions in order
def ordered_functions():
    login()
    sleep(settings.wait_time)
    remove_popups()
    sleep(settings.wait_time)
    remove_popups()
    sleep(settings.wait_time)
    remove_popups()
    # Minimizes window if variable = True
    if minimizeWindow:
        driver.minimize_window()