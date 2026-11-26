"""Build the entry picture for news-image-20261125.

Draws "THE WORLD IN ONE DAY" for Wednesday 25 November 2026 as a dense
tabloid page: masthead, giant date, numbers strip, region tabs, a UTC
timeline, eleven numbered illustrated tiles, a numbered world map, a
34-item numbered list and a date-check box. Every story was verified
against wire reporting of the day; the drawing is original.

Run at build time only:  python3 build_image.py  ->  entry.png
The shipped program (main.py) merely copies entry.png to /output.
"""
import math

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 233)
INK = (18, 28, 40)
NAVY = (13, 38, 66)
RED = (178, 32, 40)
GOLD = (198, 146, 14)
TEAL = (13, 110, 100)
GREY = (90, 98, 108)
LINE = (196, 188, 168)
WHITE = (255, 255, 255)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANSB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def text_block(d, x, y, text, font, fill, maxw, pitch):
    for ln in wrap(d, text, font, maxw):
        d.text((x, y), ln, font=font, fill=fill)
        y += pitch
    return y


def chip(d, x, y, label, fill):
    f = F(SANSB, 9)
    w = d.textlength(label, font=f) + 10
    d.rectangle([x, y, x + w, y + 14], fill=fill)
    d.text((x + 5, y + 2), label, font=f, fill=WHITE)
    return w


def badge(d, x, y, n, fill=RED):
    d.ellipse([x, y, x + 19, y + 19], fill=fill)
    f = F(SANSB, 11 if n < 10 else 10)
    s = str(n)
    d.text((x + 9 - d.textlength(s, font=f) / 2, y + 3), s, font=f, fill=WHITE)


STATUS_FILL = {"OFFICIAL": (13, 110, 100), "CONFIRMED": (30, 90, 160),
               "REPORTED": (150, 104, 20), "CLAIM": (178, 32, 40)}

REGION_FILL = {"EUROPE": (37, 99, 235), "MIDDLE EAST": (180, 83, 9),
               "ASIA": (13, 110, 100), "AMERICAS": (178, 32, 40),
               "AFRICA": (124, 58, 237), "OCEANIA": (2, 132, 199),
               "GLOBAL": (71, 85, 105), "SPACE": (13, 38, 66)}

# ---------------------------------------------------------------- stories
# Tiles: (place, field, region, status, banner, headline, body)
TILES_BIG = [
    ("WASHINGTON", "TRADE", "AMERICAS", "OFFICIAL", "14 ECONOMIES",
     "Washington proposes tariffs on 14 economies",
     "USTR cites 'structural excess capacity'. China faces 20%, Vietnam 35%, "
     "India 25%, the EU 15%. Nothing is in force — public hearings open in January."),
    ("SEOUL · TAIPEI · TOKYO", "MARKETS", "ASIA", "CONFIRMED", "KOSPI CLOSE 4,697.51",
     "AI doubts crash Asia's chip stocks",
     "Kospi closed down 6.2% at 4,697.51, a 10-month low: Samsung fell 9.9% and "
     "SK Hynix 11.1% as the AI rally fizzled — the sharpest test yet of the AI boom."),
    ("JIUQUAN · ORBIT", "SPACE", "SPACE", "OFFICIAL", "FIRST FOREIGN CREW",
     "Shenzhou-24 flies a Pakistani to Tiangong",
     "Muhammad Zeeshan Ali, 40, docked at 03:56 UTC — the first foreigner aboard "
     "China's station; he stays five days. A first foreign guest for Tiangong."),
]

TILES_SMALL = [
    ("STRAIT OF HORMUZ", "GULF", "MIDDLE EAST", "CLAIM", "2 TANKERS ABLAZE",
     "Iran says mines hit two tankers ablaze",
     "IRGC navy says the ships took an 'unauthorised route' off Khasab — one a "
     "2m-barrel supertanker. Unverified."),
    ("RAS TANURA", "SAUDI ARABIA", "MIDDLE EAST", "REPORTED", "REFINERY CLAIMED HIT",
     "Houthis claim strike on biggest Saudi refinery",
     "The claim names Ras Tanura, the kingdom's largest refinery; satellite images "
     "show thick black smoke over it."),
    ("JERUSALEM", "JUSTICE", "MIDDLE EAST", "OFFICIAL", "DROP CASE 4000",
     "Judges urge dropping Netanyahu bribery charge",
     "The panel cites steep legal hurdles in Case 4000, questions a second case "
     "and urges the bribery count be dropped."),
    ("CAIRO", "DISASTER", "AFRICA", "OFFICIAL", "30+ DEAD",
     "Fuel tanker blaze kills at least 30 in Cairo",
     "An overturned fuel truck exploded in traffic on the ring road in Imbaba; "
     "27 vehicles burned, 25 people injured."),
    ("LONDON", "ENERGY", "EUROPE", "OFFICIAL", "£2,166 · FROM 1 JAN",
     "UK energy bills to jump 26% on gas war shock",
     "Ofgem lifts the cap from £1,723 to £2,166 a year from January, blaming "
     "Middle East gas prices."),
    ("DHAKA", "LABOUR", "ASIA", "OFFICIAL", "+36%",
     "Garment workers win a 36% minimum pay rise",
     "The wage board lifts the minimum from 12,500 to 17,000 taka ($139) after "
     "weeks of protests."),
    ("BOGOR, INDONESIA", "DISASTER", "ASIA", "REPORTED", "RESCUE AT 100 M",
     "Rescuers recover bodies in flooded gold mine",
     "26 wildcat miners remain trapped 100 m under Pongkor since Monday's flood; "
     "rescuers have pulled out three bodies."),
    ("CARTAGENA, COLOMBIA", "CRIME", "AMERICAS", "CONFIRMED", "ALL FREED",
     "Forces storm supermarket, free all hostages",
     "Forces stormed the Éxito store at dawn, ending a 17-hour siege; one gunman "
     "killed, no hostage hurt."),
]

