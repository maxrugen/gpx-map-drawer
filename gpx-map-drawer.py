import argparse
import glob
import math
import re
import gpxpy
import matplotlib.pyplot as plt
import os


def is_valid_hex_color(color):
    return bool(re.match(r'^#(?:[0-9a-fA-F]{3}){1,2}$', color))


# Function to plot route from GPX file
def plot_route(gpx_file, output_file=None, color='#ffffff', linewidth=10, dpi=350, fmt='png'):
    # Parse GPX file
    with open(gpx_file, 'r') as file:
        gpx = gpxpy.parse(file)

    # Extract route data from all tracks and segments
    lats = []
    lons = []
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                lats.append(point.latitude)
                lons.append(point.longitude)

    if not lats:
        raise ValueError("No track points found in the GPX file.")

    # Apply longitude correction factor for equal-area approximation
    mean_lat = math.radians(sum(lats) / len(lats))
    corrected_lons = [lon * math.cos(mean_lat) for lon in lons]

    # Calculate latitude and longitude ranges
    lat_range = max(lats) - min(lats)
    lon_range = max(corrected_lons) - min(corrected_lons)

    # Set figure size based on longer dimension, default to square if range is zero
    if lat_range == 0 or lon_range == 0:
        fig_width = 8
        fig_height = 8
    elif lat_range > lon_range:
        fig_width = 8
        fig_height = 8 * (lat_range / lon_range)
    else:
        fig_width = 8 * (lon_range / lat_range)
        fig_height = 8

    # Plot the route, connecting each track/segment
    plt.figure(figsize=(fig_width, fig_height))  # Set figure size

    for track in gpx.tracks:
        for segment in track.segments:
            seg_lats = [p.latitude for p in segment.points]
            seg_lons = [lon * math.cos(mean_lat) for lon in (p.longitude for p in segment.points)]
            plt.plot(seg_lons, seg_lats, color=color, linewidth=linewidth)

    # Customize appearance
    plt.axis('off')  # Turn off axis
    plt.gca().set_facecolor('none')  # Set background color to transparent

    # Determine output filename
    if output_file is None:
        filename = os.path.splitext(gpx_file)[0]
        output_file = f"{filename}.{fmt}"

    # Save the image
    plt.savefig(output_file, bbox_inches='tight', pad_inches=0, dpi=dpi, transparent=True, format=fmt)
    plt.close()

    # Return the output filename
    return output_file


def process_file(input_file, output_file=None, color='#ffffff', linewidth=10, dpi=350, fmt='png'):
    """Process a single GPX file and generate the map image."""
    if not os.path.isfile(input_file):
        print(f"Error: Input file not found: {input_file}")
        return

    if not input_file.lower().endswith('.gpx'):
        print(f"Error: The file is not a GPX file: {input_file}")
        return

    try:
        result = plot_route(input_file, output_file=output_file, color=color, linewidth=linewidth, dpi=dpi, fmt=fmt)
        print("Map image generated successfully and saved as " + result + "!")
    except Exception as e:
        print(f"Error: Failed to parse the GPX file. Please ensure it is a valid GPX file.\n{e}")


def interactive_mode():
    # Ask user for input GPX file
    input_file = input("Enter the full path to the GPX file: ").strip().strip("'\"")

    # Ask for color
    color_input = input("Enter a hex color code for the route (default: #ffffff): ").strip()
    if color_input and is_valid_hex_color(color_input):
        color = color_input
    else:
        if color_input:
            print(f"Invalid hex color '{color_input}', using default #ffffff.")
        color = '#ffffff'

    process_file(input_file, color=color)


def main():
    parser = argparse.ArgumentParser(description="Generate a minimalist map image from a GPX file.")
    parser.add_argument('--input', '-i', type=str, help="Path to the input GPX file or a directory of GPX files.")
    parser.add_argument('--output', '-o', type=str, help="Path to the output image file (default: same as input with .png extension). Ignored in batch mode.")
    parser.add_argument('--color', '-c', type=str, default='#ffffff', help="Hex color code for the route line (default: #ffffff).")
    parser.add_argument('--linewidth', '-l', type=float, default=10, help="Width of the route line (default: 10).")
    parser.add_argument('--dpi', '-d', type=int, default=350, help="DPI of the output image (default: 350).")
    parser.add_argument('--format', '-f', type=str, default='png', choices=['png', 'svg'], help="Output image format (default: png).")

    args = parser.parse_args()

    # If no input file provided via CLI, fall back to interactive mode
    if args.input is None:
        interactive_mode()
        return

    if not is_valid_hex_color(args.color):
        print(f"Error: Invalid hex color '{args.color}'.")
        return

    # Batch mode: if input is a directory, process all GPX files in it
    if os.path.isdir(args.input):
        gpx_files = sorted(glob.glob(os.path.join(args.input, '*.gpx')))
        if not gpx_files:
            print("Error: No GPX files found in the directory.")
            return
        for gpx_file in gpx_files:
            process_file(gpx_file, color=args.color, linewidth=args.linewidth, dpi=args.dpi, fmt=args.format)
        return

    process_file(args.input, output_file=args.output, color=args.color, linewidth=args.linewidth, dpi=args.dpi, fmt=args.format)


if __name__ == '__main__':
    main()