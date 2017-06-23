#!/usr/bin/python

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import sys
import os
import re
import pygame
import difflib
from pprint import pprint
from pyvirtualdisplay import Display
from bs4 import BeautifulSoup


def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', unicode(element)):
        return False
    return True

class site_handler:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 3)

    def start_connection(self, url):
        print "Connecting to " + url + " ..."
        try:
            self.driver.get(url)
        except:
            print "Could not connect to " + url
        print "Successfully connected"

    def end_connection(self):
        self.driver.close()

    def refresh(self):
        self.driver.refresh()

    def get_html(self):
        return self.driver.page_source

    def get_text(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        texts = soup.findAll(text=True)
        return filter(visible, texts)


if __name__ == '__main__':
    print "Initializing..."
    url = ""
    interval_period = 3
    sound = os.getcwd() + '/sound.wav'

    if len(sys.argv) == 1:
        print "Please provide url"
        sys.exit(0)
    elif len(sys.argv) >= 2:
        url = sys.argv[1]
        if len(sys.argv) == 3:
            interval_period = float(sys.argv[2])
        if len(sys.argv) == 4:
            sound = sys.argv[3]

    d = difflib.Differ()
    display = Display(visible=0, size=(800, 600))
    display.start()
    sh = site_handler()
    sh.start_connection(url)
    time.sleep(interval_period)
    update_found = False;
    page_html = sh.get_html()
    text = sh.get_text(page_html)
    print "Waiting for updates..."
    while update_found == False:
        page_html = sh.get_html()
        new_text = sh.get_text(page_html)
        if text == new_text:
            text = new_text
            sh.refresh()
            time.sleep(interval_period)
        else:
            print "Found Update on Page!"
            result = list(d.compare(text, new_text))
            pprint(result)
            update_found = True;

            pygame.mixer.init()
            try:
                pygame.mixer.music.load(sound)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy() == True:
                    continue
                    #pygame.time.Clock().tick(10)
            except:
                print "Cannot load sound: " + sound
                print "error message: " + pygame.get_error()


    display.stop()

