import json
import time
import re
import sys
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.logs_api import LogsApi
from datetime import datetime
from dateutil.tz import tzoffset

#methods=['eth_getLogs','eth_call','eth_blockNumber','eth_getTransactionReceipt','eth_getTransactionCount','eth_chainId','eth_getBlockByNumber','eth_getBalance']
methods=['eth_getLogs']

configuration = Configuration()
print("number of logs needed - ")
target=int(input())                     #2000000
print("blockchain id - ")
blkid = input()
print("start date and time in format(year, month, day, hour, minute, second) - ")
inyear, inmonth, inday, inhour, inminute, insec = [int(x) for x in input().split(', ')]
print("end date and time in format(year, month, day, hour, minute, second) - ")
endyear, endmonth, endday, endhour, endminute, endsec = [int(x) for x in input().split(', ')]

# Getting all the logs - 
for call in methods:
    with ApiClient(configuration) as api_client:
        api_instance = LogsApi(api_client)
        response = api_instance.list_logs_get(
            filter_query="@blockchainID:"+blkid,# service:*gateway* @requestBody.method:"+call,
            filter_from=datetime(inyear, inmonth, inday, inhour, inminute, insec, tzinfo=tzoffset(None, 3600)),
            filter_to=datetime(endyear, endmonth, endday, endhour, endminute, endsec, tzinfo=tzoffset(None, 3600)),
            page_limit=1000,

    )
    
    
    def cont(cursorid):
        with ApiClient(configuration) as api_client:
            api_instance = LogsApi(api_client)
            response2 = api_instance.list_logs_get(
                filter_query="@blockchainID:"+blkid,# service:*gateway* @requestBody.method:"+call,
                filter_from=datetime(inyear, inmonth, inday, inhour, inminute, insec, tzinfo=tzoffset(None, 3600)),
                filter_to=datetime(endyear, endmonth, endday, endhour, endminute, endsec, tzinfo=tzoffset(None, 3600)),
                page_limit=1000,
                page_cursor=cursorid
        )
            return(response2)
    
    
    # only 3000 logs can be got every 10 seconds, so we wait before sending further calls
    j=0
    with open('all_logs.txt', 'a+') as f:#call+'_logs.txt', 'a+'
        for i in response.data:
                f.write(i.attributes.message+"\n")
                j+=1
        cursorid = response.meta.page.after

        while(j<=target):
            time.sleep(3.5)
            try:
                response = cont(cursorid)
            except:
                print("failed working at",j)
                continue
            for i in response.data:
                f.write(i.attributes.message+"\n")
                j+=1
            cursorid = response.meta.page.after
        

    # Final formatting to make input readable by jmeter
    with open('../fetch_logs/all_final.csv','w') as outfile:#call+'_final.csv','w'
        with open('all_logs.txt', 'r') as infile:#call+'_logs.txt', 'r'
            for row in infile:
                row1=re.sub(r'^.*?{', '', row)
                outfile.write('{'+row1[:-1]+'\n')
                
                
