#!/usr/bin/env python2
# -*- coding: utf-8 -*-

#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------------------------------------------------
# ROS-MAGNA
# ----------------------------------------------------------------------------------------------------------------------
# The MIT License (MIT)

# Copyright (c) 2016 GRVC University of Seville

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
# Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
# OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# ----------------------------------------------------------------------------------------------------------------------

"""
Created on Jul 22 2019

@author: josmilrom
"""

# import pyModeS as pms
import numpy as np
import rospy, time, tf, tf2_ros, math
import paramiko
from copy import deepcopy
from geometry_msgs.msg import *
from sensor_msgs.msg import Image, BatteryState
from std_msgs.msg import String
from nav_msgs.msg import Path
from uav_abstraction_layer.msg import State
import json
from magna.srv import *
from magna.msg import *

def serverClient(request, address, Type, print_request = False, print_response = False):

    if print_request == True:
        print(request)

    rospy.wait_for_service(address)
    try:
        client = rospy.ServiceProxy(address, Type)

        response = client(request)

        if print_response == True:
            print(response)

        return response
        
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e
        print "error in {}".format(address)

def xmlGetIndexByTagAndAttribName(root,tag,att_nam,att_val):
    for i, child in enumerate(root):
        if child.tag == tag:
            if att_nam in child.attrib.keys():
                if child.attrib[att_nam] == att_val:
                    return i, child

def xmlSetAttribValueByTagAndAttribValue(root,tag,get_att_nam,get_att_val,set_att_nam,set_att_val):
    root[xmlGetIndexByTagAndAttribName(root,tag,get_att_nam,get_att_val)[0]].attrib[set_att_nam] = set_att_val
    return root

def xmlSetTextValueByTagAndAttribValue(root,tag,get_att_nam,get_att_val,set_text_val):
    root[xmlGetIndexByTagAndAttribName(root,tag,get_att_nam,get_att_val)[0]].text = set_text_val
    return root

class SSHConnection(object):
    def __init__(self, hostname, username='', password='', port=22):

        # try:
        self.client = paramiko.SSHClient()
        self.client.load_system_host_keys()
        self.client.set_missing_host_key_policy(paramiko.WarningPolicy())
        
        self.client.connect(hostname, port=port, username=username, password=password)

        # except:
        #     self.client.close()


    def executeCommand(self, cmd):

        stdin, stdout, stderr = self.client.exec_command(cmd)
        print "out", stdout.read()
        print "err", stderr.read()


    def transferFile(self, local_path, remote_path):

        sftp = self.client.open_sftp()
        sftp.put(local_path, remote_path)


    def closeConnection(self):

        self.client.close()

    def __del__(self):

        self.closeConnection()