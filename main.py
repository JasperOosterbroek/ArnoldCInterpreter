import interpeter
import argparse
import unittest
import unittests

argParser = argparse.ArgumentParser(description="ARNOLDC interpreter")
argParser.add_argument("-f", "--file", required=True, type=str, help="FilePath to interperatable file")
argParser.add_argument("-d", "--debug", action="store_true", default=False, help="Outputs programstate per step to console")
argParser.add_argument("-t", "--test", action="store_true", default=False, help="Runs tests before parsing file")
options = argParser.parse_args()

if options.test:
    suite = unittest.TestLoader().loadTestsFromModule(unittests)
    unittest.TextTestRunner(verbosity=2).run(suite)

if options.debug:
    interpeter.executeStep = interpeter.executeDebugStep(interpeter.executeStep)

lineList = list()
with open(options.file) as f:
  for line in f:
    lineList.append(line)
interpeter.run(lineList)
