#!/bin/bash
set -e

echo "Get macOS VMware Tools 3.0.5"
echo "==============================="
echo "(c) Dave Parsons 2015-21"

# Ensure we only use unmodified commands
export PATH=/bin:/sbin:/usr/bin:/usr/sbin

./gettools.py
