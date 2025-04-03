# docs/apod/apod_lookup.md

## apod_lookup
The `apod_lookup` tool queries NASA's Astronomy Picture of the Day (APOD) API and returns details about the daily space image, including its title, description, image URL, and source link.

## Function Constructor Parameters
Function fetches the APOD data and returns a structured dictionary:

```
{
    "title": "Astronomy Picture Title",
    "description": "A brief explanation of the APOD...",
    "image": "https://apod.nasa.gov/apod/image.jpg",
    "url": "https://apod.nasa.gov/apod/apOD20240403.html"
}
```

If an error occurs, it returns:
```
{
    "error": "Failed to fetch APOD data"
}
```

## API Parameters
No parameters are required; the tool fetches the latest APOD by default.

## Example Usage
```
from gofannon.apod.apod_lookup import ApodLookup

# Create an instance of the tool
apod_tool = ApodLookup()

# Fetch the latest APOD
result = apod_tool.fn()

# Print the title and description
print(f"Title: {result['title']}")
print(f"Description: {result['description']}")

# Access the APOD image
if "image" in result and result["image"]:
    print(f"View image: {result['image']}")
```

## Error Handling

The tool handles API errors gracefully by returning an error dictionary instead of raising exceptions, making it reliable for production use.

If the APOD API returns a non-200 status code, the tool will return:
```
{
    "error": "Failed to fetch APOD data"
}
```

