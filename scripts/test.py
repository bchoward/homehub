#!/usr/bin/env python


import datetime
import time
import re

import subprocess
from subprocess import CalledProcessError

sleep_int = 3
btaddrs = [ '18:F6:43:4E:DB:6B', # bch
            ]

def detect(btaddress):
    cmd = ['/usr/bin/hcitool', 'info', btaddress]
    kwargs = {'stderr':subprocess.STDOUT}
    try:
        output = subprocess.check_output(cmd) #, **kwargs)
        print "output = {}".format(output)
        m = re.search(r'^\s+Device Name:\s+(.*)', str(output) , re.MULTILINE)
        if m:
            return m.group(1)
    except CalledProcessError as e:
        print e
        return None
    return None

def detect_list(addr_list):
    return [detect(a) for a in addr_list]

def detect_dict(addr_list):
    return {key: detect(key) for key in addr_list}



def main():
    d = {key:None for key in btaddrs}
    while True:


        rs = detect_dict(d)
        print d
        for k in d.keys():
            if d[k] != rs[k]:
                if rs[k]:
                    print "address {}({}) in range".format(k, rs[k])
                else:
                    print "address {}({}) left ".format(k, rs[k])
                d[k] = rs[k]
        time.sleep(sleep_int)




if __name__ == "__main__":
    main()
