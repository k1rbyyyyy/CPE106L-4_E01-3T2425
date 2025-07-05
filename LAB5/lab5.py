import sqlite3

# Get artist name from user input
artist_name = input("Enter the artist name: ")

# Connect to the chinook.db database
conn = sqlite3.connect('chinook.db')

# Create a cursor to execute SQL commands
cur = conn.cursor()

# Query: List tracks by the input artist longer than 5 minutes, with album and artist info
cur.execute("""
    SELECT tracks.Name AS TrackName, albums.Title AS AlbumTitle, artists.Name AS ArtistName
    FROM tracks
    JOIN albums ON tracks.AlbumId = albums.AlbumId
    JOIN artists ON albums.ArtistId = artists.ArtistId
    WHERE tracks.Milliseconds > 300000
      AND artists.Name = ?
    ORDER BY albums.Title, tracks.Name
""", (artist_name,))

results = cur.fetchall()

for row in results:
    print(f"Track: {row[0]}, Album: {row[1]}, Artist: {row[2]}")

# Close the connection
conn.close()