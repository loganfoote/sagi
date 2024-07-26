import time
import pyvisa


channels = {1: 'M', 2: 'F'}


def connect(port=0):
    """
    Connects to the function generator through the serial interface.
    Confirms the connection by printing the instrument ID.

    :param port: Usb port number.

    :return: Pyvisa resource.
    """
    resource_name = f'ASRL/dev/ttyUSB{port}::INSTR'
    rm = pyvisa.ResourceManager()
    termination = '\n'
    inst = rm.open_resource(resource_name, baud_rate=115200, write_termination=termination)

    return inst

def set_wave_type(inst, channel, wave_type):
    """ Set the waveform type using the Basic Wave command.

    :param inst: serial resource object corresponding to the waveform generator
    :param wave_type: int, 1 for sine, 2 for square, etc
    """
    wave_map = {
        'SINE': 0,
        'Square': 1,
        'Rectangle': 2,
        'Trapezoid': 3,
        'Impulse': 31,
    }
    wave_type = wave_map[wave_type]
    command = f'W{channels[channel]}W{wave_type}'
    inst.write(command)

def set_frequency(inst, channel, frequency):
    """ Set the waveform fundamental frequency.
    
    :param inst: serial resource object corresponding to the waveform generator.
    :param channel: (int) Channel on which to change the waveform type.
    :param frequency: COMPLETE THIS
    """
    command = f'W{channels[channel]}F{int(round(frequency * 1e6, 0)):010d}' 
    inst.write(command)

def set_amplitude(inst, channel, amplitude):
    """ Set the waveform amplitude in peak-to-peak units.

    :param inst: serial resource object corresponding to the waveform generator.
    :param channel: (int) Channel on which to change the waveform type.
    :param amp: COMPLETE THIS
    """
    command = f'W{channels[channel]}A{round(amplitude, 4)}'
    inst.write(command)

def set_offset(inst, channel, offset):
    """ Set the waveform DC offset.

    :param inst: serial resource object corresponding to the waveform generator.
    :param channel: (int) Channel on which to change the waveform type.
    :param offset: COMPLETE THIS
    """
    command = f'W{channels[channel]}O{round(offset, 4)}'
    inst.write(command)

def set_channel_state(inst, channel, state):
    """ Set the state of a waveform generator channel to ON or OFF
    """
    state_map = {
        'ON': 1,
        'OFF': 0,
    }
    state = state_map[state]
    command = f'W{channels[channel]}N{state}'
    inst.write(command)

def initialize(inst):
    """ Initialize both channels of the waveform generator to a sine wave w/ 1 Hz frequency,
    1 Vpp amplitude, and offset 0V. Turn off both channels.

    :param inst: Pyvisa resource.
    """
    for channel in [1, 2]:
        set_channel_state(inst, channel, 'OFF')
        sleep(0.2)
        set_wave_type(inst, channel, 'SINE')
        sleep(0.2)
        set_frequency(inst, channel, 1)
        sleep(0.2)
        set_amplitude(inst, channel, 1)
        sleep(0.2)
        set_offset(inst, channel, 1)
        sleep(0.2)

def create_log(channel, wave_type, freq, amp, offset):
    """ Create a string to log basic parameters of the FY6900 waveform generator output.

    :param channel: Which channel the parameters correspond to.
    :param wave_type: Type of waveform.
    :param freq: Frequency in Hz.
    :param amp: Amplitude in volts peak-to-peak.
    :param offset: Offset voltage.
    """
    log = "# -------------- FY6900 Waveform Settings -------------- #\n"
    log += f"Channel: {channel}\n"
    log += f"Waveform Type: {wave_type}\n"
    log += f"Frequency: {freq} Hz\n"
    log += f"Amplitude: {amp} Volts peak-to-peak\n"
    log += f"Offset: {offset} Volts\n"
    return log
