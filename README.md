# generic-camera-control

Script to handle camera actions

```
$ camera_control.py -h

usage: camera_control.py [-h] [-v] [-d] [--call-preset CALL_PRESET] [--apply-settings APPLY_SETTINGS] [--params PARAMS] --ip IP --model MODEL [--proxy PROXY]

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Set verbosity to DEBUG (default: False)
  -d, --dry-run         Avoid requesting and set verbosity to DEBUG (default: False)
  --call-preset CALL_PRESET
                        Action to call a particular preset. Examples: 1 | R00 | 1,24 (default: None)
  --apply-settings APPLY_SETTINGS
                        Action to apply settings on a camera. Example: pan=-1053&tilt=-1219&zoom=2689&ae.brightness=0 (default: None)
  --params PARAMS       Extra url params. Example: a=b&c=d (default: None)
  --ip IP               Camera ip. Example: 1.2.3.4 (default: None)
  --model MODEL         Camera model in this list [sony-generic, panasonic-generic, canon-generic] (default: None)
  --proxy PROXY         Proxy replace base uri. Example: https://proxy/12354/camera/ (default: None)
```