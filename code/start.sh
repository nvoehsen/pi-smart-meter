FILE=data/`date +%F_%H%M%S`_capture.csv
echo "Starting python process to $FILE"
nohup python code/processvid_pi.py > $FILE &
echo "Started."
