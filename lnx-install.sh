#!/bin/bash
set -e

echo "Unlocker 3.0.5 for VMware Workstation"
echo "====================================="
echo "(c) Dave Parsons 2011-21"

# Ensure we only use unmodified commands
export PATH=/bin:/sbin:/usr/bin:/usr/sbin

# Make sure only root can run our script
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

echo Creating backup folder...
rm -rf ./backup 2>/dev/null
mkdir -p ./backup
cp -pv /usr/lib/vmware/bin/vmware-vmx ./backup/
cp -pv /usr/lib/vmware/bin/vmware-vmx-debug ./backup/
cp -pv /usr/lib/vmware/bin/vmware-vmx-stats ./backup/
if [ -d /usr/lib/vmware/lib/libvmwarebase.so.0/ ]; then
    cp -pv /usr/lib/vmware/lib/libvmwarebase.so.0/libvmwarebase.so.0 ./backup/
elif [ -d /usr/lib/vmware/lib/libvmwarebase.so/ ]; then
    cp -pv /usr/lib/vmware/lib/libvmwarebase.so/libvmwarebase.so ./backup/
fi

echo Creating tools folder...
rm -rf ./tools 2>/dev/null
mkdir -p ./tools

echo Patching...
./unlocker.py

echo Finished!

