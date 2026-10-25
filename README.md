# ScoreWatch – WSSL test MVP

Mobile-first scoreboard for WSSL GotSport event 56299, initially based on a user-provided match export. Scores in `data.json` are snapshots, **not a live feed**. Both numeric scores are treated as FINAL for this MVP. Notifications are deferred.

## Publish with GitHub Pages

1. Upload the entire folder contents, including `.github/workflows`, to the `main` branch of `D0rsey/scorewatch`.
2. In repository **Settings → Pages → Build and deployment**, select **GitHub Actions** as the source.
3. The **Publish ScoreWatch** workflow should deploy to `https://d0rsey.github.io/scorewatch/`.
4. Allow a few minutes for the first deployment. The URL is not live until GitHub reports success.

## Refresh imported scores

Download the team schedule spreadsheet from GotSport, then locally run:

```bash
python update_from_export.py /path/to/export.xlsx
```

Review `changes.json`, then commit `data.json`, `data.js`, and `changes.json` to the repository. Publishing occurs automatically on push. No GotSport scraping is included.

## Limitations

- Team browser has verified data only for the initial U11 Girls division. Other divisions can be entered manually in this preview but are not centrally synchronized.
- Favorites live in browser localStorage; different browsers/devices have separate favorites.
- Scheduled repository checks only validate existing data; they do not download updated scores or standings.
- No push or SMS notifications.
- `PARKING-LOT.md` tracks tournament support and deferred features.
