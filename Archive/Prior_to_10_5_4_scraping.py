# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager

# new function to 1. Initialize the browser 2. Create a data dictionary and 
# 3.End the WebDriver and return the scraped data (from 10.5.3)
def scrape_all():
    # Initiate headless driver for deployment
    ## Set the executable path and initialize the chrome browser in splinter
    # the "headless" browsing session is when a browser is run without the users seeing it at all. 
    # So, when headless=True is declared as we initiate the browser, we are telling it to run in 
    # headless mode. All of the scraping will still be accomplished, but behind the scenes.
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

# set news title and paragraph variables (remember, this function will return two values).
    news_title, news_paragraph = mars_news(browser)

# Run all scraping functions and store results in dictionary to run all functions and store results
# When we create the HTML template, we'll create paths to the dictionary's values, 
# to present our data on our template.
# add the date the code was run last - must import datetime as dt to work
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
    }

# end the automated browsing session. only want the automated browser to remain active while we're scraping data.
# Add the return statement - This is the final line that will signal that the function is complete
# want to return the data dictionary created earlier, so our return statement will simply read return data.

    # Stop webdriver and return data
    browser.quit()
    return data

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

# The last step is  similar to the last code block in our app.py file to tell Flask that 
# our script is complete and ready for action
# The print statement will print out the results of our scraping to our terminal after executing the code.

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())










