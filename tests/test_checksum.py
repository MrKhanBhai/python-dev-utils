import hashlib
import tempfile
import unittest
from pathlib import Path

from dev_utils.checksum import hash_bytes, hash_file, sha256_file


class ChecksumTests(unittest.TestCase):
    def test_sha256_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sample.txt"
            path.write_bytes(b"hello world")
            expected = hashlib.sha256(b"hello world").hexdigest()
            self.assertEqual(sha256_file(path), expected)

    def test_empty_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "empty.bin"
            path.write_bytes(b"")
            self.assertEqual(sha256_file(path), hashlib.sha256(b"").hexdigest())

    def test_binary_file(self):
        content = bytes(range(256))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "binary.bin"
            path.write_bytes(content)
            self.assertEqual(sha256_file(path), hashlib.sha256(content).hexdigest())

    def test_missing_file_raises(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(FileNotFoundError):
                sha256_file(Path(directory) / "missing.txt")

    def test_other_algorithms_and_chunk_sizes(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "data.bin"
            path.write_bytes(b"abcdef" * 100)
            expected = hashlib.sha512(path.read_bytes()).hexdigest()
            self.assertEqual(hash_file(path, "sha512", 7), expected)

    def test_hash_bytes(self):
        self.assertEqual(hash_bytes(b"hello"), hashlib.sha256(b"hello").hexdigest())

    def test_hash_bytes_rejects_non_bytes(self):
        with self.assertRaises(TypeError):
            hash_bytes("hello")

    def test_invalid_algorithm(self):
        with self.assertRaisesRegex(ValueError, "unsupported hash algorithm"):
            hash_bytes(b"hello", "not-a-real-algorithm")

    def test_invalid_file_algorithm(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "data"
            path.write_bytes(b"x")
            with self.assertRaisesRegex(ValueError, "unsupported hash algorithm"):
                hash_file(path, algorithm="not-a-real-algorithm")

    def test_invalid_chunk_sizes(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "data"
            path.write_bytes(b"x")
            for value in (0, -1, True, 1.5, "10"):
                with self.subTest(chunk_size=value):
                    with self.assertRaises(ValueError):
                        hash_file(path, chunk_size=value)

    def test_sha256_compatibility_helper(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "data"
            path.write_bytes(b"compatibility")
            self.assertEqual(sha256_file(path), hash_file(path, "sha256"))


if __name__ == "__main__":
    unittest.main()
