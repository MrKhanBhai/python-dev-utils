
import hashlib
import tempfile
import unittest
from pathlib import Path

from dev_utils.checksum import sha256_file


class ChecksumTests(unittest.TestCase):
    def test_sha256_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sample.txt"
            path.write_bytes(b"hello world")

            expected = hashlib.sha256(b"hello world").hexdigest()
            self.assertEqual(sha256_file(str(path)), expected)


if __name__ == "__main__":
    unittest.main()
