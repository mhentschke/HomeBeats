import platform
import numpy as np
import config
import devices

def get_property_if_exists(dictionary, property, default = None):
    if property in dictionary:
        return dictionary[property]
    else:
        return default

device_list = [] 
if "devices" in config_dict:
    if "dmx" in config_dict["devices"]:
        for d in config.config_dict["devices"]["dmx"]:
            ip = d["ip"]
            name = d["device"]
            leds = d["leds"]
            universe = d["universe"]
            multicast = get_property_if_exists(d, "multicast", default = False)
            effect = get_property_if_exists(d, "effect", default = config.EFFECT)
            device_list.append(devices.Device_DMX(leds, effect, name, ip, universe, multicast))
 

if config.DISPLAY_PIXELS:
    device_list.append(devices.Device_Screen(config.EFFECT))

for d in device_list:
    d.connect()

def update(y):
    for d in device_list:
        d.update(y)

def stop():
    for d in device_list:
        d.disconnect()
