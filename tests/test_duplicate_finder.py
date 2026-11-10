import tempfile
import unittest
from pathlib import Path
from dev_utils.duplicate_finder import find_duplicate_files

class DuplicateFinderTests(unittest.TestCase):
    def test_finds_duplicates_recursively(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "one.txt").write_text("duplicate", encoding="utf-8")
            nested = root / "nested"
            nested.mkdir()
            (nested / "two.txt").write_text("duplicate", encoding="utf-8")
            (root / "different.txt").write_text("other", encoding="utf-8")
            groups = find_duplicate_files(root)
            self.assertEqual(len(groups), 1)
            self.assertEqual({p.name for p in groups[0]}, {"one.txt", "two.txt"})

    def test_non_recursive_mode(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "a").write_text("same", encoding="utf-8")
            (root / "b").write_text("same", encoding="utf-8")
            nested = root / "nested"
            nested.mkdir()
            (nested / "c").write_text("same", encoding="utf-8")
            groups = find_duplicate_files(root, recursive=False)
            self.assertEqual(len(groups), 1)
            self.assertEqual(len(groups[0]), 2)

    def test_no_duplicates(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "a").write_text("one", encoding="utf-8")
            (root / "b").write_text("two", encoding="utf-8")
            self.assertEqual(find_duplicate_files(root), [])

    def test_empty_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            self.assertEqual(find_duplicate_files(directory), [])

    def test_non_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            file_path = Path(directory) / "file"
            file_path.touch()
            with self.assertRaises(NotADirectoryError):
                find_duplicate_files(file_path)

if __name__ == "__main__":
    unittest.main()
