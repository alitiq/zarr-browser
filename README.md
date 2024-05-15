# Execute engine functions 

<h3> 1. Build the docker image </h3>

Then you can build the image passing the Token as an Argument. 
```bash
docker build -t "xarray_browser" .
```

### Use cli 
```bash
docker run --name xarray_browser --rm -v $(pwd):/app -v /home/daniel/projects/weather-forecast/data/:/app/data -p 8050:8050 xarray_browser:latest python3 /app/xarray_browser/app.py
```