# List: (place, region, text)
LIST_ITEMS = [
    ("GAZA CITY", "MIDDLE EAST", "Strike kills Hamas security chief (Reuters)"),
    ("WARSAW", "EUROPE", "Poland to build no-fly zone on Ukraine border"),
    ("SAMARA", "EUROPE", "Ukraine drones set two Volga refineries ablaze"),
    ("BLUE NILE", "AFRICA", "Sudan RSF drone attacks kill at least 19"),
    ("WASHINGTON", "AMERICAS", "US Q3 GDP revised up to 4.3% (BEA)"),
    ("WASHINGTON", "AMERICAS", "CIA–ODNI unclassified systems breached"),
    ("WASHINGTON", "AMERICAS", "Trump: Iran war funding secured to January"),
    ("CANBERRA", "OCEANIA", "Solomons–Australia pact: A$740m, no bases"),
    ("PYONGYANG", "ASIA", "North Korea expels Switzerland's envoy"),
    ("BAGHDAD", "MIDDLE EAST", "Top court lets federal troops guard oil, borders"),
    ("MISSISSIPPI", "AMERICAS", "All six bodies recovered from Cessna crash"),
    ("IOWA", "AMERICAS", "Army detonates 4.4 t lead azide; EPA clears air"),
    ("KYIV", "EUROPE", "Ukraine needs €115bn outside financing for 2027"),
    ("LEAKED DATA", "EUROPE", "Leak puts Russian dead in Ukraine at 490,334"),
    ("MADRID", "EUROPE", "Far right leads polls before Sunday snap vote"),
    ("UNITED NATIONS", "GLOBAL", "47,000 killed by kin in 2025 (UN brief)"),
    ("HONG KONG", "ASIA", "Survivors mark one year since tower fire"),
    ("MARYLAND", "AMERICAS", "Ábrego García reaches Spain; case closed"),
    ("BRUSSELS", "EUROPE", "EU unveils a €50bn quantum fund (AFP)"),
    ("LISBON", "EUROPE", "Champions League: Sporting 2–2 Man Utd"),
    ("LOS ANGELES", "AMERICAS", "Lakers beat Jazz behind Dončić's 28 points"),
    ("US NORTHEAST", "AMERICAS", "Thanksgiving storm threatens 81m trips"),
    ("BUDAPEST", "EUROPE", "Hungary–Ukraine 'fresh start' talks"),
    ("GAZA", "MIDDLE EAST", "Health officials warn meningitis spreads"),
    ("NEW YORK", "AMERICAS", "Dow erases 1,100-point fall, closes +0.3%"),
    ("WASHINGTON", "AMERICAS", "US tells citizens to leave Iran at once"),
    ("LONDON", "EUROPE", "UK warns firms of Russian sabotage threat (MI5)"),
    ("BENGHAZI", "AFRICA", "Ukraine drones sink Russian corvette; 2 die"),
    ("HODEIDAH", "MIDDLE EAST", "Coalition strikes Hodeidah port, Saada, Amran"),
    ("SHANGHAI", "ASIA", "Party chief Chen Jining probed in graft sweep"),
    ("NEW DELHI", "ASIA", "India condemns Riyadh attack; 2 Indians hurt"),
    ("TAIPEI", "ASIA", "Comedian tours with guards amid China anger"),
    ("MYANMAR", "ASIA", "Amputee rebel vows to fight on (Reuters)"),
    ("GENEVA", "GLOBAL", "WFP: wars put food aid for millions at risk"),
]

KPIS = [("35%", "top proposed US tariff — on Vietnam"),
        ("−6.2%", "Kospi close — worst day of the AI rout"),
        ("1ST", "foreign astronaut aboard Tiangong"),
        ("+26%", "UK energy cap — £2,166 from January"),
        ("30+", "killed in the Cairo fuel blaze"),
        ("+36%", "Dhaka garment minimum pay rise")]

TIMELINE = [("00:18", "Shenzhou-24 lifts off"), ("03:56", "Tiangong docking"),
            ("09:13", "US leave-Iran alert"), ("13:30", "US GDP 4.3%"),
            ("16:59", "Ras Tanura claim"), ("19:28", "Netanyahu ruling"),
            ("21:00", "Dow erases 1,100 pts")]

