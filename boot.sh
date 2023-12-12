#!/usr/bin/env bash

pwnd=$(./bin/irecovery -q | grep -c "PWND")
if [ $pwnd = 0 ]; then
    echo "Ensure device is in pwned DFU mode with signature checks removed."
    exit
fi
sleep 1
cpid=$(./bin/irecovery -q | grep "CPID" | sed "s/CPID: //")

./bin/irecovery -f boot/iBSS.img4
sleep 2
# send iBSS again.
./bin/irecovery -f boot/iBSS.img4
sleep 3
./bin/irecovery -f boot/iBEC.img4
sleep 2

if [[ "$cpid" == *"0x80"* ]]; then
    ./bin/irecovery -f boot/iBEC.img4
    sleep 2
    ./bin/irecovery -c "go"
    sleep 5
fi

./bin/irecovery -f boot/bootlogo.img4
sleep 1
./bin/irecovery -c "setpicture 0x1"
sleep 1
./bin/irecovery -f boot/devicetree.img4
sleep 1
./bin/irecovery -c "devicetree"
sleep 1
./bin/irecovery -f boot/trustcache.img4
sleep 1
./bin/irecovery -c "firmware"
sleep 1
./bin/irecovery -f boot/krnlboot.img4
sleep 1
./bin/irecovery -c "bootx"
