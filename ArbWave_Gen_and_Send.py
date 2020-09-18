'''
Creates a sine wave and sends to the SDG1025 waveform generator over USB connection
'''
import pyvisa
import numpy as np
import matplotlib.pyplot as plt
import binascii

def create_wave_file(data):
    """create a file"""
    scaled_data = scale_data(data)
    out_string = ''
    with open("wave1.bin", "wb") as f:
        for a in scaled_data:
            b = hex(int(a))
            b = b[2:]
            len_b = len(b)
            if (0 == len_b):
                b = '0000'
            elif (1 == len_b):
                b = '000' + b
            elif (2 == len_b):
                b = '00' + b
            elif (3 == len_b):
                b = '0' + b
            b = b[2:4] + b[:2]  # change big-endian to little-endian
            out_string += b
            c = binascii.a2b_hex(b)
            f.write(c)
    return out_string

def send_wave_data(dev):
    """send wave1.bin to the device"""
    f = open("wave1.bin", "rb")  # wave1.bin is the waveform to be sent
    data = f.read()
    print("data: ", data[0:10])
    print('write bytes:', len(data))
    dev.write_binary_values('C1:WVDT M50,WVNM,wave1,TYPE,5,LENGTH,32KB,FREQ,0.1,AMPL,5.0,OFST,0.0,PHASE,0.0,WAVEDATA,', data, datatype='B', header_fmt='empty')  # SDG00100 series
    dev.write("C1:ARWV NAME,wave1")
    f.close()

def scale_data(data):
    '''scale and convert the data to unsigned 14-bit integer'''
    values = []
    for idx, val in enumerate(data):
        if val < 0:
            temp = np.trunc(16384 - abs(val) * 8192)
        else:
            temp = np.trunc(val * 8192)
        values.append(int(temp))
    return values

if __name__ == '__main__':
    # uncomment the following line to see the visa communication
    # pyvisa.log_to_screen()

    t = np.linspace(0, 10, num=2 ** 14)  # The SDG1025 requires that the waveform have 32KB (32768 bytes) in length
    w = np.sin(t / (10.0 / (2.0 * np.pi)))
    plt.plot(t, w)
    plt.title("sinewave")
    plt.xlabel('t (sec)')
    plt.show()

    rm = pyvisa.ResourceManager()
    inst = rm.open_resource('USB0::0xF4ED::0xEE3A::SDG10GA2162699::INSTR')
    inst.write_termination = ''
    wave_hex_string = create_wave_file(w)
    send_wave_data(inst)
    print(wave_hex_string[0:40]) # print first 40 characters of wave string

    inst.close()