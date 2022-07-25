import unittest
from ytdl.main import main
import os
import shutil
import toml

download_folder = "Arcade Fire"

class DownloadFromTOMLTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        main(["list", "tests/resources/arcade_fire.toml"])
    
    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(download_folder)
    
    def test_two_title_playlists_creates_two_files(self):
        created_files = os.listdir(download_folder)
        self.assertEqual(2, len(created_files))

    def test_two_title_playlists_creates_mp3_files(self):
        created_files = os.listdir(download_folder)
        for filename in created_files:
            self.assertTrue(filename.endswith(".mp3"))
    
    def test_two_title_playlists_names_files_correctly(self):
        remove_ext_mp3 = lambda name: name.replace(".mp3", '')
        created_files = sorted(list(map(remove_ext_mp3, os.listdir(download_folder))))
        self.assertListEqual(["Intervention", "No Cars Go"], created_files)

class DownloadSingleUrlTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        main(["single", "https://www.youtube.com/watch?v=TeQqn3olPn0", "ade"])
    
    @classmethod
    def tearDownClass(cls):
        os.remove("ade.mp3")
    
    def test_single_url_creates_single_file(self):
        files = os.listdir()
        self.assertIn("ade.mp3", files)

class FormatPlaylistToTOMLTest(unittest.TestCase):
    expected_toml_file = "weezer_white_album.toml"

    def assertAllIn(self, subset, container):
        for elem in subset:
            self.assertIn(elem, container)

    @classmethod
    def setUpClass(cls):
        main(["format_playlist", "https://www.youtube.com/playlist?list=PLg4pQIhMIijXQI-NrFBToDVxmNB_d86wI", "Weezer", "weezer_white_album"])

    @classmethod
    def tearDownClass(cls):
        os.remove(FormatPlaylistToTOMLTest.expected_toml_file)
    
    def test_toml_file_created(self):
        self.assertIn(FormatPlaylistToTOMLTest.expected_toml_file, os.listdir())
    
    def test_correct_folder_prefix(self):
        config = toml.load(FormatPlaylistToTOMLTest.expected_toml_file)
        self.assertEqual(["Weezer"], list(config.keys()))

    def test_correct_video_names(self):
        config = toml.load(FormatPlaylistToTOMLTest.expected_toml_file)
        self.assertAllIn(["Weezer - California Kids", "Weezer - King Of The World"], config["Weezer"].keys())