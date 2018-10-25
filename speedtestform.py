#!/usr/bin/env python3

from tkinter import *
from tkinter import font
import subprocess
import socket

class SpeedTestForm:
    def __init__(self, master):
        self.master = master

        master.title('Speed Test')
        master.geometry('350x250')
        master.attributes('-fullscreen', True)
        master.config(bg='black')

        form_font = font.Font(family='Arial', size=24, weight=font.NORMAL)
        orange_code = '#dd5202'

        self.IP_text = StringVar()
        self.IP_text.set('')

        self.network_text = StringVar()
        self.network_text.set('')

        self.IP_label = Label(master, font=form_font, textvariable=self.IP_text)
        self.IP_label.config(fg=orange_code, bg='black')
        self.IP_label.pack(padx=0, pady=10, fill=X)

        self.network_label = Label(master, font=form_font, textvariable=self.network_text)
        self.network_label.config(fg=orange_code, bg='black', height=4)
        self.network_label.pack(padx=0, pady=6, fill=X)

        self.check_button = Button(master, text='Check Network', font=form_font, command=lambda: self.run_speedtest_process())
        self.check_button.config(fg=orange_code, bg='black')
        self.check_button.pack(padx=0, pady=10, fill=BOTH)

    def run_speedtest_process(self):
        self.network_text.set('Checking...')
        self.check_button.config(state=DISABLED)

        self.IP_text.set(self.read_IP())

        def run_subprocess():
            response = subprocess.Popen('/usr/local/bin/speedtest-cli --simple', shell=True, stdout=subprocess.PIPE).stdout.read()
            response_string = response.decode('utf-8')
            if not response_string:
                response_string = 'No network found.'

            self.network_text.set(response_string)
            self.check_button.config(state=NORMAL)

        self.master.after(500, run_subprocess)

    def read_IP(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            IP = 'IP: ' + s.getsockname()[0]
        except socket.error:
            IP = 'No IP found.'
        finally:
            s.close()
        return IP

root = Tk()
speed_test_form = SpeedTestForm(root)
root.mainloop()