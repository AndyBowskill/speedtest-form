#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import socket

from tkinter import *
from tkinter import font


class SpeedTestForm:
    def __init__(self, master):
        self.master = master

        master.title('Speed Test')
        master.geometry('350x250')
        master.attributes('-fullscreen', True)
        master.config(bg='black')

        form_font = font.Font(family='Arial', size=24, weight=font.NORMAL)
        orange_code = '#dd5202'

        self.ip_text = StringVar()
        self.ip_text.set('')

        self.network_text = StringVar()
        self.network_text.set('')

        self.ip_label = Label(master, font=form_font, textvariable=self.ip_text)
        self.ip_label.config(fg=orange_code, bg='black')
        self.ip_label.pack(padx=0, pady=10, fill=X)

        self.network_label = Label(master, font=form_font, textvariable=self.network_text)
        self.network_label.config(fg=orange_code, bg='black', height=4)
        self.network_label.pack(padx=0, pady=6, fill=X)

        self.check_button = Button(master, text='Check Network', font=form_font, command=lambda: self.check_network())
        self.check_button.config(fg=orange_code, bg='black')
        self.check_button.pack(padx=0, pady=10, fill=BOTH)

    def check_network(self):
        self.network_text.set('Checking...')
        self.check_button.config(state=DISABLED)

        self.ip_text.set(self.read_ip())

        def run_speedtest():
            response = subprocess.Popen('/usr/local/bin/speedtest-cli --simple', shell=True, stdout=subprocess.PIPE).stdout.read()
            response_string = response.decode('utf-8')
            if not response_string:
                response_string = 'No network found.'

            self.network_text.set(response_string)
            self.check_button.config(state=NORMAL)

        self.master.after(500, run_speedtest)

    @staticmethod
    def read_ip():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = 'IP: ' + s.getsockname()[0]
        except socket.error:
            ip = 'No IP found.'
        finally:
            s.close()
        return ip


def main():
    root = Tk()
    SpeedTestForm(root)
    root.mainloop()


if __name__ == '__main__':
    main()