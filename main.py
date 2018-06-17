# /usr/bin/env python3
"""

"""

from application import Application
import json

import time


class StartContoller(object):

	def __init__(self, applicationsJSON):
		self.timeZero = time.time()
		self.applications = [Application(applicationJSON, self.timeZero) for applicationJSON in applicationsJSON["applications"]]

		self.start()

	def start(self):
		while True:

			currentTime = time.time()

			for application in self.applications:

				if application.startTime <= currentTime and not application.isStarted:
					application.start()

			time.sleep(1)


if __name__ == '__main__':

	print("Started smartStart")

	with open("applications.json", "r") as f:

		startController = StartContoller(json.load(f))
