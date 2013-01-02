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
knownHashes = []
for directory in args.directories:
  directoryHashes = []
	for dirpath, dirnames, filenames in os.walk(directory):
		for name in filenames:
			with open(os.path.join(dirpath, name), 'rb') as f:
				hash = hashlib.sha1(f.read()).hexdigest()
				if hash in directoryHashes:
					localDuplicates += 1
					args.logfile.write("Skipping local duplicate - " + os.path.join(dirpath, name) + "|" + hash + "\n")
					continue
				else:
					directoryHashes.append(hash)
				
				if hash in knownHashes:
					actionsPreformed += 1
					if args.delete:
						args.logfile.write("Deleting file - " + os.path.join(dirpath, name) + "|" + hash + "\n")
					elif args.move:
						args.logfile.write("Moving file to " + args.move + " - " + os.path.join(dirpath, name) + "|" + hash + "\n")
					else:
						args.logfile.write("Duplicate file - " + os.path.join(dirpath, name) + "|" + hash + "\n")
				else:
					knownHashes.append(hash)
					if args.verbose:
						args.logfile.write("New global hash found - " + os.path.join(dirpath, name) + "|" + hash  + "\n")

args.logfile.write("localDuplicate=" + str(localDuplicates) + " actionsPreformed=" + str(actionsPreformed) + " knownHashes=" + str(len(knownHashes)) + "\n")
