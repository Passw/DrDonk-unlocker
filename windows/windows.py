#!/usr/bin/env python3
# coding=utf-8

"""
Copyright (c) 2014-2021 Dave Parsons & Sam Bingner

This code is pretty unpythonic so that it can be easily distributed using an embedded Python interpreter on Windows
It uses subprocess and native commands rather than install additional packages such as pywin32
"""

from configparser import ConfigParser
import ctypes
import os
from unlocker import patchsmc, patchgos
import setctime
import shutil
import subprocess
import sys
from winreg import *

SCRIPT_FOLDER = os.path.dirname(os.path.abspath(__file__))

# Windows service constants
SVC_ERROR = -1
SVC_STOPPED = 1
SVC_RUNNING = 4

# Check minimum Python version
if sys.version_info < (3, 6):
    sys.stderr.write('You need Python 3.6 or later\n')
    sys.exit(1)


# --------------------------------------------------------------------------------------------------
# ==== WINDOWS MISC FUNCTIONS  =====================================================================
# --------------------------------------------------------------------------------------------------

def is_admin():
    # Check we are running as admin
    # noinspection PyBroadException
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False


# --------------------------------------------------------------------------------------------------
# ==== FILE FUNCTIONS  =============================================================================
# --------------------------------------------------------------------------------------------------
def copyfile(src, dst):
    # Copy file and preserve ctime/atime/utime
    print(f'Copying file {src} to {dst}')
    shutil.copy2(src, dst)
    setctime.setctime(dst, os.path.getctime(src))
    print(f'src ctime: {os.path.getctime(src)} mtime: {os.path.getmtime(src)} atime: {os.path.getatime(src)}')
    print(f'dst ctime: {os.path.getctime(dst)} mtime: {os.path.getmtime(dst)} atime: {os.path.getatime(dst)}')
    return


def joinpath(folder, filename):
    # Help function to create absolute paths
    return os.path.join(folder, filename)


# --------------------------------------------------------------------------------------------------
# ==== BACKUP/RESTORE FUNCTIONS  ===================================================================
# --------------------------------------------------------------------------------------------------
def backup(version, vmx, vmx_debug, vmx_stats, vmwarebase):
    backup_path = joinpath(SCRIPT_FOLDER, 'backup')
    if not os.path.exists(backup_path):
        os.mkdir(backup_path)
    version_path = joinpath(backup_path, version)
    if not os.path.exists(version_path):
        os.mkdir(version_path)

    vmx_copy = joinpath(version_path, os.path.basename(vmx))
    copyfile(vmx, vmx_copy)

    vmx_debug_copy = joinpath(version_path, os.path.basename(vmx_debug))
    copyfile(vmx_debug, vmx_debug_copy)

    vmx_stats_copy = joinpath(version_path, os.path.basename(vmx_stats))
    copyfile(vmx_stats, vmx_stats_copy)

    vmwarebase_copy = joinpath(version_path, os.path.basename(vmwarebase))
    copyfile(vmwarebase, vmwarebase_copy)
    return


def restore(version, vmx, vmx_debug, vmx_stats, vmwarebase):
    return


def checksum():
    return


# --------------------------------------------------------------------------------------------------
# ==== SERVICE FUNCTIONS  ==========================================================================
# --------------------------------------------------------------------------------------------------
def svc_start(name):
    # Use the sc.exe to start a service
    # noinspection PyBroadException
    try:
        os.system(f'net start {name}')
        while True:
            status = svc_status(name)
            if status == SVC_RUNNING:
                break
            elif status == SVC_ERROR:
                break
            else:
                continue
    except Exception:
        status = SVC_ERROR
    return status


def svc_status(name):
    # Use the sc.exe to get the status of a service
    status = None
    # noinspection PyBroadException
    try:
        # Parse output in language independant way to get status code
        output = subprocess.check_output(f'sc.exe query {name}').decode('UTF-8')
        output = output.splitlines()
        status = int(output[3].strip(' ').split(':')[1].strip(' ').split(' ')[0])
    except Exception:
        status = -1
    return status


def svc_stop(name):
    # Use the sc.exe to stop a service
    # noinspection PyBroadException
    try:
        os.system(f'net stop {name}')
        while True:
            status = svc_status(name)
            if status == SVC_STOPPED:
                break
            elif status == SVC_ERROR:
                break
            else:
                continue
    except Exception:
        status = SVC_ERROR
    return status


# --------------------------------------------------------------------------------------------------
# ==== TASK FUNCTIONS  ==========================================================================
# --------------------------------------------------------------------------------------------------
def task_start(name):
    return


def task_stop(name):
    return


# --------------------------------------------------------------------------------------------------
# ==== MAIN FUNCTION  ==============================================================================
# --------------------------------------------------------------------------------------------------
# noinspection PyUnresolvedReferences
def main():
    if not is_admin():
        # Re-run the program with admin rights
        # Use sys.argv[1:] instead of sys.argv for pyinstaller etc.
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

    print('Unlocker 3.0.5 for VMware Workstation/Player')
    print('============================================')
    print('(c) David Parsons 2011-21')

    # Get the product verison, build and paths from registry
    reg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
    key = OpenKey(reg, r'SOFTWARE\Wow6432Node\VMware, Inc.\VMware Player')
    buildnumber = QueryValueEx(key, 'BuildNumber')[0]
    productversion = QueryValueEx(key, 'ProductVersion')[0]
    installpath = QueryValueEx(key, 'InstallPath')[0]
    installpath64 = QueryValueEx(key, 'InstallPath64')[0]

    # Create paths to all relevant files
    vmx = joinpath(installpath64, 'vmware-vmx.exe')
    vmx_debug = joinpath(installpath64, 'vmware-vmx-debug.exe')
    vmx_stats = joinpath(installpath64, 'vmware-vmx-stats.exe')
    vmwarebase = joinpath(installpath, 'vmwarebase.dll')
    vmware_tray = joinpath(installpath, 'vmware-tray.exe')

    print(f'Patching version {productversion}')
    backup(productversion, vmx, vmx_debug, vmx_stats, vmwarebase)
    return
    # Stop services
    config = ConfigParser()
    config.read('./config.toml')
    for service in config['services']:
        flag = config['services'][service]
        status = svc_status(service)
        if status != SVC_ERROR and status == SVC_RUNNING:
            svc_stop(service)

    # # Patch the vmx executables skipping stats version for Player
    # patchsmc(vmx, vmx_so)
    # patchsmc(vmx_debug, vmx_so)
    # if os.path.isfile(vmx_stats):
    #     patchsmc(vmx_stats, vmx_so)
    #
    # # Patch vmwarebase for Workstation and Player
    # vmx_so = False
    # patchbase(vmwarebase)

    # Start services
    for service in config['services']:
        flag = config['services'][service]
        status = svc_status(service)
        if status != SVC_ERROR and status == SVC_STOPPED:
            svc_start(service)
    return


if __name__ == '__main__':
    main()
