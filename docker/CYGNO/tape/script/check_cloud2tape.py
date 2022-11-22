#!/usr/bin/env python3
#
# G. Mazzitelli 2022
# versione DAQ LNGS/LNF per midas file2cloud 
# cheker and sql update Nov 22 
#

def main(bucket, TAG, session, fcopy, fsql, verbose):
    #

    import os,sys

    import numpy as np
    import cygno as cy
    
    import time
    import subprocess
    import mysql.connector
    start = end = time.time()
    tmpout = '/tmp/tmp.dat'
    tape_path = 'davs://xfer-archive.cr.cnaf.infn.it:8443/cygno/'
    if fsql:
        connection = cy.daq_sql_cennection(verbose)
        if not connection:
            print ("ERROR: Sql connetion")
            sys.exit(1)
    file_in_dir=cy.s3.bucket_list(tag=TAG, bucket=bucket, session=session, filearray=True, verbose=verbose)
    print ("File in dir %d" % np.size(file_in_dir))
    for i in range(0, np.size(file_in_dir)):
        if ('run' in str(file_in_dir[i]))   and \
        ('.mid.gz' in str(file_in_dir[i]))  and \
        (not file_in_dir[i].startswith('.')):
            #
            # loop on run*.gz files
            #
            file_in= file_in_dir[i].split("/")[-1]
            run_number = int(file_in.split('run')[-1].split('.mid.gz')[0])

            filesize = int(cy.s3.obj_size(file_in, tag=TAG, bucket=bucket, session=session, verbose=verbose))

            if (verbose): 
                print("-------------------------")
                print("Cloud name", file_in)
                print("run_number", run_number) 
                print("Cloud size", filesize)
                print("fsql", fsql)
                print("fcopy", fcopy)
            # if (fsql): 
            #     cy.daq_update_runlog_replica_status(connection, run_number, storage="cloud", status=1, verbose=verbose)
            #     cy.daq_update_runlog_replica_size(connection, run_number, filesize, verbose=verbose)
            if (start-end)>1000 or (start-end)==0:
                output = subprocess.check_output("source ./oicd-setup.sh", shell=True)
                print (output)
                start = time.time()
            try:
                tape_data_file = subprocess.check_output("gfal-ls -l "+tape_path\
                                                +TAG+"/"+file_in+" | awk '{print $5\" \"$9}'", shell=True)
            
                remotesize, tape_file = tape_data_file.decode("utf-8").split(" ")
                remotesize = int(remotesize)
            except:
                remotesize=0
                tape_file=file_in
            if (verbose): 
                print("Tape", tape_file) 
                print("Tape size", remotesize)
            

            if (filesize != remotesize) and (filesize>0):
                print ("WARNING: file size mismatch", file_in, filesize, remotesize)
                if (fcopy):
                    print (">>> coping file: "+file_in)

                    cy.obj_get(file_in, tmpout, tag, bucket=bucket, session=session, verbose=verbose)
                    # status, isthere = cy.s3.obj_put(INAPATH+file_in,tag=TAG, 
                    #                              bucket=bucket, session=session, 
                    #                              verbose=verbose)
                    tape_data_copy = subprocess.check_output("gfal-copy "+tape_path\
                                                +TAG+"/"+file_in, shell=True)
                    
                    cy.cmd.rm(tmpout)
                    if verbose: print (">>> status: ", status, "sql:", fsql)
                    if (not status and fsql):
                        cy.daq_update_runlog_replica_status(connection, run_number, 
                                                            storage="tape", status=1, verbose=verbose)
                        cy.daq_update_runlog_replica_tag(connection, run_number, TAG=TAG, verbose=verbose)
                    else:
                        print ("ERROR: Copy on TAPE faliure")
            else:
                print ("File ", file_in, " ok")
                if (fsql):
                    cy.daq_update_runlog_replica_status(connection, run_number, 
                                                        storage="tape", status=1, verbose=verbose)
            end = time.time()
                
    sys.exit(0)
if __name__ == "__main__":
    from optparse import OptionParser
    #
    # deault parser value
    #
    TAG         = 'LNGS'
    BUCKET      = 'cygno-data'
    SESSION     = 'infncloud-wlcg'


    parser = OptionParser(usage='usage: %prog [-b [{:s}] -t [{:s}] -s[{:s}] -csv]\n'.format(BUCKET,TAG,SESSION))
    parser.add_option('-b','--bucket', dest='bucket', type='string', default=BUCKET, help='PATH to raw data')
    parser.add_option('-t','--tag', dest='tag', type='string', default=TAG, help='tag where dir for data')
    parser.add_option('-c','--copy', dest='copy', action="store_true", default=False, help='upload data to TAPE if not present')
    parser.add_option('-s','--session', dest='session', type='string', default=SESSION, help='token profile [infncloud-iam];');
    parser.add_option('-q','--sql', dest='sql', action="store_true", default=False, help='update sql')
    parser.add_option('-v','--verbose', dest='verbose', action="store_true", default=False, help='verbose output')
    (options, args) = parser.parse_args()
    if options.verbose: 
        print ("options", options)
        print ("args", args)
     
    main(options.bucket, options.tag, options.session, options.copy, options.sql, options.verbose)