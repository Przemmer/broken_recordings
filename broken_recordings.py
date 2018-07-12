#!/usr/bin/python

import wave
import matplotlib.pyplot as plt
import numpy as np
import sys
import config


def read_wave_file(file_name):
    wave_read = wave.open(file_name)
    str_data = wave_read.readframes(wave_read.getnframes())
    wave_read.close()
    return np.frombuffer(str_data, dtype=np.short)


####################
#                  #
#  First method    #
#  (gradient/log)  #
#                  #
####################


def mean_window(data, window = 8):
    new_size = int(data.size/window)
    result = np.zeros(new_size)
    for i in range (0, new_size):
        wsum = 0.0
        for j in range(0, window):
            wsum += abs(data[i*window+j])
        result[i] = wsum / window
        result[i] += 1.0 # for later log calculation
    return result


def detect_broken_recording(file_name, min_treshold = -2.0, max_treshold = 2.0, window = 8):
    wave_full = read_wave_file(file_name)
    wave_mean = mean_window(wave_full)
    wave_log_gradient = np.gradient(np.log(wave_mean))
    min_gradient, max_gradient = np.min(wave_log_gradient), np.max(wave_log_gradient)
    if min_gradient < min_treshold and max_gradient > max_treshold:
        drop_begins = np.argmin(wave_log_gradient) * window
        drop_ends = np.argmax(wave_log_gradient) * window
        print (file_name + ": invalid (fr. " + str(drop_begins) + "-" + str(drop_ends) + ")")
    else:
        print (file_name + ": valid")


####################
#                  #
#  Second method   #
#  (sudden drop)   #
#                  #
####################


def calculate_mean(wave_data, from_frame, to_frame):
    fb_count = 0.0
    fb_sum = 0.0
    for i in range(from_frame, to_frame):
        fb_sum += abs(wave_data[i])
        fb_count += 1
    if fb_count > 0:
        return fb_sum / fb_count
    else:
        return 0


def drop_begins_suddenly(wave_data, begin_frame_index, num_frames_before=32, 
                         treshold_before=256):
    fb_mean = calculate_mean(wave_data, max(begin_frame_index-num_frames_before, 0), 
                             begin_frame_index)
    if fb_mean > treshold_before:
        return True
    else:
        return False


def drop_ends_suddenly(wave_data, end_frame_index, num_frames_after=32, treshold_after=256):
    fb_mean = calculate_mean(wave_data, end_frame_index, 
                             min(end_frame_index+num_frames_after, wave_data.size))
    if fb_mean > treshold_after:
        return True
    else:
        return False


def detect_signal_drop(file_name, ls_treshold=2, ls_min_length=64, 
                       num_frames_before=32, num_frames_after=32, 
                       treshold_before=256, treshold_after=256):

    wave_data = read_wave_file(file_name)
    
    fn = 0 # frame number
    low_signal = False
    
    ls_start = 0
    ls_length = 0
    
    while fn < wave_data.size:
        if wave_data[fn] < ls_treshold:
            if low_signal:
                ls_length += 1
            else:
                ls_start = fn
                ls_length = 1
                low_signal = True
        elif low_signal: # end of 'low signal'
                _dbs = drop_begins_suddenly(wave_data, ls_start, num_frames_before=num_frames_before, 
                                            treshold_before=treshold_before)
                _des = drop_ends_suddenly(wave_data, fn, num_frames_after=num_frames_after, 
                                          treshold_after=treshold_after)
                if (ls_length > ls_min_length) and _dbs and _des:
                    print (file_name + ": invalid (fr. " + str(ls_start) + "-" + str(fn) + ")")
                    return
                low_signal = False
        fn += 1
        
    print (file_name + ": valid")


def print_usage():
    print()
    print("Usage:")
    print("  python broken_recordings.py  <file_name>  method_1 | method_2")
    print()


def main():
    file_name = sys.argv[1]
    method = sys.argv[2]

    if method == 'method_1': 
        detect_broken_recording(file_name, min_treshold=config.min_treshold, 
                                max_treshold=config.max_treshold, window=config.window)
        return

    if method == 'method_2':
        detect_signal_drop(file_name, ls_treshold=config.ls_treshold, ls_min_length=config.ls_min_length, 
                           num_frames_before=config.num_frames_before, num_frames_after=config.num_frames_after, 
                           treshold_before=config.treshold_before, treshold_after=config.treshold_before)
        return
    print_usage()
    

if __name__ == '__main__': 
    if len(sys.argv) < 3:
        print_usage()
    else:
        main()
