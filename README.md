# generic-camera-control

Script to handle camera actions

```
camera_control.py -h
camera_control.py --model sony-generic --ip 1.2.3.4 --action preset --params "PresetCall=1,24&test=test" [--proxy "https://mm.ubicast.eu/.../audiovideo/"] [-h] [--help]
-h, --help
    This help
-v, --verbose
    Verbose mode
-d,  --dry-run
    No request enable debug mode
--action
    Action to apply on camera default is preset
--params
    url params a=b&c=d&e=f
--model
    choice in ['sony-generic', 'canon-generic']
--ip
    camera ip
--proxy
    url prefix to make requests
```