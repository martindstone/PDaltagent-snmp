#!/usr/bin/env python3

#####
# trap handler for Net-SNMP snmptrapd to send traps to PD via PDaltagent
#####

from sys import stdin
import subprocess
import os

routing_key = os.getenv('PDAGENTD_DEFAULT_ROUTING_KEY', 'set your PDAGENTD_DEFAULT_ROUTING_KEY!')

lines = [x.rstrip('\n') for x in stdin]
# first two lines are host and IP
host = lines[0]
ip = lines[1]
# the rest is varbinds
vars = lines[2:]

fields = [
  f"-f 'host={host}'",
  f"-f 'ip={ip}'"
]
for var in vars:
  (k, v) = var.replace('"', '').split(' ', 1)

  # if you want to put PD routing key in a varbind:
  if k == "DISMAN-EVENT-MIB::mteTriggerComment":
    routing_key = v

  fields.append(f"-f '{k}={v}'")

cmd = f"pd-send -k {routing_key} -t trigger -d 'hey snmp' " + ' '.join(fields)
subprocess.run(cmd, shell=True, capture_output=True)

