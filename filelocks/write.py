import fcntl
import os
import time

filename = "./test.txt"
filename = "/tmp/test.txt"

if not os.path.exists(filename):
  os.mknod(filename)

with open(filename, 'r+') as handle:
  print("waiting for lock")
  fcntl.flock(handle, fcntl.LOCK_EX)

  print("locked")
  time.sleep(5)

  handle.truncate()
  handle.write("python\n")

  fcntl.flock(handle, fcntl.LOCK_UN)
  handle.close();
  print("unlocked")
#end_with

