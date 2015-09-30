import tkinter as tk
# for 2.7 python Tkinter
from tkinter.ttk import *
from subprocess import call,Popen,PIPE, STDOUT

class App():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("devices networks")
        self.labels = []
        self.update_clock()
        self.root.mainloop()

    def update_clock(self):
        i=0

        #This is the path of adt when intsalling android studio 1.2 on windows
        adb_absolute_path = "C:\\Users\\ilan.MAXTECH\\AppData\\Local\\Android\\Sdk\\Platform-tools\\"

        # Get the list of connected devices
        cmd = adb_absolute_path+"adb.exe devices"
        proc = Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT)
        device_list = proc.communicate()[0].decode().split("\r\n")
        # remove unnecessary text in devices call
        device_list.pop(0)
        device_list.remove("")
        device_list.remove("")


#### not working.... #######
#        #erase the old labels ( in case a device has been disconected
#        for line in range(10):
#            lb = Label(self.root, text="")
#            lb.grid(row=1, column=line)
###########################
        #destroy all old labels so that they can be garbage collected
        for label in self.labels:
            label.grid_remove()
            label.destroy()
        self.labels.clear();

        #print netcfg for each device
        for device in device_list:

            #get the netcfg for specific device
            device_serial = device.split("\t")[0]
            cmd = adb_absolute_path + "adb.exe -s " + device_serial + " shell netcfg"
            proc = Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT)
            netcfg_output = proc.communicate()[0].decode()

            #add a new label to the screen
            lb = Label(self.root, text=device_serial+"\n"+netcfg_output)
            lb.grid(row=1, column=i)
            lbblank = Label(self.root,text="\t\t")
            lbblank.grid(row=1, column=i+1)
            i += 2

            self.labels.append(lb)
            self.labels.append(lbblank)

        self.root.geometry(str(device_list.__len__()*450)+"x700")
        self.root.after(1000, self.update_clock)

app=App()