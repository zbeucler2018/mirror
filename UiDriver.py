

from selenium import webdriver
import sys

class UI_Driver:
	def __init__(self, port):
		self.URL = "http://localhost:"+str(port)
		self.current_wallpaper = ""

		options = webdriver.ChromeOptions()
		# https://peter.sh/experiments/chromium-command-line-switches/
		options.add_experimental_option("useAutomationExtension", False)
		options.add_experimental_option("excludeSwitches",["enable-automation"])
		options.add_argument("--kiosk") 													# make the window full screen and remove the activity bar
		

		self.driver = webdriver.Chrome(options=options)

		try:
			self.driver.get(self.URL)
		except Exception as e:
			if e == "Message: unknown error: net::ERR_CONNECTION_REFUSED":
				print("Please start the web server")
			sys.exit(0)




	def change_ui(self, name):
		if name == self.current_wallpaper or name is None: return

		
		if name == "init":
			self.driver.get(self.URL)
			self.current_wallpaper = name
		#elif name == "one":								# Newton's craddle
		#	self.driver.get(self.URL+"/....")
		#	self.current_wallpaper = name
		#elif name == "two":								# weather?
		#	self.driver.get(self.URL+"/....")
		#	self.current_wallpaper = name
		elif name == "three":
			self.driver.get(self.URL+"/Rain/rain.html")
			self.current_wallpaper = name
		elif name == "four":
			self.driver.get(self.URL+"/Clock/clock.html")
			self.current_wallpaper = name
		elif name == "five":
			self.driver.get(self.URL+"/PomodoroTimer/timer.html")
			self.current_wallpaper = name
		#elif name == "closed": 							# close the programs and reboot the microcontroller?
		#	self.driver.get(self.URL+"/....")
		#	self.current_wallpaper = name

"""
snow falling: https://editor.p5js.org/codingtrain/sketches/UMUPBVuH5
hyper jump https://editor.p5js.org/codingtrain/sketches/1wLHIck3T
Wifi speed test


"""



			



