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
import pygame
from pyvirtualdisplay import Display

class site_handler:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 3)

    def start_connection(self, url):
        self.driver.get(url)

    def end_connection(self):
        self.driver.close()

    def refresh(self):
        self.driver.refresh()

    def get_html(self):
        return self.driver.page_source

if __name__ == '__main__':
    url = ""
    interval_period = 3
    sound = os.getcwd() + '/sound.wav'

    if len(sys.argv) == 1:
        print "Please provide url"
        sys.exit(0)
    elif len(sys.argv) >= 2:
        url = sys.argv[1]
        if len(sys.argv) == 3:
            interval_period = sys.argv[2]
        if len(sys.argv) == 4:
            sound = sys.argv[3]

    display = Display(visible=0, size=(800, 600))
    display.start()
    sh = site_handler()
    sh.start_connection(url)
    update_found = False;
    page_html = sh.get_html()
    f = open("site.html", 'w')
    f.write(page_html.encode('utf-8'))
    while update_found == False:
        new_page_html = sh.get_html()
        f2 = open("new_site.html", 'w')
        f2.write(new_page_html.encode('utf-8'))
        if page_html == new_page_html:
            page_html = new_page_html
            time.sleep(interval_period)
            sh.refresh()
        else:
            print "Found Update on Page!"
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

