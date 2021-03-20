# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

## insert original code into a function
## add an argument to the function in this case 'browser' to tell Python 
## that we'll be using the browser variable we defined outside the function
def mars_news(browser):

   # Visit the mars nasa news site
   url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
   browser.visit(url)

   # Optional delay for loading the page
   browser.is_element_present_by_css('div.list_text', wait_time=1)

   # Convert the browser html to a soup object and then quit the browser
   html = browser.html
   news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
    ## Instead of having title and paragraph printed within the function 
    ## return them from the function so they can be used outside of it
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    ##news_p
    except AttributeError:
        return None, None
    #include them in the return statement instead
    return news_title, news_p

#use markdown to separate the article scraping from the image scraping.


# # Featured Images
## Declare and define function
## remove print statement(s) and return them instead
def featured_image(browser):
    # Visit URL
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

# the doc says there are 3 buttons, but actually there are 9
    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'

    return img_url


# # Featured Tables
# import pandas as pd

def mars_facts():
    # Add try/except for error handling
    try:
      ## Search for and returns the first table - thus use [0] - found in the HTML.     
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]

# Use BaseException which is a catchall when it comes to error handling. 
# It is raised when any of the built-in exceptions are encountered and it won't handle any user-defined 
# exceptions. We're using it here because we're using Pandas' read_html() function to pull data, 
# instead of scraping with BeautifulSoup and Splinter.
    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html()

# IMPORTANT section 10.5.2 does NOT include tHE browser.quit so check here if something

# end the automated browsing session. only want the automated browser to remain active while we're scraping data.
browser.quit()






