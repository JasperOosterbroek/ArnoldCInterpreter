import sys
import interpeter

debug = True
file = "testcode.arnoldc" # default
if len(sys.argv) > 1:
    file = sys.argv[1]
    if len(sys.argv) > 2:
        debug = sys.argv[2]
if debug:
    executeStep = interpeter.executeDebugStep(interpeter.executeStep)

lineList = list()
with open(file) as f:
  for line in f:
    lineList.append(line)
interpeter.run(lineList)
