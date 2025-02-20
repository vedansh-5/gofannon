# docs/open_notify_space/open_notify_space.md

## iss_locator
The `open_notify_space` API queries the Open Notify Space API and returns the current latitude and longitude of the International Space Station (ISS).

## Parameters

*   None, this is a simple REST GET call that returns the location.

## Example Usage

```python  
from gofannon.open_notify_space.iss_locator import IssLocator  
  
current_location_iss = IssLocator(json=False)
current_location = current_location_iss.fn()
#
# With json=False, Returns one of two strings:
#   "According to OpenNotify.org, the International Space Station can be found at (lat, long) (x,y)"
#   or
#   "The ISS endpoint returned an error. No location for the ISS can be determined"
#
# With json=True, the following strings:
#   "{
#        "message": "success",
#       "timestamp": 1739999640,
#       "iss_position": {"longitude": "-11.6885", "latitude": "-50.0654"},
#   }" 
#   or
#   "{
#       "message": "failure",
#       "error": "Error: The ISS endpoint returned an error. No location for the ISS can be determined",
#   }"
print(current_location)

```