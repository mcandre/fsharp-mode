#! /usr/bin/python

import re
import sys
import urllib
import time
import getopt
import subprocess
from pprint import pprint




text = """script /home/fsharp/test.fsx
type Hello(who) =
  member x.Say() =
    printfn "Hello %s!" who

let hi = Hello("world")
hi.S
<<EOF>>
"""

test = text + """completion 5 4
quit
"""

la = """
completion 5 1
completion 5 2
completion 5 3
completion 5 4
completion 5 5
tip 4 5
quit
"""

def main():
  try:
    opts, args = getopt.getopt(sys.argv[1:], "nva:w:")
  except getopt.GetoptError, err:
    # print help information and exit:
    print str(err) # will print something like "option -a not recognized"
    sys.exit(2)
  upload   = True
  verbose  = False
  wait     = 0
  attempts = 1
  for o, a in opts:
    if o == "-n":
      upload = False
    elif o == "-v":
      verbose = True
    elif o == "-a":
      attempts = int(a)
    elif o == "-w":
      wait = int(a)
    else:
      assert False, "unhandled option"


  child = subprocess.Popen(['mono', '../bin/fsautocomplete.exe'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)

  out, err = child.communicate(test)

  print "output:\n%s" % out

  sys.exit(0)

  child.stdin.write(text)

  child.stdout.flush()
  output = child.stdout.readline()

  print output

  child.stdin.write("completion 5 4\n")

  child.stdin.write("tip 4 5\n")

  child.stdout.flush()
  output = child.stdout.readline()
  output = child.stdout.readline()
  output = child.stdout.readline()
  output = child.stdout.readline()
  output = child.stdout.readline()
  print output

  child.terminate()

  sys.exit(0)


  child = pexpect.spawn(r"mono bin/fsintellisense.exe")
#  child.interact()
  child.send(text)
  
  # ^[[52;1R2;1R

  print "sent, waiting for ack"

  child.expect("DONE: Script loaded")
  
  print "received, asking for completion"

  child.sendline("completion 5 4")

  child.sendline("tip 4 5")

  while True:
    child.expect(".*")

    #print "Received:\n--\n%s--" % child.after

  

if __name__ == "__main__":
  main()
