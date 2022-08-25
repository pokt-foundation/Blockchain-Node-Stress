#bash script
echo -n "IP Adress of node: "
read IP
echo -n "Port number on node: "
read Port



sed -i "1429s/.*/          <stringProp name=\"HTTPSampler.domain\">$IP<\/stringProp>/" Stresser.jmx 
sed -i "1430s/.*/          <stringProp name=\"HTTPSampler.port\">$Port<\/stringProp>/" Stresser.jmx


echo $"-----------------------------------------------------\n"
echo $"Machine Chosen Successfully !!\n"
echo $"-----------------------------------------------------\n"
