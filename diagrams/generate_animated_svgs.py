#!/usr/bin/env python3
"""Generates the animated SVGs in images/animations/ (SMIL animation; GitHub shows these when embedded with <img>).
Usage (repo root): python3 diagrams/generate_animated_svgs.py"""
import os
NAVY="#0B2545"; TEAL="#13A89E"; LIGHT="#bfe9e5"
OUT="images/animations"; os.makedirs(OUT,exist_ok=True)
FONT='font-family="Helvetica, Arial, sans-serif"'

def head(w,h,title,desc,bg=None):
    s=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" {FONT}><title>{title}</title><desc>{desc}</desc>'
    if bg: s+=f'<rect width="{w}" height="{h}" fill="{bg}"/>'
    return s
def text(x,y,t,size=14,col="#fff",anc="middle",bold=False):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{col}" text-anchor="{anc}"'+(' font-weight="700"' if bold else '')+f'>{t}</text>'
def box(x,y,w,h,title,sub="",fill=NAVY,tcol="#fff"):
    s=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{fill}"/>'
    s+=text(x+w/2,y+h/2-(2 if sub else -5),title,15,tcol,bold=True)
    if sub: s+=text(x+w/2,y+h/2+16,sub,11,LIGHT if fill==NAVY else "#444")
    return s
def ripple(cx,cy,col=TEAL,rmax=46,dur=2.4,n=3,r0=8):
    s=""
    for k in range(n):
        d=dur*k/n
        s+=(f'<circle cx="{cx}" cy="{cy}" r="{r0}" fill="none" stroke="{col}" stroke-width="3">'
            f'<animate attributeName="r" values="{r0};{rmax}" dur="{dur}s" begin="{d:.2f}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0.9;0" dur="{dur}s" begin="{d:.2f}s" repeatCount="indefinite"/></circle>')
    return s
def line(x1,y1,x2,y2,col="#888",w=3): return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" stroke-width="{w}" stroke-linecap="round"/>'
def seq_dot(path,col,i,n,T=8.0,r=6):
    a=i/n; b=a+0.85/n
    kt=f"0;{a:.4f};{b:.4f};1"
    return (f'<circle r="{r}" fill="{col}" opacity="0">'
      f'<animateMotion dur="{T}s" repeatCount="indefinite" path="{path}" keyPoints="0;0;1;1" keyTimes="{kt}" calcMode="linear"/>'
      f'<animate attributeName="opacity" dur="{T}s" repeatCount="indefinite" values="0;0;1;1;0;0" keyTimes="0;{a:.4f};{a+0.001:.4f};{b:.4f};{b+0.001:.4f};1"/></circle>')
def pulse(cx,cy,r,col,dur=2,begin=0,lo=0.15):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{col}"><animate attributeName="opacity" values="{lo};1;{lo}" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/></circle>'
def blink(cx,cy,r,col,T,i,n):
    a=i/n; b=(i+1)/n
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{col}" opacity="0.15"><animate attributeName="opacity" dur="{T}s" repeatCount="indefinite" '
            f'values="0.15;0.15;1;1;0.15;0.15" keyTimes="0;{a:.3f};{a+0.001:.3f};{b:.3f};{b+0.001:.3f};1"/></circle>')
def save(name,body,w,h,title,desc,bg="#ffffff"):
    s=head(w,h,title,desc,bg)+body+"</svg>"
    open(f"{OUT}/{name}","w",encoding="utf-8").write(s); print("wrote",name)

# ---------- 1. animated banner ----------
b=text(60,110,"Talking Medicine Label",54,"#fff","start",True)
b+=text(60,158,"An IoT-based assistive medicine information and audio system",22,LIGHT,"start")
b+=text(60,190,"for visually impaired people",22,LIGHT,"start")
b+=text(60,238,"ESP32 / PN532 NFC / DFPlayer Mini / PAM8403 - Community Service Project (CSP)",16,"#fff","start")
b+=ripple(1000,140,TEAL,95,3.0,4,10)
b+='<rect x="982" y="122" width="22" height="36" rx="4" fill="#fff"/><path d="M1004 122 l24 -16 v68 l-24 -16z" fill="#fff"/>'
b+=f'<rect x="0" y="268" width="1200" height="12" fill="{TEAL}"/><rect x="0" y="268" width="240" height="12" fill="#fff" opacity="0.7"><animate attributeName="x" values="-240;1200" dur="4s" repeatCount="indefinite"/></rect>'
save("banner-animated.svg",b,1200,280,"Talking Medicine Label animated banner","Navy banner with the project title, pulsing NFC rings and a moving highlight bar. Decorative; not a photograph of the hardware.",NAVY)

