import subprocess as sp


class Application(object):
	"""
		Manage data of a application and provide functionality for starting the application
	"""
	def __init__(self, applicationJSON, timeZero):
		"""
			applicationJSON is the json data for the application and timeZero the time in which's relation the delay is calculated
		"""

		self.name = applicationJSON["application"]
		self.path = applicationJSON["path"]
		self.startTime = applicationJSON["delay"] + timeZero

		self.isStarted = False

	def start(self):
		"""
			Open the application in the background
		"""
		sp.Popen(["open", "-jg", self.path])
		self.isStarted = True
		print("Started {}".format(self.name))
