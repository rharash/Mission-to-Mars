#!/usr/bin/env python
# coding: utf-8

# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
from os import system

# Path to chromedriver
#get_ipython().system('where chromedriver')

# Set the executable path and initialize the chrome browser in splinter
# print(system('where chromedriver'))
# executable_path = {'executable_path': 'C:/Users/db2admin/Desktop/Class/Mission-to-Mars'}
# browser = Browser('chrome', **executable_path)
browser = Browser("chrome", executable_path="chromedriver", headless=True)

# Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

html = browser.html
news_soup = BeautifulSoup(html, 'html.parser')
slide_elem = news_soup.select_one('ul.item_list li.slide')

slide_elem.find("div", class_='content_title')

# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title

# Use the parent element to find the paragraph text
news_p = slide_elem.find("div", class_='article_teaser_body').get_text()
news_p

# to get the image- Visit URL
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_id('full_image')
full_image_elem.click()

# Find the more info button and click that
browser.is_element_present_by_text('more info', wait_time=1)
more_info_elem = browser.find_link_by_partial_text('more info')
more_info_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = BeautifulSoup(html, 'html.parser')

# Find the relative image url
img_url_rel = img_soup.select_one('figure.lede a img').get("src")
img_url_rel

# Use the base URL to create an absolute URL
img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
img_url

df = pd.read_html('http://space-facts.com/mars/')[0]
df.columns=['description', 'value']
df.set_index('description', inplace=True)
df

#convert our DataFrame back into HTML-ready code using the .to_html() function. 
df.to_html()
#end the automated browsing session. This is an important line to add to our web app also. Without it, the automated browser won’t know to shut down—it will continue to listen for instructions and use the computer’s resources (it may put a strain on memory or a laptop’s battery if left on). We really only want the automated browser to remain active while we’re scraping data.
browser.quit()

