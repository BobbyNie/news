# 2026-07-08 stock source review

- Data window: 2026-07-06 12:03 ~ 2026-07-08 12:03（澳门时间 UTC+8）.
- Date basis: `python3 scripts/report_date.py` returned `REPORT_DATE=20260708`; no `automation_trigger_info.triggeredAt` variable was exposed.

## New or elevated sources

- AP market close pages: timely index levels and AI-stock selloff explanation for 2026-07-07.
- Reuters-syndicated market updates: useful cross-check for global stocks, oil and chip pressure where available.
- HKEX Nexchip prospectus: official source for price range, listing timetable and offering risk.
- SEC S-1 filings for Jersey Mike's and Scribe Therapeutics: official IPO pipeline evidence.
- Vertex official release: official M&A source for the Crinetics event.
- Rivian offering coverage: material financing event; company filing/source should be checked again if available.

## IPO source decisions

- Keep Nexchip as the most concrete HK upcoming IPO because HKEX filing has terms and July 8 price-setting deadline.
- Keep Jersey Mike's and Scribe as U.S. pipeline candidates from SEC S-1 filings; both lack final price range/share count.
- Treat SK hynix U.S. listing/offering as media-reported unless official filing is found.

## Access gaps

- Some Bloomberg/WSJ/FT pages were snippet-only or paywalled.
- Real-time quotes are from major-media close summaries and market pages; no trading advice is made.
