#!/usr/bin/env python

root = '/sys/class/hwmon'
descriptors = []

import os, glob, re

def temp_finder(name):
    params = re.search (r'.*_dev(\d+)_temp(\d+)_input', name).groups()
    path = os.path.join(root, 'hwmon%d/device/temp%d_input' % (int(params[0]), int(params[1])))
    val = open(path).read().strip()
    return int(val) / 1000.0

def metric_init(params):
    global descriptors

    sensors = sorted(glob.glob(os.path.join(root, 'hwmon*')))

    for s in sensors:
        temps = glob.glob(os.path.join(s, 'device/temp*_input'))
        probes = zip([s.replace('input', 'label') for x in temps], temps)

        for i, l in probes:
            l = os.path.basename(l)
            num = re.search('\d+', i)
            device = i[num.start():num.end()]
            label = l.replace(' ', '_').lower()
            item = {'name': 'hwmon_dev%s_%s' % (device, label),
                    'call_back': temp_finder,
                    'time_max': 90,
                    'value_type': 'float',
                    'units': 'C',
                    'slope': 'both',
                    'format': '%0.2f',
                    'description': 'Temperature for hwmon probe %s' % l,
                    'groups': 'hwmon'}
            descriptors.append(item)

    return descriptors

def metric_cleanup():
    '''Clean up the metric module.'''
    pass

if __name__ == '__main__':
    metric_init(None)
    for d in descriptors:
        v = d['call_back'](d['name'])
        print 'value for %s: %s' % (d['name'], str(v))
