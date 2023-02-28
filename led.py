
'''def get_property_if_exists(dictionary, property, default = None):
    if property in dictionary:
        return dictionary[property]
    else:
        return default

device_list = [] 
if "devices" in config.config_dict:
    if "dmx" in config.config_dict["devices"]:
        for d in config.config_dict["devices"]["dmx"]:
            ip = d["ip"]
            name = d["device"]
            leds = d["leds"]
            universe = d["universe"]
            multicast = get_property_if_exists(d, "multicast", default = False)
            effect = get_property_if_exists(d, "effect", default = config.EFFECT)
            device_list.append(devices.Device_DMX(leds, effect, name, ip, universe, multicast))
 

if config.DISPLAY_PIXELS:
    device_list.append(devices.Device_Screen(config.EFFECT))'''

class Outputs:
    def __init__(self, devices):
        self.devices = devices
    def connect(self):
        for d in self.devices:
            d.connect()

    def update(self, y):
        for d in self.devices:
            d.update(y)

    def stop(self):
        for d in self.devices:
            d.disconnect()
