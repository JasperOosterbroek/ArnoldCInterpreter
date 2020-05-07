import sys
import interpeter
import argparse
import unittests

argParser = argparse.ArgumentParser(description="ARNOLDC PARSER")
argParser.add_argument("-f", "--file", required=True, type=str, help="FilePath to interperatable file")
argParser.add_argument("-d", "--debug", action="store_true", help="Outputs programstate per step to console")
argParser.add_argument("-t", "--tests", action="store_true", help="Runs tests before parsing file")
args = argParser.parse_args()

if args.tests:
    unittests.unittest.main()

if args.debug:
    interpeter.executeStep = interpeter.executeDebugStep(interpeter.executeStep)

lineList = list()
with open(args.file) as f:
  for line in f:
    lineList.append(line)
interpeter.run(lineList)


# een method moet assigned aan een variable worden, het moet argumenten mee krijgen en het moet een return waarden hebben
