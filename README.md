# HomeBeats

Audio Visualization software compatible with E1.31/SACN with a focus on expandability

## Quick Start

To see this in action first time, follow this steps:

1) Clone the repository
2) Change to repository directory
3) Install the requirements by using `pip install -r requirements.txt`
4) Run the code using `python visualization.py`
5) The script will, by default, display the animation in the terminal.

## Advanced

### Command Line Arguments

* `--config-file path_to_file.yaml` - set a configuration file to use
* `--config-override '{\"config_entry_to_override\":value}'` - set overrides for the config file in JSON format. Remember to escape the double quotes and wrap the JSON in single quotes.
* `--list-inputs` - list input devices and exit immediately

### HASS.Agent Configuration

You can configure HASS.Agent to Enable the audio visualization through Home Assistant by creating the following two commands:

1) `python c:/PATH/TO/REPOSITORY/visualization.py --config-file c:/PATH/TO/REPOSITORY/config.yaml`
2) `C:\Users\Matheus\Repos\github\HomeBeats\stop.ps1` NOTE: For this to work, you need to [Enable Powershell scripts](#foo).

You can also configure additional commands for different audio sources for example by using command overrides in the command line:

`python c:/PATH/TO/REPOSITORY/visualization.py --config-file c:/PATH/TO/REPOSITORY/config.yaml --config-override '{\\\"input_device_index\\\":1}'`

### Enabling Powershell scripts

To enable stop.ps1 to be executed, you need to allow powershell scripts by running the following command in an administrator powershell instance:
`Set-ExecutionPolicy -ExecutionPolicy Unrestricted`
Note: Enabling powershell scripts can put your machine at risk according to the official Microsoft documentation: https:/go.microsoft.com/fwlink/?LinkID=135170. Use this at your own risk!




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
input_device_index: 0

devices: # [Optional]
  dmx: # [Optional] E1.31 or SACN protocol device
    - device: my_dmx_device # [Mandatory] The name of your device
      ip: 192.168.1.154 # [Mandatory] The IP address of the device
      leds: 48 # [Mandatory] Number of LEDs
      universe: 2 # [Mandatory] The universe to which the device is listening
      multicast: false # [Optional] Whether to use multicast or not
```


