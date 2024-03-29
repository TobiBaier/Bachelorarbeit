import matplotlib.pyplot as plt
import numpy as np
import re
import time
import serial
import os
import csv
import json
from pprint import pprint


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
        self.get_paths()
        # ------------------------------------------------------------------------

        # measurement parameters
        self.start_wl = 250
        self.stop_wl = 750
        self.delta_wl = 5

    '''
    FUNCTION ALIASES (for easier calling)
    '''
    def goto(self, wl):
        self.goto_wavelength(wl)

    def get(self):
        self.get_wavelength()

    def loop(self, single_value=True):
        self.cont_photo(single_value=single_value)

    def measure(self, lu=True, sv=True):
        self.measure_spectrum(live_update=lu, sv=sv)

    '''
    DEPENDING ON YOUR PC, YOU MAY HAVE TO CHANGE THE KWARGS IN THE FUNCTION BELOW!!!
    '''
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

    """
    Spectrometer Functions
    """
    def get_wavelength(self):
        self.ser_spec.flushInput()
        self.ser_spec.write("?NM\r".encode())
        ret = self.ser_spec.readline()

        print(ret.decode())

    def goto_wavelength(self, wl):
        """
        Drives the grid spectrometer to the desired wavelength

        :param wl: wavelength to go to (type=float, two comma spaces)
        :return: the wavelength that was reached
        """
        # reformat wavelength
        wl_str = f"{wl:.2f}"
        self.ser_spec.flushInput()

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

    '''
    Photodetector functions
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
            try:
                data = self.ser_photo.readline()
                count = float(data.decode())
                return count
            except ValueError:
                print("Error -> Measuring again!")
                return self.read_photo(single_value=single_value)

        # cumulative measurement
        else:
            try:
                data = np.array([])
                time.sleep(self.wait_time)
                while self.ser_photo.inWaiting() != 0:
                    # if len(data) >= self.wait_time:
                    #    break
                    # else:
                    temp = self.ser_photo.readline().decode()
                    data = np.append(data, float(temp))
                print(data)
                return np.sum(data)
            except ValueError:
                print("Error -> Measuring again!")
                return self.read_photo(single_value=single_value)

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

        # plt.savefig(self.file_name + ".png", dpi=400)
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
        fn = "new_spectrum"

        print(f"The measured spectrum will be saved as: {fn}.csv")
        inp = input("Change name? (y/n):")

        if inp == "y":
            self.file_name = input("Please enter a new name (can include directory, no file ending): ")
        elif inp == "n":
            self.file_name = fn
        else:
            self.file_name = fn

        with open(self.save_path + self.file_name + ".csv", "w", newline="") as savefile:
            writer = csv.writer(savefile, delimiter=";")
            writer.writerows(self.current_spectrum)

    def get_paths(self):
        with open("data_paths.json", "r") as of:
            data = json.load(of)

        print("")
        print("Aktuell ist folgender Pfad zum Speichern ausgewählt:")
        print(f"{data['latest_path']}: {data[data['latest_path']]}")

        self.save_path = data[data['latest_path']]
        data.pop("latest_path")

        print("")
        print("Im System sind die folgenden weiteren Pfade hinterlegt ")
        pprint(data)
        p = input("Geben Sie den Namen des Pfads ein, um den aktuellen zu überschreiben (sonst einfach Enter):")

        if p in data:
            self.save_path = data[p]

        print("")
        print(f"The save path has been updated to: {self.save_path}")

    def add_path(self):
        with open("data_paths.json", "r") as of:
            data = json.load(of)

        print(f"Adding '{self.save_path}' to library!")
        key = input("Please enter a key: ")

        data[key] = self.save_path

        j_data = json.dumps(data, indent=4, sort_keys=True, separators=(",", ": "), ensure_ascii=False)
        with open("data_paths.json", "w") as of:
            of.write(j_data)

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
    def measure_spectrum(self, live_update=True, sv=True):
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

        if self.wait_time != 1:
            sv = False

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

        print("Process finished without errors!")

        self.save_values()
        self.draw_spectrum()

    def terminate_serials(self):
        self.ser_photo.close()
        self.ser_spec.close()


def name_call():
    return GridSpec()


if __name__ == "__main__":
    name_call()


