#!/usr/bin/env python3

import sys, os, argparse

verbosePrint = None

def main():
	excludeFilePath = None
	excludeFileContent = []
	backupDir = None

	parser = argparse.ArgumentParser()
	parser.add_argument("-v", "--verbosity", action="count", help="increase output verbosity (e.g., -vv is more than -v)")
	parser.add_argument("-i", "--excludePatternFile", type=argparse.FileType('r'), help="provide path to the exclude-pattern file")
	parser.add_argument("-b", "--backupDir", help="path to the backup directory")

	args = parser.parse_args()

	if args.verbosity:
		def _verbosePrint(*verb_args):
			if verb_args[0] > (3 - args.verbosity):
				print(verb_args[1])
	else:
		_verbosePrint = lambda *a: None

	global verbosePrint
	verbosePrint = _verbosePrint

	if args.backupDir:
		backupDir = args.backupDir.rstrip("/")

	if args.excludePatternFile and backupDir is not None:

		with args.excludePatternFile as f:
			excludeFileContent = list(filter(None, f.read().splitlines()))

		for elem in excludeFileContent:
			if elem[0:1] == "+":
				path = elem[1:].strip()
				verbosePrint(1, "Plus {}".format(path))

				if not isDirValid(backupDir + path, True):
					verbosePrint(3, "Warning: Path {} should exist in the backupdir {} but it does not: {}".format(path, backupDir, backupDir + path))
				else:
					verbosePrint(1, "Path {} exists in backupdir {}".format(path, backupDir))

			elif elem[0:1] == "-":
				path = elem[1:].strip()
				verbosePrint(1, "Minus {}".format(path))

				if not isDirValid(backupDir + path, False):
					verbosePrint(3, "Warning: Path {} should not exist in the backupdir {} but it is there: {}".format(path, backupDir, backupDir + path))
				else:
					verbosePrint(1, "Path {} is not available in backupdir {}".format(path, backupDir))

			else:
				verbosePrint(2, "Not valid entry: {}".format(elem))

	else:
		verbosePrint(3, "Command not valid, please refere to the help page")

def isDirValid(path, shouldExist):

	if (os.path.isdir(path) and shouldExist) or (not os.path.isdir(path) and not shouldExist):
		return True

	else:
		return False

if __name__ == "__main__":
	main()
