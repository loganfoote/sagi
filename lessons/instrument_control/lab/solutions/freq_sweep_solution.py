import os
import numpy as np
from time import sleep
import siglent_sds1104xe_oscope_solution as osc 
import siglent_sdg2082x_fgen_solution as fgen

def capture_freq_sweep(out_directory, osc_inst, fgen_inst, start_freq, end_freq, npoints, yscale):
    """
    Executes a frequency sweep. Iteratively sets the function generator frequency and captures 
    data from the oscilloscope, and saves each set of data. 

    :param out_directory: str, directory to save the data 
    :param osc_inst: oscilloscope pyvisa resource 
    :param fgen_inst: function generator pyvisa resource
    :param start_freq: float, starting frequency for the sweep 
    :param end_freq: float, ending frequency for the sweep 
    :param npoints: int, number of points in the sweep
    :param yscale: float, oscilloscope voltage per division in V / div
    """
    # initialize instruments
    osc.initialize(osc_inst)
    xscale = 'VARIABLE' 
    xoffset, yoffset = 0, 0
    amplification = 1 
    trigger_mode = 'AUTO'
    osc.set_yscale(osc_inst, yscale)
    inst_log = osc.create_log(xscale, xoffset, yscale, yoffset, amplification, trigger_mode) + '\n'
    
    fgen.initialize(fgen_inst)
    fgen.set_amplitude(fgen_inst, 1, 5)
    channel = 1 
    wave_type = 'SINE'
    freq = 'VARIABLE' 
    amp = 5 
    offset = 0
    inst_log += fgen.create_log(channel, wave_type, freq, amp, offset) + '\n'
    # set up frequency sweep    
    frequencies = np.geomspace(start_freq, end_freq, npoints)
    log = inst_log + "# --------- Geometric frequency sweep settings --------- #\n" 
    log += f'start frequency: {start_freq} Hz\n' 
    log += f'end frequency: {end_freq} Hz\n' 
    log += f'number of points: {npoints}\n'
    # save log file
    out_directory = '/home/vn-neu-daq01/SAGI2024/data/group0/sweep_00/'
    out_directory = r'C:\Users\logan\Downloads\temp/'
    log_path = out_directory + 'freqsweep.log' 
    if os.path.exists(log_path):
        raise FileExistsError(f'{log_path} already exists')
    with open(log_path, 'w') as f:
        f.write(log)
    # execute frequency sweep
    sleep(0.5)
    fgen.set_channel_state(fgen_inst, 1, 'ON')
    sleep(5)
    for index, frequency in enumerate(frequencies):
        set_freq(fgen_inst, osc_inst, frequency)
        tsample, time, voltage = osc.capture_data(osc_inst) 
        np.save(out_directory + f'freqsweep_{index:03d}.npy', [time, voltage])
    fgen.set_channel_state(fgen_inst, 1, 'OFF')

def set_freq(fgen_inst, osc_inst, freq):
    """ 
    Sets the function generator to the given frequency and sets up the 
    oscilloscope x scale to roughly ten periods per division 

    :param freq: float, frequency in Hz 
    """
    # set frequency of function generator
    fgen.set_frequency(fgen_inst, 1, freq)
    # set xscale of oscilloscope
    tperiod = 1 / freq 
    xscale = tperiod * 10
    osc.set_xscale(osc_inst, xscale)
    # sleep
    sleep(0.1)