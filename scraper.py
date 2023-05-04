from PIL import Image
from pygame.image import frombuffer
from pygame.transform import scale
from requests_html import HTMLSession
from requests import ConnectionError
from consts import *

class Scraper:
	def __init__(self):
		self.urls = {"tv":{"img":"https://www.themoviedb.org/t/p/w600_and_h900_bestv2/{}.jpg",
						   "search":"https://www.themoviedb.org/search/tv?query={}",
						   "embed":"https://www.2embed.ru/embed/tmdb/tv?id={}&s={}&e={}"},
					 "movie":{"img":"https://www.themoviedb.org/t/p/w600_and_h900_bestv2/{}.jpg",
						 	  "search":"https://www.themoviedb.org/search/movie?query={}",
							  "embed":"https://www.2embed.ru/embed/tmdb/movie?id={}"},
					 "host":"https://www.themoviedb.org"}
								 
		self.session = HTMLSession()
		
		self.reset()
		
	def reset(self):
		self.info = None 
		self.error = None 
		self.got_info = False 
		self.running = False 
		
	def get_results(self, type, query):
		self.info = None
		self.got_info = False 
		
		try:
			response = self.session.get(self.urls[type]["search"].format(query))
		except ConnectionError:
			self.error = "No internet"
		
		if self.error != "No internet":
			if response.status_code == 200:
				try:
					results = response.html.find(".results", first=True).find(".card")
					if len(results) > MAX_RESULTS:
						results = results[:MAX_RESULTS]
					for result in results:
						info = result.find(".result", first=True)
						img_info = info.find("img", first=True)
						if img_info != None:
							img = Image.open(self.session.get(self.urls[type]["img"].format(img_info.attrs["src"][25:-4]), stream=True).raw).convert("RGB")
							item = (img_info.attrs["alt"], scale(frombuffer(img.tobytes(), img.size, "RGB"), (IMG_W, IMG_H)), self.urls["host"] + info.attrs["href"])
							try:
								self.info.append(item)
							except AttributeError:
								self.info = [item]
					if self.info == None:
						self.error = "No results"
					else:
						self.got_info = True
				except:
					self.error = "Data error"
			else:
				self.error = "Connection error"
		
		self.running = False
			
	def get_page(self, url):
		self.info = None 
		self.got_info = False
		
		try:
			response = self.session.get(url)
		except ConnectionError:
			self.error = "No internet"
		
		if self.error != "No internet":
			if response.status_code == 200:
				try:
					if url[27:29] == "tv":
						type = "tv"
					else:
						type = "movie"
					facts = response.html.find(".facts", first=True)
					episodes = response.html.find(".season", first=True)
					self.info = {"Score":int(float(response.html.find(".user_score_chart", first=True).attrs["data-percent"])),
								 "Year":response.html.find(".tag", first=True).text[1:-1]}
					if episodes != None:
						self.info["Lastest season"] = episodes.find("h4", first=True).text.replace("|", "-")
						self.info["Type"] = "TV"
					else:
						self.info["type"] = "Movie"
						self.info["Length"] = facts.find(".runtime", first=True).text
					genres = facts.find("a")
					if len(genres) > MAX_GENRES:
						genres = genres[:MAX_GENRES]
					self.info["Genres"] = ", ".join(genre.text for genre in genres)
					if "TV Movie" in self.info["Genres"]:
						self.info["Genres"].remove("TV Movie")
					img = Image.open(self.session.get(self.urls["host"] + response.html.find(".image_content", first=True).find("img", first=True).attrs["src"].replace("w300", "w600").replace("h450", "h900").replace("_filter(blur)", ""), stream=True).raw).convert("RGB")
					self.info["image"] = scale(frombuffer(img.tobytes(), img.size, "RGB"), (IMG_LW, IMG_LH))
					self.info["link"] = url 
					self.info["name"] = response.html.find(".title", first=True).find("a", first=True).text
					
					if url[27:32] == "movie":
						id = url[33:].split("-")[0]
						link = self.urls["movie"]["embed"].format(id)
					else:
						id = url[30:].split("-")[0]
						link = self.urls["tv"]["embed"].format(id, 1, 1)
					self.info["watch"] = None
					response = self.session.get(link)
					if response.status_code == 200:
						heading = response.html.find(".heading-large", first=True) #check if video 404
						if heading == None:
							self.info["watch"] = link
							
					self.got_info = True
				except:
					self.error = "Data error"
			else:
				self.error = "Connection error"
			
		self.running = False