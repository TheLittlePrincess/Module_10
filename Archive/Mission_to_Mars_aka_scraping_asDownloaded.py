#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# In[2]:

# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[3]:


# Visit the mars nasa news site
url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[11]:


#assigned slide_elem as the variable to look for the <div /> tag and its descendent 
# re: the other tags within the <div /> element. It is the parent so will be reference when we want to filter further
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')

#The . is used for selecting classes, such as list_text
# 'div.list_text' pinpoints the <div /> tag with the class of list_text. 
#CSS works from right to left, such as returning the last item on the list instead of the first. 
#Because of this, when using select_one, the first matching element returned will be a <li /> element 
#with a class of slide and all nested elements within it.


# In[12]:


# the module has an error, it says class=_'content...' but class is a reserved word, has to be class_
#assign the title and summary text to variables we'll reference later
# chain .find onto our previously assigned variable, slide_elem. (it means"This variable holds a ton of information.
# so look inside of that information to find this specific data.")
# The data we're looking for is the content title in a <div /> with a class of 'content_title'

slide_elem.find('div', class_='content_title')


# In[13]:


# Use the parent element to find the first `a` tag and save it as `news_title`
# when .get_text() is chained onto .find() is used, only the text of the element is returned 
# & not any of the HTML tags or elements
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[14]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# In[18]:


# There are two methods used to find tags and attributes with BeautifulSoup:
#.find() is used when we want only the first class and attribute we've specified.
#.find_all() is used when we want to retrieve all of the tags and attributes


# In[ ]:


#use markdown to separate the article scraping from the image scraping.


# # Featured Images

# In[19]:


# Visit URL
url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
browser.visit(url)


# In[ ]:


# the doc says there are 3 buttons, but actually there are 9


# In[24]:


# Find and click the full image button
# create a new variable to hold teh scraping result ('full_image_elem') 
# the browser finds an element by is tag using 'browser.find_by_tag('button')'
# splinter will 'click' the image to view it full size 'full_image_elem.click()'
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[25]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[26]:


# Find the relative image url
# tell BeautifulSoup to look inside the <img /> tag for an image with a class of fancybox-image. 
# An 'img' tag is nested within this HTML, included it
# .get('src') pulls the link to the image.
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[27]:


# Use the base URL to create an absolute URL
# img_url is the variable to hold the f-string
# use an f-string, because it's a cleaner way to create print statements
# The curly brackets hold a variable that will be inserted into the f-string when it's executed.

img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
img_url


# # Featured Tables

# In[29]:


# import pandas as pd


# In[ ]:


# Tables in HTML are basically made up of many smaller containers. The main container is the <table /> tag. 
#Inside the table is <tbody />, which is the body of the table—the headers, columns, and rows.
# <tr /> is the tag for each table row. Within that tag, the table data is stored in <td /> tags. 
#This is where the columns are established.


# In[30]:


# Function read_html() searches for and returns a list of tables found in the HTML. 
# pull the desired one by specifying an index, in this case 0 since we want the 1st one 
# assign columns (description', 'Mars', 'Earth') to the new DataFrame
# turn the Description column into the DataFrame's index
# use 'inplace=True' to have the updated index in place, without having to reassign the DF to a new variable
df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df


# In[ ]:


# df by itself calls it and prints it here


# In[32]:


# convert the DataFrame back into HTML-ready code so we can use then present it in OUR website
df.to_html()


# In[33]:


# end the automated browsing session. only want the automated browser to remain active while we're scraping data.
browser.quit()


# In[ ]:




