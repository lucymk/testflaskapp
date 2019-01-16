import pytest

from .handle_files import get_extension, get_filename_from_hash, get_hash_from_filename


class TestGetFilenameFromHash(object):
    def test_extension_supplied_with_period(self):
        assert get_filename_from_hash("abc-123", ".jpg") == "abc-123.jpg"

    def test_extension_supplied_without_period(self):
        assert get_filename_from_hash("def-456", "png") == "def-456.png"


class TestGetHashFromFilename(object):
    def test_name_is_returned(self):
        assert get_hash_from_filename("abcdef.jpg") == "abcdef"


class TestGetExtension(object):
    def test_extension_is_returned(self):
        assert get_extension("test.jpg") == "jpg"

    def test_only_one_extension_is_returned(self):
        assert get_extension("what.gif.jpg") == "jpg"
