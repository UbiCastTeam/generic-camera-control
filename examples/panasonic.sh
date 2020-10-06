#!/bin/bash
set -e

# call preset
curl "http://${IP}/cgi-bin/aw_ptz?cmd=%23R00&res=1"

#preset 1 = R00
#preset 2 = R01
#preset 3 = R02
#preset 3 = R03