#Will allow user to map web application that is downloaded and extracted on local machine. Can see what files are reachable on the remote target
#only works on python 2.7.x

import Queue
import threading
import os
import urllib2

threads = 10

target = "http://www.blackhatpython.com"
directory = "/Users/justin/Downloads/joomla-3.1.1.1"
filters = [".jpg",".gif",".png",".css"]

os.chdir(directory)

web_paths = Queue.Queue()

for r,d,f in os.walk("."):
	for files in f: remote_path = "%s/%s" % (r,files)
	if remote_path.startswith("."):
		remote_path = remote_path[1:]
	if os.path.splittext(files)[1] not in filters:
		web_paths.put(remote_path)

def test_remote():
	while not web_paths.empty():
		path = web_paths.get()
		url = "%s%s" % (target,path)

		request = urllib2.Request(url)

		try:
			response = urllib2.urlopen(request)
			content = response.read()

			print "[%d] => %s" % (response.code,path)
			response.close()
		except urllib2.HTTPError as error:
			pass

for i in range(threads):
	print "Spawning thread: %d" % it = threading.Thread(target=test_remote)
	t.start()