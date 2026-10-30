#!/usr/bin/env python3
"""Generates images/circuit/wiring-diagram.svg (schematic style, matches docs/circuit-connections.md).
Usage (repo root): python3 diagrams/generate_wiring_diagram.py"""
import os
NAVY="#0B2545"; TEAL="#13A89E"
C=dict(vbat="#E67E22",v5="#C0392B",v33="#D81B60",gnd="#222222",sda="#1E88E5",scl="#00897B",
       rx="#2E7D32",tx="#7CB342",aud="#7B1FA2",audr="#AB47BC",spk="#607D8B",btn="#6D4C41",irq="#F9A825",irq2="#EF6C00")
o=[]
def box(x,y,w,h,title,sub="",dy=0):
    o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{NAVY}"/>')
    o.append(f'<text x="{x+w/2}" y="{y+h/2-(2 if sub else -5)+dy}" text-anchor="middle" font-size="16" font-weight="700" fill="#fff">{title}</text>')
    if sub: o.append(f'<text x="{x+w/2}" y="{y+h/2+16+dy}" text-anchor="middle" font-size="12" fill="#bfe9e5">{sub}</text>')
def wire(pts,col,wd=3):
    o.append('<polyline points="'+" ".join(f"{a},{b}" for a,b in pts)+f'" fill="none" stroke="{col}" stroke-width="{wd}" stroke-linejoin="round"/>')
def pin(x,y,label,side):
    # side = which edge of the box the pin sits on; the label is drawn INSIDE the box (white on navy)
    o.append(f'<circle cx="{x}" cy="{y}" r="5" fill="#fff" stroke="{TEAL}" stroke-width="2"/>')
    dx={"l":10,"r":-10,"t":0,"b":0}[side]; dy={"l":4,"r":4,"t":19,"b":-9}[side]
    anc={"l":"start","r":"end","t":"middle","b":"middle"}[side]
    o.append(f'<text x="{x+dx}" y="{y+dy}" text-anchor="{anc}" font-size="12" fill="#fff">{label}</text>')
def dot(x,y,c): o.append(f'<circle cx="{x}" cy="{y}" r="4.5" fill="{c}"/>')
def txt(x,y,s,size=12,anc="start",col="#222",bold=False):
    o.append(f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anc}" fill="{col}"'+(' font-weight="700"' if bold else '')+f'>{s}</text>')
def gnd_sym(x,y):
    for i,w in enumerate((12,8,4)):
        o.append(f'<line x1="{x-w}" y1="{y+i*4}" x2="{x+w}" y2="{y+i*4}" stroke="{C["gnd"]}" stroke-width="2"/>')
def resistor(x,y,w=40): o.append(f'<rect x="{x}" y="{y-8}" width="{w}" height="16" fill="#fff" stroke="#222" stroke-width="2"/>'); txt(x+w/2,y+4,"1k",11,"middle")
def led(x,y,col):
    o.append(f'<polygon points="{x},{y-10} {x},{y+10} {x+22},{y}" fill="{col}" stroke="#222" stroke-width="1.5"/>')
    o.append(f'<line x1="{x+22}" y1="{y-10}" x2="{x+22}" y2="{y+10}" stroke="#222" stroke-width="2.5"/>')
def led_chain(y,src,col,ledcol,dst,wcol):
    txt(30,y+4,src,11); wire([(185,y),(225,y)],wcol); resistor(225,y); wire([(265,y),(300,y)],wcol)
    led(300,y,ledcol); wire([(322,y),(360,y)],wcol); txt(366,y+4,dst,11)

