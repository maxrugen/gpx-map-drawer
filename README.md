# GPX Map Drawer

This script generates a minimalist map image from a GPX file containing route data of a cycling or running track. It supports multi-track/multi-segment GPX files, batch processing, and outputs in PNG or SVG format.

## Usage

### Interactive Mode

1. Make sure you have Python installed on your system.

2. Install the required dependencies using pip3:

    ```
    pip3 install -r requirements.txt
    ```

3. Run the script without arguments to enter interactive mode:

    ```
    python3 gpx-map-drawer.py
    ```

4. Follow the prompts to enter the full path to the GPX file and a route color.

5. The script will generate a PNG map image based on the GPX data, with the same filename as the input GPX file.

### CLI Mode

You can also use command-line arguments to skip the interactive prompts:

```
python3 gpx-map-drawer.py --input route.gpx
```

#### Available Options

| Flag | Short | Description | Default |
|------|-------|-------------|---------|
| `--input` | `-i` | Path to a GPX file or a directory of GPX files | *(interactive prompt)* |
| `--output` | `-o` | Output image file path (ignored in batch mode) | Same as input with `.png` extension |
| `--color` | `-c` | Hex color code for the route line | `#ffffff` |
| `--linewidth` | `-l` | Width of the route line | `10` |
| `--dpi` | `-d` | DPI of the output image | `350` |
| `--format` | `-f` | Output format: `png` or `svg` | `png` |

#### Examples

Generate a PNG with a custom color:

```
python3 gpx-map-drawer.py -i route.gpx -c "#fc5266"
```

Generate an SVG:

```
python3 gpx-map-drawer.py -i route.gpx -f svg
```

Batch process all GPX files in a directory:

```
python3 gpx-map-drawer.py -i ./gpx-files/
```

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