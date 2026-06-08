from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
READER = ROOT / "assets" / "report-reader.js"


class ReportReaderAssetTest(unittest.TestCase):
    def test_reader_asset_contains_google_tts_contract_and_fallback(self) -> None:
        script = READER.read_text(encoding="utf-8")

        required = [
            "https://texttospeech.googleapis.com/v1/text:synthesize?key=",
            "newsReportReader.googleTtsApiKey",
            "newsReportReader.googleTtsVoice",
            "localStorage",
            'querySelectorAll("section")',
            "cmn-CN",
            "cmn-CN-Wavenet-A",
            "audioEncoding: \"MP3\"",
            "4500",
            "speechSynthesis",
            "SpeechSynthesisUtterance",
            "zh-CN",
            "data-google-tts-key",
            "data-google-tts-save",
            "data-google-tts-clear",
        ]

        for text in required:
            with self.subTest(text=text):
                self.assertIn(text, script)


if __name__ == "__main__":
    unittest.main()
