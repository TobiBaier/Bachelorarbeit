import matplotlib.pyplot as plt
import numpy as np
import re, time, serial, os, csv, json
from pprint import pprint

import matplotlib

matplotlib.use("TkAgg")


def init_serial(prt):
    ret = serial.Serial()
    ret.port = prt
    ret.baudrate = 9600
    ret.open()
    if ret.is_open:
        print(f"Opened a serial port at {ret}")

    return ret


class GridSpec:

    def __init__(self, step_time=0.25, wait_time=1, nAvg=4):
        self.step_time = step_time  # waiting for servo/grid
        self.wait_time = wait_time  # waiting during measurement (cumulative values) // maybe rename ??
        self.nAvg = nAvg

        # vars for serial ports
        self.ser_photo = None
        self.ser_spec = None
        self.init_serials()

        # list with saved spectra (in current instance)
        self.spectra = []
        self.current_spectrum = None
        self.file_name = "new_spectrum"

        # ------------------------------------------------------------------------
        # HIER DEN Standard-DATEIPFAD ZUM SPEICHERN ANPASSEN!
        self.save_path = "/run/user/1000/gvfs/sftp:host=sftp.zih.tu-dresden.de/glw/aspabl/Studenten/Baier/Messungen/sortme/"
        # self.get_paths()
        # ------------------------------------------------------------------------

        # measurement parameters
        self.start_wl = 250
        self.stop_wl = 750
        self.delta_wl = 5

    def init_serials(self, win_photo="COM4", win_spec="COM3", lnx_photo="/dev/ttyACM0", lnx_spec="/dev/ttyUSB0"):
        # Windows System
        if os.name == "nt":
            self.ser_photo = init_serial(win_photo)
            self.ser_spec = init_serial(win_spec)

        # Linux System
        if os.name == "posix":
            self.ser_photo = init_serial(lnx_photo)
            self.ser_spec = init_serial(lnx_spec)

        # wait short time to make sure devices are ready
        time.sleep(2)

    def terminate_serials(self):
        self.ser_photo.close()
        self.ser_spec.close()

    def loop(self):
        plt.ion()

        x = np.linspace(1, 10, 20)
        y = []

        fig = plt.figure()
        ax = fig.add_subplot(111)



        graph = ax.plot([1,2],[1,2], "o-")[0]        # plt.show()

        ax.set_xbound([0, 10])
        ax.set_ybound([-0.4, 2.5])

        for i, nr in enumerate(x):
            self.ser_photo.flushInput()
            data = self.ser_photo.readline()
            count = float(data.decode())
            y.append(count)

            print(y)
            print(x[:i+1])
            print("")

            graph.set_xdata(x[:i+1])
            graph.set_ydata(y)
            plt.draw()




            plt.pause(0.5)

        plt.show()


g = GridSpec()

g.loop()

