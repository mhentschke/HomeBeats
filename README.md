# HomeBeats

Audio Visualization software compatible with E1.31/SACN with a focus on expandability

## Quick Start

To see this in action first time, follow this steps:

1) Clone the repository
2) Change to repository directory
3) Install the requirements by using `pip install -r requirements.txt`
4) Run the code using `python visualization.py`
5) The script will, by default, display the animation in the terminal.


## Configuration

The configuration file `config.yaml` is intended to change the behavior and add different devices. It looks like this:
```yaml
display_fps: true # [Mandatory] Whether to display or not the FPS value
display_pixels: true # [Mandatory] Whether to display the animation in the terminal
mic_rate: 44100 # [Mandatory] Mic Sampling rate
fps: 60 # [Mandatory] Frames per second target for all devices
min_frequency: 30 # [Mandatory] Minimum frequency to be captured and displayed
max_frequency: 2000 # [Mandatory] Maximum frequency to be captured and displayed
n_fft_bins: 16 # [Mandatory] Number of FFT Bins to use
n_rolling_history: 2 # [Mandatory] Rolling History size
min_volume_threshold: 0.00001 # [Mandatory] Minimum volume that triggers animations
effect: spectrum # [Mandatory] Effect type

devices: # [Optional]
  dmx: # [Optional] E1.31 or SACN protocol device
    - device: my_dmx_device # [Mandatory] The name of your device
      ip: 192.168.1.154 # [Mandatory] The IP address of the device
      leds: 48 # [Mandatory] Number of LEDs
      universe: 2 # [Mandatory] The universe to which the device is listening
      multicast: false # [Optional] Whether to use multicast or not
```


