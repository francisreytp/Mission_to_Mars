#%%
# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup
# import pandas
import pandas as pd
import datetime as dt
import requests

#%%
def scrape_all():
    # Initiate headless driver for deployment
    #browser = Browser('chrome', executable_path='chromedriver.exe', headless=False)
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path)

    news_title, news_paragraph = mars_news(browser)

#   # Hemisphere
#     mars_list = list()
#     names = ['Cerberus', 'Schiaparelli', 'Syrtis Major', 'Valles Marineris']
#     for name in names:
#         hemi_title, hemi_img_url = mars_hemispheres(browser,hemi_name)
#         hemi_dict = {"img_url":hemi_img_url, "title": hemi_title}
#         mars_list.append(hemi_dict)
  
    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        # "hemispheres": mars_hemispheres(browser), # replacing w (cerb_hemi, scha_hemi, syrt_hemi, vall_hemi)
        "cerb_hemi": cerb_hemi(browser),
        "scha_hemi": schi_hemi(browser),
        "syrt_hemi": syrt_hemi(browser),
        "vall_hemi": vall_hemi(browser),
        "last_modified": dt.datetime.now()
      }

    browser.quit()
    return data


#%%

def featured_image(browser):
    img_url = 'https://www.jpl.nasa.gov/spaceimages/?search=category=Mars'
    browser.visit(img_url)
    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')[0]
    full_image_elem.click()
        
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.find_link_by_partial_text('more info')
    more_info_elem.click()
        
    # Parse the resulting html with soup
    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')
    
    try:
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")
        img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
        return img_url
    except AttributeError:
        return None

#%%

# def featured_image(browser):
#     img_url = 'https://www.jpl.nasa.gov/spaceimages/?search=category=Mars'
#     browser.visit(img_url)
#     # Find and click the full image button
#     full_image_elem = browser.find_by_id('full_image')[0]
#     full_image_elem.click()

#     browser.is_element_present_by_text('more info', wait_time=1)
#     more_info_elem = browser.find_link_by_partial_text('more info')
#     more_info_elem.click()

#     # Parse the resulting html with soup
#     html = browser.html
#     img_soup = BeautifulSoup(html, 'html.parser')

#     try:
#         img_url_rel = img_soup.select_one('figure.lede a img').get("src")
#     except AttributeError:
#         return None
    
#     img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
#     return img_url


#%%
# mars_news
def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')
   
    try:
        slide_elem = news_soup.select_one('ul.item_list li.slide')
        # slide_elem.find("div", class_='content_title')
        news_title = slide_elem.find("div", class_='content_title').get_text()
        news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
    except AttributeError:
        return None, None
    
    return news_title, news_p


#%%
# mars_facts
def mars_facts():
    try:
        df = pd.read_html('http://space-facts.com/mars/')[0]
        df.columns=['Description', 'Mars']
        df.set_index('Description', inplace=True)
        return(df.to_html())
        # return df.to_html(classes="table table-striped")

    except BaseException:
        return None

    # # Assign columns and set index of dataframe
    # df.columns=['Description', 'Mars']
    # df.set_index('Description', inplace=True)
    # # Convert dataframe into HTML format, add bootstrap
    # return df.to_html(classes="table table-striped")

#%%
# def mars_hemispheres(browser):

#     hemisphere_url =  "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
#     browser.visit(hemisphere_url)

#     hemisphere_image_urls = []
#     for i in range(4):
#         browser.find_by_css("a.product-item h3")[i].click()
#         hemi_data = scrape_hemisphere(browser.html)
#         hemisphere_image_urls.append(hemi_data)
#         browser.back()
#     return hemisphere_image_urls
    
# #%%
# def scrape_hemisphere(html_text):
#     html_soup = BeautifulSoup(html_text, "html.parser")
#     try:
#         title_elem = html_soup.find("h2.title").get_text()
#         sample_elem = html_soup.find("a", text="Sample").get("href")
#     except AttributeError:
#         title_elem = None
#         sample_elem = None
#     hemispheres = {
#         "title": title_elem,
#         "img_url": sample_elem
#     }
#     return hemispheres
######################

