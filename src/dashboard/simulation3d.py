# ===== LINE 1 =====
from vpython import *
import pandas as pd

# =========================
# SCENE SETUP
# =========================
scene.title = "AI Airport Control System (Final Clean Version)"
scene.width = 1200
scene.height = 650
scene.background = vector(0.53, 0.81, 0.92)

scene.camera.pos = vector(0, 35, 30)
scene.camera.axis = vector(0, -30, -25)

scene.ambient = color.gray(0.4)
distant_light(direction=vector(1,-1,-1), color=color.white)

# =========================
# LOAD DATA
# =========================
schedule = pd.read_csv("data/generated_schedule.csv")
schedule = schedule.sort_values(by="scheduled_landing")

# =========================
# GROUND
# =========================
ground = box(pos=vector(0, -0.3, 0),
             size=vector(200, 0.1, 200),
             color=vector(0.1, 0.5, 0.1))

# =========================
# RUNWAY
# =========================
runway = box(pos=vector(0,0,0),
             size=vector(60,0.2,6),
             color=color.gray(0.4))

curve(pos=[vector(-30,0.01,0), vector(30,0.01,0)],
      color=color.white, radius=0.08)

# =========================
# RUNWAY LIGHTS
# =========================
runway_lights = []
for x in range(-28, 29, 2):
    l1 = sphere(pos=vector(x,0.05,2.8), radius=0.08,
                color=color.white, emissive=True)
    l2 = sphere(pos=vector(x,0.05,-2.8), radius=0.08,
                color=color.white, emissive=True)
    runway_lights.append((l1,l2))

# =========================
# TAXIWAY + TERMINAL
# =========================
taxiway = box(pos=vector(0,0.01,-12),
              size=vector(45,0.05,4),
              color=vector(0.25,0.25,0.25))

terminal = box(pos=vector(0,2,-20),
               size=vector(25,4,6),
               color=vector(0.7,0.7,0.75))

# =========================
# CLOUDS
# =========================
for i in range(5):
    sphere(pos=vector(-40+i*20, 20, -25),
           radius=3,
           color=color.white,
           opacity=0.6)

# =========================
# STATUS ICON
# =========================
def get_status_icon(state):
    return {
        "approach": "🟠",
        "landing": "🔴",
        "taxi": "🟢"
    }[state]

# =========================
# ATC PANEL
# =========================
panel = label(pos=vector(-35,18,0),
              text="",
              height=14,
              box=True,
              background=color.black,
              color=color.cyan)

# =========================
# CONTROLS
# =========================
RUN_SIM = True

def key_controls(evt):
    global RUN_SIM
    if evt.key == 'p':
        RUN_SIM = not RUN_SIM

scene.bind('keydown', key_controls)

# =========================
# AIRCRAFT CREATION (FIXED)
# =========================
landing_positions = [18, 10, 2, -6, -14]   # ✅ better spacing
planes = []

for i, row in schedule.head(5).iterrows():

    # ===== AIRCRAFT MODEL =====
    body = cylinder(axis=vector(4,0,0), radius=0.22, color=color.white)
    nose = cone(pos=vector(4,0,0), axis=vector(1,0,0), radius=0.22, color=color.white)
    tail = sphere(pos=vector(0,0,0), radius=0.22, color=color.white)

    wing = box(pos=vector(2,0,0),
               size=vector(1.5,0.05,6),
               color=color.gray(0.7))

    engine_l = cylinder(pos=vector(2,-0.25,1.8),
                        axis=vector(0.6,0,0),
                        radius=0.12,
                        color=color.gray(0.6))

    engine_r = cylinder(pos=vector(2,-0.25,-1.8),
                        axis=vector(0.6,0,0),
                        radius=0.12,
                        color=color.gray(0.6))

    tail_wing = box(pos=vector(0.6,0.25,0),
                    size=vector(0.8,0.05,2.5),
                    color=color.gray(0.75))

    vertical_tail = cone(pos=vector(0.6,0.25,0),
                         axis=vector(0,1,0),
                         radius=0.35,
                         color=color.gray(0.8))

    plane = compound([body, nose, tail,
                      wing, engine_l, engine_r,
                      tail_wing, vertical_tail])

    # ✅ FIXED SPACING
    plane.pos = vector(-35 - i*7, 10 + i*3, 0)

    # STATUS LIGHT
    light = sphere(pos=plane.pos + vector(0,0.6,0),
                   radius=0.2,
                   color=vector(1,0.6,0),
                   emissive=True)

    planes.append({
        "plane": plane,
        "light": light,
        "target_x": landing_positions[i],
        "state": "approach",
        "speed": 0.05,
        "callsign": row["callsign"]
    })

# =========================
# LOOP
# =========================
RUNWAY_Y = 0.2
PLANE_HEIGHT = 0.25

t = 0

while True:
    rate(30)
    t += 0.1

    if not RUN_SIM:
        continue

    # runway blinking
    blink = abs(sin(t*3))
    for l1, l2 in runway_lights:
        l1.color = vector(blink,blink,blink)
        l2.color = vector(blink,blink,blink)

    status_text = "✈ ATC CONTROL PANEL\n\n"

    for p in planes:

        plane = p["plane"]
        light = p["light"]
        target_x = p["target_x"]

        # ===== APPROACH =====
        if p["state"] == "approach":
            plane.pos.x += p["speed"]

            if plane.pos.x > target_x - 10:
                plane.pos.y -= 0.025   # smoother descent

            if plane.pos.y <= RUNWAY_Y + PLANE_HEIGHT:
                plane.pos.y = RUNWAY_Y + PLANE_HEIGHT
                p["state"] = "landing"

        # ===== LANDING =====
        elif p["state"] == "landing":
            plane.pos.x += p["speed"]
            p["speed"] *= 0.96

            if p["speed"] < 0.01:
                p["state"] = "taxi"

        # ===== TAXI =====
        elif p["state"] == "taxi":
            plane.pos.z -= 0.05   # move toward taxiway

        # ===== KEEP ABOVE GROUND ALWAYS =====
        if plane.pos.y < RUNWAY_Y + PLANE_HEIGHT:
            plane.pos.y = RUNWAY_Y + PLANE_HEIGHT

        # ===== STATUS LIGHT =====
        if p["state"] == "approach":
            light.color = vector(1,0.6,0)
        elif p["state"] == "landing":
            light.color = vector(1,0,0)
        elif p["state"] == "taxi":
            light.color = vector(0,1,0)

        light.pos = plane.pos + vector(0,0.6,0)

        # ===== PANEL =====
        icon = get_status_icon(p["state"])
        status_text += f"{icon} {p['callsign']} → {p['state']}\n"

    panel.text = status_text