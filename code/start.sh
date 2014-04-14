DIR="/home/pi/data"
echo "Starting python process in dir $DIR"
nohup python code/processvid_pi.py $DIR &
echo "Started."
