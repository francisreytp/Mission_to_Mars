# Mission_to_Mars

Our objective is to scrape information about Mars. Those data will then be displayed on a webpage Flask, with the help of MongoDB.

### Scraping
-- import necessary dependencie
-- connected to the chromedriver and set up my browser to open each webpage I needed to scrape.
-- I first scraped website for the title and text of the most recent article, storing the results in variables to be referenced later. The second page, was the Jet Propulsion Laboratory’s Mars page, where I would grab the full-sized featured image.Next, was scraping Mars facts from the Space Facts website.Lastly, I wanted to grab the images and names of all four of Mars’ hemispheres from the USGS Astrogeology page.

Flask
In a separate file, Flask was used to trigger the scrape function, update the Mongo database with the results, and then return that record of data from the database on a webpage.

Files
app.py
index.htm
mission_to_mars.ipynb
scrapping.py
