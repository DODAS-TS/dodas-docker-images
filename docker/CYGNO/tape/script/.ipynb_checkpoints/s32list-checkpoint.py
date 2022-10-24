#!/usr/bin/env python3
import logging
import optparse
import sys
import os
from optparse import OptionParser
from cygno import s3
import numpy as np


    
def main(backet, intag, outtag, session, verbose):
    if verbose: 
        print("Destination Token: %s" % dest_cred)
        print(backet, intag, outtag, session, verbose)
        
    print("Generating index...")
    lsfilekey = s3.backet_list(tag=intag, bucket=backet, session=session, filearray=True, verbose=verbose)
    f = open("./index.txt", "w")
    if verbose: print (lsfilekey)
#    np.save("./index.npy", lsfilekey)
    for i, filekey in enumerate(lsfilekey):
        f.write(filekey+"\n")
        if verbose: print(filekey.split('/')[-1])
    f.close()
    
    
if __name__ == '__main__':
    cygno_backet_list = ["cygnus", "cygno-data", "cygno-sim", "cygno-analysis"]
    #
    parser = OptionParser(usage='usage: %prog\t [-tsv] [ls backet]\n\t\t\t [put backet filename]\n\t\t\t [[get backet filein] fileout]\n\t\t\t [rm backet fileneme]\nAvailable Backet: '+str(cygno_backet_list)+\
        "\n recall to run comman: \n eval \`oidc-agent\` \n oidc-gen --reauthenticate --flow device infncloud-iam")
    parser.add_option('-b','--backet', dest='backet', type='string', default='cygno-data', help='backet on s3;');
    parser.add_option('-t','--intag', dest='intag', type='string', default='', help='tag on s3;');
    parser.add_option('-o','--outtaag', dest='outtag', type='string', default='', help='out tag on tape;');
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
    
    
    main(backet=options.backet, intag=options.intag, outtag=options.outtag, session=options.session, verbose=options.verbose)

