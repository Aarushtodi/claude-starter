---
type: project
status: active
domain: school
updated: 2026-01-01
---
# Phone Setup

> Goal: the phone switches itself by time of day. School hours show only school apps, homework time shows study apps, night shows almost nothing, and the rest of the time is normal. Social apps live in the App Library, off every home page. About 20 minutes on the phone. Based on Aarush's setup, cut down to what a student needs.

## Current state
(Phase 8c fills this in: phone type, his bedtime, which apps go on which page. Nothing built yet.)

## His answers (Claude fills in during the Phase 8c interview)
- Phone: iPhone or Android:
- Bedtime on school nights (Sun to Thu) / weekend bedtime or none / wake time:
- Blocked sites and apps:
- Apps needed during school:
- Apps hidden during school:

## The four modes

| Mode | When | What shows | Notifications |
|---|---|---|---|
| School | Mon to Fri, 9:00 to 16:30 (the Wakeland bell schedule in `~/school/.config/bells.json`) | Canvas, Calendar, Gmail, Claude, Notes, Camera, Phone | Only parents and the Claude app. Social apps silent |
| Study | Sun to Thu, 19:00 to 21:00, or turned on by hand | Claude, Notes, Canvas, Calendar, Spotify | Only parents |
| Sleep | His bedtime to wake time (same as the laptop block) | Nearly empty: Clock and Claude | Only parents |
| Free | No mode on | Everything normal, social apps only in the App Library | Normal |

A and B days do not matter here. A phone cannot compute them, so School just runs every weekday 9:00 to 16:30. On a no school day, turn School off for the day (Control Center, tap the mode). The laptop side (`school_clock.py`) does know the real A/B days and no school dates.

## One home page per mode (iPhone)

Dock on every page: Phone, Messages, Claude, Camera.

- **School page:** Google Calendar widget, then Canvas, Gmail, Claude, Notes, Calculator, Google Drive.
- **Study page:** Claude, Notes (or Obsidian), Canvas, Calendar, Clock timer, Spotify.
- **Sleep page:** Clock (alarm) and Claude. Nothing to scroll to.
- **Free page (the only page when no mode is on):** Camera, Photos, Maps, Spotify, Weather, plus whatever else he likes. TikTok, Instagram, YouTube and Snapchat only in the App Library.

## iPhone, in order (about 20 minutes)

1. Send Claude a screenshot of Settings > Focus (the list of Focus modes). Claude says which to rename or delete.
2. Settings > Focus. Tap the + at the top right, pick **Custom**. Name it **School**, pick a blue color and the graduation cap icon, tap Next, Customize Focus.
3. **People**: tap People > Silence Notifications From > Add People, add his parents. **Apps**: Apps > Allow Notifications From > Add Apps, add Canvas, Google Calendar, Gmail, Claude. Tap Done.
4. Still in School: tap **Add Schedule** > **Time**. Pick Mon to Fri, From 9:00 AM to 4:30 PM. Turn it on.
5. In School, tap **Choose** under Home Screen, pick the School page (see step 9 if the pages do not exist yet).
6. Repeat steps 2 to 5 for **Study** (green, book icon). Schedule: Sun to Thu, 7:00 PM to 9:00 PM. Allow only parents and Claude.
7. **Sleep**: Settings > Focus > Sleep (it already exists). Set the schedule to his bedtime and wake time from the interview. Allow only parents.
8. Delete Focus modes he never uses (Fitness, Personal, Reduce Interruptions) by tapping them, scrolling down, Delete Focus.
9. Home screen pages: press and hold an empty spot on the home screen, tap the dots at the bottom. Check the pages he wants for the mode, uncheck the rest. Make one page per mode as in the table, then in each Focus's Home Screen setting pick that page. Social apps: press and hold the app, Remove App, **Remove from Home Screen** (never Delete App). Settings > Home Screen & App Library > new apps go to **App Library Only**.
10. Notifications: Settings > Notifications > Instagram > turn off Banners, or Scheduled Summary. TikTok and YouTube: Allow Notifications off.
11. Shortcuts automation (grayscale at night): open Shortcuts > Automation > + > **Sleep** > Is Turned On > Run Immediately > add action **Set Color Filters** > On. Make the same one for Is Turned Off > Set Color Filters > Off. Phone goes black and white at bedtime, which makes it boring.
12. Shortcuts automation (homework start): Automation > + > **Time of Day** > 7:00 PM > Weekly, Sun to Thu > Run Immediately > add actions **Set Focus** (Study, On) and **Open App** (Claude). Claude opens ready to drill him.
13. Lock screens (30 seconds each, optional): press and hold the lock screen, tap +, pick a plain color, tap the Focus button at the bottom and pick the mode so it switches with it.
14. Test: Control Center > Focus > tap School, confirm the page changes. Tap it off. Send Claude a screenshot of the School page.

Then Claude does the Screen Time part (bedtime Downtime and App Limits) from BOOTSTRAP Phase 8c.

## Android, in order (about 20 minutes)

Android has no separate home page per mode. Use one clean home screen (school apps on page 1, everything else in the app drawer) and let the modes do the quiet.

1. Send Claude a screenshot of Settings > Digital Wellbeing.
2. **Android 15 or newer (Pixel, many others):** Settings > Notifications > Do Not Disturb > Modes, or Settings > Modes. Tap **Add mode**, make **School**, **Study**, **Sleep**. For each: Set a schedule (School Mon to Fri 9:00 to 16:30, Study Sun to Thu 19:00 to 21:00, Sleep = his bedtime to wake). Under People allow parents only. Under Apps allow Canvas, Gmail, Calendar, Claude. Turn on **Display options > Grayscale** for Sleep.
3. **Samsung:** Settings > Modes and Routines > Modes > add School, Study, Sleep, same rules, then Routines for the time windows.
4. **Older Android:** Settings > Digital Wellbeing > Focus mode. Pick Instagram, TikTok, YouTube, Snapchat as distracting apps. Tap **Set a schedule**, Mon to Fri, 9:00 to 16:30. Then Bedtime mode (next section).
5. Home screen: long press, move Canvas, Calendar, Gmail, Claude, Notes, Camera, Phone to page 1. Move social apps off the home screen (long press, Remove, not Uninstall).
6. Notifications: Settings > Notifications > App notifications > Instagram, TikTok, YouTube off.
7. Test: pull down the quick settings, turn School on, check the social apps are paused and gray. Send Claude a screenshot.

## Rules

- No social apps on the School or Study page, ever. If one shows up there, move it back.
- Do not delete apps. Remove from the home screen only.
- The laptop bedtime block and the phone Sleep mode use the same times. If he changes one, change the other (Claude does the laptop one with `~/school/.config/bedtime.json`).

## Log