# ------------------------------------------------------------- continents
# Coarse polygons in (lon, lat); rasterised to a dot matrix for the map.
CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 68), (-95, 69), (-85, 66),
     (-80, 62), (-78, 58), (-85, 55), (-90, 50), (-85, 45), (-76, 42),
     (-70, 44), (-66, 45), (-60, 47), (-65, 50), (-70, 48), (-76, 38),
     (-75, 35), (-80, 32), (-80, 27), (-84, 25), (-86, 21), (-90, 20),
     (-95, 18), (-97, 16), (-95, 15), (-90, 14), (-86, 13), (-83, 9),
     (-79, 9), (-80, 8), (-85, 11), (-90, 13), (-95, 16), (-102, 18),
     (-105, 20), (-110, 23), (-114, 28), (-117, 33), (-122, 37),
     (-124, 42), (-124, 47), (-130, 54), (-140, 60), (-155, 60),
     (-162, 62), (-168, 66)],
    [(-79, 9), (-72, 11), (-64, 10), (-55, 6), (-50, 0), (-44, -3),
     (-35, -8), (-39, -13), (-40, -20), (-48, -26), (-54, -33), (-58, -38),
     (-62, -41), (-65, -45), (-67, -50), (-68, -54), (-71, -54), (-73, -50),
     (-73, -44), (-73, -37), (-71, -30), (-70, -22), (-70, -18), (-75, -15),
     (-79, -8), (-80, -4), (-80, 1), (-77, 4), (-77, 7), (-79, 9)],
    [(-10, 36), (-9, 43), (-2, 44), (0, 46), (-5, 48), (-1, 50), (2, 51),
     (5, 53), (8, 55), (8, 57), (10, 59), (5, 59), (5, 61), (10, 64),
     (14, 67), (18, 69), (25, 71), (30, 70), (35, 68), (32, 66), (30, 64),
     (28, 60), (30, 60), (28, 56), (24, 59), (21, 58), (19, 55), (18, 56),
     (21, 55), (24, 57), (28, 59), (30, 60), (30, 62), (28, 64), (24, 64),
     (22, 63), (21, 60), (18, 58), (12, 56), (10, 54), (14, 54), (18, 55),
     (20, 54), (24, 55), (28, 55), (30, 54), (28, 50), (30, 46), (28, 45),
     (24, 44), (28, 41), (23, 40), (22, 38), (20, 40), (16, 40), (12, 44),
     (10, 44), (6, 43), (3, 43), (3, 42), (0, 39), (-2, 37), (-6, 36),
     (-10, 36)],
    [(-17, 15), (-16, 20), (-13, 27), (-10, 31), (-6, 35), (-2, 35),
     (5, 37), (10, 37), (11, 34), (20, 32), (30, 31), (32, 31), (35, 28),
     (38, 22), (40, 15), (43, 12), (48, 11), (51, 12), (51, 10), (45, 5),
     (42, 0), (40, -6), (39, -12), (37, -18), (35, -24), (33, -26),
     (30, -29), (27, -33), (20, -35), (18, -33), (15, -27), (13, -18),
     (12, -12), (13, -6), (9, -1), (9, 4), (6, 4), (0, 5), (-5, 5),
     (-10, 7), (-13, 8), (-16, 12), (-17, 15)],
    [(35, 36), (40, 38), (44, 38), (48, 38), (50, 40), (48, 42), (50, 45),
     (55, 46), (60, 46), (66, 46), (70, 48), (75, 50), (80, 50), (88, 48),
     (95, 50), (100, 50), (105, 52), (110, 52), (118, 52), (125, 52),
     (132, 53), (140, 52), (142, 50), (141, 45), (140, 40), (142, 38),
     (140, 35), (138, 35), (135, 34), (130, 33), (127, 34), (127, 38),
     (122, 38), (122, 32), (120, 28), (118, 25), (110, 20), (108, 15),
     (107, 12), (105, 8), (103, 5), (100, 6), (98, 10), (97, 15),
     (94, 17), (92, 15), (91, 22), (89, 22), (86, 20), (80, 15), (77, 8),
     (73, 18), (70, 21), (66, 25), (61, 25), (57, 26), (52, 25), (50, 26),
     (48, 28), (50, 29), (48, 30), (47, 30), (44, 29), (42, 28), (40, 30),
     (39, 32), (36, 33), (35, 36)],
    [(113, -22), (114, -28), (115, -34), (118, -35), (124, -33), (129, -32),
     (132, -32), (135, -35), (138, -36), (140, -38), (145, -38), (147, -39),
     (150, -37), (153, -30), (153, -26), (151, -24), (149, -20), (146, -19),
     (143, -15), (142, -11), (141, -13), (140, -18), (139, -20), (136, -15),
     (135, -12), (132, -11), (129, -14), (126, -14), (122, -17), (118, -20),
     (114, -21), (113, -22)],
]


def in_poly(lon, lat, poly):
    inside = False
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        if (y1 > lat) != (y2 > lat):
            xin = x1 + (lat - y1) * (x2 - x1) / (y2 - y1)
            if lon < xin:
                inside = not inside
    return inside


def land(lon, lat):
    return any(in_poly(lon, lat, p) for p in CONTINENTS)


