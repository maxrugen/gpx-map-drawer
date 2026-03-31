import argparse
import re
import gpxpy
import matplotlib.pyplot as plt
import os
import shlex


def is_valid_hex_color(color):
    return bool(re.match(r'^#(?:[0-9a-fA-F]{3}){1,2}$', color))


# Function to plot route from GPX file
def plot_route(gpx_file, output_file=None, color='#ffffff', linewidth=10, dpi=350):
    # Parse GPX file
    with open(gpx_file, 'r') as file:
        gpx = gpxpy.parse(file)

    # Extract route data
    route = gpx.tracks[0].segments[0].points
    lats = [point.latitude for point in route]
    lons = [point.longitude for point in route]

    # Calculate latitude and longitude ranges
    lat_range = max(lats) - min(lats)
    lon_range = max(lons) - min(lons)

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

    # Plot the route
    plt.figure(figsize=(fig_width, fig_height))  # Set figure size
    plt.plot(lons, lats, color=color, linewidth=linewidth)  # Set color and line width

    # Customize appearance
    plt.axis('off')  # Turn off axis
    plt.gca().set_facecolor('none')  # Set background color to transparent

    # Determine output filename
    if output_file is None:
        filename = os.path.splitext(gpx_file)[0]
        output_file = f"{filename}.png"

    # Save the image
    plt.savefig(output_file, bbox_inches='tight', pad_inches=0, dpi=dpi, transparent=True)
    plt.close()

    # Return the output filename
    return output_file


def interactive_mode():
    # Ask user for input GPX file
    input_file = input("Enter the full path to the GPX file: ")

    # Split the input string into a list of arguments
    input_file_args = shlex.split(input_file)

    # Join the arguments back into a single string with spaces in the filename
    input_file = " ".join(input_file_args)

    # Ask for color
    color_input = input("Enter a hex color code for the route (default: #ffffff): ").strip()
    if color_input and is_valid_hex_color(color_input):
        color = color_input
    else:
        if color_input:
            print(f"Invalid hex color '{color_input}', using default #ffffff.")
        color = '#ffffff'

    # Check if the file exists
    if os.path.isfile(input_file):
        if not input_file.lower().endswith('.gpx'):
            print("Error: The file is not a GPX file. Please provide a file with a .gpx extension.")
        else:
            try:
                output_file = plot_route(input_file, color=color)
                print("Map image generated successfully and saved as " + output_file + "!")
            except Exception as e:
                print(f"Error: Failed to parse the GPX file. Please ensure it is a valid GPX file.\n{e}")
    else:
        print("Error: Input file not found.")


def main():
    parser = argparse.ArgumentParser(description="Generate a minimalist map image from a GPX file.")
    parser.add_argument('--input', '-i', type=str, help="Path to the input GPX file.")
    parser.add_argument('--output', '-o', type=str, help="Path to the output image file (default: same as input with .png extension).")
    parser.add_argument('--color', '-c', type=str, default='#ffffff', help="Hex color code for the route line (default: #ffffff).")
    parser.add_argument('--linewidth', '-l', type=float, default=10, help="Width of the route line (default: 10).")
    parser.add_argument('--dpi', '-d', type=int, default=350, help="DPI of the output image (default: 350).")

    args = parser.parse_args()

    # If no input file provided via CLI, fall back to interactive mode
    if args.input is None:
        interactive_mode()
        return

    input_file = args.input

    if not os.path.isfile(input_file):
        print("Error: Input file not found.")
        return

    if not input_file.lower().endswith('.gpx'):
        print("Error: The file is not a GPX file. Please provide a file with a .gpx extension.")
        return

    if not is_valid_hex_color(args.color):
        print(f"Error: Invalid hex color '{args.color}'.")
        return

    try:
        output_file = plot_route(input_file, output_file=args.output, color=args.color, linewidth=args.linewidth, dpi=args.dpi)
        print("Map image generated successfully and saved as " + output_file + "!")
    except Exception as e:
        print(f"Error: Failed to parse the GPX file. Please ensure it is a valid GPX file.\n{e}")


if __name__ == '__main__':
    main()