# ---------- 2. signal flow ----------
nodes=[(30,"NFC tag","TML:007 + lang"),(230,"PN532","NFC reader, I2C"),(430,"ESP32","controller"),(630,"DFPlayer Mini","microSD audio"),(830,"PAM8403","stereo amp"),(1030,"Speakers","L and R")]
s=text(600,38,"From tag to spoken instruction",20,NAVY,bold=True)
for x,t,sub in nodes: s+=box(x,120,150,90,t,sub)
labels=["RF","I2C+IRQ","UART2","DAC L/R","BTL L/R"]
cols=["#13A89E","#1E88E5","#2E7D32","#7B1FA2","#607D8B"]
for i in range(5):
    x1=nodes[i][0]+150; x2=nodes[i+1][0]
    s+=line(x1,165,x2,165,cols[i],4)+text((x1+x2)/2,152,labels[i],11,"#333")
n=8
for i in range(5): s+=seq_dot(f"M{nodes[i][0]+150},165 L{nodes[i+1][0]},165",cols[i],i,n,8.0,7)
s+=box(430,260,150,50,"3 buttons","vol +/-, language",fill=TEAL,tcol="#fff")
s+=line(505,260,505,210,"#6D4C41",4)+text(560,240,"GPIO25/26/27",11,"#333","start")
s+=seq_dot("M505,260 L505,210","#6D4C41",6,n,8.0,7)
s+=ripple(180,165,TEAL,34,2.4,2,6)+ripple(1165,165,"#607D8B",30,2.4,3,6)
s+=text(600,345,"Dots show the direction of data; the animation repeats forever.",12,"#555")
save("signal-flow.svg",s,1200,360,"Signal flow animation","Animated flow from NFC tag through PN532, ESP32, DFPlayer Mini and PAM8403 amplifier to two speakers, with buttons feeding the ESP32.")

# ---------- 3. power flow ----------
s=text(600,30,"Power flow",20,NAVY,bold=True)
s+=box(30,150,130,80,"Li-ion cell","18650 / 21700")
s+=box(210,150,150,80,"TP4056","Type-C + protection")
s+=box(410,150,110,80,"Switch","COM to OUT")
s+=box(570,150,150,80,"MT3608","boost to 5.0 V")
s+=box(210,52,150,50,"USB-C 5 V","charging only",fill=TEAL)
s+=line(285,102,285,150,"#C0392B",4)+seq_dot("M285,102 L285,150","#C0392B",0,10,10.0,6)
s+=line(160,190,210,190,"#E67E22",4)+line(360,190,410,190,"#E67E22",4)+line(520,190,570,190,"#E67E22",4)
s+=seq_dot("M210,190 L160,190","#E67E22",1,10,10.0,6)+seq_dot("M360,190 L410,190","#E67E22",2,10,10.0,6)+seq_dot("M520,190 L570,190","#E67E22",3,10,10.0,6)
s+=text(390,125,"Charge LEDs",11,"#333")+blink(380,138,9,"#E53935",4.0,0,2)+blink(405,138,9,"#43A047",4.0,1,2)
s+=text(390,160,"",1)
# rail
s+=line(720,190,760,190,"#C0392B",5)+line(760,190,760,262,"#C0392B",5)+line(760,262,1160,262,"#C0392B",6)
s+=text(1100,250,"5 V rail",12,"#C0392B","end",True)
s+=seq_dot("M720,190 L760,190 L760,262 L1160,262","#C0392B",4,10,10.0,7)
cons=[(780,"ESP32","+ PN532 3.3 V"),(920,"DFPlayer","VCC"),(1050,"PAM8403","5V"),]
for x,t,sub in cons:
    s+=box(x,310,120,60,t,sub); s+=line(x+60,262,x+60,310,"#C0392B",4)
    s+=seq_dot(f"M{x+60},262 L{x+60},310","#C0392B",5+cons.index((x,t,sub)),10,10.0,6)