# ----------------------------------------------------------------- scenes
def scene_ship(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 44, 74))
    d.rectangle([x, y + h - 24, x + w, y + h], fill=(23, 78, 116))
    for i in range(9):
        d.arc([x + 12 + i * 34, y + h - 20, x + 40 + i * 34, y + h - 6], 0, 180, fill=(90, 160, 200))
    hx, hy = x + 26, y + h - 52
    d.polygon([(hx, hy + 22), (hx + 8, hy + 30), (hx + 210, hy + 30), (hx + 200, hy + 22)], fill=(30, 34, 40))
    cols = [(178, 32, 40), (198, 146, 14), (13, 110, 100), (37, 99, 235), (124, 58, 237), (2, 132, 199)]
    for r in range(2):
        for c in range(6):
            cx0 = hx + 18 + c * 31
            d.rectangle([cx0, hy - 12 - r * 13, cx0 + 27, hy - 1 - r * 13], fill=cols[(r * 6 + c) % 6], outline=(10, 14, 20))
    d.rectangle([hx + 196, hy - 26, hx + 212, hy + 22], fill=(220, 222, 226))
    d.rectangle([hx + 200, hy - 22, hx + 208, hy - 16], fill=(16, 44, 74))
    rates = [("CHINA 20%", (178, 32, 40)), ("INDIA 25%", (180, 83, 9)),
             ("EU 15%", (37, 99, 235)), ("VIETNAM 35%", (124, 58, 237))]
    fx = x + w - 86
    for i, (s, col) in enumerate(rates):
        yy = y + 24 + i * 16
        d.rectangle([fx, yy, fx + 80, yy + 14], fill=col)
        f = F(SANSB, 9)
        d.text((fx + 40 - d.textlength(s, font=f) / 2, yy + 2), s, font=f, fill=WHITE)


def scene_chart(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(10, 16, 26))
    for gy in range(4):
        yy = y + 14 + gy * (h - 40) // 3
        d.line([x + 10, yy, x + w - 108, yy], fill=(40, 54, 72))
    pts = [(0, 18), (30, 22), (58, 16), (86, 26), (112, 38), (140, 44),
           (168, 62), (196, 74), (220, 96)]
    P = [(x + 12 + px, y + 8 + py) for px, py in pts]
    d.line(P, fill=(240, 70, 70), width=3)
    for px, py in P:
        d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(240, 70, 70))
    d.polygon([(P[-1][0], P[-1][1]), (P[-1][0] - 9, P[-1][1] - 2), (P[-1][0] - 3, P[-1][1] + 8)], fill=(240, 70, 70))
    rows = [("KOSPI", "−6.2%", (240, 70, 70)), ("SK HYNIX", "−11.1%", (240, 70, 70)),
            ("SAMSUNG", "−9.9%", (240, 70, 70)), ("TAIEX", "−4.8%", (240, 150, 90)),
            ("NIKKEI", "−2.8%", (240, 150, 90))]
    bx = x + w - 104
    for i, (a, b, col) in enumerate(rows):
        yy = y + 18 + i * 15
        d.text((bx, yy), a, font=F(SANSB, 9), fill=(200, 210, 220))
        d.text((bx + 52, yy), b, font=F(SANSB, 10), fill=col)
    d.rectangle([x + 12, y + h - 22, x + 62, y + h - 8], fill=(70, 30, 30))
    d.text((x + 19, y + h - 20), "AI CHIP", font=F(SANSB, 9), fill=(255, 180, 180))


def scene_station(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(8, 14, 34))
    for sx, sy in [(30, 14), (80, 30), (150, 10), (230, 22), (290, 12), (60, 44), (200, 40)]:
        d.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2], fill=(220, 228, 240))
    cx_e, cy_e = x + w / 2, y + h + 50
    rx, ry = w / 2 + 50, 80
    cap = []
    for a in range(180, 361, 4):
        px = cx_e + rx * math.cos(math.radians(a))
        py = cy_e + ry * math.sin(math.radians(a))
        if py <= y + h:
            cap.append((min(max(px, x), x + w), py))
    d.polygon(cap + [(x + w, y + h), (x, y + h)], fill=(16, 52, 110))
    d.line(cap, fill=(110, 180, 240), width=3)
    cx, cy = x + w // 2, y + h // 2 - 8
    d.rectangle([cx - 52, cy - 9, cx + 52, cy + 9], fill=(216, 220, 226), outline=(90, 96, 104))
    d.rectangle([cx - 8, cy - 20, cx + 8, cy + 20], fill=(196, 200, 206), outline=(90, 96, 104))
    for sgn in (-1, 1):
        for k in range(3):
            px = cx + sgn * (58 + k * 22)
            d.rectangle([px - 9, cy - 13, px + 9, cy + 13], fill=(38, 84, 168), outline=(16, 40, 80))
        xa, xb = cx + sgn * 52, cx + sgn * 56
        d.rectangle([min(xa, xb), cy - 2, max(xa, xb), cy + 2], fill=(150, 154, 160))
    d.rectangle([cx - 74, cy - 6, cx - 54, cy + 6], fill=(240, 242, 244), outline=(90, 96, 104))
    d.rectangle([cx - 71, cy - 3, cx - 65, cy + 3], fill=(13, 110, 60))
    d.polygon([(cx - 74, cy - 6), (cx - 82, cy), (cx - 74, cy + 6)], fill=(198, 146, 14))
    d.rectangle([cx + 54, cy - 4, cx + 66, cy + 4], fill=(178, 32, 40))



