#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt


# In[2]:


# function to initialize browser, create data dictionery, end the webdriver and return scraped data.
def scrape_all():

    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    news_title, news_paragraph = mars_news(browser)
    titles_url = mars_h(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres": titles_url,
        "last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data


# In[3]:


def mars_news(browser):

    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    try:

        slide_elem = news_soup.select_one('div.list_text')
        # slide_elem.find('div', class_='content_title')

        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # news_title

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
        # news_p

    except AttributeError:
        return None, None 

    return news_title, news_p


# In[4]:


# ### Featured Images

def featured_image(browser):

    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
        # img_url_rel

    except AttributeError:
        return None

    
    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    
    return img_url


# In[5]:


# ### Mars Facts

def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")

def mars_h(browser):
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    hemisphere_image_urls = []
    
    # Add try/except for error handling
    
    for mars in range(4):
        # Browse through each article
        browser.links.find_by_partial_text('Hemisphere')[mars].click()
    
        # Parse the HTML
        html = browser.html
        planet_soup = soup(html,'html.parser')
    
        # Scraping
        title = planet_soup.find('h2', class_='title').text
        img_url = planet_soup.find('li').a.get('href')
    
        # Store findings into a dictionary and append to list
        hemispheres = {}
        hemispheres['img_url'] = f'https://marshemispheres.com/{img_url}'
        hemispheres['title'] = title
        hemisphere_image_urls.append(hemispheres)
    
        # Browse back to repeat
        browser.back()

    return hemisphere_image_urls


# In[6]:


if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())


# In[ ]:




