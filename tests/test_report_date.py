import importlib.util
import pathlib
import sys
import unittest
from datetime import date, datetime
from zoneinfo import ZoneInfo


ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "report_date.py"


def load_module():
    spec = importlib.util.spec_from_file_location("report_date", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class ReportDateTests(unittest.TestCase):
    def test_macau_date_differs_from_utc_near_midnight(self):
        module = load_module()
        utc_late = datetime(2026, 5, 26, 23, 30, tzinfo=ZoneInfo("UTC"))
        macau = utc_late.astimezone(ZoneInfo("Asia/Macau")).date()
        self.assertEqual(macau, date(2026, 5, 27))
        self.assertEqual(module.report_yyyymmdd(macau), "20260527")
        self.assertEqual(module.report_iso(macau), "2026-05-27")
        self.assertEqual(module.report_month(macau), "2026-05")

    def test_collection_window_uses_macau_evening_bounds(self):
        module = load_module()
        report_day = date(2026, 5, 27)
        start, end = module.collection_window(report_day)
        self.assertEqual(start, datetime(2026, 5, 25, 22, 0, tzinfo=ZoneInfo("Asia/Macau")))
        self.assertEqual(end, datetime(2026, 5, 27, 22, 0, tzinfo=ZoneInfo("Asia/Macau")))
        self.assertIn("2026-05-25 22:00", module.format_window(report_day))
        self.assertIn("2026-05-27 22:00", module.format_window(report_day))


if __name__ == "__main__":
    unittest.main()
