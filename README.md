# Stress Testing for EVM based blockchains

### Author
- __[Shai Sundar](https://github.com/shaisundar)__



## Step 0 - Access to Stress Test main server
Set up a Machine for Stress testing.
If you are looking at creating an AWS instance for this, you can follow along from an SSH terminal.

(**General Hardware Estimation** - Higher the core count = Emulate more users hitting the server.
For my testing, I could comfortably emulate 5000 users on a 32core, 64gb RAM machine. (c6a.8large) )


## Step 1 - Log collection
This step focuses on collecting calls for a given blockchain. The datasource is up to you. Some options are -
<ol>
<li>You can get a list of calls from any Public Database (if available)
<li>You can packet capture your own network requests from a previously running server.
<li>You can use 3rd party logging tools like Datadog to collect the logs- from your network, if you have such a thing setup. 
</ol>

Make sure that your logs have all the different types of calls for a blockchain captured to get realistic results.
The final format of this logs must be in csv format, with one call per line. Like this - 
![image](https://user-images.githubusercontent.com/30902543/185180694-825d6e56-0491-4a43-9e86-2a1fb34a07ef.png)

The below steps are for collecting from Datadog - 
Start by cloning this repo.

Create a chain directory, by copying from one of the existing chain directories.(polygon-stress/ harmony-stress)

In the chain directory, run this command 
DD_SITE="datadoghq.eu" DD_API_KEY="<API_KEY>" DD_APP_KEY="<APP_KEY>" python3 get_logs.py

![image](https://user-images.githubusercontent.com/30902543/185181381-fa5906e4-492f-46d1-bbfc-a586dab4a975.png)

Fill the required data(make sure the date is in the exact format as above). This should fetch the  requested logs. 

Wherever you get the logs from, make sure they are placed into "fetch_logs" directory, with the name "all_final.csv"





## Step 2 -  Connecting to the Blockchain node

Make sure that your Stress testers Public IP address is whitelisted on the nodes inbound rules and ports.

Next, remove the specific server out of rotation to block public data from hitting this node - for accurate results.

CD into the correct chain folder, and set up the stress testing using the below commands -

<code>
sh set_IP.sh

sh set_threshold.sh
</code>

Fill in the info for the data node that you are stress testing like below -
![image](https://user-images.githubusercontent.com/30902543/185190423-baf85b52-6d9f-421b-893a-99858b1ea66a.png)



Now its time to run the stress tester, using the below command - 

<code>
sh ../apache-jmeter-5.5/bin/jmeter.sh -n -t Stresser.jmx
</code>

The results and logs of this run will be stored in the "fetch_logs" folder with the prefix "all_*".

##### Note- The prefix **"all_"** depicts the current set of results. Once done with the current chain, and you want to move onto the next chain, please store these results elsewhere, or rename them. 


## Step 3 : Monitoring

Lets keep the Stress tester running, while monitoring your node on the 2nd screen - 
This would be upto to figure out if your node is in sync with the genesys or not. One easy way to do this would be to use CURL calls to your server and the genesys - comparing the current block_height. Anyways, I will leave that to you.

(In my case, We are using an in-house tool to monitor this).

As shown below, Once your node goes out of sync, It means that we are overloading it - 

![image](https://user-images.githubusercontent.com/30902543/185407859-ff6b2307-6ce8-4708-bb70-8198cd117a05.png)


This means - In your next iteration, you reduce your throughput to the server. 

You simply need to do

<code>sh set_threshold</code>

and reduce the throughput. Then re-run the stresstester as described in the previous step.




## Step 4: Results 
Now it is a matter of fine tuning the throughput to a point where your node remains stable and in sync with the Genesys.(This part remains to be automated)

Find the maximum throughput such that the node stays in sync for at least 4-5 minutes without going out-of-sync.

That is the limit of the node and the result that we are looking for. 

After simple calculations, Below is how a result will look like (just for visualization)

![image](https://user-images.githubusercontent.com/30902543/185410020-3b13b058-d6b1-40d1-b9aa-cc9e4177f583.png)



## Bonus: Performance Tuning

If you want your Node to cater to a certain QoS threshold, you can also find the max throughput to achieve this. 

You can look at the "latency.csv" file under the "fetch_logs" folder - and graph this result to see how your latency changes with different thresholds.

Something like this - (just for visualization)

![image](https://user-images.githubusercontent.com/30902543/185409962-2f841e78-261d-4270-a404-ea52fbda94fb.png)
