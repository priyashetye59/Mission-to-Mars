#!/usr/bin/env python
# coding: utf-8

# In[1]:


from webdriver_manager.chrome import ChromeDriverManager
import datetime as dt
import pandas as pd
from bs4 import BeautifulSoup as soup
from splinter import Browser


# In[2]:


def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)


# In[3]:


news_title, news_paragraph = mars_news(browser)


# In[ ]:


# Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemisphere": hemisphere_data(browser),
        "last_modified": dt.datetime.now()
    }


# In[4]:


# Stop webdriver and return data
 browser.quit()
 return data


# In[5]:


def mars_news(browser):

    # Scrape Mars News
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
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find(
            'div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p


# In[6]:


def featured_image(browser):
    # Visit URL
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

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


# In[7]:


def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html(
            'https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns = ['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")


# In[8]:


def hemisphere_data(browser):
    # 1. Use browser to visit the URL
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    html = browser.html
    hemisphere_soup = soup(html, 'html.parser')

    # 2. Create a list to hold the images and titles.
    hemisphere_info = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    items = hemisphere_soup.find(
        'div', class_='collapsible results').find_all('div', class_='item')

    # Find the title urls
    titles = [i.find('h3') for i in items]
    titles = [i.text for i in titles]

    # Find the image urls
    images_url = [i.find('a', class_='itemLink product-item') for i in items]
    images_url = [i.get('href') for i in images_url]

    images = []
    for i in images_url:
        img_url = url + i

        browser.visit(img_url)
        html = browser.html
        image_soup = soup(html, 'html.parser')

        image_link = image_soup.find('div', class_='downloads')
        image_link = image_link.find('a')
        image_link = image_link.get('href')
        images.append(url + image_link)
        
    # Create a list of the images_url and titles
    [hemisphere_info.append({'image': images[i], 'title': titles[i]})
     for i in range(len(images))]

    return hemisphere_info


# In[9]:


if __name__ == "__main__":

    # If running as script, print scraped data
    print(mars_facts())


# In[ ]:




