import matplotlib.pyplot as plt
import numpy as np
import re
import time
import serial
import os
import csv
from datetime import datetime


def init_serial(prt):
    ret = serial.Serial()
    ret.port = prt
    ret.baudrate = 9600
    ret.open()
    if ret.is_open:
        print(f"Opened a serial port at {ret}")

    return ret


class GridSpec:

    def __init__(self, step_time=1, wait_time=1, nAvg=4):
        self.step_time = step_time  # waiting for servo/grid
        self.wait_time = wait_time  # waiting during measurement (cumulative values) // maybe rename ??
        self.nAvg = nAvg
        self.photo_update_time = 0.1

        # vars for serial ports
        self.ser_photo = None
        self.ser_spec = None
        self.init_serials()

        # list with saved spectra (in current instance)
        self.spectra = []
        self.current_spectrum = None
        self.file_name = "spectrum"

        # measurement parameters
        self.start_wl = 400
        self.stop_wl = 420
        self.delta_wl = 5

    '''
    DEPENDING ON YOUR PC, YOU MAY HAVE TO CHANGE THE KWARGS IN THE FUNCTION BELOW!!!
    '''

    def init_serials(self, win_photo="COM4", win_spec="COM3", lnx_photo="/dev/ttyACMO", lnx_spec="/dev/ttyUSB0"):
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

    def get_wavelength(self):
        self.ser_spec.write("?NM\r".encode())
        ret = self.ser_spec.readline()

        print(ret.decode())

    '''
    communication functions (with spectrometer and photodetector
    '''

    def cont_photo(self, single_value=True):
        while True:
            print(self.read_photo(single_value=single_value))

    def read_photo(self, single_value=True):
        """
        soll tun:
        check, ob daten im Buffer sind
        wenn ja, Daten aus Zeile auslesen und zurückgeben
        wenn nein, gebe False zurück
        :return:
        """
        # clear data from photo serial port (to get most new data)
        self.ser_photo.flushInput()
        data = None

        # collect only one value (meaning as fast as possible)
        # wait until new data has arrived
        if single_value:
            for i in range(100):
                time.sleep(self.photo_update_time)
                if self.ser_photo.inWaiting():
                    # save incoming data
                    data = self.ser_photo.readline()
                    break
                else:
                    data = None

            # if waiting time is too big (~10s), error is raised
            if data is None:
                raise ValueError("There was no feedback from the Photodetector!")

            count = float(re.findall(r"[\d]*[.][\d]", data.decode())[0])

            return count

        # cumulative measurement
        else:
            data = np.array([])
            time.sleep(self.wait_time)
            while True:
                if len(data) > self.wait_time:
                    break
                else:
                    temp = self.ser_photo.readline().decode()
                    count = float(re.findall(r"[\d]*[.][\d]", temp)[0])
                    data = np.append(data, count)

            return np.sum(data)

    def goto_wavelength(self, wl):
        """
        Drives the grid spectrometer to the desired wavelength

        :param wl: wavelength to go to (type=float, two comma spaces)
        :return: the wavelength that was reached
        """
        # reformat wavelength
        wl_str = f"{wl:.2f}"

        # send wavelength to spectrometer
        comm = wl_str + " <GOTO>" + "\r"
        self.ser_spec.write(comm.encode())

        # get actual wavelength from spectrometer
        ret = self.ser_spec.readline().decode()
        self.ser_spec.write("?NM\r".encode())

        # reformat return string
        curr_wl = float(re.findall(r"[\d]*[.][\d]+", ret)[0])

        # read out spectrometer again (value might stay in cache?)
        self.ser_spec.readline()

        return curr_wl

    """
    functions to save and draw spectrum
    """

    def draw_spectrum(self, load_save=False):
        if not load_save:
            draw_arr = np.swapaxes(self.current_spectrum, 0, 1)
        else:
            draw_arr = self.load_values()
            draw_arr = np.swapaxes(draw_arr, 0, 1)
            draw_arr = draw_arr.astype(float)

        wl = draw_arr[0]
        counts = draw_arr[1]
        
        fig = plt.figure()
        ax = fig.add_subplot(111)

        ax.plot(wl, counts, "-+", c="blue", mec="black", ms=6)
        ax.set_xlabel(r"$\lambda$/nm")
        ax.set_ylabel("counts")
        ax.set_title(self.file_name)
        ax.grid()

        plt.savefig(self.file_name + ".png", dpi=400)
        plt.show()

    def load_values(self):
        self.file_name = input("Please enter a filename (.csv will be added): ")
        draw_arr = []
        with open(self.file_name + ".csv", "r") as data:
            reader = csv.reader(data, delimiter=";")
            for i in reader:
                draw_arr.append(i)

        return np.array(draw_arr)

    def save_values(self):
        dt = datetime.fromtimestamp(time.time())
        fn = self.file_name + "on" + dt.strftime("%m_%d_%Yat%H_%M")

        print(f"The measured spectrum will be saved as: {fn}")
        inp = input("Change name? (y/n):")

        if inp == "y":
            self.file_name = input("Please enter a new name (can include directory, no file ending): ")
        elif inp == "n":
            pass

        with open(self.file_name + ".csv", "w", newline="") as savefile:
            writer = csv.writer(savefile, delimiter=";")
            writer.writerows(self.current_spectrum)

    """
    utility functions for system dialogs
    """

    def current_params(self):
        print("----------")
        print("These are the parameters currently saved in the system:")
        print(f" - measurement range: {self.start_wl}nm - {self.stop_wl}nm")
        print(f" - distance between to wavelengths: {self.delta_wl}nm")
        # print(f" - grid adjustment time: {self.step_time}s")
        print(f" - time to let counts accumulate: {self.wait_time}s")
        print(f" - # of measurements taken per wl: {self.nAvg}")
        print("----------")

    def param_dialog(self, nested=False):
        if not nested:
            self.current_params()
            inp = input("Would you like to change any of these parameters? (y/n):")
        else:
            inp = "y"

        if inp == "y":
            print("")
            print("Enter a new value or press 'Enter' to skip!")
            inp2 = input("starting wavelength (nm): ")
            if inp2 != "":
                self.start_wl = float(inp2)

            inp2 = input("stopping wavelength (nm): ")
            if inp2 != "":
                self.stop_wl = float(inp2)

            inp2 = input("distance between wavelengths (nm): ")
            if inp2 != "":
                self.delta_wl = float(inp2)

            # inp2 = input("grid adjustment time (s): ")
            # if inp2 != "":
            #     self.step_time = float(inp2)

            inp2 = input("accumulation time (s): ")
            if inp2 != "":
                self.wait_time = float(inp2)

            inp2 = input("number of measurements per position (#): ")
            if inp2 != "":
                self.nAvg = int(inp2)

            print("")
            print("The parameters in the system have been updated!")
            self.current_params()
            inp = input("Continue with these parameters? (y/n):")
            if inp == "y":
                return
            else:
                self.param_dialog(nested=True)

        elif inp == "n":
            return

    """
    main measurement control function
    """

    def measure_spectrum(self, live_update=False, sv=True):
        """
        Asks user for measurement parameters and then starts program
        :return:
        """
        # start system dialog to confirm/change parameters
        self.param_dialog()

        # create wavelength list
        wl = np.arange(self.start_wl, self.stop_wl + self.delta_wl, self.delta_wl)

        # round list values to 2 decimal places
        wl = np.round(wl, 2)

        # create return array
        self.current_spectrum = np.zeros((len(wl), 2))

        # make measurement
        for i, curr_wl in enumerate(wl):
            actual_wl = self.goto_wavelength(curr_wl)
            current_count = 0
            for j in range(self.nAvg):
                current_count += self.read_photo(single_value=sv)
            mean_count = current_count / self.nAvg

            if live_update:
                print(f"Measured {mean_count} at {actual_wl}nm")

            self.current_spectrum[i][0] = actual_wl
            self.current_spectrum[i][1] = mean_count

        self.save_values()
        self.draw_spectrum()

    def terminate_serials(self):
        self.ser_photo.close()
        self.ser_spec.close()


def name_call():
    return GridSpec()


if __name__ == "__main__":
    name_call()
