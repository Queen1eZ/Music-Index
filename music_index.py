from os import walk, listdir, makedirs
from os.path import join, isfile, isdir, dirname
import shutil
from datetime import datetime
from hashtable import Hashtable, KeyValuePair

class Track:
    """
    A Track represents an audio file, with a name (including the extension, such as "01 Track.m4p") and a
    filename that includes a relative path to the file.
    """
    def __init__(self, name, path):
        self.name = name
        """The track name from the file, something like '04 Okay.m4p'"""
        self.file_with_path = path
        """The file path to the audio file for this track """

    def copy_track_to_new_directory(self, new_dir, prefix=''):
        """
        Copy the track audio file to the specified new location, with the specified prefix
        :param new_dir: The directory to write to
        :param prefix: A prefix (defaults to '') to write before the track name
        :return: Nothing, but writes a new file "<new_dir>/<prefix><track.name>"
        """
        if not isdir(new_dir):
            makedirs(new_dir)

        new_path = join(new_dir, prefix + self.name)
        shutil.copy(self.file_with_path, new_path)
        print(f"Copied {self.file_with_path} to {new_path}")
        return

class Album:
    """
    An album that has an Artist, AlbumName, ReleaseDate, and a set of Tracks.
    """
    def __init__(self, artist: str = '', release_date: str = '', album_name: str = '', tracks: [Track] = []):
        """
        Instantiates an Album.
        :param artist: The Artist
        :param release_date: The release date, "YYYY-MM" format
        :param album_name: The name of the album
        :param tracks: A list of Tracks on the album
        """
        self.artist = artist
        '''The Artist who produced this album'''
        self.release_date = release_date
        '''The Year/Month of the release of this album; YYYY-MM'''
        self.album_name = album_name
        '''Name of the Album'''
        self.tracks = tracks
        '''A list of the tracks on this album'''

    def __repr__(self):
        return f'"{self.album_name}" by ~{self.artist}~ released on [{self.release_date}]'

    def write_to_new_dir(self, new_dir):
        """
        Writes all the tracks for this album to the new specified directory.
        Writes all tracks to the new directory with the format "<release_date>_<artist>_<album_name>_<track_name>"
        :param new_dir: The new directory to write this albums tracks to.
        :return: None
        """
        if not isdir(new_dir):
            makedirs(new_dir)

        prefix = f"{self.release_date}_{self.artist}_{self.album_name}_"
        for track in self.tracks:
            track.copy_track_to_new_directory(new_dir, prefix)
            print(f"Copied {track.name} to {new_dir} with prefix {prefix}")

        return


class MusicIndex(Hashtable):
    """
    A data structure that stores Albums efficiently, keyed by the release date.
    A MusicIndex extends a Hashtable, with a KVP where the Key is the ReleaseDate
    and the value is a list of Albums.
    """
    def __init__(self):
        super().__init__()

    def add_album(self, album: Album):
        """
        Adds an album to this MusicIndex, keyed by release_date.
        :param album: An album to put into the MusicIndex
        :return:
        """
        ## If there are already albums stored with the same release date as the new album,
        ##   get that list of albums
        ## Add this new album to the list
        ## Otherwise, put this album into a new list and store in the index.
        ## Hint: Be sure to use your Hashtable.get() and Hashtable.put() functions!
        try:
            albums = self.get(album.release_date)
        except KeyError:
            albums = []

        albums.append(album)
        self.put(album.release_date, albums)

    def get_albums(self, release_date: str) -> [Album]:
        """
        Returns all the albums with the specified release_date
        :param release_date: A release date of form "YYYY-MM"
        :return:
        """
        ## Return the list of albums released on the provided release date
        ## Input should be of the form YYYY-MM
        try:
            return self.get(release_date)
        except KeyError:
            return []

    def print(self):
        """
        Helper function to printout all the albums stored in this MusicIndex.
        :return:
        """
        for index, item in enumerate(self):
            print(f"Key: {item.key}")
            music_set = item.value
            music_set.print()

    def write_playlist(self, base_dir, start_date: str = "1900-01", end_date: str = "2025-01"):
        """
        Write out a playlist to a specified location. The playlist will be written to a folder
        of the format "Music {start_date} through {end_date}" in the base_dir folder.
        :param base_dir: Where the new playlist folder should be created
        :param start_date: The start date (inclusive) of albums to write, in YYYY-MM format
        :param end_date: The end date (inclusive) of albums to write, in YYYY-MM format
        :return:
        """
        playlist_path = join(base_dir, f'Music {start_date} through {end_date}')

        # if not isdir(playlist_path):
        makedirs(playlist_path, exist_ok=True)

        start_date_obj = datetime.strptime(start_date, "%Y-%m")
        end_date_obj = datetime.strptime(end_date, "%Y-%m")

        for item in self:
            release_date = datetime.strptime(item.key, "%Y-%m")
            if start_date_obj <= release_date <= end_date_obj:
                # Write all albums in the current bucket to the new playlist directory
                for album in item.value:
                    album.write_to_new_dir(playlist_path)
                    print(f"Written album '{album.album_name}' to {playlist_path}")

        return


