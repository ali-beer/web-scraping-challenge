from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import time


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    browser = init_browser()

    # NASA Mars News
    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Time delay for landing page 1 second 
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)
    # time.sleep(1) - allow 1 second for complete page content to be loaded

    # Create a Beautiful Soup object
    html = browser.html # grab the current page html
    soup = bs(html, 'html.parser') # parsing the html to create a beautful soup object, then you can use find to scrape info 

    # Collect the latest News Title
    # News titles are returned as an iterable list
    news_titles = soup.find_all('div', class_="content_title")

    # Create list to hold news titles
    titles = []

    # Loop through returned results
    for news in news_titles:
        # Error Handling
        try:
            # Identify and return title of news and print results
            title = news.find('a').text   
            titles.append(title)
        except:
            pass

    # Get the first titles in the titles list
    latest_title = titles[0]

    # Collect the latest News Paragraph Text
    news_p = soup.find('div', class_="article_teaser_body").text

    # JPL Mars Space Images
    # URL of page to be scraped
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Splinter interacting with browser - click 'full image' 'button'
    browser.click_link_by_partial_text('FULL IMAGE')

    # Splinter interacting with browser - click 'more info' 'button'
    browser.click_link_by_partial_text('more info')

    # Create a Beautiful Soup object (Scrape page into Soup)
    html = browser.html
    soup = bs(html, 'html.parser')

    # Find the image url
    image = soup.find_all('div', class_="download_tiff")

    # Use square brackets to grab href
    thread = image[1]
    featured_image_url = thread.find('a')['href']

    ## Mars Facts
    # Use read_html function in Pandas to scrape tabular data from page
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)

    # Use indexing to slice off the df containing facts about the planet including Diameter, Mass, etc.
    mars_df = tables[0]

    # Rename columns
    df = mars_df.rename(columns={0: "Facts", 1: "Mars"})

    # Set the index
    df.set_index("Facts", inplace=True)

    # Use Pandas to_html method to generate html table from df
    html_table = df.to_html()

    # Strip unwanted new lines to clean up the table
    html_table = html_table.replace('\n', '')

    # Save the table directly to a file for displaying on webpage later
    # df.to_html('table.html')

    # Mars Hemispheres
    # URL of pages to be scraped
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    # Create the list for the 4 hemisphere dicts 
    hemisphere_image_urls = []

    # First, get a list of all of the hemispheres
    links = browser.find_by_css("a.product-item h3")

    # Next, loop through those links, click the link, find the sample anchor, return the href
    for i in range(len(links)):
        
        hemisphere = {}
        
        # Find the elements on each loop to avoid a stale element exception
        browser.find_by_css("a.product-item h3")[i].click()
        
        # Next, find the Sample image anchor tag and extract the href
        sample_elem = browser.links.find_by_text('Sample').first
        hemisphere['img_url'] = sample_elem['href']
        
        # Get Hemisphere title
        hemisphere['title'] = browser.find_by_css("h2.title").text
        
        # Append hemisphere dict to list
        hemisphere_image_urls.append(hemisphere)
        
        # Navigate backwards and complete for remaining hemisphere's
        browser.back()

    # Store data in a dictionary
    mars_data = {
        "Latest news title": latest_title,
        "Latest news paragraph": news_p,
        "Featured image": featured_image_url,
        "html table": html_table,
        "Hemisphere image urls": hemisphere_image_urls
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data
