#!/usr/bin/env python2

import optparse
import sys
import os
import numpy as np
import time
import gfal2

dest_cred = os.environ['TAPE_TOKEN']
def event_callback(event):
    #print event
    print("[%s] %s %s %s" % (event.timestamp, event.domain, event.stage, event.description))

def monitor_callback(src, dst, average, instant, transferred, elapsed):
    print("[%4d] %.2fMB (%.2fKB/s)\r" % (elapsed, transferred / 1048576, average / 1024)),
    sys.stdout.flush()
    
def copy_s32tape(file_name, bucket, tag, outtag, session, verbose=False):   
    import urllib
    import gfal2
    import os

    #filekey=urllib.pathname2url(filekey)
    source =  "https://s3.cloud.infn.it/v1/AUTH_2ebf769785574195bde2ff418deac08a/{:s}/{:s}/{:s}".format(bucket, tag, file_name)
    dest   =  "davs://xfer-archive.cr.cnaf.infn.it:8443/cygno/{:s}/{:s}".format(outtag, file_name)

# ADD here the T1 tape token
    if verbose: 
        print("Source:      %s" % source)
        print("Destination: %s" % dest)


# Instantiate gfal2
    ctx = gfal2.creat_context()

# Set transfer parameters
    params = ctx.transfer_parameters()
#    params.event_callback   = event_callback
    params.monitor_callback = monitor_callback

# to enable if needed [basic examples]
# gfal2.set_verbose(gfal2.verbose_level.debug)
    params.overwrite = True
#    params.checksum_check = True

# writing on tape at T1 requires authN/Z
    
    d_cred = ctx.cred_new("BEARER",dest_cred)
    ctx.cred_set(dest,d_cred)
#    print("Destination credentials: %s" % dest_cred)

# Five minutes timeout
    params.timeout = 300

# Do actual copy using different protocols for source and destination 
    try:
        r = ctx.filecopy(params, source, dest)
        print("Copy succeeded!")
        return 0
    except Exception as e:
        print("Copy failed: %s" % str(e))
        # sys.exit(1)
        return 1
    
def main(file_name, bucket, tag, outtag, session, fsql, verbose=False):
    if fsql:
        connection = cy.daq_sql_cennection(verbose)
        if not connection:
            print ("ERROR: Sql connetion")
            sys.exit(1)

    if verbose: 
        print("Destination Token: %s" % dest_cred)
        print(file_name, bucket, tag, outtag, session)
    copy_s32tape(file_name, bucket, tag, outtag, session, verbose=verbose)
    if fsql:
        cy.daq_update_runlog_replica_status(connection, run_number, 
                                            storage="tape", status=1, verbose=verbose)
    
    sys.exit(0)
if __name__ == '__main__':
    from optparse import OptionParser
    TAG         = 'LNGS'
    BUCKET      = 'cygno-data'
    SESSION     = 'infncloud-wlcg'
    #
    parser = OptionParser(usage='usage: %prog [-b [{:s}] -t [{:s}] -s[{:s}] -csv]\n'.format(BUCKET,TAG,SESSION))
    parser.add_option('-b','--bucket', dest='bucket', type='string', default=BUCKET, help='PATH to raw data')
    parser.add_option('-t','--tag', dest='tag', type='string', default=TAG, help='in tag on S3')
    parser.add_option('-o','--outtag', dest='outtag', type='string', default=TAG, help='out tag on tape')
    parser.add_option('-s','--session', dest='session', type='string', default=SESSION, help='token profile '+SESSION);
    parser.add_option('-q','--sql', dest='sql', action="store_true", default=False, help='update sql')
    parser.add_option('-v','--verbose', dest='verbose', action="store_true", default=False, help='verbose output')
    (options, args) = parser.parse_args()
    if options.verbose: 
        print ("options", options)
        print ("args", args)
          
    if len(args) < 1:
        parser.error("incorrect number of arguments")
    else:
        file_name=args[0]
        main(file_name, bucket=options.bucket, tag=options.tag, outtag=options.outtag, 
             session=options.session, fsql=options.sql, verbose=options.verbose)

