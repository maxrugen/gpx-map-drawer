# GPX Map Drawer

This script generates a minimalist map image from a GPX file containing route data of a cycling or running track.

## Usage

1. Make sure you have Python installed on your system.

2. Install the required dependencies using pip3:

    ```
    pip3 install -r requirements.txt
    ```

3. Run the script `gpx-map-drawer.py`:

    ```
    python3 gpx-map-drawer.py
    ```

4. Follow the prompts to enter the full path to the GPX file you want to use.

5. The script will generate a PNG map image based on the GPX data, with the same filename as the input GPX file.

## Customization

You can customize the appearance of the map by modifying the following values directly in the `gpx-map-drawer.py` script:

- **Line Width:** Modify the `linewidth` parameter in the `plot_route` function to adjust the thickness of the route line.
  
- **Line Color:** Modify the `color` parameter in the `plt.plot` function to change the color of the route line. You can use hexadecimal color codes or named colors.

- **Background Color:** Modify the `set_facecolor` function to change the background color of the map. You can use hexadecimal color codes or named colors.

## Required Libraries

- [gpxpy](https://pypi.org/project/gpxpy/): Python library for parsing GPX files.
- [matplotlib](https://matplotlib.org/): Python library for creating static, animated, and interactive visualizations in Python.

## Dependencies

The dependencies for this project are listed in the `requirements.txt` file. You can install them using pip:

```
pip3 install -r requirements.txt
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.