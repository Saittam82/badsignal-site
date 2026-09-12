#!/usr/bin/env python3
"""Regenerate demo/epg.xml with programmes spanning ±36h from now.

Run before a screenshot session so the guide and now/next look alive:
    python3 demo/generate_epg.py && git commit -am "Refresh demo EPG" && git push
"""
from datetime import datetime, timedelta, timezone

CHANNELS = {
    "nova1.demo": ("Nova One HD", [
        "Morning Light", "The Update", "Homes by the Sea", "Quiz Night",
        "The Grand Meal", "Evening Stories", "Late Edition",
    ]),
    "nova2.demo": ("Nova Two HD", [
        "Second Breakfast", "Open Studio", "The Workshop", "City Walks",
        "Panel Talk", "Night Owls",
    ]),
    "pulse.demo": ("Pulse Sports 1", [
        "Warm-Up", "Matchday Live", "Halftime Report", "The Big Game",
        "Extra Time", "Sports Tonight",
    ]),
    "pulse2.demo": ("Pulse Sports 2", [
        "Court Side", "Race Week", "The Paddock", "Ringside",
        "Championship Hour", "Final Whistle",
    ]),
    "arena.demo": ("Arena Football", [
        "Training Ground", "Kickoff", "First Half", "Second Half",
        "Full Time Analysis", "Classic Matches",
    ]),
    "orbit.demo": ("Orbit News 24", [
        "Dawn Briefing", "World This Hour", "Business Pulse", "The Interview",
        "Evening Wrap", "Overnight Desk",
    ]),
    "daily.demo": ("The Daily News Channel", [
        "Daily Morning", "Headline Hour", "The Long Read", "Field Reports",
        "Daily Evening", "The Midnight Brief",
    ]),
    "cinema1.demo": ("Cinema One", [
        "The Silent Harbor", "Paper Kites", "A Winter in Motion",
        "The Last Cartographer", "Glass Gardens",
    ]),
    "cinema2.demo": ("Cinema Classics", [
        "The Clockmaker's Son", "Harvest Moon", "Steel and Silk",
        "The Blue Umbrella", "Midnight Train Home",
    ]),
    "reel.demo": ("Reel Film HD", [
        "Directors' Cut", "Short Film Hour", "Festival Favorites",
        "Behind the Lens", "The Reel Review",
    ]),
    "minis.demo": ("Minis Kids TV", [
        "Sunny Meadow Friends", "Puzzle Parade", "The Little Explorers",
        "Storytime", "Bedtime Songs",
    ]),
    "cosmos.demo": ("Cosmos Docs", [
        "Edge of the Universe", "Deep Ocean", "The Ancient Builders",
        "Wild Frontiers", "Future Cities",
    ]),
    "terra.demo": ("Terra Nature", [
        "River Kingdoms", "The High Peaks", "Forest Seasons",
        "Islands of Life", "Night in the Wild",
    ]),
    "beat.demo": ("Beat Music TV", [
        "Fresh Rotation", "The Acoustic Room", "Chart Countdown",
        "Live Sessions", "After Hours Mix",
    ]),
    "wave.demo": ("Wave Channel HD", [
        "Surf Report", "The Wave Show", "Coastline", "Harbor Nights",
    ]),
}


def fmt(dt: datetime) -> str:
    return dt.strftime("%Y%m%d%H%M%S +0000")


def main() -> None:
    now = datetime.now(timezone.utc)
    start = (now - timedelta(hours=36)).replace(minute=0, second=0, microsecond=0)
    end = now + timedelta(hours=36)

    out = ['<?xml version="1.0" encoding="UTF-8"?>', "<tv>"]
    for cid, (name, _) in CHANNELS.items():
        out.append(f'  <channel id="{cid}"><display-name>{name}</display-name></channel>')

    for ci, (cid, (_, titles)) in enumerate(CHANNELS.items()):
        t = start
        i = ci  # offset per channel so schedules don't look copy-pasted
        while t < end:
            dur = [60, 90, 120, 45][ (i + ci) % 4 ]
            t2 = t + timedelta(minutes=dur)
            title = titles[i % len(titles)]
            out.append(
                f'  <programme start="{fmt(t)}" stop="{fmt(t2)}" channel="{cid}">'
                f"<title>{title}</title>"
                f"<desc>Demo programme for store screenshots. Fictional content.</desc>"
                f"</programme>"
            )
            t = t2
            i += 1

    out.append("</tv>")
    with open(__file__.replace("generate_epg.py", "epg.xml"), "w") as f:
        f.write("\n".join(out) + "\n")
    print(f"epg.xml: {sum(1 for l in out if '<programme' in l)} programmes, "
          f"{fmt(start)} → {fmt(end)}")


if __name__ == "__main__":
    main()
