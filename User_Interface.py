# User Interface

import os
import music_index
from music_index import create_index
from datetime import datetime

def validate_date(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m")
        return True
    except ValueError:
        return False


def main():
    music_library_dir = input("Enter your music library: ")
    while not os.path.isdir(music_library_dir):
        print("Invalid directory. Please enter a valid path to your music library.")
        music_library_dir = input("Enter your music library: ")

    output_dir = input("Enter output directory: ")

    start_date = input("Enter start date (YYYY-MM): ")
    while not validate_date(start_date):
        print("Invalid date format. Please enter the start date in YYYY-MM format.")
        start_date = input("Enter start date (YYYY-MM): ")

    end_date = input("Enter end date (YYYY-MM): ")
    while not validate_date(end_date):
        print("Invalid date format. Please enter the end date in YYYY-MM format.")
        end_date = input("Enter end date (YYYY-MM): ")

    music_index = create_index(music_library_dir)
    print(f"Writing playlist for range {start_date} to {end_date}...")
    music_index.write_playlist(output_dir, start_date, end_date)
    print("Playlist created successfully!")

if __name__ == "__main__":
    main()