W,H=1340,1110
o.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="Helvetica, Arial, sans-serif">')
o.append('<title>Talking Medicine Label - schematic-style wiring diagram</title><desc>Battery, TP4056 with LEDs, switch, MT3608, ESP32 with three buttons, PN532, DFPlayer Mini, PAM8403 and two speakers with GPIO labels.</desc>')
o.append(f'<rect width="{W}" height="{H}" fill="#fff"/>')
txt(30,28,"Talking Medicine Label - wiring diagram (schematic style; pin positions are NOT the physical board layout)",15,bold=True,col=NAVY)
# battery + TP4056
box(30,60,190,70,"Li-ion cell","18650 / 21700"); pin(70,130,"+","b"); pin(150,130,"-","b")
box(30,190,190,150,"TP4056 Type-C","DW01A protected",dy=28); pin(70,190,"B+","t"); pin(150,190,"B-","t")
wire([(70,130),(70,190)],C["vbat"]); wire([(150,130),(150,190)],C["gnd"])
pin(220,230,"OUT+","r"); pin(220,265,"OUT-","r")
txt(125,324,"USB-C IN (charge only)",11,"middle","#bfe9e5"); txt(30,358,"VCC / CHRG / STDBY LED circuits: see panel below",11)
# switch
o.append(f'<rect x="290" y="205" width="90" height="50" rx="8" fill="#fff" stroke="{NAVY}" stroke-width="3"/>'); txt(335,226,"SPDT SWITCH",12,"middle",NAVY,True)
txt(298,246,"COM",11); txt(352,246,"OUT",11)
o.append(f'<circle cx="335" cy="255" r="4" fill="#fff" stroke="#888" stroke-width="2"/>'); txt(335,284,"NC (unused)",10,"middle","#555")
txt(335,198,"positive line only",11,"middle")
wire([(220,230),(290,230)],C["vbat"]); wire([(380,230),(440,230)],C["vbat"])
# MT3608
box(440,190,190,110,"MT3608","boost - set to 5.0 V",dy=28); pin(440,230,"VIN+","l"); pin(440,265,"VIN-","l")
wire([(220,265),(440,265)],C["gnd"]); pin(630,230,"OUT+","r"); pin(630,265,"OUT-","r")
# rails
wire([(630,230),(650,230),(650,44),(1270,44),(1270,800)],C["v5"],4)
wire([(630,265),(780,265)],C["gnd"],4); wire([(780,265),(780,800)],C["gnd"],4)
txt(1230,38,"5 V rail (switched, regulated)",12,"end",C["v5"],True); txt(700,255,"GND rail",12,col=C["gnd"],bold=True)
# PN532
box(840,60,360,120,"PN532 NFC V3","I2C mode: S1=ON, S2=OFF")
pin(840,100,"GND","l"); wire([(840,100),(815,100),(815,420),(855,420)],C["gnd"]); dot(855,420,C["gnd"])
pin(880,180,"VCC 3.3V","b"); pin(960,180,"SDA","b"); pin(1030,180,"SCL","b"); pin(1100,180,"RSTO","b"); pin(1165,180,"IRQ","b")
# ESP32
box(840,250,360,140,"ESP32 NodeMCU 30-pin","CP2102, powered via VIN")
pin(840,300,"GND","l"); wire([(780,300),(840,300)],C["gnd"]); dot(780,300,C["gnd"])
pin(1200,300,"VIN","r"); wire([(1200,300),(1270,300)],C["v5"]); dot(1270,300,C["v5"])
pin(880,250,"3V3","t"); pin(960,250,"GPIO21","t"); pin(1030,250,"GPIO22","t"); pin(1100,250,"GPIO5","t"); pin(1165,250,"GPIO4","t")
wire([(880,180),(880,250)],C["v33"]); wire([(960,180),(960,250)],C["sda"]); wire([(1030,180),(1030,250)],C["scl"]); wire([(1100,180),(1100,250)],C["irq"]); wire([(1165,180),(1165,250)],C["irq2"])
pin(855,390,"GND*","b"); pin(925,390,"GPIO16","b"); pin(1010,390,"GPIO17","b")
for x,l,g in ((1070,"VOL-","GPIO25"),(1120,"VOL+","GPIO26"),(1170,"LANG","GPIO27")):
    pin(x,390,g[4:] and g,"b")
    wire([(x,390),(x,408)],C["btn"]); o.append(f'<rect x="{x-21}" y="408" width="42" height="24" rx="4" fill="#fff" stroke="{C["btn"]}" stroke-width="2.5"/>'); txt(x,424,l,11,"middle")
    wire([(x,432),(x,452)],C["btn"]); gnd_sym(x,452); txt(x,482,"GND*",10,"middle")
