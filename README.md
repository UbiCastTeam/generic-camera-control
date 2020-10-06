# generic-camera-control

Script to handle camera actions

```
camera_control.py -h
camera_control.py --model sony-generic --ip 1.2.3.4 [--call-preset 1,24 | --apply-settings "pan=-1053&tilt=-1219&zoom=2689&ae.brightness=0&focus=auto&shade=off&shade.param=0&wb=auto"] [--params "a=b&c=d"] [--proxy "https://mm.ubicast.eu/.../audiovideo/"] [-h] [--help]
-h, --help
    This help
-v, --verbose
    Verbose mode
-d,  --dry-run
    No request enable debug mode
--call-preset
    Action to call camera preset
--apply-settings
    Action to apply settings to a camera
--params
    url params a=b&c=d&e=f
--model
    choice in ['sony-generic', 'canon-generic']
--ip
    camera ip
--proxy
    url prefix to make requests
```