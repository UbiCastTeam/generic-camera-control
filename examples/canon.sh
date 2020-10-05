#! /bin/bash
###Canon camera preset 1
set -e
# Get Session ID
session_id=`curl -k  '${PROXY}/${CAMERA_IP}/-wvhttp-01-/open.cgi' | awk -F's:=' '{print $2}'`
# Request camera control
curl -k "${PROXY}/${CAMERA_IP}/-wvhttp-01-/claim.cgi?s=${session_id}"
# Call preset 1
curl -k "${PROXY}/${CAMERA_IP}/-wvhttp-01-/control.cgi?s=${session_id}&pan=-1053&tilt=-1219&zoom=2689&ae.brightness=0&focus=auto&shade=off&shade.param=0&wb=auto"
# Give back control to others
curl -k "${PROXY}/${CAMERA_IP}/-wvhttp-01-/yield.cgi?s=${session_id}"