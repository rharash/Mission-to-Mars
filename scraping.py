# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt

##################SCRAPE ALL############################

def scrape_all():
    # Initiate headless driver for deployment
    browser = Browser("chrome", executable_path="chromedriver", headless=True)
    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
      "news_title": news_title,
      "news_paragraph": news_paragraph,
      "featured_image": featured_image(browser),
      "facts": mars_facts(),
      "last_modified": dt.datetime.now(),
      "title_url": title_hemisphere(browser),
      "image_url": image_hemisphere(browser)
      }

    browser.quit()

    return data

###########1.Scrape Mars Data: The News- Start################
# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': 'chromedriver'}
browser = Browser('chrome', **executable_path)

def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # set up the HTML parser
    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')
    
    #Try/except
    try:
        slide_elem = news_soup.select_one('ul.item_list li.slide')

        # Assign the title and summary text to variables
        slide_elem.find("div", class_='content_title')

        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find("div", class_='content_title').get_text()
        
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find("div", class_='article_teaser_body').get_text()
    
    except AttributeError:
        return None, None

    return news_p, news_title
#xxxxxxxxxxxxxx1.Scrape Mars Data: The News-Endxxxxxxxxxxxxx#

###############2.Scrape Mars Data: Featured Image-Start###########

def featured_image(browser):
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

    #Try/except
    try:
        # Find the relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")

    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'

    return img_url
#XXXXXXXXXXXXXXXX2.Scrape Mars Data: Featured Image- EndXXXXXXXXXXXXXXXXXX#
###############Challenge title-Start###########

def title_hemisphere(browser):

    # to get the image1- Visit URL
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    # Find the more info button and click that
    browser.is_element_present_by_css('a.image h3', wait_time=1)

    for i in range(4):
    #print(i)
        image_all_hemisphere = browser.find_by_css('a.image h3')[i].click()
        image_all_hemisphere
    #Try/except
        try:
            html = browser.html
            title_soup = BeautifulSoup(html, 'html.parser')
        
            # Use the base URL to create an absolute URL
            title_url = title_soup.find('h2', class_='title').get_text()
           
        except AttributeError:
            
            return title_url
            
    
#XXXXXXXXXXXXXXXXChallenge title- EndXXXXXXXXXXXXXXXXXX#


###############Challenge Image-Start###########

def image_hemisphere(browser):
     # to get the image1- Visit URL
     url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
     browser.visit(url)



     # Find the more info button and click that
     browser.is_element_present_by_css('a.image h3', wait_time=1)

   
     for i in range(4):
     #print(i)
        image_all_hemisphere = browser.find_by_css('a.image h3')[i].click()
        image_all_hemisphere
     #Try/except
        try:
            html = browser.html
            img_soup = BeautifulSoup(html, 'html.parser')

             # Use the base URL to create an absolute URL
            image_url = img_soup.select_one('ul li a').get('href')
            
        except AttributeError:
             return None

     return image_url
#XXXXXXXXXXXXXXXXChallenge Image- EndXXXXXXXXXXXXXXXXXX#

####################3.Scrape Mars Data: Mars Facts-Start###################

def mars_facts():
    #Try/except
    try:
        #use 'read_html" to scrape the facts table into a dataframe
        df = pd.read_html('http://space-facts.com/mars/')[0]

    except BaseException:
        return None
    
    #Assign columns and set index in dataframe
    df.columns=['description', 'value']
    df.set_index('description', inplace=True)
    
    #convert our DataFrame into HTML format,, add bootstrap-ready code using the .to_html() function. 
    return df.to_html()

#end the automated browsing session. This is an important line to add to our web app also. Without it, the automated browser won’t know to shut down—it will continue to listen for instructions and use the computer’s resources (it may put a strain on memory or a laptop’s battery if left on). We really only want the automated browser to remain active while we’re scraping data.
browser.quit()

#XXXXXXXXXXXXXXX3.Scrape Mars Data: Mars Facts-EndXXXXXXXXXXXXXXXXXXXXX

# ##################SCRAPE ALL############################

# def scrape_all():
#     # Initiate headless driver for deployment
#    browser = Browser("chrome", executable_path="chromedriver", headless=True)
#    news_title, news_paragraph = mars_news(browser)

#    # Run all scraping functions and store results in dictionary
# data = {
#       "news_title": news_title,
#       "news_paragraph": news_paragraph,
#       "featured_image": featured_image(browser),
#       "facts": mars_facts(),
#       "last_modified": dt.datetime.now()
#       }

#     browser.quit()

#     return data

#The final bit of code we need for Flask is to tell it to run. Add these two lines to the bottom of your script and save your work:
if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())