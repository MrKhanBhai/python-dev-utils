import tempfile
import unittest
from pathlib import Path
from dev_utils.cli import main

class CliTests(unittest.TestCase):
    def test_hash_command(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "data.txt"
            path.write_text("hello", encoding="utf-8")
            self.assertEqual(main(["hash", str(path)]), 0)

    def test_compare_exit_codes(self):
        with tempfile.TemporaryDirectory() as directory:
            first, second = Path(directory) / "a", Path(directory) / "b"
            first.write_text("same", encoding="utf-8")
            second.write_text("same", encoding="utf-8")
            self.assertEqual(main(["compare", str(first), str(second)]), 0)
            second.write_text("diff", encoding="utf-8")
            self.assertEqual(main(["compare", str(first), str(second)]), 1)

    def test_manifest_create_and_verify(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "data"
            root.mkdir()
            (root / "hello.txt").write_text("hello", encoding="utf-8")
            manifest = Path(directory) / "manifest.json"
            self.assertEqual(main(["manifest", str(root), str(manifest)]), 0)
            self.assertEqual(main(["verify", str(root), str(manifest)]), 0)
            (root / "hello.txt").write_text("changed", encoding="utf-8")
            self.assertEqual(main(["verify", str(root), str(manifest)]), 1)

if __name__ == "__main__":
    unittest.main()
