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

				application.start()
				self.toStart.remove(application)

			else:
				print("Error: Application should be started but not ready yet")


if __name__ == '__main__':

	print("Started smartStart")

	with open("applications.json", "r") as f:

		startController = StartContoller(json.load(f))
