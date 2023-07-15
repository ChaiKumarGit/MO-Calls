import subprocess
import time

def calls(phoneNumber,noCalls,selectedDeviceCode,path,callTime):
    connect = path+r'\data\ -s '+dial+phoneNumber   #Make Call
    disconnect = path+r'\data\ -s '+ENDCALL    #Disconnect Call
    for x in range(noCalls):
        time.sleep(3)
        procVar = subprocess.Popen(connect, shell=True,
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(callTime)
        procVar = subprocess.Popen(disconnect, shell=True,
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
