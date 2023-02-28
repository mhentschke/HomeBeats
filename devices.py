import numpy as np
import dsp
import sacn
import os
from scipy.ndimage.filters import gaussian_filter1d
#import config

def memoize(function):
    """Provides a decorator for memoizing functions"""
    from functools import wraps
    memo = {}

    @wraps(function)
    def wrapper(*args):
        if args in memo:
            return memo[args]
        else:
            rv = function(*args)
            memo[args] = rv
            return rv
    return wrapper


@memoize
def _normalized_linspace(size):
    return np.linspace(0, 1, size)

def interpolate(y, new_length):
    """Intelligently resizes the array by linearly interpolating the values

    Parameters
    ----------
    y : np.array
        Array that should be resized

    new_length : int
        The length of the new interpolated array

    Returns
    -------
    z : np.array
        New array with length of new_length that contains the interpolated
        values of y.
    """
    if len(y) == new_length:
        return y
    x_old = _normalized_linspace(len(y))
    x_new = _normalized_linspace(new_length)
    z = np.interp(x_new, x_old, y)
    return z

class Device():
    def __init__(self, leds, effect, name, config):
        self.name = name
        self.leds = leds
        self.effect = effect
        self.last_data = None
        self.config = config
        if self.effect == "spectrum":
            self.calculate_effect = self._effect_spectrum
        elif self.effect == "scroll":
            self.calculate_effect = self._effect_scroll
        elif self.effect == "energy":
            self.calculate_effect = self._effect_energy

    def connect(self):
        print("Device", self.name, "Connected")
    def disconnect(self):
        print("Disconnecting Device", self.name)
    def validate_data(self, data):
        if data.shape[1] != self.leds*3:
            raise(ValueError("Number of leds incorrect. Hardware has " + str(self.leds*3) + "LEDs and data sent was " + str(data.shape)))
        return(True) # todo: remove this and fix the array comparison on the bottom
        repeated_data = True
        print(data)
        return(data != self.last_data)
    def _effect_spectrum(self, y):
        if self.effect == "spectrum":
            y = np.copy(interpolate(y, self.leds // 2))
            try: self._prev_spectrum # This being undefined means the effect has not been initialized
            except AttributeError:
                self._prev_spectrum = np.tile(0.01, self.leds // 2)
                self.r_filt = dsp.ExpFilter(np.tile(0.01, self.leds // 2),
                                        alpha_decay=0.2, alpha_rise=0.99)
                self.g_filt = dsp.ExpFilter(np.tile(0.01, self.leds // 2),
                                        alpha_decay=0.05, alpha_rise=0.3)
                self.b_filt = dsp.ExpFilter(np.tile(0.01, self.leds // 2),
                                        alpha_decay=0.1, alpha_rise=0.5)
                self.common_mode = dsp.ExpFilter(np.tile(0.01, self.leds // 2),
                                        alpha_decay=0.99, alpha_rise=0.01)
            self.common_mode.update(y)
            diff = y - self._prev_spectrum
            
            self._prev_spectrum = np.copy(y)
            # Color channel mappings
            r = self.r_filt.update(y - self.common_mode.value)
            g = np.abs(diff)
            b = self.b_filt.update(np.copy(y))
            # Mirror the color channels for symmetric output
            if self.leds % 2 == 0:
                r = np.concatenate((r[::-1], r))
                g = np.concatenate((g[::-1], g))
                b = np.concatenate((b[::-1], b))
            else:
                r = np.concatenate((r[::-1], r[0:1], r))
                g = np.concatenate((g[::-1], g[0:1], g))
                b = np.concatenate((b[::-1], b[0:1], b))
            output = np.array([r, g,b]) * 255
            return output
        else:
            raise(Exception("Unexpected behavior. Device has effect " + self.effect + " but effect called was spectrum"))
    def _effect_scroll(self, y):
        """Effect that originates in the center and scrolls outwards"""
        try: self._p # This being undefined means the effect has not been initialized
        except AttributeError:
            self._p = np.tile(1.0, (3, self.leds // 2))
            self._gain = dsp.ExpFilter(np.tile(0.01, self.config.N_FFT_BINS),
                    alpha_decay=0.001, alpha_rise=0.99)
        y = y**2.0
        self._gain.update(y)
        y /= self._gain.value
        y *= 255.0
        r = int(np.max(y[:len(y) // 3]))
        g = int(np.max(y[len(y) // 3: 2 * len(y) // 3]))
        b = int(np.max(y[2 * len(y) // 3:]))
        # Scrolling effect window
        self._p[:, 1:] = self._p[:, :-1]
        self._p *= 0.98
        self._p = gaussian_filter1d(self._p, sigma=0.2)
        # Create new color originating at the center
        self._p[0, 0] = r
        self._p[1, 0] = g
        self._p[2, 0] = b
        # Update the LED strip
        return np.concatenate((self._p[:, ::-1], self._p), axis=1)
    def _effect_energy(self, y):
        try: self._p # This being undefined means the effect has not been initialized
        except AttributeError:
            self._p = np.tile(1.0, (3, self.leds // 2))
            self._gain = dsp.ExpFilter(np.tile(0.01, self.config.N_FFT_BINS),
                    alpha_decay=0.001, alpha_rise=0.99)
            self._p_filt = dsp.ExpFilter(np.tile(1, (3, self.leds // 2)),
                       alpha_decay=0.1, alpha_rise=0.99)
        y = np.copy(y)
        self._gain.update(y)
        y /= self._gain.value
        # Scale by the width of the LED strip
        y *= float((self.leds // 2) - 1)
        # Map color channels according to energy in the different freq bands
        scale = 0.9
        r = int(np.mean(y[:len(y) // 3]**scale))
        g = int(np.mean(y[len(y) // 3: 2 * len(y) // 3]**scale))
        b = int(np.mean(y[2 * len(y) // 3:]**scale))
        # Assign color to different frequency regions
        self._p[0, :r] = 255.0
        self._p[0, r:] = 0.0
        self._p[1, :g] = 255.0
        self._p[1, g:] = 0.0
        self._p[2, :b] = 255.0
        self._p[2, b:] = 0.0
        self._p_filt.update(self._p)
        self._p = np.round(self._p_filt.value)
        # Apply substantial blur to smooth the edges
        self._p[0, :] = gaussian_filter1d(self._p[0, :], sigma=4.0)
        self._p[1, :] = gaussian_filter1d(self._p[1, :], sigma=4.0)
        self._p[2, :] = gaussian_filter1d(self._p[2, :], sigma=4.0)
        # Set the new pixel value
        return np.concatenate((self._p[:, ::-1], self._p), axis=1)
    

class Device_DMX(Device):
    def __init__(self, leds, effect, name, config, ip, universe, multicast):
        self.ip = ip
        self.multicast = multicast
        self.universe = universe
        Device.__init__(self, leds, effect, name, config)
    def connect(self):
        if self.multicast:
            self.sender = sacn.sACNsender("self.ip")    
        self.sender = sacn.sACNsender()
        self.sender.start()
        self.sender.activate_output(self.universe)
        self.sender[self.universe].destination = self.ip
        Device.connect(self)
    def disconnect(self):
        self.sender.stop()
    def update(self, y):
        #todo: check shape of the input and adapt accordingly
        data = self.calculate_effect(y)
        data = self._reshape(data)
        try:
            if self.validate_data(data):
                prepped_data = tuple(np.clip(data[0].astype(int), 0, 255).tolist())
                self.sender[self.universe].dmx_data = prepped_data
        except ValueError as exception:
            print("Exception occurred while trying to update the LEDs:", exception)
    def _reshape(self, data):
        return(np.reshape(data, (1, -1), order='F'))

class Device_Screen(Device):
    def __init__(self, effect, config):
        leds = os.get_terminal_size()[0]
        name = "Terminal"
        Device.__init__(self, leds, effect, name, config)
    def update(self, y):
        data = self.calculate_effect(y)
        string = ""
        data = np.clip(data, 0, 255)
        for p in data.T:
            string += "\u001b[48;2;{};{};{}m{}\u001b[0m".format(int(p[0]), int(p[1]), int(p[2]), " ")
        print(string + "\r", end="")
    
    