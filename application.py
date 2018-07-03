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

		self.flags = list(applicationJSON["flags"])

		self.isStarted = False

		# If internt connectivity is required then count the number of fails
		if "i" in self.flags:
			self.retryCount = 0

	def __repr__(self):
		return self.name

	def start(self):
		"""
			Open the application in the background
		"""
		sp.Popen(["open", "-jg", self.path])
		self.isStarted = True
		print("Started {}".format(self.name))
