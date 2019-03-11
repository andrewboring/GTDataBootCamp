import requests
from bs4 import BeautifulSoup as bs
from splinter import Browser
import re
import pandas as pd

def scrape(): 
	
	headers = {
		'User-Agent': 'Shoe Scraper/1.0 (+https://a10g.com/shoe-scraper)'
	}

	news_url = "https://mars.nasa.gov/news/"
	news_response = requests.get(news_url, headers=headers)
	soup = bs(news_response.text, 'lxml')

	article_titles = soup.find_all('div', class_='content_title')
	news_titles = []
	for article in article_titles:
		title = article.find('a')
		title_text = title.text.strip()
		news_titles.append(title_text)

	paragraphs = soup.find_all('div', class_='rollover_description')
	news_content = []
	for paragraph in paragraphs:
		ptext = paragraph.find('div')
		newsp = ptext.text.strip()
		news_content.append(newsp)


	all_latest_news = dict(zip(news_titles, news_content))
	latest_title = news_titles[0]
	latest_content = news_content[0]

	mars_images_browser = Browser('chrome', headless=False)
	jpl_url = 'https://www.jpl.nasa.gov'
	space_img = 'spaceimages'
	qstring = '?search=&category=Mars'
	nasa_url = jpl_url + "/" + space_img + "/" + qstring

	mars_images_browser.visit(nasa_url)


	mars_images_html = mars_images_browser.html
	jpl_soup = bs(mars_images_html, 'html.parser')


	featured_image = jpl_soup.find_all('a', class_='button fancybox')
	featured_image[0].attrs
	jpl_img = featured_image[0]['data-fancybox-href']
	jpl_img_url = jpl_url + jpl_img 

	jpl_img_url_step1 = re.sub(r'mediumsize', 
    	                    r'largesize',
       		                jpl_img_url, re.IGNORECASE)
	jpl_img_url_lg = re.sub(r'_ip', 
   		                     r'_hires',
       		                 jpl_img_url_step1, re.IGNORECASE)
	mars_images_browser.quit()


	twiturl="https://twitter.com/marswxreport?lang=en"
	twitresponse = requests.get(twiturl)
	twitsoup = bs(twitresponse.text, 'lxml')

	tweets = twitsoup.find_all('p', class_='TweetTextSize')
	weather_on_mars = tweets[0].text
	weather_on_mars



	space_facts = 'https://space-facts.com/mars/'
	sf_table = pd.read_html(space_facts)

	mars_table = pd.DataFrame(sf_table[0])
	mars_table.columns=['Attribute', 'Value']
	mars_facts = mars_table.to_html()


	usgs_browser = Browser('chrome', headless=False)
	usgs_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
	usgs_browser.visit(usgs_url)
	mh_html = usgs_browser.html
	mh_soup = bs(mh_html, 'html.parser')


	mh = mh_soup.find_all('div', class_='description')
	mh_image_urls = []
	for image in mh:
		h_url = image.find('a', class_='itemLink')
		h = h_url.get('href')
		h_link = 'https://astrogeology.usgs.gov' + h

		usgs_browser.visit(h_link)
		h_image_dict = {}

		h_html = usgs_browser.html
		h_soup = bs(h_html, 'html.parser')

		h_link = h_soup.find('a', text='Original').get('href')

		h_title = h_soup.find('h2', class_='title').text.replace(' Enhanced', '')

		h_image_dict['title'] = h_title
		h_image_dict['img_url'] = h_link

		mh_image_urls.append(h_image_dict)

	usgs_browser.quit()


	mars_bars = {
    	'latest_news':{
        	'headline':latest_title,
        	'content':latest_content
    	},
    	'current_weather':weather_on_mars,
    	'jpl_featured_image':jpl_img_url_lg,
    	'facts':mars_facts,
    	'hemispheres':mh_image_urls    
	}
	return mars_bars

