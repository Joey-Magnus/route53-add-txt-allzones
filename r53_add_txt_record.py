#!/usr/bin/env python3
#To run on local machine User must generate AWS token/keys in credentials file
#Author: Joey Magnus | jmagnus@slyport.com | jmagnus@manh.com
########################################################

import boto3
from boto.route53.record import ResourceRecordSets

r53 = boto3.client('route53')
r53zones = r53.list_hosted_zones_by_name()

#Iterate through each DNS Zone
def main():
    i = 0                                       #iteration starting value
    while i < len(r53zones['HostedZones']):
        srcID = r53zones['HostedZones'][i]['Id']
        srcName = r53zones['HostedZones'][i]['Name']
        add_record(srcID, srcName)
        print(srcID + srcName)
        i += 1

#Function to write record to Zone File
def add_record(sourceid, sourcename):
	try:
		reply = r53.change_resource_record_sets(
		HostedZoneId = sourceid,
		ChangeBatch= {
						'Comment': 'DMARC record for proofpoint',
						'Changes': [
							{
							 'Action': 'UPSERT',
							 'ResourceRecordSet': {
								 'Name': sourcename,
								 'Type': 'TXT',
								 'TTL': 300,
								 'ResourceRecords': [{'Value': '\"v=DMARC1; p=reject; fo=1; rua=mailto:dmarc_rua@emaildefense.proofpoint.com ; ruf=mailto:dmarc_ruf@emaildefense.proofpoint.com \"'}]
							}
						}]
		})
	except Exception as e:
		print (e)

main()


