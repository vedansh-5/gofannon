# docs/open_notify_space/open_notify_space.md
# google_search

The `open_notify_space` API queries the Open Notify Space API and returns the current latitude and longitude of the International Space Station (ISS).

## Parameters

*   None, this is a simple REST GET call that returns the location.

## Example Usage

```python  
from gofannon.open_notify_space.iss_locator import IssLocator  
  
current_location_iss = IssLocator()
current_location = current_location_iss.fn()
# Returns one of two strings:
# "According to OpenNotify.org, the International Space Station can be found at (lat, long) (x,y)"
# or
# "The ISS endpoint returned an error. No location for the ISS can be determined"
print(current_location)

```