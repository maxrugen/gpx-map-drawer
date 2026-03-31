import gpxpy
import matplotlib.pyplot as plt
import os
import shlex

# Function to plot route from GPX file
def plot_route(gpx_file):
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

    # Set figure size based on longer dimension
    if lat_range > lon_range:
        fig_width = 8
        fig_height = 8 * (lat_range / lon_range)
    else:
        fig_width = 8 * (lon_range / lat_range)
        fig_height = 8

    # Plot the route
    plt.figure(figsize=(fig_width, fig_height))  # Set figure size
    plt.plot(lons, lats, color='#ffffff', linewidth=10)  # Set color and line width

    # Customize appearance
    plt.axis('off')  # Turn off axis
    plt.gca().set_facecolor('none')  # Set background color to transparent

    # Get the filename without extension
    filename = os.path.splitext(gpx_file)[0]

    # Save the image with the same filename as the GPX file
    output_file = f"{filename}.png"
    plt.savefig(output_file, bbox_inches='tight', pad_inches=0, dpi=350, transparent=True)

    # Return the output filename
    return output_file

# Ask user for input GPX file
input_file = input("Enter the full path to the GPX file: ")

# Split the input string into a list of arguments
input_file_args = shlex.split(input_file)

# Join the arguments back into a single string with spaces in the filename
input_file = " ".join(input_file_args)

# Check if the file exists
if os.path.isfile(input_file):
    if not input_file.lower().endswith('.gpx'):
        print("Error: The file is not a GPX file. Please provide a file with a .gpx extension.")
    else:
        try:
            output_file = plot_route(input_file)
            print("Map image generated successfully and saved as " + output_file + "!")
        except Exception as e:
            print(f"Error: Failed to parse the GPX file. Please ensure it is a valid GPX file.\n{e}")
else:
    print("Error: Input file not found.")