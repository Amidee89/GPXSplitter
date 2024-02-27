Arc for iOS doesn't really export daily GPX files as it says it does; as per its author, it will stop doing so at will and leave you with uncomplete data.
What actually works, though, are the monthly exports. So to extract the daily files from the monthly files, I made this small script.
It finds all GPX files with yyyy-mm.gpx format and splits them into yyyy-mm-dd.gpx filtering all elements by date.
Crude, but it works. 
