PID=`ps -eaf | grep "python.*processvid*" | grep -v grep | sed -e "s/^pi\s*\([0-9]*\)\s.*$/\1/"`

if [ -n "$PID" ]; then
    echo "Killing $PID"
    kill $PID
    echo "Killed."
fi
