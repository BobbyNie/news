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
        macau = utc_late.astimezone(ZoneInfo("Asia/Macau"))
        self.assertEqual(macau.date(), date(2026, 5, 27))
        self.assertEqual(module.report_yyyymmdd(macau), "20260527")
        self.assertEqual(module.report_iso(macau), "2026-05-27")

    def test_cron_utc_23_maps_to_macau_next_morning(self):
        module = load_module()
        triggered = "2026-05-27T23:02:33.581Z"
        dt = module.macau_datetime(triggered)
        self.assertEqual(module.report_yyyymmdd(dt), "20260528")
        self.assertEqual(module.format_generated_at(dt), "2026-05-28 07:02（澳门时间）")
        start, end = module.collection_window_from_trigger(dt)
        self.assertEqual(start, "2026-05-26 07:02")
        self.assertEqual(end, "2026-05-28 07:02")

    def test_backfill_uses_morning_trigger_on_report_day(self):
        module = load_module()
        report_day = date(2026, 5, 28)
        dt = module.resolve_trigger(report_day=report_day)
        self.assertEqual(module.report_yyyymmdd(dt), "20260528")
        start, end = module.collection_window_from_trigger(dt)
        self.assertEqual(end, "2026-05-28 07:00")


if __name__ == "__main__":
    unittest.main()
