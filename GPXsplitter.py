import gpxpy
import gpxpy.gpx
from datetime import datetime, timedelta
import os
import glob

def get_date_range(gpx):
    dates = [point.time.date() for track in gpx.tracks for segment in track.segments for point in segment.points]
    if gpx.waypoints:
        dates.extend([wp.time.date() for wp in gpx.waypoints if wp.time])
    return min(dates), max(dates)

def split_gpx_by_day(input_gpx_file, output_directory):
    with open(input_gpx_file, 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)

    start_date, end_date = get_date_range(gpx)
    delta = timedelta(days=1)

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    current_date = start_date
    while current_date <= end_date:
        day_str = current_date.strftime('%Y-%m-%d')
        daily_gpx = gpxpy.gpx.GPX()

        for track in gpx.tracks:
            day_track = gpxpy.gpx.GPXTrack(name=track.name)
            day_track.type = track.type  # Copy metadata
            track_added = False

            for segment in track.segments:
                day_segment = gpxpy.gpx.GPXTrackSegment()

                for point in segment.points:
                    if point.time.date() == current_date:
                        day_segment.points.append(point)
                        track_added = True
                
                if day_segment.points:
                    day_track.segments.append(day_segment)
            
            if track_added:
                daily_gpx.tracks.append(day_track)

        for waypoint in gpx.waypoints:
            if waypoint.time and waypoint.time.date() == current_date:
                daily_gpx.waypoints.append(waypoint)

        if daily_gpx.tracks or daily_gpx.waypoints:
            filename = os.path.join(output_directory, f"{day_str}.gpx")
            with open(filename, 'w') as out_file:
                out_file.write(daily_gpx.to_xml())
            print(f"Saved {filename}")

        current_date += delta

def process_all_gpx_files_in_directory(directory_path, output_directory):
    for gpx_file in glob.glob(os.path.join(directory_path, '*.gpx')):
        split_gpx_by_day(gpx_file, output_directory)
        
directory_path = '.'  
output_directory = './split_gpx' 
process_all_gpx_files_in_directory(directory_path, output_directory)