# DFPlayer
box(840,510,360,150,"DFPlayer Mini","MP3-TF-16P + microSD")
pin(855,510,"GND","t"); pin(925,510,"TX","t"); pin(1010,510,"RX","t")
wire([(855,390),(855,510)],C["gnd"]); wire([(925,390),(925,510)],C["rx"])
wire([(1010,390),(1010,418)],C["tx"]); wire([(1010,448),(1010,510)],C["tx"])
o.append(f'<rect x="998" y="418" width="24" height="30" fill="#fff" stroke="{C["tx"]}" stroke-width="2"/>'); txt(1028,437,"1k",11)
pin(1200,570,"VCC","r"); wire([(1200,570),(1270,570)],C["v5"]); dot(1270,570,C["v5"])
pin(900,660,"DAC_L (5)","b"); pin(960,660,"DAC_R (4)","b"); pin(1030,660,"GND (10)","b")
# PAM8403
box(840,740,360,150,"PAM8403 amplifier","BTL - never ground L- or R-")
pin(900,740,"L in","t"); pin(960,740,"R in","t"); pin(1030,740,"GND in","t")
wire([(900,660),(900,740)],C["aud"]); wire([(960,660),(960,740)],C["audr"]); wire([(1030,660),(1030,740)],C["gnd"])
pin(840,800,"GND","l"); wire([(780,800),(840,800)],C["gnd"]); dot(780,800,C["gnd"])
pin(1200,800,"VCC","r"); wire([(1200,800),(1270,800)],C["v5"]); dot(1270,800,C["v5"])
txt(1050,704,"C1 470 uF + C2 100 nF across",11); txt(1050,720,"5 V and GND at DFPlayer / PAM8403",11)
pin(880,890,"L+","b"); pin(940,890,"L-","b"); pin(1060,890,"R+","b"); pin(1120,890,"R-","b")
# speakers
box(840,960,170,50,"Speaker L"); pin(880,960,"+","t"); pin(940,960,"-","t")
box(1030,960,170,50,"Speaker R"); pin(1060,960,"+","t"); pin(1120,960,"-","t")
for a,b in ((880,880),(940,940),(1060,1060),(1120,1120)): wire([(a,890),(b,960)],C["spk"])
# LED panel
txt(30,392,"Indicator LEDs (each with a 1 kOhm series resistor)",14,col=NAVY,bold=True)
led_chain(424,"TP4056 VCC (USB 5V)",C["v5"],"#E53935","(-)  TP4056 CHRG, pin 7",C["v5"])
led_chain(464,"TP4056 VCC (USB 5V)",C["v5"],"#43A047","(-)  TP4056 STDBY, pin 6",C["v5"])
led_chain(504,"Switched +5 V rail",C["v5"],"#1E88E5","(-)  GND",C["v5"])
txt(30,530,"LED anode (+) on the resistor side. Red = charging, green = fully charged, blue = main power ON.",11)
# legend
lx,ly=30,570
txt(lx,ly,"Legend",14,col=NAVY,bold=True)
items=[("vbat","Battery / protected 3.0-4.2 V (before boost)"),("v5","5 V (MT3608 output)"),("v33","3.3 V (ESP32 3V3 pin)"),("gnd","Ground"),
 ("sda","I2C SDA"),("scl","I2C SCL"),("irq","PN532 RSTO to GPIO5 (monitor input)"),("irq2","PN532 IRQ to GPIO4 (data ready)"),("rx","UART: DFPlayer TX to ESP32 GPIO16"),("tx","UART: ESP32 GPIO17 to DFPlayer RX"),
 ("aud","Analog audio DAC_L to PAM8403 L"),("audr","Analog audio DAC_R to PAM8403 R"),("spk","Speaker pairs (differential)"),("btn","Push buttons (to GND, internal pull-up)")]
for i,(k,l) in enumerate(items):
    y=ly+24+i*21; wire([(lx,y-4),(lx+40,y-4)],C[k]); txt(lx+50,y,l,12)
sy=ly+24+len(items)*21+24
txt(lx,sy,"Notes and safety",14,col=NAVY,bold=True)
notes=["* GND* = ESP32 GND pin beside 3V3: PN532, DFPlayer pin 7 and the 3 buttons.","DFPlayer pin 10 (GND) goes to the PAM8403 GND between L and R.",
"Measure MT3608 output = 5.0 V BEFORE connecting any module.","Switch: TP4056 OUT+ to COM; OUT terminal to MT3608 VIN+.",
"Never connect speaker terminals to ground or to each other (BTL).","PN532 runs from 3.3 V; never feed 5 V into ESP32 GPIO pins.",
"Switch OFF before connecting USB to the ESP32 or charging.","Buttons (top to bottom): D25 vol -, D26 vol +, D27 language.","PN532 RSTO is read only (GPIO5 strapping pin); IRQ on GPIO4.","Verify every pin label on YOUR boards first."]
for i,n in enumerate(notes): txt(lx,sy+22+i*19,"- "+n if not n.startswith("*") else n,12)
o.append('</svg>')
os.makedirs("images/circuit",exist_ok=True)
open("images/circuit/wiring-diagram.svg","w").write("\n".join(o))
print("written")
