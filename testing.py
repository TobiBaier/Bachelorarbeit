import numpy as np
import re
import time
import serial
import os


def init_serial(prt):
    ret = serial.Serial()
    ret.port = prt
    ret.baudrate = 9600
    ret.open()
    if ret.is_open:
        print(f"Opened a serial port at {ret}")

    return ret


class Grid_Spec:

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
            # self.ser_spec = init_serial(win_spec)

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
                    time.sleep(self.photo_update_time)
                    data = self.ser_photo.readline()
                    break
                else:
                    data = None

            # if waiting time is too big (~10s), error is raised
            if data is None:
                raise ValueError("There was no feedback from the Photodetector!")

            data = data.decode()

            count = float(re.findall(r"[\d]*[.][\d]", data)[0])


            #count = int(data)
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
                    if temp.startswith("R: "):
                        count = float(re.findall(r"[\d]*[.][\d]", temp)[0])
                        data = np.append(data, count)
                    else:
                        raise ValueError(f"There has been an error reading Photo data! data: {data}")

            return np.sum(data)