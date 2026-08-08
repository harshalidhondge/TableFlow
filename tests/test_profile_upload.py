import unittest

from routes.auth import is_allowed_image


class ProfileUploadTests(unittest.TestCase):
    def test_allows_common_image_types(self):
        self.assertTrue(is_allowed_image("photo.jpg"))
        self.assertTrue(is_allowed_image("photo.png"))
        self.assertTrue(is_allowed_image("photo.jpeg"))

    def test_rejects_unsafe_extensions(self):
        self.assertFalse(is_allowed_image("photo.exe"))
        self.assertFalse(is_allowed_image("script.php"))


if __name__ == "__main__":
    unittest.main()
