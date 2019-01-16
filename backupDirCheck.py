#!/usr/bin/env python3

import sys, argparse

def main(argv=[]):
	excludeFilePath = None
	excludeFileContent = []

	parser = argparse.ArgumentParser()
	parser.add_argument('-v', '--verbosity', action="count", help="increase output verbosity (e.g., -vv is more than -v)")

	try:
		opts, args = getopt.getopt(argv,"hi:",["help", "excludeFile="])
	except getopt.GetoptError:
		print("Usage:")
		print(sys.argv[0]+ " -i <excludeFile>")
		sys.exit(2)

	for opt, arg in opts:
		if opt == '-h':
			print(sys.argv[0]+ " -i <excludeFile>")
			sys.exit()
		elif opt in ("-i", "--excludeFile"):
			excludeFilePath = arg

	with open(excludeFilePath, "r") as f:
		excludeFileContent = list(filter(None, f.read().splitlines()))

	print(excludeFileContent)

	for elem in excludeFileContent:
		if elem[0:1] == "+":
			print("Plus " + elem[1:].strip())

		elif elem[0:1] == "-":
			print("Minus " + elem[1:].strip())

		else:
			print("Not a valid exclude pattern. Ignoring it.")

if verbose:
    def verbosePrint(*verb_args):
            if verb_args[0] > (3 - verbose):
                print verb_args[1]
    else:
        _v_print = lambda *a: None  # do-nothing function

verboseprint = print( if verbose else lambda *a, **k: None

if __name__ == "__main__":
	# main(sys.argv[1:])
	verboseprint("look at all my verbosity!", object(), 3)
