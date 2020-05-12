
<p align="center">
  <img src="https://i.imgur.com/jQ0Y5V6.png" width="154">
  <h1 align="center">Auto Instagram Posting Bot (AIPB)</h1>
  <p align="center">AIPB  <b>automates</b> your Instagram posts by taking images from sites like 9gag or other Instagram accounts and posting it onto your page. 
  </p>
  <p align="center">
    <a href="https://github.com/timgrossmann/InstaPy/blob/master/LICENSE">
      <img src="https://img.shields.io/badge/license-GPLv3-blue.svg" />
    </a>
    <a href="https://github.com/SeleniumHQ/selenium">
      <img src="https://img.shields.io/badge/built%20with-Selenium-yellow.svg" />
    </a>
    <a href="https://www.python.org/">
    	<img src="https://img.shields.io/badge/built%20with-Python3-red.svg" />
    </a>
	<p align="center">⭐️ Star this project on GitHub — it helps!  </p>
  </p>
</p>
<p align="center">
  <img src="https://media.giphy.com/media/iFV5dUAJQhloDkw9Zz/giphy.gif" width="">
</p>

## Features

* Adjustable interval between posts   
* Original captions/title as post captions  
* Multiple 9gag categories   
* Log into Instagram with Facebook credentials 
* Duplicate post prevention  
* Get Instagram users past photos and add to queue  
* Max post limit  
* Listens for new images 
* Automatically resizes images to fit Instagram  
* Simulates real clicking
   
<p align="center">
  <img src="https://i.imgur.com/do77oSN.png" width="70%">
</p> 

  
  
## Installation  
  
Clone or download this repo:
`` git clone https://github.com/HenryAlbu/auto-Instagram-posting-bot.git``

Go to the project directory
`` cd auto-Instagram-posting-bot ``

Install the requirements:
``pip install -r requirements.txt``  

This project is Selenium based and requires a `chromedriver`. I have already included one in the project files for Chrome 81/Windows. If you want to get a newer version or for a different OS, [download it here](https://sites.google.com/a/chromium.org/chromedriver/downloads) and drag and drop it into the directory.

## Running
Just run: 
``python app.py``

 
## File structure
  

| Files/Folders | Description |
| --- | --- |
| app.py | The main file for the project contains the UI and connections calls the other files. (Run this file) |
| insta.py | Contains the functions and steps that sign you into Instagram. Also contains the Selenium driver options |
| ninegag.py | Contains the functions to download and queue up 9gag posts   |
| settings.py | Contains the global variables   |
| insta_scraper.py | Contains the functions to download and queue up scrapped Instagram posts from selected user   |
| filesCheck.txt | (created on initial run) Contains the id's of images that have been downloaded to prevent duplicate uploads (keeps the last 50 id's) |
| filesDict.json | (created on initial run) When images are downloaded they are given an id's and put into this JSON file that acts as the queue |
| images (folder) | (created on initial run) Where the images are downloaded to.  |

  
  
## UI (PySimpleGUI)
https://github.com/PySimpleGUI/PySimpleGUI
<p align="center">
  <img src="https://i.imgur.com/wOwNMsi.png" width="70%">
</p>   
  
  
## Limitations  
  
Currently, the bot only uploads images. This is due to the fact that it is using Selenium to interact with the Instagram web interface. The Instagram interface only allows for uploads of images. (currently looking into a way around this)
  
 ## Caution 
  
This project uses Selenium. What this means is that it does not use the Instagram API for posting, making Instagram think that it's a real user posting, **BUT**
You should still be cautious by setting a reasonable wait times before posts. By default, this is set at 50 seconds. If you set it to something like 10 seconds, there is a chance that Instagram will notice bot activity. 

## TODOs
* Adding Imgur.com to the list of options to take images from

* Ability to add your own files to queue. Kind of like those sites that charge you to schedule Instagram posts.

* Figuring out how to get videos to upload

If you want to contribute to the project, I would greatly appreciate it :) 

  
## License

This code is in no way affiliated with, authorized, maintained, sponsored, or endorsed by Instagram, Facebook inc. or any of its affiliates or subsidiaries. This is an independent and unofficial API. Use it at your own risk.
