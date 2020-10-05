#!/bin/bash
### SONY cameras
set -e
# call preset
curl http://${CAMERA_IP}/command/presetposition.cgi?PresetCall=1,24