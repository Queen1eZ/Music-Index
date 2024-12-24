
import pytest
from os import makedirs
from os.path import join
from unittest.mock import patch
import music_index
from music_index import MusicIndex, Album, Track, get_album_from_folder


class TestTracks():


    def test_track_copy_to_new_location_no_prefix(self):
        with patch('shutil.copy') as mock_copy:
            track_path = join('root', 'music', 'artist', 'album', 'test.m4p')
            test_track = Track('test.m4p', track_path)

            # Call your function that uses shutil.copy
            test_track.copy_track_to_new_directory('my_new_dir')

            # Assert that shutil.copy was called with the correct arguments
            mock_copy.assert_called_once_with(track_path,
                                              join('my_new_dir', 'test.m4p'))

    def test_track_copy_to_new_location_with_prefix(self):
        with patch('shutil.copy') as mock_copy:
            track_path = join('root', 'music', 'artist', 'album', 'test.m4p')
            test_track = Track('test.m4p', track_path)

            # Call your function that uses shutil.copy
            test_track.copy_track_to_new_directory('my_new_dir', 'foo')

            # Assert that shutil.copy was called with the correct arguments
            mock_copy.assert_called_once_with(track_path,
                                              join('my_new_dir', 'footest.m4p'))

class TestAlbum():
    def test_create_album(self):
        pass

    def test_write_to_new_dir(self):
        pass



class TestMusicIndex():

    def test_add_new_album(self):
        test_music_index = MusicIndex()
        sample_album = Album()
        sample_album.artist = "Some Artist"
        sample_album.release_date = "2021-03"
        sample_album.album_name = "Album1"

        test_music_index.add_album(sample_album)

        assert test_music_index.num_elements == 1

    def test_get_album(self):
        test_music_index = MusicIndex()
        sample_album = Album()
        sample_album.artist = "Some Artist"
        sample_album.release_date = "2021-03"
        sample_album.album_name = "Album1"

        test_music_index.add_album(sample_album)

        assert test_music_index.num_elements == 1

        album_list = test_music_index.get_albums("2021-03")

        assert album_list is not None
        assert len(album_list) == 1
        assert album_list[0].release_date == "2021-03"


    def test_add_many_albums_single_release(self):
        test_music_index = MusicIndex()
        album1 = Album()
        album1.artist = "Some Artist"
        album1.release_date = "2021-03"
        album1.album_name = "Album1"

        album2 = Album()
        album2.artist = "Artist2"
        album2.release_date = "2021-03"
        album2.album_name = "AlbumByArtist2"

        test_music_index.add_album(album1)
        test_music_index.add_album(album2)

        assert test_music_index.num_elements == 1

        album_list = test_music_index.get_albums("2021-03")

        assert album_list is not None
        assert len(album_list) == 2
        for album in album_list:
            assert album.release_date == "2021-03"

    def test_add_many_albums_multiple_release(self):
        test_music_index = MusicIndex()
        album1 = Album()
        album1.artist = "Some Artist"
        album1.release_date = "2021-03"
        album1.album_name = "Album1"

        album2 = Album()
        album2.artist = "Artist2"
        album2.release_date = "2021-03"
        album2.album_name = "AlbumByArtist2"

        album3 = Album()
        album3.artist = "Artist3"
        album3.release_date = "2023-12"
        album3.album_name = "AlbumByArtist3"

        test_music_index.add_album(album1)
        test_music_index.add_album(album2)
        test_music_index.add_album(album3)

        assert test_music_index.num_elements == 2

        album_list = test_music_index.get_albums("2021-03")

        assert album_list is not None
        assert len(album_list) == 2
        for album in album_list:
            assert album.release_date == "2021-03"

        album_list = test_music_index.get_albums("2023-12")

        assert album_list is not None
        assert len(album_list) == 1
        for album in album_list:
            assert album.release_date == "2023-12"

    # @patch('music_index.makedirs')
    def test_write_playlist(self, mocker):
        mocker.patch('music_index.makedirs')

        mocker.patch('music_index.Album.write_to_new_dir')


        # mocker.patch('os.makedirs')

        test_music_index = MusicIndex()
        album1 = Album()
        album1.artist = "Some Artist"
        album1.release_date = "2021-03"
        album1.album_name = "Album1"

        album2 = Album()
        album2.artist = "Artist2"
        album2.release_date = "2021-03"
        album2.album_name = "AlbumByArtist2"

        album3 = Album()
        album3.artist = "Artist3"
        album3.release_date = "2023-12"
        album3.album_name = "AlbumByArtist3"

        test_music_index.add_album(album1)
        test_music_index.add_album(album2)
        test_music_index.add_album(album3)


        test_music_index.write_playlist("MyPlaylist")

        music_index.makedirs.assert_called_once_with(join('MyPlaylist','Music 1900-01 through 2025-01'), exist_ok =True)
        music_index.Album.write_to_new_dir.assert_called_with(join('MyPlaylist', 'Music 1900-01 through 2025-01'))
        assert music_index.Album.write_to_new_dir.call_count == 3


    @patch('music_index.Track.copy_track_to_new_directory')
    def test_write_playlist(self, mock_copy_function):
        ## When
        track_path = join('root', 'music', 'artist', 'album', 'test.m4p')
        test_track = Track('test.m4p', track_path)
        test_album = Album('Bjork', '1999-05', 'Iceland', [test_track])

        ## Then
        test_album.write_to_new_dir('adrienne')

        mock_copy_function.assert_called_once_with('adrienne', '1999-05_Bjork_Iceland_')

    def test_write_playlist_in_range(self, mocker):
        ## Mock so these don't actually *do* anything
        mocker.patch('music_index.makedirs')
        mocker.patch('music_index.Album.write_to_new_dir')

        ## Set up
        test_music_index = MusicIndex()
        album1 = Album()
        album1.artist = "Some Artist"
        album1.release_date = "1999-03"
        album1.album_name = "Album1"

        album2 = Album()
        album2.artist = "Artist2"
        album2.release_date = "2010-03"
        album2.album_name = "AlbumByArtist2"

        album3 = Album()
        album3.artist = "Artist3"
        album3.release_date = "2023-12"
        album3.album_name = "AlbumByArtist3"

        test_music_index.add_album(album1)
        test_music_index.add_album(album2)
        test_music_index.add_album(album3)

        start_date = '2000-01'
        end_date = '2020-01'
        test_music_index.write_playlist("MyPlaylist", start_date, end_date)

        music_index.makedirs.assert_called_once_with(join('MyPlaylist', 'Music 2000-01 through 2020-01'), exist_ok =True)
        music_index.Album.write_to_new_dir.assert_called_with(join('MyPlaylist', 'Music 2000-01 through 2020-01'))
        assert music_index.Album.write_to_new_dir.call_count == 1


