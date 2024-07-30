import os
import numpy as np
from time import sleep

def capture_freq_sweep(out_directory, osc_inst, fgen_inst, start_freq, end_freq, npoints):
    """
    Executes a frequency sweep. Iteratively sets the function generator frequency and captures 
    data from the oscilloscope, and saves each set of data. 

    :param out_directory: str, directory to save the data 
    :param osc_inst: oscilloscope pyvisa resource 
    :param fgen_inst: function generator pyvisa resource
    :param start_freq: float, starting frequency for the sweep 
    :param end_freq: float, ending frequency for the sweep 
    :param npoints: int, number of points in the sweep
    """
    # initialize instruments
    osc.initialize(osc_inst)
    inst_log = osc.create_log('VARIABLE', 0, 1, 0, 1, 'AUTO') + '\n'
    fgen.initialize(fgen_inst)
    fgen.set_amplitude(fgen_inst, 1, 5)
    inst_log += fgen.create_log(1, 'SINE', 'VARIABLE', 5, 0) + '\n'
    # set up frequency sweep
    freqs = np.linspace(start_freq, end_freq, npoints)
    log = inst_log + "# -------------- Frequency sweep settings -------------- #\n" 
    log += f'start frequency: {start_freq} Hz\n' 
    log += f'end frequency: {end_freq} Hz\n' 
    log += f'number of points: {npoints}\n'
    # save log file
    log_path = out_directory + 'freqsweep.log' 
    if os.path.exists(log_path):
        raise FileExistsError(f'{log_path} already exists')
    with open(log_path, 'w') as f:
        f.write(log)
    # execute frequency sweep
    fgen.set_channel_state(fgen_inst, 1, 'ON')
    for index, freq in enumerate(freqs):
        set_freq(freq)
        tsample, time, voltage = osc.capture_data(osc_inst) 
        np.save(out_directory + f'freqsweep_{index:03d}.npy', [time, voltage])
    fgen.set_channel_state(fgen_inst, 1, 'OFF')

def set_freq(freq):
    """ 
    Sets the function generator to the given frequency and sets up the 
    oscilloscope x scale to roughly two periods per division 

    :param freq: float, frequency in Hz 
    """
    # set frequency of function generator
    fgen.set_frequency(fgen_inst, 1, freq)
    # set xscale of oscilloscope
    tperiod = 1 / freq 
    xscale = tperiod / 2
    osc.set_xscale(osc_inst, xscale)
    # sleep
    sleep(0.1)