def cerb_hemi(browser):
    try:
        hemi_url =  "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
        browser.visit(hemi_url)

        cerb_img = browser.find_by_text('Cerberus Hemisphere Enhanced', wait_time=1)
        cerb_img.click()
        
        html = browser.html
        cerb_title_soup = BeautifulSoup(html, 'html.parser')
        cerb_img_soup = BeautifulSoup(html, 'html.parser')
        
        # Find the title
        cerb_title = cerb_title_soup.find("h2", class_='title').get_text()
        # cerb_sample = cerb_img_soup.find("a", text="Sample").get("href")
        cerb_sample = browser.links.find_by_partial_text('Sample')
        cerb_sample.click()

        # cerb_hemisphere = {
        #     "CerbTitle": cerb_title,
        #     "CerbImg": 

        # Find the relative image url
        cerb_url = cerb_img_soup.select_one('img.wide-image').get('src')
        # Use the base URL to create an absolute URL
        cerb_img = f'https://astrogeology.usgs.gov{cerb_url}'
        return(cerb_img, cerb_title)
    except AttributeError:
        return None, None


def schi_hemi(browser):
    try:
        hemisphere_url =  "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
        browser.visit(hemisphere_url)

        schi_img = browser.find_by_text('Schiaparelli Hemisphere Enhanced', wait_time=1)
        schi_img.click()
        html = browser.html

        schi_title_soup = BeautifulSoup(html, 'html.parser')
        schi_img_soup = BeautifulSoup(html, 'html.parser')
        
        # Find the title
        schi_title = schi_title_soup.find("h2", class_='title').get_text()
        schi_sample = browser.links.find_by_partial_text('Sample')
        schi_sample.click()
        # Find the relative image url
        schi_url = schi_img_soup.select_one('img.wide-image').get('src')
        # Use the base URL to create an absolute URL
        schi_img = f'https://astrogeology.usgs.gov{schi_url}'
        return(schi_img, schi_title)
    except AttributeError:
        return None, None

def syrt_hemi(browser):
    try:
        hemisphere_url =  "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
        browser.visit(hemisphere_url)

        syrt_img = browser.find_by_text('Syrtis Major Hemisphere Enhanced', wait_time=1)
        syrt_img.click()
        html = browser.html

        syrt_title_soup = BeautifulSoup(html, 'html.parser')
        syrt_img_soup = BeautifulSoup(html, 'html.parser')
        
        # Find the title
        syrt_title = syrt_title_soup.find("h2", class_='title').get_text()
        syrt_sample = browser.links.find_by_partial_text('Sample')
        syrt_sample.click()
        # Find the relative image url
        syrt_url = syrt_img_soup.select_one('img.wide-image').get('src')
        # Use the base URL to create an absolute URL
        syrt_img = f'https://astrogeology.usgs.gov{syrt_url}'
        return(syrt_img, syrt_title)
    except AttributeError:
        return None, None


def vall_hemi(browser):
    try:
        hemisphere_url =  "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
        browser.visit(hemisphere_url)

        vall_img = browser.find_by_text('Valles Marineris Hemisphere Enhanced', wait_time=1)
        vall_img.click()
        html = browser.html

        vall_title_soup = BeautifulSoup(html, 'html.parser')
        vall_img_soup = BeautifulSoup(html, 'html.parser')
        
        # Find the title
        vall_title = vall_title_soup.find("h2", class_='title').get_text()
        vall_sample = browser.links.find_by_partial_text('Sample')
        vall_sample.click()
        # Find the relative image url
        vall_url = vall_img_soup.select_one('img.wide-image').get('src')
        # Use the base URL to create an absolute URL
        vall_img = f'https://astrogeology.usgs.gov{vall_url}'
        return(vall_img, vall_title)
    except AttributeError:
        return None, None


#%%

if __name__ == "__main__":
    print(scrape_all())