def scene_hormuz(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(26, 92, 138))
    d.polygon([(x, y), (x + w * 0.44, y), (x + w * 0.34, y + h * 0.36),
               (x + w * 0.24, y + h * 0.50), (x, y + h * 0.56)], fill=(206, 188, 140))
    d.polygon([(x + w * 0.66, y + h), (x + w * 0.62, y + h * 0.64),
               (x + w * 0.74, y + h * 0.56), (x + w, y + h * 0.70), (x + w, y + h)],
              fill=(206, 188, 140))
    d.text((x + 36, y + 6), "IRAN", font=F(SANSB, 9), fill=(90, 74, 40))
    d.text((x + w - 40, y + h - 15), "OMAN", font=F(SANSB, 8), fill=(90, 74, 40))
    route = [(x + 14, y + h - 12), (x + w * 0.36, y + h * 0.60), (x + w * 0.55, y + h * 0.46),
             (x + w * 0.82, y + h * 0.30)]
    for i in range(len(route) - 1):
        d.line([route[i], route[i + 1]], fill=(255, 220, 90), width=2)
    for mx, my in [(x + w * 0.44, y + h * 0.55), (x + w * 0.63, y + h * 0.42)]:
        d.ellipse([mx - 5, my - 5, mx + 5, my + 5], fill=(20, 24, 30), outline=(255, 120, 60), width=2)
    tx, ty = x + w * 0.50, y + h * 0.30
    d.polygon([(tx, ty + 10), (tx + 5, ty + 16), (tx + 52, ty + 16), (tx + 47, ty + 10)], fill=(40, 44, 50))
    d.rectangle([tx + 10, ty + 3, tx + 38, ty + 10], fill=(120, 128, 136))
    d.polygon([(tx + 21, ty + 3), (tx + 27, ty - 9), (tx + 33, ty + 3)], fill=(255, 130, 40))
    d.ellipse([tx + 19, ty - 14, tx + 35, ty + 0], fill=(255, 170, 50))


def scene_refinery(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 178, 120))
    d.rectangle([x, y + h - 12, x + w, y + h], fill=(150, 110, 70))
    for tx, th in [(30, 20), (58, 27), (150, 23), (196, 18)]:
        d.rectangle([x + tx, y + h - 12 - th, x + tx + 12, y + h - 12], fill=(96, 100, 106))
        d.rectangle([x + tx, y + h - 16 - th, x + tx + 12, y + h - 12 - th], fill=(70, 74, 80))
    for cx0 in (88, 116, 168):
        d.rectangle([x + cx0, y + h - 26, x + cx0 + 24, y + h - 12], fill=(176, 180, 186), outline=(96, 100, 106))
        d.arc([x + cx0, y + h - 32, x + cx0 + 24, y + h - 20], 180, 360, fill=(96, 100, 106))
    fx = x + 226
    d.line([fx, y + h - 12, fx, y + 12], fill=(70, 74, 80), width=3)
    d.polygon([(fx, y + 12), (fx + 5, y + 2), (fx + 10, y + 12)], fill=(255, 130, 40))
    d.ellipse([fx + 1, y + 4, fx + 9, y + 13], fill=(255, 180, 60))
    dx, dy = x + w - 66, y + 10
    d.polygon([(dx, dy + 5), (dx + 16, dy), (dx + 30, dy + 5), (dx + 16, dy + 9)], fill=(40, 44, 50))
    d.line([dx + 15, dy + 8, dx + 15, dy + 13], fill=(40, 44, 50), width=2)
    d.line([dx + 4, dy + 16, dx + 26, dy + 16], fill=(178, 32, 40), width=1)


def scene_scales(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 226, 208))
    for cx0 in (26, 210):
        d.rectangle([x + cx0, y + 10, x + cx0 + 10, y + h - 8], fill=(168, 158, 130))
        d.rectangle([x + cx0 - 3, y + 6, x + cx0 + 13, y + 11], fill=(140, 130, 100))
    cx, cy = x + w // 2, y + 12
    d.rectangle([cx - 2, cy, cx + 2, y + h - 16], fill=(120, 100, 50))
    d.line([cx - 52, cy + 8, cx + 52, cy + 8], fill=(120, 100, 50), width=3)
    for sgn in (-1, 1):
        px = cx + sgn * 48
        d.line([px, cy + 8, px - 12, cy + 30], fill=(120, 100, 50))
        d.line([px, cy + 8, px + 12, cy + 30], fill=(120, 100, 50))
        d.arc([px - 15, cy + 24, px + 15, cy + 40], 0, 180, fill=(120, 100, 50), width=3)
    d.rectangle([cx - 16, y + h - 14, cx + 16, y + h - 9], fill=(120, 100, 50))
    d.text((x + w - 76, y + h - 30), "CASE 4000", font=F(SANSB, 9), fill=(120, 100, 50))


def scene_truck(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(70, 74, 84))
    d.rectangle([x, y + h - 10, x + w, y + h], fill=(46, 48, 54))
    for i in range(6):
        d.line([x + 8 + i * 42, y + h - 5, x + 30 + i * 42, y + h - 5], fill=(220, 200, 90), width=2)
    tx, ty = x + 52, y + h - 30
    d.polygon([(tx, ty), (tx + 66, ty - 4), (tx + 70, ty + 8), (tx + 4, ty + 10)], fill=(196, 200, 206))
    d.rectangle([tx + 66, ty - 2, tx + 84, ty + 8], fill=(150, 60, 50))
    for wx in (tx + 12, tx + 56):
        d.ellipse([wx, ty + 7, wx + 11, ty + 18], fill=(20, 22, 26), outline=(120, 124, 130))
    d.polygon([(tx + 26, ty - 2), (tx + 36, ty - 18), (tx + 46, ty - 2)], fill=(255, 120, 40))
    d.polygon([(tx + 31, ty - 2), (tx + 37, ty - 12), (tx + 43, ty - 2)], fill=(255, 180, 60))
    for gx in range(5):
        d.line([tx + 18 + gx * 8, ty - 16 - gx * 2, tx + 22 + gx * 8, ty - 26 - gx * 2], fill=(110, 112, 118), width=2)


