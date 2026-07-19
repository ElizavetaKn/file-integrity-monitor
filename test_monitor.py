import sys
import tempfile
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from file_integrity_monitor.monitor import build_baseline, compare_baseline


class FileIntegrityTests(unittest.TestCase):
    def test_detects_added_modified_deleted(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "a.txt").write_text("one", encoding="utf-8")
            (root / "b.txt").write_text("two", encoding="utf-8")
            baseline = build_baseline(root)

            (root / "a.txt").write_text("changed", encoding="utf-8")
            (root / "b.txt").unlink()
            (root / "c.txt").write_text("new", encoding="utf-8")

            current = build_baseline(root)
            report = compare_baseline(current, baseline)

            self.assertEqual(report["added"], ["c.txt"])
            self.assertEqual(report["modified"], ["a.txt"])
            self.assertEqual(report["deleted"], ["b.txt"])


if __name__ == "__main__":
    unittest.main()
