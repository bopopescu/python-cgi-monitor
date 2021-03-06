#!/usr/bin/python

import cgi
from easysnmp import Session
import ast
import Devices
import Interfaces
import Utillity
import time


def singleOutput():
    print '''
        <table class="table is-bordered is-narrow is-fullwidth">
          <tr>
            <th>OID</th>
            <th>Description</th>
          </tr>
        '''
    # --------------------------------------------------------------
    user = Devices.Devices(community, 2)
    user.main(ipList, community, 2, mib)

    for item in user.result:
        print '<tr class="is-selected"><td><strong>' + mib.upper() + '</strong></td><td></td></tr>'
        for x in range(len(item)):
            if item[x].value != '':
                if (item[x].snmp_type).upper() == 'TICKS':
                    t_item = tools.humanize(int(item[x].value))
                else:
                    t_item = item[x].value
                print '<tr><td>' + item[x].oid + '</td><td>' + t_item + '</td></tr>'
    # --------------------------------------------------------------


def interfaceOutput():
    CONVERT = 1048576
    interface = Interfaces.Interface()
    interface.loadDictionary('exchangex')
    for ip in ipList:
        interface.operation(ip, community, 2)
        print '''<table class="table is-bordered is-narrow is-fullwidth">
        <tr class="is-selected"><th></th><td><strong>''' + mib.upper() + '''</strong></td><td></td><td></td><td></td><td></td><td></td></tr>
        <tr><th>#</th><td>Description</td><td>Type</td><td>MTU</td><td>Speed (Mbps)</td><td>AdminStatus</td><td>OperaStatus</td></tr>'''
        for temp in range(len(interface.result_desc)):
            print '''
            <tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>'''.format(
                temp,
                interface.result_desc[temp].value, interface.typeList[int(interface.result_Type[temp].value)],
                interface.result_Mtu[temp].value, round(float(interface.result_Speed[temp].value) / CONVERT, 2),
                interface.case[int(interface.result_Admin[temp].value)],
                interface.case[int(interface.result_Opera[temp].value)])
        interface.__del__()


def convertListToString(str):
    temp = ast.literal_eval(str)
    temp = [n.strip() for n in temp]
    return temp


form = cgi.FieldStorage()
tools = Utillity.Utilities()

ipAddress = form['ipList'].value

ipList = tools.convertStringToList(ipAddress)

community = form['community'].value

mib = form['droplist'].value

print "Content-type: text/html\n\n"

print '<h1 class="title"><strong>Testing Result!</strong></h1>'
print '<strong>Last Update on:</strong>', tools.gettime_ntp(), '<br>'
print ipList, '<br>'
print community, '<br>'
print mib, '<br><br>'
# print '<p class="subtitle"> You want to monitor router that contain ip address <strong>' + ipAddress + '.</strong> Wait a min ... </p>'

if (mib == "interface"):
    interfaceOutput()
else:
    singleOutput()

print '</table>'

# def manyToMany():
#     walker = Devices.Devices(community, 2)
#     print '''
#             <table class="table is-bordered is-narrow is-fullwidth">
# '''
#     for ip in ipList:
#         for oid in mib:
#             temp = walker.walkthrongh(ip, oid)
