#!/usr/bin/env python2
import gfal2
import logging
import optparse
import sys
import os
"""
This is a basics example that should evolve based on user needs. 
The purpose is to enable the third party copy (TPC) from a generic source
to a generic destination. 
gfal usage grant the possibility to use two distinct protocols for source
and destination, including two disting authN/Z method. 
All this enable the copy to Tier1 CNAF Tape buffer.  
"""

def event_callback(event):
    #print event
    print("[%s] %s %s %s" % (event.timestamp, event.domain, event.stage, event.description))

def monitor_callback(src, dst, average, instant, transferred, elapsed):
    print("[%4d] %.2fMB (%.2fKB/s)\r" % (elapsed, transferred / 1048576, average / 1024)),
    sys.stdout.flush()

if __name__ == '__main__':
    #init. Note all these should become opts        
    filename = "run02308.mid.gz"
    source =  "https://s3.cloud.infn.it/v1/AUTH_2ebf769785574195bde2ff418deac08a/cygno-data/LNGS/%s" %filename
    dest   =  "davs://xfer-archive.cr.cnaf.infn.it:8443/cygno/%s" %filename

# ADD here the T1 tape token
    #dest_cred = ""
    dest_cred = os.environ['TAPE_TOKEN']

    print("Source:      %s" % source)
    print("Destination: %s" % dest)
#    print("Destination Token: %s" % dest_cred)

# Instantiate gfal2
    ctx = gfal2.creat_context()

# Set transfer parameters
    params = ctx.transfer_parameters()
#    params.event_callback   = event_callback
    params.monitor_callback = monitor_callback

# to enable if needed [basic examples]
#    gfal2.set_verbose(gfal2.verbose_level.debug)
#    params.overwrite = True
#    params.checksum_check = True

# not necessarily needed. 
# current cygno data are www readable 
#       s_cred = ctx.cred_new("BEARER",source_cred)
#       ctx.cred_set(source,s_cred)
#       print("Source credentials: %s" % source_cred)

# writing on tape at T1 requires authN/Z
    d_cred = ctx.cred_new("BEARER",dest_cred)
    ctx.cred_set(dest,d_cred)
    print("Destination credentials: %s" % dest_cred)

# Five minutes timeout
    params.timeout = 300

# Do actual copy using different protocols for source and destination 
    try:
        r = ctx.filecopy(params, source, dest)
        print("Copy succeeded!")
    except Exception as e:
        print("Copy failed: %s" % str(e))
        sys.exit(1)