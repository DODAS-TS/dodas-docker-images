#!/usr/bin/env python
import gfal2
import logging
import optparse
import sys
import os
from optparse import OptionParser
import cygno as cy

def event_callback(event):
    #print event
    print("[%s] %s %s %s" % (event.timestamp, event.domain, event.stage, event.description))

def monitor_callback(src, dst, average, instant, transferred, elapsed):
    print("[%4d] %.2fMB (%.2fKB/s)\r" % (elapsed, transferred / 1048576, average / 1024)),
    sys.stdout.flush()
    
def copy_s32tape(filename, backet="cygno-data", intag="LNGS", outtag=""):   
    # filename = "run02308.mid.gz"
    source =  "https://s3.cloud.infn.it/v1/AUTH_2ebf769785574195bde2ff418deac08a/{:s}/{:s}/{:s}".format(backet, intag, filename)
    if outtag != "":
        dest_p = "{:s}/{:s}".format(outtag, filename)
    else:
        dest_p = filename
    dest   =  "davs://xfer-archive.cr.cnaf.infn.it:8443/cygno/{:s}".format(dest_p)
    dest_cred = os.environ['TAPE_TOKEN']

# ADD here the T1 tape token
# dest_cred = ""

    print("Source:      %s" % source)
    print("Destination: %s" % dest)
    print("Destination Token: %s" % dest_cred)

# Instantiate gfal2
    ctx = gfal2.creat_context()

# Set transfer parameters
    params = ctx.transfer_parameters()
    params.event_callback   = event_callback
    params.monitor_callback = monitor_callback

        # to enable if needed [basic examples]
#        gfal2.set_verbose(gfal2.verbose_level.debug)
    params.overwrite = True
#        params.checksum_check = True

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
    
def main(backet, options, options, options):
    print(backet, options, options, options)

if __name__ == '__main__':
    cygno_backet_list = ["cygnus", "cygno-data", "cygno-sim", "cygno-analysis"]
    #
    parser = OptionParser(usage='usage: %prog\t [-tsv] [ls backet]\n\t\t\t [put backet filename]\n\t\t\t [[get backet filein] fileout]\n\t\t\t [rm backet fileneme]\nAvailable Backet: '+str(cygno_backet_list)+\
        "\n recall to run comman: \n eval \`oidc-agent\` \n oidc-gen --reauthenticate --flow device infncloud-iam")
    parser.add_option('-b','--backet', dest='backet', type='string', default='cygno-data', help='backet on s3;');
    parser.add_option('-t','--intag', dest='intag', type='string', default='LNGS', help='tag on s3;');
    parser.add_option('-o','--outtaag', dest='intag', type='outtaag', default='LNGS', help='out tag on tape;');
    parser.add_option('-s','--session', dest='session', type='string', default='infncloud-iam', help='token profile [infncloud-iam];');
    parser.add_option('-v','--verbose', dest='verbose', action="store_true", default=False, help='verbose output;');
    (options, args) = parser.parse_args()
    #
    if options.verbose: 
        print(">> resquested arguments:", args)
        print(">> resquested options:", options)
    #       
    # if len(args) < 2:
    #     parser.error("incorrect number of arguments")
    # if not (args[1] in cygno_backet_list):
    #     error = "backet not availabe in cygno repo: "+str(cygno_backet_list)
    #     parser.error(error)
    
    
    main(options.backet, options.intag, options.outtag, options.session)

