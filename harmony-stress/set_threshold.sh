#bash script
echo -n "number of threads: "
read Threadd
echo -n "throughput in req/sec: "
read Through
echo -n "test time in seconds: "
read Timee



sed -i "1409s/.*/        <stringProp name=\"ThreadGroup.num_threads\">$Threadd<\/stringProp>/" Stresser.jmx 
sed -i "1472s/.*/              <stringProp name=\"50547\">$Through<\/stringProp>/" Stresser.jmx
sed -i "1473s/.*/              <stringProp name=\"50547\">$Through<\/stringProp>/" Stresser.jmx
sed -i "1474s/.*/              <stringProp name=\"1448635039\">$Timee<\/stringProp>/" Stresser.jmx

echo $"-----------------------------------------------------\n"
echo $"Config Succesfull, Ready to Run tests !!\n"
echo $"-----------------------------------------------------\n"
