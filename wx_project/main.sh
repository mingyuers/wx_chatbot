#!/bin/sh
echo '====='
while true
do
ID=`ps -ef | grep "wx.py" | grep -v "$0" | grep -v "grep" | awk '{print $2}'`
for id in $ID
do
kill -9 $id
echo "killed $id"
done
DATE=$(date '+%Y-%m-%d %H:%M:%S')
echo $DATE+" restart wx.py"
bash wx.sh
sleep 7200
done

