import sys
import os
import argparse
import hashlib

parser = argparse.ArgumentParser(description='Hash base file duplication detection.')
parser.add_argument('directories', nargs='+')
parser.add_argument('--logfile', default=sys.stdout, type=argparse.FileType('w'))
parser.add_argument('--verbose', action='store_true')
actionGroup = parser.add_mutually_exclusive_group()
actionGroup.add_argument('--move', metavar='DESTINATION')
actionGroup.add_argument('--delete', action='store_true')

args = parser.parse_args()
print(args)

localDuplicates = 0
actionsPreformed = 0
knownHashes = set()

directoryIndex = 0
for directory in args.directories:
	directoryIndex += 1
	directoryHashes = set()
	for dirpath, dirnames, filenames in os.walk(directory):
		for name in filenames:
			file = os.path.join(dirpath, name)
			newFile = ''
			with open(file, 'rb') as f:
				hash = hashlib.sha1(f.read()).hexdigest()
				if hash in directoryHashes:
					args.logfile.write("Skipping local duplicate - " + file + "|" + hash + "\n")
					localDuplicates += 1
					continue
				else:
					directoryHashes.add(hash)
				
				if hash in knownHashes:
					if args.delete:
						args.logfile.write("Deleting file - " + file + "|" + hash + "\n")
					elif args.move:
						oldFile = file
						newFile = os.path.join(args.move, str(directoryIndex), file[len(directory)+1:])

						args.logfile.write("Moving file to " + newFile + " - " + file + "|" + hash + "\n")
					else:
						args.logfile.write("Duplicate file - " + file + "|" + hash + "\n")
					actionsPreformed += 1
				else:
					knownHashes.add(hash)
					if args.verbose:
						args.logfile.write("New global hash found - " + file + "|" + hash  + "\n")
			if newFile != '':
				os.renames(oldFile, newFile)

args.logfile.write("localDuplicate=" + str(localDuplicates) + " actionsPreformed=" + str(actionsPreformed) + " knownHashes=" + str(len(knownHashes)) + "\n")
