import fcntl
import os
import time

filename = "./test.txt"
filename = "/tmp/test.txt"

with open(filename, 'r') as handle:
  print("waiting for lock")
  fcntl.flock(handle, fcntl.LOCK_SH)

  print("locked")
  print("read: ", handle.read())

  time.sleep(5)

  fcntl.flock(handle, fcntl.LOCK_UN)
  handle.close()
  print("unlocked")
#end_with