def scene_house(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(196, 220, 236))
    hx, hy = x + 34, y + h - 34
    d.rectangle([hx, hy, hx + 74, hy + 26], fill=(240, 238, 230), outline=(120, 124, 130))
    d.polygon([(hx - 5, hy), (hx + 37, hy - 16), (hx + 79, hy)], fill=(150, 60, 50))
    d.rectangle([hx + 30, hy + 10, hx + 44, hy + 26], fill=(110, 80, 50))
    d.rectangle([hx + 8, hy + 8, hx + 20, hy + 18], fill=(250, 210, 90), outline=(120, 124, 130))
    d.rectangle([hx + 54, hy + 8, hx + 66, hy + 18], fill=(250, 210, 90), outline=(120, 124, 130))
    fx, fy = x + 150, y + 16
    d.polygon([(fx, fy + 22), (fx + 8, fy + 6), (fx + 12, fy + 14), (fx + 17, fy + 2),
               (fx + 22, fy + 14), (fx + 27, fy + 7), (fx + 30, fy + 22)], fill=(255, 130, 40))
    d.polygon([(fx + 9, fy + 22), (fx + 14, fy + 12), (fx + 20, fy + 22)], fill=(255, 190, 70))
    d.text((x + 138, y + 44), "£2,166", font=F(SERIF, 17), fill=(178, 32, 40))
    d.text((x + 138, y + 63), "from 1 JAN", font=F(SANSB, 8), fill=INK)


def scene_factory(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 226, 210))
    d.rectangle([x + 20, y + h - 34, x + 150, y + h - 8], fill=(150, 156, 150), outline=(96, 100, 96))
    d.polygon([(x + 20, y + h - 34), (x + 44, y + h - 44), (x + 68, y + h - 34),
               (x + 92, y + h - 44), (x + 116, y + h - 34), (x + 140, y + h - 44),
               (x + 150, y + h - 34)], fill=(110, 116, 110))
    for r in range(2):
        for c in range(6):
            d.rectangle([x + 28 + c * 20, y + h - 28 + r * 11, x + 42 + c * 20, y + h - 21 + r * 11],
                        fill=(250, 220, 120))
    d.rectangle([x + 158, y + h - 52, x + 168, y + h - 8], fill=(120, 124, 120))
    d.text((x + 178, y + 12), "+36%", font=F(SERIF, 20), fill=(13, 110, 100))
    d.text((x + 178, y + 36), "TK 17,000", font=F(SANSB, 10), fill=INK)
    d.line([x + 182, y + 54, x + 226, y + 54], fill=(13, 110, 100), width=2)
    d.polygon([(x + 226, y + 54), (x + 218, y + 50), (x + 218, y + 58)], fill=(13, 110, 100))


def scene_mine(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(206, 190, 160))
    d.rectangle([x, y + 22, x + w, y + h], fill=(140, 116, 84))
    d.rectangle([x, y + 34, x + w, y + h], fill=(110, 88, 60))
    d.rectangle([x + 30, y + 6, x + 40, y + 26], fill=(90, 70, 44))
    d.line([x + 20, y + 6, x + 50, y + 6], fill=(90, 70, 44), width=3)
    d.rectangle([x + 100, y + 40, x + 190, y + 52], fill=(52, 44, 32))
    d.rectangle([x + 100, y + 40, x + 190, y + 46], fill=(40, 90, 150))
    for wx in range(5):
        d.arc([x + 106 + wx * 17, y + 40, x + 118 + wx * 17, y + 48], 180, 360, fill=(120, 180, 230))
    d.text((x + 196, y + 38), "100 m", font=F(SANSB, 10), fill=(240, 230, 200))
    d.text((x + 196, y + 50), "FLOODED", font=F(SANSB, 8), fill=(240, 230, 200))
    d.polygon([(x + 66, y + 12), (x + 74, y + 4), (x + 82, y + 12)], fill=(178, 32, 40))
    d.text((x + 70, y + 13), "!", font=F(SANSB, 10), fill=WHITE)


def scene_store(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(120, 160, 190))
    d.rectangle([x + 16, y + 16, x + w - 16, y + h - 6], fill=(238, 238, 236), outline=(110, 114, 120))
    d.rectangle([x + 16, y + 16, x + w - 16, y + 34], fill=(240, 190, 40))
    d.text((x + w / 2 - d.textlength("ÉXITO", font=F(SANSB, 13)) / 2, y + 18), "ÉXITO",
           font=F(SANSB, 13), fill=(150, 30, 30))
    for c in range(5):
        d.rectangle([x + 26 + c * 42, y + 42, x + 58 + c * 42, y + 56], fill=(170, 205, 225),
                    outline=(110, 114, 120))
    d.rectangle([x + w / 2 - 12, y + 42, x + w / 2 + 12, y + h - 6], fill=(90, 96, 104))
    for px in (x + 40, x + w - 52):
        d.polygon([(px, y + h - 6), (px + 5, y + h - 20), (px + 10, y + h - 6)], fill=(40, 60, 90))


