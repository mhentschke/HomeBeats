"""Settings for audio reactive LED strip"""
import yaml
import devices
try:
    with open('config.yaml') as f:
        config_dict = yaml.safe_load(f)

        DISPLAY_FPS = config_dict["display_fps"]
        DISPLAY_PIXELS = config_dict["display_pixels"]
        MIC_RATE = config_dict["mic_rate"]
        FPS = config_dict["fps"]
        MIN_FREQUENCY = config_dict["min_frequency"]
        MAX_FREQUENCY = config_dict["max_frequency"]
        N_FFT_BINS = config_dict["n_fft_bins"]
        N_ROLLING_HISTORY = config_dict["n_rolling_history"]
        MIN_VOLUME_THRESHOLD = config_dict["min_volume_threshold"]
        EFFECT = config_dict["effect"]


        USE_GUI = False
except FileNotFoundError as e:
    print("Could not find the configuration file. Will load hardcoded defaults.")

def get_property_if_exists(dictionary, property, default = None):
    if property in dictionary:
        return dictionary[property]
    else:
        return default

class Config():
    def __init__(self, filepath):
        self.filepath = filepath
        self.load_from_file()

    def load_from_file(self):
        with open(self.filepath) as f:
            config_dict = yaml.safe_load(f)
        self.DISPLAY_FPS = config_dict["display_fps"]
        self.DISPLAY_PIXELS = config_dict["display_pixels"]
        self.MIC_RATE = config_dict["mic_rate"]
        self.FPS = config_dict["fps"]
        self.MIN_FREQUENCY = config_dict["min_frequency"]
        self.MAX_FREQUENCY = config_dict["max_frequency"]
        self.N_FFT_BINS = config_dict["n_fft_bins"]
        self.N_ROLLING_HISTORY = config_dict["n_rolling_history"]
        self.MIN_VOLUME_THRESHOLD = config_dict["min_volume_threshold"]
        self.EFFECT = config_dict["effect"]
        self.devices = [] 
        if "devices" in config_dict:
            if "dmx" in config_dict["devices"]:
                for d in config_dict["devices"]["dmx"]:
                    ip = d["ip"]
                    name = d["device"]
                    leds = d["leds"]
                    universe = d["universe"]
                    multicast = get_property_if_exists(d, "multicast", default = False)
                    effect = get_property_if_exists(d, "effect", default = self.EFFECT)
                    self.devices.append(devices.Device_DMX(leds, effect, name, self, ip, universe, multicast))
        if self.DISPLAY_PIXELS:
            self.devices.append(devices.Device_Screen(self.EFFECT, self))
    
    def unload(self):
        for d in self.devices:
            d.disconnect=()

    def reload(self, filepath = None):
        if filepath is not None:
            self.filepath = filepath
        self.unload()
        self.load_from_file()
    
    def save_to_file():
        raise(NotImplementedError)
        with open(self.filepath, "w") as f:
            config_dict = {}
            config_dict["display_fps"] = self.DISPLAY_FPS
            config_dict["display_pixels"] = self.DISPLAY_PIXELS
            config_dict["mic_rate"] = self.MIC_RATE
            config_dict["fps"] = self.FPS
            config_dict["min_frequency"] = self.MIN_FREQUENCY
            config_dict["max_frequency"] = self.MAX_FREQUENCY
            config_dict["n_fft_bins"] = self.N_FFT_BINS
            config_dict["n_rolling_history"] = self.N_ROLLING_HISTORY
            config_dict["min_volume_threshold"] = self.MIN_VOLUME_THRESHOLD
            config_dict["effect"] = self.EFFECT
            config_dict["devices"] = {}