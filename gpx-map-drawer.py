import gpxpy
import matplotlib.pyplot as plt
import os

# Function to plot route from GPX file
def plot_route(gpx_file):
    # Parse GPX file
    with open(gpx_file, 'r') as file:
        gpx = gpxpy.parse(file)

    # Extract route data
    route = gpx.tracks[0].segments[0].points
    lats = [point.latitude for point in route]
    lons = [point.longitude for point in route]

    # Plot the route
    # Set figure size
    plt.figure(figsize=(8, 6))
    # Set color and line width
    plt.plot(lons, lats, color='#fc5266', linewidth=15)

    # Customize appearance
    # Turn off axis
    plt.axis('off')
    # Set background color
    plt.gca().set_facecolor('#f5f5f5')

    # Get the filename without extension
    filename = os.path.splitext(gpx_file)[0]

    # Save the image with the same filename as the GPX file
    output_file = f"{filename}.png"
    plt.savefig(output_file, bbox_inches='tight', pad_inches=0, dpi=350)

    # Return the output filename
    return output_file

# Ask user for input GPX file
input_file = input("Enter the full path to the GPX file: ")

# Check if the file exists
if os.path.isfile(input_file):
    # Plot the route and get the output filename
    output_file = plot_route(input_file)
    print("Map image generated successfully and saved as " + output_file + "!")
else:
    print("Error: Input file not found.")