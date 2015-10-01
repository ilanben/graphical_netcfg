import tkinter as tk
# for 2.7 python Tkinter
from tkinter.ttk import *
from subprocess import call, Popen, PIPE, STDOUT


class App():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("devices networks")
        self.labels = []
        self.update_clock()
        self.root.mainloop()

    def update_clock(self):
        i = 0

        # This is the path of adt when intsalling android studio 1.2 on windows
        adb_absolute_path = "C:\\Users\\ilan.MAXTECH\\AppData\\Local\\Android\\Sdk\\Platform-tools\\"

        # destroy all old labels so that they can be garbage collected
        # Clear the labels from last clock cycle
        for label in self.labels:
            label.grid_remove()
            label.destroy()
        self.labels.clear();

        # Get the list of connected devices
        cmd = adb_absolute_path + "adb.exe devices"
        proc = Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT)
        device_list = proc.communicate()[0].decode().split("\r\n")
        # remove unnecessary text in devices call
        device_list.pop(0)
        device_list.remove("")
        device_list.remove("")

        # retrieve maximum Device row to adjust the window dynamically to max rows
        maxRowsColumn = 0
        # print netcfg for each device
        for device in device_list:

            # get the netcfg for specific device
            device_serial = device.split("\t")[0]
            cmd = adb_absolute_path + "adb.exe -s " + device_serial + " shell netcfg"
            proc = Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT)
            netcfg_output = proc.communicate()[0].decode()

            # add a new label to the screen
            lb = Label(self.root, text=device_serial + "\n" +"interface   status \t\t ip \t \t flag \t mac"+ "\n\n"+ netcfg_output)
            lb.grid(row=1, column=i)

            lbblank = Label(self.root, text="\t\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|")
            lbblank.grid(row=1, column=i + 1)
            i += 2

            self.labels.append(lb)
            self.labels.append(lbblank)

            # the // 50 is to get approximately the line avg length and not every char
            # +5 is the static additional lines
            var = netcfg_output.__len__() // 50 + 3
            if var > maxRowsColumn:
                maxRowsColumn = var

        self.root.geometry(str(device_list.__len__() * 450) + "x" + str(maxRowsColumn * 25))
        self.root.after(1000, self.update_clock)

app = App()
