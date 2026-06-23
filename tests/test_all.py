import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from unirun.core.detector import detect
from unirun.config import load_config, reset_config


class TestDetector(unittest.TestCase):
    def test_detect_windows_exe(self):
        self.assertEqual(detect("setup.exe"), "windows")

    def test_detect_windows_msi(self):
        self.assertEqual(detect("installer.msi"), "windows")

    def test_detect_android_apk(self):
        self.assertEqual(detect("game.apk"), "android")

    def test_detect_appimage(self):
        self.assertEqual(detect("app.AppImage"), "appimage")

    def test_detect_web_http(self):
        self.assertEqual(detect("http://example.com"), "web")

    def test_detect_web_https(self):
        self.assertEqual(detect("https://example.com"), "web")

    def test_detect_xdg_pdf(self):
        self.assertEqual(detect("doc.pdf"), "xdg")

    def test_detect_xdg_txt(self):
        self.assertEqual(detect("note.txt"), "xdg")

    def test_detect_xdg_png(self):
        self.assertEqual(detect("image.png"), "xdg")

    def test_detect_xdg_mp4(self):
        self.assertEqual(detect("video.mp4"), "xdg")

    def test_detect_xdg_mp3(self):
        self.assertEqual(detect("song.mp3"), "xdg")

    def test_detect_native(self):
        self.assertEqual(detect("some_script.sh"), "native")

    def test_detect_native_no_ext(self):
        self.assertEqual(detect("Makefile"), "native")


class TestConfig(unittest.TestCase):
    def setUp(self):
        reset_config()

    def test_default_config(self):
        cfg = load_config()
        self.assertIn("search_dirs", cfg._data)
        self.assertIn("history_file", cfg._data)

    def test_config_path_expansion(self):
        cfg = load_config()
        history = cfg.get("history_file")
        self.assertIn("~", history)


class TestSearch(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        # Create some test files
        for f in ["hello.txt", "world.txt", "test.py", "README.md"]:
            path = os.path.join(self.tmpdir.name, f)
            with open(path, "w") as fh:
                fh.write("test")

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_find_exact_file(self):
        from unirun.core.search import find_file
        # Temporarily override search dirs
        import unirun.core.search as search_mod
        original = search_mod.get_search_dirs
        search_mod.get_search_dirs = lambda: [self.tmpdir.name]
        result = find_file("hello.txt")
        search_mod.get_search_dirs = original
        self.assertIsNotNone(result)
        self.assertTrue(result.endswith("hello.txt"))

    def test_fuzzy_find(self):
        from unirun.core.search import fuzzy_find
        import unirun.core.search as search_mod
        original = search_mod.get_search_dirs
        search_mod.get_search_dirs = lambda: [self.tmpdir.name]
        result = fuzzy_find("hello", max_results=1)
        search_mod.get_search_dirs = original
        self.assertIsNotNone(result)
        if isinstance(result, list):
            self.assertTrue(any("hello" in r for r in result))
        else:
            self.assertIn("hello", result)


if __name__ == "__main__":
    unittest.main()