class TestMisc():
    def test_get_release_date(self):
        pass

    def test_get_album_from_folder(self, mocker):
        ## Mock so these don't actually *do* anything
        mocker.patch('music_index.listdir')
        ## If listdir is called, return this fake list of "tracks"
        music_index.listdir.return_value = ['track1', 'track2', 'details.txt']
        mocker.patch('music_index.isfile')
        mocker.patch('music_index.get_release_date')
        ## Don't actually open up and read the details.txt file, just return something to test
        music_index.get_release_date.return_value = '2005-04'

        new_album = get_album_from_folder('album', 'folder', 'artist')

        assert new_album.release_date == '2005-04'
        assert new_album.artist == 'artist'
        assert new_album.album_name == 'album'
        assert len(new_album.tracks) == 2


    def test_get_albums(self, mocker):
        ## Mock so these don't actually *do* anything
        mocker.patch('music_index.listdir')
        music_index.listdir.return_value = ['Artist1', 'Artist2', 'Artist3']
        mocker.patch('music_index.isdir')
        music_index.isdir.return_value = True
        ## Mock so these don't actually *do* anything
        mocker.patch('music_index.get_albums_for_artist')
        music_index.get_albums_for_artist.return_value = []

        albums = music_index.get_albums('My Music')

        assert music_index.get_albums_for_artist.call_count == 3 ## 1 call for each Artist

    def test_create_index(self, mocker):
        ## Mock so these don't actually *do* anything
        mocker.patch('music_index.get_albums')

        album1 = Album()
        album1.artist = "Some Artist"
        album1.release_date = "2021-03"
        album1.album_name = "Album1"

        album2 = Album()
        album2.artist = "Artist2"
        album2.release_date = "2021-03"
        album2.album_name = "AlbumByArtist2"

        album3 = Album()
        album3.artist = "Artist3"
        album3.release_date = "2023-12"
        album3.album_name = "AlbumByArtist3"

        ## Mock the albums that are returned
        music_index.get_albums.return_value = [album1, album2, album3]

        new_index = music_index.create_index('My Music')

        assert new_index.num_elements == 2
        assert new_index.key_exists('2023-12')
        assert new_index.key_exists('2021-03')
        assert len(new_index.get('2021-03')) == 2