s+=text(1170,345,"",1)
s+=f'<circle cx="1000" cy="215" r="0"/>'
s+=line(650,230,650,300,"#C0392B",3)  # branch to blue LED
s+=box(600,300,100,50,"Blue LED","power ON",fill="#1E88E5")+pulse(650,285,10,"#1E88E5",2.0)
s+=text(600,400,"Orange = battery side (3.0-4.2 V), red = regulated 5 V. Red/green LEDs alternate to show the two charge states.",12,"#555")
save("power-flow.svg",s,1200,420,"Power flow animation","Animated power path: USB-C charges the cell through the TP4056, the switch feeds the MT3608 boost converter, and the 5 V rail feeds ESP32, DFPlayer, PAM8403 and the blue LED.")

# ---------- 4. NFC read ----------
s=text(450,30,"Reading a tag",20,NAVY,bold=True)
s+=box(60,90,200,110,"PN532","NFC reader")+ripple(260,145,TEAL,70,2.4,3,10)
s+=('<g><rect x="340" y="105" width="170" height="80" rx="10" fill="#fff" stroke="'+NAVY+'" stroke-width="4"/>'
    +text(425,140,"NTAG213",15,NAVY,bold=True)+text(425,164,"tag on medicine box",11,"#444")
    +'<animateTransform attributeName="transform" type="translate" values="340 0;0 0;0 0;340 0" keyTimes="0;0.4;0.8;1" dur="8s" repeatCount="indefinite"/></g>')
s+=f'<g opacity="1"><animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;0.42;0.5;0.8;1" dur="8s" repeatCount="indefinite"/>'+text(450,245,"Text record: language te, text TML:007",14,NAVY,bold=True)+text(450,270,"ESP32 plays /02/007.mp3 (folder 02 = Telugu)",13,"#333")+'</g>'
save("nfc-read.svg",s,900,300,"NFC tag reading animation","A tag slides next to the PN532 reader, radio rings pulse, then the decoded record and the audio file name appear.")

# ---------- 5. audio chain ----------
s=text(500,30,"Audio path",20,NAVY,bold=True)
s+=box(40,100,140,90,"microSD","/01 /02 /99")+box(240,100,160,90,"DFPlayer Mini","DAC_L, DAC_R")+box(470,100,160,90,"PAM8403","HW-104, BTL")
s+=box(780,40,170,60,"Speaker L","L+ / L-")+box(780,160,170,60,"Speaker R","R+ / R-")
s+=line(180,145,240,145,"#888",4)+line(400,125,470,125,"#7B1FA2",4)+line(400,165,470,165,"#AB47BC",4)
s+=line(630,125,700,125,"#607D8B",4)+line(700,125,700,70,"#607D8B",4)+line(700,70,780,70,"#607D8B",4)
s+=line(630,165,700,165,"#607D8B",4)+line(700,165,700,190,"#607D8B",4)+line(700,190,780,190,"#607D8B",4)
s+=seq_dot("M180,145 L240,145","#888",0,6,6.0)+seq_dot("M400,125 L470,125","#7B1FA2",1,6,6.0)+seq_dot("M400,165 L470,165","#AB47BC",1,6,6.0)
s+=seq_dot("M630,125 L700,125 L700,70 L780,70","#607D8B",3,6,6.0)+seq_dot("M630,165 L700,165 L700,190 L780,190","#607D8B",3,6,6.0)
s+=ripple(950,70,"#607D8B",40,2.0,3,6)+ripple(950,190,"#607D8B",40,2.0,3,6)
s+=text(435,118,"DAC_L",10,"#7B1FA2")+text(435,184,"DAC_R",10,"#AB47BC")
save("audio-chain.svg",s,1000,250,"Audio path animation","Audio flows from microSD through the DFPlayer Mini DAC outputs to the PAM8403 and then to the left and right speakers.")

# ---------- 6. firmware states ----------
steps=["Poll tag","Read memory","Validate TML","Play audio","Wait for removal"]
s=text(500,34,"Firmware loop",20,NAVY,bold=True)
for i,t in enumerate(steps):
    cx=100+i*200
    s+=f'<circle cx="{cx}" cy="130" r="58" fill="#fff" stroke="{NAVY}" stroke-width="4"/>'
    s+=f'<circle cx="{cx}" cy="130" r="58" fill="{TEAL}" opacity="0"><animate attributeName="opacity" dur="10s" repeatCount="indefinite" values="0;0;0.9;0.9;0;0" keyTimes="0;{i/5:.3f};{i/5+0.001:.3f};{(i+1)/5:.3f};{(i+1)/5+0.001:.3f};1"/></circle>'
    s+=text(cx,135,t,13,NAVY,bold=True)
    if i<4: s+=line(cx+60,130,cx+140,130,NAVY,3)+f'<polygon points="{cx+140},130 {cx+130},124 {cx+130},136" fill="{NAVY}"/>'