# ------------------------------------------------------------- rendering
SCENES_BIG = [scene_ship, scene_chart, scene_station]
SCENES_SMALL = [scene_hormuz, scene_refinery, scene_scales, scene_truck,
                scene_house, scene_factory, scene_mine, scene_store]
CARD = (255, 254, 248)


def tile(d, x, y, w, h, n, t, scene, big):
    place, field, region, status, banner, head, body = t
    d.rectangle([x, y, x + w, y + h], fill=CARD, outline=LINE)
    sh = 106 if big else 50
    scene(d, x + 1, y + 1, w - 2, sh)
    bw = d.textlength(banner, font=F(SANSB, 10)) + 14
    d.rectangle([x + 1, y + sh - 15, x + 1 + bw, y + sh + 1], fill=(16, 22, 30))
    d.text((x + 8, y + sh - 13), banner, font=F(SANSB, 10), fill=(255, 214, 90))
    cw = chip(d, x + w - 4 - (d.textlength(status, font=F(SANSB, 9)) + 10), y + 5,
              status, STATUS_FILL[status])
    badge(d, x + 5, y + 5, n)
    ty = y + sh + 7
    d.text((x + 8, ty), place, font=F(SANSB, 9), fill=REGION_FILL[region])
    pw = d.textlength(place, font=F(SANSB, 9))
    d.text((x + 12 + pw, ty), "· " + field, font=F(SANSB, 9), fill=GREY)
    ty += 14
    ty = text_block(d, x + 8, ty, head, F(SERIF, 18 if big else 13), INK,
                    w - 16, 21 if big else 15)
    text_block(d, x + 8, ty + 2, body, F(SANS, 9 if big else 8), (52, 60, 70),
               w - 16, 11.5 if big else 10.5)


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 242, 246), outline=LINE)
    d.text((x + 8, y + 5), "WHERE IT HAPPENED", font=F(SANSB, 10), fill=NAVY)
    d.text((x + 128, y + 5), "· PINS 1–11 MATCH THE PICTURES", font=F(SANS, 8), fill=GREY)
    cell = 6.4
    ox, oy = x + 8, y + 24
    cols, rows = int((w - 16) / cell), int((h - 52) / cell)
    for r in range(rows):
        lat = 78 - r * (138 / rows)
        for c in range(cols):
            lon = -168 + c * (348 / cols)
            if land(lon, lat):
                cxp, cyp = ox + c * cell + 2, oy + r * cell + 2
                d.ellipse([cxp - 1.6, cyp - 1.6, cxp + 1.6, cyp + 1.6], fill=(120, 132, 148))
    pins = [(1, -77, 39), (2, 127, 37), (3, 100, 41), (4, 56, 26), (5, 49, 28),
            (6, 35, 33), (7, 30, 29), (8, 0, 51), (9, 90, 24), (10, 107, -7),
            (11, -75, 10)]
    regs = {1: "AMERICAS", 2: "ASIA", 3: "SPACE", 4: "MIDDLE EAST", 5: "MIDDLE EAST",
            6: "MIDDLE EAST", 7: "AFRICA", 8: "EUROPE", 9: "ASIA", 10: "ASIA",
            11: "AMERICAS"}
    for n, lon, lat in pins:
        px = ox + (lon + 168) / 348 * (w - 16)
        py = oy + (78 - lat) / 138 * (h - 52)
        col = REGION_FILL[regs[n]]
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=col, outline=WHITE, width=1)
        s = str(n)
        f = F(SANSB, 9 if n < 10 else 8)
        d.text((px - d.textlength(s, font=f) / 2, py - 5), s, font=f, fill=WHITE)
    ly = y + h - 22
    lx = x + 8
    for reg in ["EUROPE", "AMERICAS", "MIDDLE EAST", "ASIA", "AFRICA", "OCEANIA", "GLOBAL", "SPACE"]:
        d.rectangle([lx, ly + 2, lx + 8, ly + 10], fill=REGION_FILL[reg])
        d.text((lx + 11, ly), reg.title(), font=F(SANS, 8), fill=INK)
        lx += 11 + d.textlength(reg.title(), font=F(SANS, 8)) + 12


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # Masthead
    d.rectangle([0, 0, W, 30], fill=NAVY)
    d.text((12, 7), "THE WORLD IN ONE DAY", font=F(SANSB, 15), fill=WHITE)
    right = "45 STORIES · 8 REGIONS · 11 ILLUSTRATED · EVERY ONE FIRST REPORTED WED 25 NOV 2026"
    d.text((W - 12 - d.textlength(right, font=F(SANSB, 9)), 10), right, font=F(SANSB, 9),
           fill=(255, 214, 90))
    # Date + sub-lead
    d.text((12, 38), "Wednesday 25 November 2026", font=F(SERIF, 47), fill=INK)
    d.text((12, 94), "America taxes 14 economies · Asia's chip rally breaks · mines in the Strait "
                     "of Hormuz — and Wall Street erases a 1,100-point fall",
           font=F(SERIF, 13), fill=RED)
    # KPI strip
    ky = 116
    d.line([12, ky - 4, W - 12, ky - 4], fill=LINE)
    kw = (W - 24) / 6
    for i, (num, lab) in enumerate(KPIS):
        kx = 12 + i * kw
        if i:
            d.line([kx - 6, ky, kx - 6, ky + 30], fill=LINE)
        d.text((kx, ky), num, font=F(SERIF, 22), fill=RED if i in (0, 1, 3) else INK)
        text_block(d, kx, ky + 27, lab, F(SANS, 8), GREY, kw - 14, 10)
    # Region tabs
    ty = 158
    tabs = [("AMERICAS", 12), ("EUROPE", 10), ("ASIA", 9), ("MIDDLE EAST", 7),
            ("AFRICA", 3), ("GLOBAL", 2), ("OCEANIA", 1), ("SPACE", 1)]
    tx = 12
    for reg, cnt in tabs:
        label = f"{reg} {cnt}"
        tw = d.textlength(label, font=F(SANSB, 9)) + 14
        d.rectangle([tx, ty, tx + tw, ty + 16], fill=REGION_FILL[reg])
        d.text((tx + 7, ty + 3), label, font=F(SANSB, 9), fill=WHITE)
        tx += tw + 5
    d.text((tx + 4, ty + 3), "— every story counted once, by dateline", font=F(SANS, 8), fill=GREY)
    # Timeline
    ly = 180
    d.rectangle([12, ly, 118, ly + 15], fill=INK)
    d.text((19, ly + 2), "THE DAY IN UTC", font=F(SANSB, 9), fill=WHITE)
    tx = 126
    for tm, ev in TIMELINE:
        d.text((tx, ly + 2), tm, font=F(SANSB, 9), fill=RED)
        tx += d.textlength(tm, font=F(SANSB, 9)) + 3
        d.text((tx, ly + 2), ev, font=F(SANS, 9), fill=INK)
        tx += d.textlength(ev, font=F(SANS, 9)) + 12
    d.line([12, ly + 19, W - 12, ly + 19], fill=LINE)
    # Big tiles
    bw = (W - 24 - 16) // 3
    for i, t in enumerate(TILES_BIG):
        tile(d, 12 + i * (bw + 8), 206, bw, 208, i + 1, t, SCENES_BIG[i], True)
    # Small tiles
    sw = (W - 24 - 24) // 4
    for i, t in enumerate(TILES_SMALL):
        r, c = divmod(i, 4)
        tile(d, 12 + c * (sw + 8), 422 + r * 136, sw, 128, i + 4, t, SCENES_SMALL[i], False)
    # Bottom band: map + list
    by = 698
    draw_map(d, 12, by, 452, 258)
    lx = 476
    d.text((lx, by + 2), "ALSO ON WEDNESDAY", font=F(SANSB, 12), fill=NAVY)
    d.text((lx + 168, by + 4), "— 34 MORE STORIES, NUMBERED & COLOUR-MATCHED BY REGION",
           font=F(SANS, 8), fill=GREY)
    d.line([lx, by + 20, W - 12, by + 20], fill=LINE)
    colw = (W - 12 - lx - 14) // 2
    pf, tf = F(SANSB, 8), F(SANS, 8)
    for i, (place, region, text) in enumerate(LIST_ITEMS):
        c, r = divmod(i, 17)
        ix = lx + c * (colw + 14)
        iy = by + 26 + r * 12.5
        n = i + 12
        d.ellipse([ix, iy, ix + 11, iy + 11], fill=REGION_FILL[region])
        s = str(n)
        d.text((ix + 5.5 - d.textlength(s, font=F(SANSB, 7)) / 2, iy + 1.5), s,
               font=F(SANSB, 7), fill=WHITE)
        d.text((ix + 15, iy + 1), place, font=pf, fill=REGION_FILL[region])
        tx0 = ix + 15 + d.textlength(place, font=pf) + 4
        budget = ix + colw - tx0
        t = text
        while t and d.textlength(t, font=tf) > budget:
            t = t.rsplit(" ", 1)[0]
        if t != text:
            t += "…"
        d.text((tx0, iy + 1), t, font=tf, fill=(52, 60, 70))
    # Date check + sources
    dy = 962
    d.rectangle([12, dy, W - 12, dy + 30], outline=RED, width=1)
    d.text((20, dy + 4), "DATE CHECK", font=F(SANSB, 9), fill=RED)
    d.text((92, dy + 3), "Left out as other days' news: Huawei's 10-count Brooklyn verdict (Tue 24) · Houthi strike on Riyadh's PIF Tower (Tue 24) ·",
           font=F(SANS, 8), fill=INK)
    d.text((92, dy + 15), "Huang restored as Nvidia CEO (Mon 23) · COP31 ends without a deal (Sun 22). Not yet: US Thanksgiving (Thu 26) · UK cap starts 1 Jan 2027.",
           font=F(SANS, 8), fill=INK)
    d.text((12, dy + 36), "Every story happened, or was first reported, on Wednesday 25 November 2026 — day 329 of 2026, 36 days remain.",
           font=F(SANS, 8), fill=GREY)
    d.text((12, dy + 45), "HOW SURE: OFFICIAL = an authority's own word · CONFIRMED = 2+ major outlets · REPORTED = one outlet · CLAIM = one side's account, unverified.",
           font=F(SANS, 8), fill=GREY)
    d.text((12, dy + 54), "Sources: Reuters, AP, WSJ, Yonhap, CNN, BBC, AFP, UNODC/UN Women, Ofgem, BEA, USTR. Drawings original, made for this page.",
           font=F(SANS, 8), fill=GREY)
    img.save("entry.png")
    print("entry.png written")


if __name__ == "__main__":
    main()
