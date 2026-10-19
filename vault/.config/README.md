# ~/school/.config

Settings for the automations in ~/.claude/bin. Claude fills these in during setup. Never commit or share them.

- canvas.json: your Canvas access token and school URL. Made from canvas.json.example (copy it, paste the token in). Needed by canvas_watch, assess_watch and weak_notes. Until it exists they print "not configured yet" and stop.
- bells.json: bell schedule, no school days and the A/B day rule for school_clock.py. Default is Wakeland HS 2026-27. Edit it if the schedule changes.
