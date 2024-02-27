import gpxpy
import gpxpy.gpx
from datetime import datetime
import os
import glob

def split_gpx_by_day(input_gpx_file, output_directory):
    # Load the GPX file
    with open(input_gpx_file, 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)

    # Extract year and month from the file name
    file_name = os.path.basename(input_gpx_file)
    year, month = map(int, file_name.split('.')[0].split('-'))
    
    # Initialize a dictionary to hold data grouped by day
    daily_segments = {}

    # Helper function to process waypoints and track points
    def process_point(point, daily_segments):
        if point.time.year == year and point.time.month == month:
            day = point.time.strftime('%Y-%m-%d')
            if day not in daily_segments:
                daily_segments[day] = gpxpy.gpx.GPX()
            return day
        return None

    # Process waypoints
    for waypoint in gpx.waypoints:
        day = process_point(waypoint, daily_segments)
        if day:
            daily_segments[day].waypoints.append(waypoint)

    # Process tracks
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                day = process_point(point, daily_segments)
                if day:
                    # Check if we need to create a new track for this day
                    if not any(t for t in daily_segments[day].tracks if t.name == track.name):
                        new_track = gpxpy.gpx.GPXTrack(name=track.name)
                        daily_segments[day].tracks.append(new_track)
                        new_segment = gpxpy.gpx.GPXTrackSegment()
                        new_track.segments.append(new_segment)
                    else:
                        new_segment = daily_segments[day].tracks[-1].segments[-1]
                    new_segment.points.append(point)

    # Save files for each day
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for day, gpx_data in daily_segments.items():
        filename = os.path.join(output_directory, f"{day}.gpx")
        with open(filename, 'w') as out_file:
            out_file.write(gpx_data.to_xml())
        print(f"Saved {filename}")

def process_all_gpx_files_in_directory(directory_path, output_directory):
    for gpx_file in glob.glob(os.path.join(directory_path, '*.gpx')):
        split_gpx_by_day(gpx_file, output_directory)

# Usage:
# Set your directory path and output directory
directory_path = '.'  # Current directory
output_directory = './split_gpx'  # Modify as needed
process_all_gpx_files_in_directory(directory_path, output_directory)
