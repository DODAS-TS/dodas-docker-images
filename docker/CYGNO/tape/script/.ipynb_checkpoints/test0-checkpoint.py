#!/usr/bin/env python2
import gfal2
import logging
import optparse
import sys
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
        source_cred = ""

        # ADD here the T1 tape token
        dest_cred = "eyJraWQiOiJyc2ExIiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiIxZTU0YTNkYi0yOTRiLTQ1OTAtYjc2Ni0zNTk0OGYyZWJlMDgiLCJzY29wZSI6ImFkZHJlc3MgcGhvbmUgb3BlbmlkIG9mZmxpbmVfYWNjZXNzIHByb2ZpbGUgZWR1cGVyc29uX3Njb3BlZF9hZmZpbGlhdGlvbiBlZHVwZXJzb25fZW50aXRsZW1lbnQgZW1haWwiLCJpc3MiOiJodHRwczpcL1wvaWFtLXQxLWNvbXB1dGluZy5jbG91ZC5jbmFmLmluZm4uaXRcLyIsIm5hbWUiOiJHaW92YW5uaSBNYXp6aXRlbGxpIiwiZ3JvdXBzIjpbIkN5Z25vIl0sInByZWZlcnJlZF91c2VybmFtZSI6Im1henppdGVsIiwib3JnYW5pc2F0aW9uX25hbWUiOiJ0MS1jb21wdXRpbmciLCJleHAiOjE2NjkwNDYyNDgsImlhdCI6MTY2OTA0MjY0OCwianRpIjoiODM4ZjJjOWMtYmY5Ny00OWQ5LThjOGEtN2M4MmIxZDU4MWJjIiwiY2xpZW50X2lkIjoiYzdhMmIzNDEtZjE2OS00M2Y1LWJmYTktNDdiZDNkZjc5MzY5IiwiZW1haWwiOiJnaW92YW5uaS5tYXp6aXRlbGlAbG5mLmluZm4uaXQifQ.JvniZbgq6sQ0wBJSF1sVDccezel_7fOWkHuydyE0_k6CZUzAELIkIPXt-bL8QfodKTTvW_6WcC2Zzsv224nbv9T9LZ2-_qq9ZcsyQrbnigRgOSDhmaFBwn-EWdhyzmEJo5nDpg61V_1wTghyNDrvzuLlS7Fh8r-55TEor9b6NaE"


#       cred = gfal2.cred_new("BEARER", os.getenv('TOKEN'))

	print("Source:      %s" % source)
	print("Destination: %s" % dest)

	# Instantiate gfal2
	ctx = gfal2.creat_context()

	# Set transfer parameters
	params = ctx.transfer_parameters()
	params.event_callback   = event_callback
	params.monitor_callback = monitor_callback

        # to enable if needed [basic examples]
#        gfal2.set_verbose(gfal2.verbose_level.debug)
#        params.overwrite = True
#        params.checksum_check = True

        # not necessarily needed. 
        # current cygno data are www readable 
 #       s_cred = ctx.cred_new("BEARER",source_cred)
 #       ctx.cred_set(source,s_cred)
 #       print("Source credentials: %s" % source_cred)

        #writing on tape at T1 requires authN/Z
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