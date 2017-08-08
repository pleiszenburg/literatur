#!/usr/bin/python3.4
# -*- coding: utf-8 -*-

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPORTS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

import atexit
from time import process_time
from functools import reduce


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# TIMING ROUTINES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def lw_secondsToStr(t):
	
    return "%d:%02d:%02d.%03d" % reduce(lambda ll,b : divmod(ll[0],b) + ll[1:], [(t*1000,),1000,60,60])


def lw_log(s, elapsed = None):
	
    print(lw_line)
    print(lw_secondsToStr(process_time()) + ' - ' + s)
    if elapsed:
        print("Elapsed time:", elapsed)
    print(lw_line)


def lw_endlog():
	
    lw_end = process_time()
    elapsed = lw_end - lw_start
    lw_log("End Program", lw_secondsToStr(elapsed))


def lw_now():
    return lw_secondsToStr(process_time())


lw_line = "=" * 40

lw_start = process_time()
atexit.register(lw_endlog)
lw_log("Start Program")
