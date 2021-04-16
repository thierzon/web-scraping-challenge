from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
from webdriver_manager.chrome import ChromeDriverManager

def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=True)

def scrape():
    browser = init_browser()

    # Scrape NASA Mars News
    browser.visit('http://mars.nasa.gov/news')
    
    time.sleep(1)

    html = browser.html
    soup = bs(html, 'html.parser')

    article = soup.select_one('div.list_text')

    news_title = article.find('a').text

    news_p = article.find('div', class_='article_teaser_body').get_text()

    # Scrape JPL Mars Space Image
    browser.visit('http://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html')

    time.sleep(1)

    html = browser.html
    soup = bs(html, 'html.parser')

    image_url = soup.select_one('div.thmbgroup').find('a')['href']

    featured_image_url = 'http://data-class-jpl-space.s3.amazonaws.com/JPL_Space/' + image_url

    # Scrape Mars Facts
    facts_table = pd.read_html('http://space-facts.com/mars/')[0]
    facts_table.columns = ['Description', 'Mars']
    facts_table.set_index('Description', inplace=True)
    facts_html = facts_table.to_html(classes="table table-striped")

    # Scrape Mars Hemisphere images
    hemisphere_image_urls = [
        {"title": "Cerberus Hemisphere","img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg"},
        {"title": "Schiaparelli Hemisphere","img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg"},
        {"title": "Syrtis Major Hemisphere","img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg"},
        {"title": "Valles Marineris Hemisphere","img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg"}
    ]

    # Save data to Python Dictionary
    mars_data = {
        "news_title": news_title,
        "news_paragraph": news_p,
        "featured_image": featured_image_url,
        "facts_table": facts_html,
        "hemispheres": hemisphere_image_urls
    }

    # Close the browser after scraping
    browser.quit()
    
    # Return results
    return mars_data