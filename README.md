gmond-hwmon-module
==================

A python gmond module that reads /sys/class/hwmon.

![Demo image](https://raw.github.com/handyman5/gmond-hwmon-module/screenshots/hwmon.png)

It should automatically figure out what sensors exist and give the metrics reasonable names.

**NEW**: This module will now read the `device/tempX_label` files (if they exist) to get more descriptive metric names.