def get_release_date_from_file(fileptr):
    """
    Given an open file pointer, read the first line and return it.
    :param fileptr: A fileptr to the open file (details.txt) that has the release date for an album.
    :return: The first line of the file, which should be the release date in YYYY-MM format.
    """
    for line in fileptr:
        return line


def get_release_date(artist, album, music_library_folder='') -> str:
    """
    Gets the release date for a given artist and album.
    This is primarily a wrapper function: by using this function rather than the
    "get_release_date_from_file" function directly, this function can choose to query
    Spotify rather than read the file.
    :param artist: The artist who released the album
    :param album: The album name
    :param music_library_folder: The folder that holds the library/files-- defaults to ''
    :return: The release date for this album, in YYYY-MM format.
    """
    ## For the core implementation, this function should open a file to the relevant
    ##`details.txt' file for the release date.
    ## If you are doing the Spotify option this function should query Spotify (probably with
    ## some helper functions)
    album_folder = join(music_library_folder, artist, album)
    date_path = join(album_folder, 'details.txt')

    try:
        with open(date_path, 'r') as f:
            return get_release_date_from_file(f)
    except FileNotFoundError:
        return "Unknown"
    #return get_release_date_from_file(open(join(album_folder, "details.txt"))) ## <-- Better check this is right! Might not be ;)


def get_album_from_folder(album_name, album_folder, artist) -> Album:
    """
    Creates and returns an Album from the specified parameters.
    :param album_name: The album name
    :param album_folder: The folder holding all the album track files
    :param artist: The artist who released this album
    :return: An Album containing all the Tracks
    """
    track_files = [f for f in listdir(album_folder) if isfile(join(album_folder, f)) and f != 'details.txt']
    tracks = [Track(name=f, path=join(album_folder, f)) for f in track_files]
    music_library_folder = dirname(dirname(album_folder))
    release_date = get_release_date(artist, album_name, music_library_folder)
    return Album(artist, release_date, album_name, tracks)


def get_albums_for_artist(artist, artist_folder) -> [Album]:
    """
    Returns all the albums for a given artist with data in the given artist_folder
    :param artist: The Artist to load Albums for
    :param artist_folder: The folder where the artist's album live
    :return: A list of Albums
    """
    albums = []
    album_folders = [f for f in listdir(artist_folder) if isdir(join(artist_folder, f))]
    for album_name in album_folders:
        album_folder_path = join(artist_folder, album_name)
        try:
            album = get_album_from_folder(album_name, album_folder_path, artist)
            albums.append(album)
        except Exception as e:
            print(f"Error processing album '{album_name}' for artist '{artist}': {e}")

    return albums


def get_albums(starting_dir: str) -> [Album]:
    """
    Creates albums from the specified starting location. Assumes that
    the files and folders are as specified in the "MyMusic" example ("MyMusic" is starting_dir,
    which holds Artists; each Artist dir holders Albums; each Album dir holds "details.txt" and track files).
    :param starting_dir: The directory where all the Artist/Album/Track files are stored.
    :return: A list of Albums
    """
    albums = []
    artist_folders = [f for f in listdir(starting_dir) if isdir(join(starting_dir, f))]
    for artist_name in artist_folders:
        artist_folder_path = join(starting_dir, artist_name)
        try:
            artist_albums = get_albums_for_artist(artist_name, artist_folder_path)
            albums.extend(artist_albums)
        except Exception as e:
            print(e)

    return albums


def create_index(music_library_dir: str) -> MusicIndex:
    """
    Starts in the directory that holds the Music Library and returns a
    MusicIndex, populated with all the albums in that library.
    :param music_library_dir: The folder that holds the music files (Artist/Album/Track)
    :return: A MusicIndex with all the albums from the Music Library directory
    """
    music_index = MusicIndex()
    albums = get_albums(music_library_dir)
    for album in albums:
        music_index.add_album(album)
    return music_index