s+=f'<path d="M900,190 C900,250 100,250 100,190" fill="none" stroke="{NAVY}" stroke-width="3" stroke-dasharray="8 6"/>'
s+=text(500,262,"tag removed: ready for the next tag. Buttons are checked on every pass.",12,"#555")
save("firmware-states.svg",s,1000,280,"Firmware loop animation","Five states highlighted in turn: poll tag, read memory, validate record, play audio, wait for tag removal, then repeat.")

# ---------- 7. checklist ----------
items=["MT3608 measured at 5.0 V","PN532 found at I2C 0x24","DFPlayer online, SD card read","Tag plays the right recording","Same tag does not repeat","Buttons change volume and language","Charging LEDs and switch work"]
s=text(300,32,"Validation checklist",20,NAVY,bold=True)
T=14.0
for i,t in enumerate(items):
    y=60+i*44; a=i/(len(items)+1); 
    s+=f'<rect x="30" y="{y}" width="28" height="28" rx="5" fill="#fff" stroke="{NAVY}" stroke-width="3"/>'
    s+=(f'<path d="M36,{y+15} L43,{y+22} L53,{y+7}" fill="none" stroke="{TEAL}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="30" stroke-dashoffset="0">'
        f'<animate attributeName="stroke-dashoffset" dur="{T}s" repeatCount="indefinite" values="30;30;0;0;30" keyTimes="0;{a:.3f};{a+0.04:.3f};0.93;1"/></path>')
    s+=text(76,y+20,t,15,"#222","start")
save("checklist.svg",s,620,380,"Checklist animation","Seven validation items are ticked one after another, then the animation restarts.")

# ---------- 8. section strips ----------
def strip(name,title,subtitle,kind="waves"):
    w,h=1200,130
    s=text(40,62,title,36,"#fff","start",True)+text(40,98,subtitle,16,LIGHT,"start")
    if kind=="warning":
        s+=f'<g><polygon points="1090,30 1140,110 1040,110" fill="none" stroke="#FFB300" stroke-width="6" stroke-linejoin="round"/>'+text(1090,100,"!",44,"#FFB300",bold=True)+'<animate attributeName="opacity" values="1;0.35;1" dur="1.6s" repeatCount="indefinite"/></g>'
    elif kind=="steps":
        for i in range(12):
            s+=f'<circle cx="{660+i*42}" cy="65" r="14" fill="{TEAL}" opacity="0.2"><animate attributeName="opacity" values="0.2;1;0.2" dur="6s" begin="{i*0.5}s" repeatCount="indefinite"/></circle>'+text(660+i*42,70,str(i+1),12,"#fff",bold=True)
    else:
        s+=ripple(1090,65,TEAL,55,3.0,3,8)+f'<circle cx="1090" cy="65" r="9" fill="{TEAL}"/>'
    s+=f'<rect x="0" y="118" width="1200" height="12" fill="{TEAL}"/><rect x="0" y="118" width="200" height="12" fill="#fff" opacity="0.65"><animate attributeName="x" values="-200;1200" dur="4s" repeatCount="indefinite"/></rect>'
    save(name,s,w,h,title+" header animation",subtitle+". Decorative animated header.",NAVY)
strip("strip-contributing.svg","Contributing","Help improve the build, the docs and the audio")
strip("strip-security.svg","Security and safety policy","No network features, no personal data","warning")
strip("strip-overview.svg","Project overview","Tag, reader, controller, audio, speakers")
strip("strip-components.svg","Hardware components","Modules, accessories and specifications")
strip("strip-circuit.svg","Circuit connections","Verified against the author's reference diagram")
strip("strip-assembly.svg","Assembly guide","Twelve stages, each with a checkpoint","steps")
strip("strip-safety.svg","Safety guidelines","Medical and electrical precautions","warning")
strip("strip-limitations.svg","Limitations and future work","What is not done yet")
strip("strip-references.svg","References and image register","Sources, status and licences")
strip("strip-troubleshooting.svg","Testing and troubleshooting","Symptoms, causes and meter checks")
