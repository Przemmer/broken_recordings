#!/usr/bin/python

####################
#                  #
#  First method    #
#  (gradient/log)  #
#                  #
####################

# tresholds for value of gradient of log of filtered ('mean window') signal
min_treshold = -2.0
max_treshold =  2.0

# width (number of frames/samples) of window to calculate mean of absolute values
window = 8



####################
#                  #
#  Second method   #
#  (sudden drop)   #
#                  #
####################

# treshold for absolute value of sample to be considered as 'low signal'
ls_treshold = 2

# minimal length of 'low signal' (number of frames/samples)
ls_min_length = 64

# number of frames before and after 'low signal' to be checked for 'sudden drop'
num_frames_before = 32
num_frames_after  = 32

# treshold for mean of absolute values of samples to be considered as 'sudden drop'
treshold_before = 256
treshold_after  = 256