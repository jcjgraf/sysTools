# /usr/bin/env python3
"""

"""

from application import Application
import json
import os  # Absolut file path
import socket  # For checking if we have internet connectivity

import time


class StartContoller(object):

	def __init__(self, applicationsJSON):
		self.timeZero = time.time()
		self.applications = [Application(applicationJSON, self.timeZero) for applicationJSON in applicationsJSON["applications"]]

		self.config = self.loadConfig()

		# Hold the application such that the first one is the next to launch. After launch they are removed
		self.toStart = sorted(self.applications, key=lambda application: application.startTime)

		self.start()

	def start(self):
		"""
			While not all applications are started. Get the first one and wait for the deltatime. Launch the application then
		"""
		while len(self.toStart):

			application = self.toStart[0]  # get next application to start

			# Get time till next launch
			delaTime = application.startTime - time.time()

			if delaTime >= 0:
				time.sleep(delaTime)

			else:
				time.sleep(0)

			if application.startTime <= time.time() and not application.isStarted:

				# Check flags
				for flag in application.flags:
					if flag == "i" and not isConnected():

						application.retryCount += 1
						if application.retryCount >= self.config["maxRetry"]:

							self.toStart.remove(application)
							self.isStarted = False
							break

						application.startTime = application.startTime + int(self.config["retryTime"])
						print("Not internet connectivity. Delay restart of {}".format(application.name))
						self.toStart = sorted(self.toStart, key=lambda application: application.startTime)

						break

				else:
					application.start()
					self.toStart.remove(application)
					print("Remaining applications to start: {}".format(self.toStart))

					continue

			else:
				"""
					Should not be called
				"""
				print("Error: Application {} should be started but not ready yet".format(application.name))

	def loadConfig(self):
		"""
			Return the json of the config
		"""
		jsonPath = os.path.split(os.path.abspath(__file__))[0]
		with open(jsonPath + "/config.json", "r") as f:
			return json.load(f)


def isConnected(host="8.8.8.8", port=53):
	"""
		Checking if we are connected to the internet by trying to establish
		a connection to google's DNS server
	"""

	try:
		socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
		return True

	except Exception as e:
		return False


if __name__ == '__main__':

	print("Started smartStart")

	# Absolut path regardless on the location of the project
	jsonPath = os.path.split(os.path.abspath(__file__))[0]

	with open(jsonPath + "/applications.json", "r") as f:

		startController = StartContoller(json.load(f))
