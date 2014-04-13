rsync -ave ssh /Volumes/Userdata/nik/bastel/2014-03-29_Pi_hacking/code pi@192.168.0.43:

#python code/processvid_pi.py
sleep 1
ssh pi@192.168.0.43 -c "bash code/stop.sh"
sleep 1
ssh pi@192.168.0.43 -c "bash code/start.sh"




