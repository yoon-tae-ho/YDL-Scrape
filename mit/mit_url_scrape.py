import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pickle

def get_urls():
  chromedriver = "/opt/homebrew/bin/chromedriver"
  s = Service(chromedriver)
  # to use brave browser
  option = webdriver.ChromeOptions()
  option.binary_location = '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser'

  ##### Web scrapper for infinite scrolling page #####
  driver = webdriver.Chrome(service=s, options=option)
  driver.get("https://ocw.mit.edu/search/?f=Lecture%20Videos")
  time.sleep(2)  # Allow 2 seconds for the web page to open
  scroll_pause_time = 2 # You can set your own pause time. My laptop is a bit slow so I use 1 sec
  screen_height = driver.execute_script("return window.screen.height;")   # get the screen height of the web
  i = 1

  while True:
      # scroll one screen height each time
      driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
      i += 1
      time.sleep(scroll_pause_time)
      # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
      scroll_height = driver.execute_script("return document.body.scrollHeight;")  
      # Break the loop when the height we need to scroll to is larger than the total scroll height
      # print(f"scroll_height: {scroll_height}")
      # print(f"screen_height: {screen_height}")
      # print(f"screen_height * i: {screen_height * i}")
      if (screen_height) * i > scroll_height + 1:
          break 

  ##### Extract Reddit URLs #####
  urls = []
  soup = BeautifulSoup(driver.page_source, "html.parser")
  driver.close()
  for parent in soup.find_all("article"):
      title = parent.find("div", class_="course-title")
      a_tag = title.find("a")
      base = "https://ocw.mit.edu"
      link = a_tag.attrs['href']
      url = urljoin(base, link)
      urls.append(url)

  print("length of urls: ", len(urls))
  outp = open('mit_urls', 'wb')
  pickle.dump(urls, outp)
  outp.close()
  return