#!/usr/bin/env python3
"""Second set of animated SVGs (images/animations/). Usage (repo root): python3 diagrams/generate_more_animations.py
All numbers shown are derived from docs/ or computed in this script; timings and currents are ESTIMATES, not measurements."""
import os
NAVY="#0B2545"; TEAL="#13A89E"; LIGHT="#bfe9e5"; OUT="images/animations"; os.makedirs(OUT,exist_ok=True)
FONT='font-family="Helvetica, Arial, sans-serif"'
def head(w,h,title,desc): return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" {FONT}><title>{title}</title><desc>{desc}</desc><rect width="{w}" height="{h}" fill="#fff"/>'
def T(x,y,t,size=14,col="#222",anc="middle",bold=False,extra=""):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{col}" text-anchor="{anc}"'+(' font-weight="700"' if bold else '')+f' {extra}>{t}</text>'
def R(x,y,w,h,fill=NAVY,stroke="none",sw=0,rx=8,extra=""): return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'
def L(x1,y1,x2,y2,col="#888",w=3,dash=""): return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" stroke-width="{w}" stroke-linecap="round" '+(f'stroke-dasharray="{dash}"' if dash else '')+'/>'
def win(a,b,Tdur,persist=False,e=0.012):
    """opacity animation visible from fraction a to b (or until the end if persist)"""
    if persist: return f'<animate attributeName="opacity" dur="{Tdur}s" repeatCount="indefinite" values="0;0;1;1;0" keyTimes="0;{a:.4f};{a+e:.4f};0.95;1"/>'
    return f'<animate attributeName="opacity" dur="{Tdur}s" repeatCount="indefinite" values="0;0;1;1;0;0" keyTimes="0;{a:.4f};{a+e:.4f};{b:.4f};{b+e:.4f};1"/>'
def G(inner,anim): return f'<g opacity="1">{inner}{anim}</g>'
def dotpath(path,col,Tdur,a,b,r=6):
    return (f'<circle r="{r}" fill="{col}" opacity="0"><animateMotion dur="{Tdur}s" repeatCount="indefinite" path="{path}" keyPoints="0;0;1;1" keyTimes="0;{a:.4f};{b:.4f};1" calcMode="linear"/>'
            f'<animate attributeName="opacity" dur="{Tdur}s" repeatCount="indefinite" values="0;0;1;1;0;0" keyTimes="0;{a:.4f};{a+0.001:.4f};{b:.4f};{b+0.001:.4f};1"/></circle>')
def save(name,body,w,h,title,desc):
    open(f"{OUT}/{name}","w",encoding="utf-8").write(head(w,h,title,desc)+body+"</svg>"); print("wrote",name)

# ================= 1. sequence diagram =================
W,H=1200,640; Td=16.0
lanes=[("NFC tag",110),("PN532",340),("ESP32",570),("DFPlayer Mini",800),("PAM8403 + speakers",1040)]
s=T(600,34,"One tap, step by step (sequence diagram)",20,NAVY,bold=True)
for n,x in lanes:
    s+=R(x-80,56,160,40,NAVY)+T(x,82,n,14,"#fff",bold=True)+L(x,96,x,H-30,"#bbb",2,"6 5")
X={n:x for n,x in lanes}
msgs=[("Tag enters the 13.56 MHz field","NFC tag","PN532","#13A89E","RF"),
 ("poll: InListPassiveTarget (I2C 0x24)","ESP32","PN532","#1E88E5",""),
 ("UID (7 bytes) ready: IRQ goes low","PN532","ESP32","#EF6C00",""),
 ("read pages 4-19 (64 bytes of user memory)","ESP32","PN532","#1E88E5",""),
 ("NDEF bytes returned","PN532","ESP32","#1E88E5",""),
 ("validate: Text record, TML:007, language known","ESP32","ESP32","#222",""),
 ("UART 9600: 7E FF 06 0F 01 02 07 FE E2 EF (folder 02, file 007)","ESP32","DFPlayer Mini","#2E7D32",""),
 ("analog audio on DAC_L and DAC_R","DFPlayer Mini","PAM8403 + speakers","#7B1FA2",""),
 ("amplified audio: speaker L and speaker R play","PAM8403 + speakers","PAM8403 + speakers","#607D8B","")]
n=len(msgs)
for i,(label,a,b,col,note) in enumerate(msgs):
    y=140+i*54; xa,xb=X[a],X[b]; fa=i/(n+1); fb=fa+0.02
    if a==b:
        inner=f'<path d="M{xa},{y} h46 v22 h-46" fill="none" stroke="{col}" stroke-width="3"/><polygon points="{xa},{y+22} {xa+10},{y+16} {xa+10},{y+28}" fill="{col}"/>'+T(xa+56,y+14,label,13,"#222","start")
        if a=="PAM8403 + speakers": inner=inner.replace(f'M{xa},{y} h46 v22 h-46',f'M{xa},{y} h-46 v22 h46').replace(f'{xa+10},{y+16} {xa+10},{y+28}',f'{xa-10},{y+16} {xa-10},{y+28}').replace(T(xa+56,y+14,label,13,"#222","start"),T(xa-56,y+14,label,13,"#222","end"))
    else:
        d=1 if xb>xa else -1
        inner=L(xa,y+12,xb,y+12,col,3)+f'<polygon points="{xb},{y+12} {xb-d*12},{y+5} {xb-d*12},{y+19}" fill="{col}"/>'+T((xa+xb)/2,y+2,label,13,"#222")
    s+=G(inner+T(30,y+16,str(i+1),13,NAVY,"start",True),win(fa,fb,Td,True))
    if a!=b: s+=dotpath(f"M{xa},{y+12} L{xb},{y+12}",col,Td,fa,fa+0.05,6)
s+=T(600,H-8,"Timings are not shown because they were not measured; the firmware polls every 250 ms and releases the latch after about 1 s without a tag.",12,"#555")
save("sequence-tag-to-audio.svg",s,W,H,"Sequence diagram animation","Nine messages appear in order between tag, PN532, ESP32, DFPlayer Mini and amplifier with speakers.")

# ================= 2. NDEF bytes =================
def byte_anim(name,title,bytes_,fields,desc_title,foot,w=1200):
    n=len(bytes_); bw=min(64,(w-60)//n-6); x0=(w-(bw+6)*n)//2+3
    s=T(w/2,34,title,20,NAVY,bold=True)
    for i,b in enumerate(bytes_): s+=R(x0+i*(bw+6),90,bw,52,"#fff",NAVY,3,6)+T(x0+i*(bw+6)+bw/2,124,b,20,NAVY,bold=True)
    cols=["#13A89E","#1E88E5","#EF6C00","#7B1FA2","#C0392B","#2E7D32","#B8860B","#607D8B","#6D4C41","#00897B"]
    tot=len(fields); Tdur=2.2*tot+2
    for k,(lab,first,cnt,desc) in enumerate(fields):
        col=cols[k%len(cols)]; xa=x0+first*(bw+6); wd=cnt*(bw+6)-6
        a=k/(tot+1); b=(k+1)/(tot+1)
        ly=184+(k%2)*20
        s+=R(xa-4,84,wd+8,64,col,"none",0,8,'fill-opacity="0.18"')+R(xa-4,84,wd+8,64,"none",col,3,8)+L(xa,160,xa+wd,160,col,5)+T(xa+wd/2,ly,lab,13,col,bold=True)
        hl=R(xa-6,82,wd+12,68,col,"none",0,8,'fill-opacity="0.35"')+R(xa-6,82,wd+12,68,"none",col,6,8)
        s+=f'<g opacity="0">{hl}{win(a,b,Tdur)}</g>'
        s+=f'<g opacity="0">{T(w/2,250,desc_title+": "+lab,18,col,bold=True)}{T(w/2,280,desc,15,"#222")}{win(a,b,Tdur)}</g>'
    y=325
    s+=T(60,y,"All fields (static reference):",14,NAVY,"start",True)
    for k,(lab,first,cnt,desc) in enumerate(fields):
        s+=T(60,y+24+k*20,f"{lab}: {desc}",12,"#333","start")
    H=y+24+len(fields)*20+40
    s+=T(w/2,H-14,foot,12,"#555")
    save(name,s,w,H,title,"Animated byte-by-byte explanation; each field is highlighted in turn, with a static reference list below.")
byte_anim("ndef-bytes.svg","The tag memory: 17 bytes for TML:007 (language en)",
 ["03","0E","D1","01","0A","54","02","65","6E","54","4D","4C","3A","30","30","37","FE"],
 [("TLV type",0,1,"0x03 = NDEF message TLV (blank tags have no 0x03 here)"),
  ("TLV length",1,1,"0x0E = 14 bytes of NDEF record follow"),
  ("Record header",2,1,"0xD1 = first + last record, short record, type name format 1 (well-known)"),
  ("Type length",3,1,"0x01 = the record type is one byte long"),
  ("Payload length",4,1,"0x0A = 10 bytes: 1 status + 2 language + 7 text"),
  ("Record type",5,1,"0x54 = ASCII T, a Text record"),
  ("Status byte",6,1,"0x02 = UTF-8 text, language code is 2 bytes long"),
  ("Language",7,2,"65 6E = en. The language code of the tag (te = 74 65)"),
  ("Text TML:007",9,7,"54 4D 4C 3A 30 30 37 = TML:007. Medicine ID 7 (valid range 1-255)"),
  ("Terminator",16,1,"0xFE = end of TLV data. Total 17 bytes = 5 pages of 4 bytes")],
 "Field","Generated from the same builder used in tests/ndef_parser_test.cpp. NTAG213 has 36 user pages (144 bytes); this record uses 5 of them.")
# ================= 3. DFPlayer frame =================
byte_anim("dfplayer-frame.svg","DFPlayer command frame: play folder 02, file 007",
 ["7E","FF","06","0F","01","02","07","FE","E2","EF"],
 [("Start",0,1,"0x7E starts every frame"),("Version",1,1,"0xFF fixed version byte"),("Length",2,1,"0x06 = six bytes follow before the checksum (version excluded count per manual)"),
  ("Command",3,1,"0x0F = play a track in a folder (folder 01-99, track 001-255)"),
  ("Feedback",4,1,"0x01 = ask the module to acknowledge (the firmware begins with isACK = true)"),
  ("Param high",5,1,"0x02 = folder 02 (Telugu)"),("Param low",6,1,"0x07 = file 007.mp3 (medicine ID 7)"),
  ("Checksum",7,2,"FE E2 = 0x10000 - (FF+06+0F+01+02+07 = 0x11E) = 0xFEE2"),("End",9,1,"0xEF ends the frame")],
 "Byte","10 bytes x 10 bits per byte / 9600 baud = 10.4 ms on the wire. Volume 9 example: 7E FF 06 06 01 00 09 FE EB EF.")
# ================= 4. charging cycle =================
Td=14.0; s=T(600,34,"TP4056 charging cycle (schematic shape, not measured)",20,NAVY,bold=True)
s+=R(60,80,360,150,"#fff",NAVY,4,10)+R(420,125,24,60,NAVY,"none",0,4)
s+=f'<rect x="68" y="88" width="344" height="134" rx="6" fill="{TEAL}"><animate attributeName="width" values="0;40;150;344;344;0" keyTimes="0;0.12;0.5;0.85;0.97;1" dur="{Td}s" repeatCount="indefinite"/></rect>'
phases=[("Pre-charge: cell below about 2.9 V, small current",0.0,0.12),("Constant current: 1 A until 4.2 V",0.12,0.55),("Constant voltage 4.2 V: current falls",0.55,0.85),("Charge complete: STDBY pin low, green LED",0.85,1.0)]
for lab,a,b in phases: s+=f'<g opacity="0">{T(60,265,lab,16,NAVY,"start",True)}{win(a,min(b,0.98),Td)}</g>'
s+=T(60,310,"Typical datasheet values (not verified in this repository); termination near one tenth of the set current.",12,"#555","start")
# LEDs
s+=f'<circle cx="560" cy="120" r="18" fill="#E53935" opacity="0.25"><animate attributeName="opacity" dur="{Td}s" repeatCount="indefinite" values="0;1;1;0;0" keyTimes="0;0.02;0.84;0.85;1"/></circle>'+T(560,162,"CHRG red",12)
s+=f'<circle cx="650" cy="120" r="18" fill="#43A047" opacity="1"><animate attributeName="opacity" dur="{Td}s" repeatCount="indefinite" values="0;0;1;1;0" keyTimes="0;0.85;0.86;0.97;1"/></circle>'+T(650,162,"STDBY green",12)
# graph
gx,gy,gw,gh=720,70,420,200
s+=R(gx,gy,gw,gh,"#fafafa","#999",1,4)+T(gx+gw/2,gy+gh+22,"time",12)+T(gx-8,gy+14,"V / I",12,"#222","end")
def curve(pts,col,begin,dur): 
    d="M"+" L".join(f"{gx+x*gw},{gy+gh-y*gh}" for x,y in pts)
    return f'<path d="{d}" fill="none" stroke="{col}" stroke-width="4" stroke-dasharray="900" stroke-dashoffset="0"><animate attributeName="stroke-dashoffset" values="900;0;0;900" keyTimes="0;{dur};0.97;1" dur="{Td}s" repeatCount="indefinite"/></path>'
s+=curve([(0,0.2),(0.08,0.35),(0.12,0.55),(0.3,0.68),(0.55,0.78),(0.7,0.78),(1,0.78)],"#1E88E5",0,0.9)+T(gx+gw-4,gy+gh*0.16,"cell voltage",12,"#1E88E5","end",True)
s+=curve([(0,0.12),(0.12,0.12),(0.13,0.8),(0.55,0.8),(0.7,0.45),(0.85,0.1),(1,0.05)],"#EF6C00",0,0.9)+T(gx+gw-4,gy+gh*0.92,"charge current",12,"#EF6C00","end",True)
s+=T(600,370,"Charge with the main switch OFF. The MT3608 never charges the cell; only the TP4056 does.",13,"#222")
save("charging-cycle.svg",s,1200,400,"Charging cycle animation","Battery fills while the red LED is lit; phases are named; the green LED lights when charging completes; schematic voltage and current curves are drawn.")
# ================= 5. MT3608 adjust =================
Td=12.0; s=T(600,34,"Setting the MT3608 to 5.0 V before connecting anything",20,NAVY,bold=True)
s+=R(60,70,420,260,"#1565C0",NAVY,4,14)+T(270,100,"MT3608 (output unconnected)",15,"#fff",bold=True)
s+=R(100,130,120,120,"#1E88E5","#fff",3,10)+'<g transform="translate(160,190)"><circle r="40" fill="#FFD54F" stroke="#333" stroke-width="3"/><line x1="-30" y1="0" x2="30" y2="0" stroke="#333" stroke-width="7" stroke-linecap="round"/><animateTransform attributeName="transform" type="rotate" values="0;540;540;0" keyTimes="0;0.7;0.95;1" dur="12s" repeatCount="indefinite" additive="sum"/></g>'
s=s.replace('<g transform="translate(160,190)">','<g transform="translate(160,190)"><g>',1).replace('<animateTransform attributeName="transform" type="rotate" values="0;540;540;0" keyTimes="0;0.7;0.95;1" dur="12s" repeatCount="indefinite" additive="sum"/></g>','<animateTransform attributeName="transform" type="rotate" values="0;540;540;0" keyTimes="0;0.7;0.95;1" dur="12s" repeatCount="indefinite"/></g></g>')
s+=T(160,275,"trimmer",12,"#fff")+T(380,170,"VIN+ / VIN-",13,"#fff")+T(380,200,"from TP4056 via switch",12,"#bfe9e5")+T(380,260,"OUT+ / OUT-",13,"#fff")+T(380,288,"to the multimeter",12,"#bfe9e5")
s+=R(600,70,360,260,"#212121","#555",4,16)+R(630,100,300,100,"#B2D8B2","#333",3,6)
vals=[("3.70",0.0,0.16),("4.10",0.16,0.32),("4.55",0.32,0.48),("4.90",0.48,0.62),("5.00",0.62,0.97)]
for v,a,b in vals: s+=f'<g opacity="{1 if v=="5.00" else 0}">{T(780,172,v+" V",52,"#1B5E20",bold=True)}{win(a,b,Td)}</g>'
s+=T(780,235,"multimeter, DC volts",13,"#ddd")+T(780,265,"probes on OUT+ and OUT-",12,"#aaa")
s+=f'<g opacity="1">{R(630,280,300,34,"#2E7D32")}{T(780,303,"5.00 V: stop turning, switch OFF",14,"#fff",bold=True)}{win(0.64,0.97,Td)}</g>'
s+=T(600,370,"Turn slowly and watch the meter. The turning direction differs between modules; the meter is the only reference.",13,"#222")
s+=T(600,392,"Never assume the factory setting is 5 V: it may be well above and would destroy the other modules.",13,"#C0392B",bold=True)
save("mt3608-adjust.svg",s,1200,410,"MT3608 adjustment animation","The trimmer rotates while the multimeter reading climbs from 3.70 V to 5.00 V, then a stop message appears.")
# ================= 6. buttons demo =================
Td=18.0; s=T(600,34,"The three buttons (D25 volume down, D26 volume up, D27 language)",20,NAVY,bold=True)
btn=[(180,"D25","VOL -"),(330,"D26","VOL +"),(480,"D27","LANG")]
for x,g,l in btn: s+=f'<circle cx="{x}" cy="150" r="52" fill="#37474F" stroke="#111" stroke-width="4"/>'+T(x,155,l,18,"#fff",bold=True)+T(x,235,g,14,"#333")
presses=[(0,1),(1,1),(2,1),(3,1),(4,0),(5,2),(6,2)]
events=[1,1,1,1,0,2,2]  # which button per event
for e,bi in enumerate(events):
    a=(e+0.5)/(len(events)+1); b=a+0.05; x=btn[bi][0]
    s+=f'<circle cx="{x}" cy="150" r="52" fill="{TEAL}" opacity="0"><animate attributeName="opacity" dur="{Td}s" repeatCount="indefinite" values="0;0;0.85;0;0" keyTimes="0;{a:.4f};{a+0.01:.4f};{b:.4f};1"/></circle>'
# volume ladder
levels=[3,5,7,9,11,13,15]
s+=T(860,90,"Volume (DFPlayer 0-30; firmware range 3-15, step 2)",15,NAVY,bold=True)
for i,v in enumerate(levels): s+=R(670+i*52,110,44,100,"#ECEFF1","#90A4AE",2,6)+T(692+i*52,235,str(v),13)
idx=[3,4,5,6,6,5,5]
kt="0;"+";".join(f"{(e+0.5)/(len(events)+1):.4f}" for e in range(len(events)))+";1"
xs=";".join(str(670+i*52) for i in [3]+idx+[idx[-1]])
s+=f'<rect x="826" y="110" width="44" height="100" rx="6" fill="{TEAL}" opacity="0.6"><animate attributeName="x" dur="{Td}s" repeatCount="indefinite" calcMode="discrete" values="{xs}" keyTimes="{kt}"/></rect>'
s+=T(860,270,"Start at 9. Four presses of + stop at 15 (limit beep). One - goes back to 13.",13,"#555")
# language
s+=T(330,330,"Language (button D27)",15,NAVY,bold=True)
for i,(lab,x) in enumerate((("English",230),("Telugu",430))): s+=R(x-80,350,160,50,"#ECEFF1","#90A4AE",2,8)+T(x,383,lab,16)
a1=5.5/8; a2=6.5/8
s+=f'<rect x="150" y="350" width="160" height="50" rx="8" fill="{TEAL}" opacity="0.35"><animate attributeName="x" dur="{Td}s" repeatCount="indefinite" calcMode="discrete" values="150;350;150;150" keyTimes="0;{a1:.4f};{a2:.4f};1"/></rect>'
s+=T(860,350,"Each press of D27 plays a spoken confirmation (/99/005 English, /99/006 Telugu).",13,"#555")+T(860,372,"Changing language does not replay the medicine: present the tag again.",13,"#555")
save("buttons-demo.svg",s,1200,430,"Buttons demo animation","Button presses light up in sequence; the volume marker moves along a seven-step ladder and the language marker switches between English and Telugu.")
# ================= 7. latch timeline =================
Td=20.0; gx0,gx1=120,1120; sc=(gx1-gx0)/20.0
s=T(600,34,"Same-tag latch and re-detection (illustrative timeline)",20,NAVY,bold=True)
rows=[("Tag in range",100),("Latch",170),("Audio",240)]
for n,y in rows: s+=T(100,y+26,n,14,"#222","end",True)+R(gx0,y,gx1-gx0,40,"#F5F5F5","#CCC",1,4)
for t0,t1 in ((2,8),(11,14.5)): s+=R(gx0+t0*sc,100,(t1-t0)*sc,40,"#90CAF9","#1E88E5",2,4)+T(gx0+(t0+t1)/2*sc,126,"tag present",13)
for t0,t1 in ((2.25,9.0),(11.25,15.5)): s+=R(gx0+t0*sc,170,(t1-t0)*sc,40,"#FFE082","#FFA000",2,4)+T(gx0+(t0+t1)/2*sc,196,"latched: no repeat",13)
for t in (2.3,11.3): s+=R(gx0+t*sc,240,70,40,TEAL,"none",0,4)+T(gx0+t*sc+35,266,"PLAY",14,"#fff",bold=True)
for t,lab in ((9.0,"4 misses (1 s): released"),(15.5,"released")): s+=L(gx0+t*sc,300,gx0+t*sc,330,"#C0392B",2)+T(gx0+t*sc,348,lab,12,"#C0392B")
for k in range(0,81): 
    x=gx0+k*0.25*sc; s+=L(x,296,x,303,"#888",1)
s+=T(gx0,320,"polls every 250 ms",12,"#555","start")
for t in range(0,21,2): s+=T(gx0+t*sc,388,f"{t} s",11,"#555")
s+=f'<line x1="{gx0}" y1="86" x2="{gx0}" y2="296" stroke="#C0392B" stroke-width="3"><animate attributeName="x1" values="{gx0};{gx1}" dur="{Td}s" repeatCount="indefinite"/><animate attributeName="x2" values="{gx0};{gx1}" dur="{Td}s" repeatCount="indefinite"/></line>'
s+=T(600,420,"Holding the tag at 11-14.5 s does not repeat the message. Set REPLAY_AFTER_MS above 0 in config.h to allow timed repeats.",13,"#222")
save("latch-timeline.svg",s,1200,440,"Same-tag latch timeline animation","A playhead sweeps a timeline: first presentation plays audio, the latch blocks repeats while the tag stays, releases after four missed polls, and the next presentation plays again.")
# ================= 8. power budget =================
Td=10.0; s=T(600,34,"Estimated 5 V rail current by load (mA, estimates)",20,NAVY,bold=True)
loads=[("ESP32 (radios off)",65,120),("PN532 polling",35,50),("DFPlayer Mini",25,40),("PAM8403 + 2 x 0.5 W speakers",100,250),("LEDs",3,10)]
scale=2.0; y=80
for n,typ,pk in loads:
    s+=T(300,y+22,n,14,"#222","end")
    s+=f'<rect x="320" y="{y}" width="{typ*scale}" height="20" rx="3" fill="{TEAL}"><animate attributeName="width" values="0;{typ*scale};{typ*scale};0" keyTimes="0;0.35;0.95;1" dur="{Td}s" repeatCount="indefinite"/></rect>'
    s+=f'<rect x="320" y="{y+24}" width="{pk*scale}" height="20" rx="3" fill="#EF6C00"><animate attributeName="width" values="0;0;{pk*scale};{pk*scale};0" keyTimes="0;0.2;0.55;0.95;1" dur="{Td}s" repeatCount="indefinite"/></rect>'
    s+=T(330+typ*scale,y+15,f"{typ}",11,"#fff","start")+T(330+pk*scale,y+39,f"{pk}",11,"#fff","start") if False else ""
    s+=f'<g opacity="0">{T(330+typ*scale,y+15,str(typ),12,"#222","start")}{win(0.36,0.94,Td)}</g>'+f'<g opacity="0">{T(330+pk*scale,y+39,str(pk),12,"#222","start")}{win(0.56,0.94,Td)}</g>'
    y+=64
s+=R(320,y+4,16,16,TEAL,"none",0,3)+T(344,y+17,"typical",13,"#222","start")+R(430,y+4,16,16,"#EF6C00","none",0,3)+T(454,y+17,"peak (speakers at their 0.5 W rating)",13,"#222","start")
tot=[("Rail total","about 230 mA typical, about 470 mA peak"),("Cell side at 3.7 V","about 0.37 A typical, 0.75 A peak"),("Cell side at 3.2 V (nearly empty)","about 0.42 A typical, 0.86 A peak")]
for i,(a,b) in enumerate(tot): s+=T(40,y+60+i*26,a+": ",14,NAVY,"start",True)+T(330,y+60+i*26,b,14,"#222","start")
s+=T(40,y+150,"Boost converter efficiency assumed 85%. MT3608 comfortable range is 1-1.5 A. Overdriving the amplifier would exceed this and damage the speakers.",12,"#555","start")
save("power-budget.svg",s,1200,y+175,"Power budget bar chart animation","Bars grow for typical and peak current of each load, followed by totals on the rail and the cell side.")
# ================= 9. assembly stages =================
steps=[("1","Inspect","no bridges, chips match"),("2","Pinouts","every label found"),("3","Power section","cell, TP4056, switch"),("4","Tune MT3608","exactly 5.0 V"),("5","ESP32 + PN532","I2C + IRQ + RSTO"),("6","DFPlayer","UART + 1k resistor"),
 ("7","Amp + speakers","L- R- not grounded"),("7b","Buttons + LEDs","GPIO25/26/27"),("8","microSD","FAT32 + /01 /02 /99"),("9","Program","switch OFF, USB"),("10","Test tag + audio","plays, no repeat"),("11","Switch + charge","charge with switch OFF")]
Td=18.0; s=T(600,34,"Twelve stages, one checkpoint each",20,NAVY,bold=True)
for i,(n,t,c) in enumerate(steps):
    cx=40+(i%4)*290; cy=70+(i//4)*150
    s+=R(cx,cy,270,120,NAVY)+T(cx+30,cy+40,n,26,TEAL,"middle",True)+T(cx+60,cy+42,t,18,"#fff","start",True)+T(cx+20,cy+84,"Checkpoint: "+c,13,LIGHT,"start")
    a=i/(len(steps)+1)
    s+=R(cx-4,cy-4,278,128,"none",TEAL,6,12,f'opacity="0"')[:-2]+f'><animate attributeName="opacity" dur="{Td}s" repeatCount="indefinite" values="0;0;1;0;0" keyTimes="0;{a:.4f};{a+0.01:.4f};{a+1/(len(steps)+1):.4f};1"/></rect>'
s+=f'<rect x="40" y="520" width="1120" height="14" rx="7" fill="{TEAL}"><animate attributeName="width" values="0;1120" dur="{Td}s" repeatCount="indefinite"/></rect>'+R(40,520,1120,14,"none","#999",1,7)
s+=T(600,560,"Do not advance until the checkpoint passes. Record each result in tests/hardware-validation-checklist.md.",13,"#555")
save("assembly-stages.svg",s,1200,580,"Assembly stages animation","Twelve assembly stage cards are highlighted in turn with a progress bar underneath.")
# ================= 10. enclosure layout =================
Td=8.0; s=T(600,34,"Suggested enclosure layout (design suggestion, untested)",20,NAVY,bold=True)
s+=R(60,70,520,300,"#ECEFF1","#37474F",4,18)+T(320,92,"TOP VIEW",13,"#37474F",bold=True)
s+=f'<circle cx="320" cy="210" r="70" fill="none" stroke="{TEAL}" stroke-width="4" stroke-dasharray="10 8"/>'+T(320,215,"NFC tap zone",16,NAVY,bold=True)+T(320,238,"PN532 antenna below, nothing metal above",12,"#444")
for k in range(3): s+=f'<circle cx="320" cy="210" r="78" fill="none" stroke="{TEAL}" stroke-width="3" opacity="0"><animate attributeName="r" values="30;78" dur="2.4s" begin="{k*0.8}s" repeatCount="indefinite"/><animate attributeName="opacity" values="0.9;0" dur="2.4s" begin="{k*0.8}s" repeatCount="indefinite"/></circle>'
s+=f'<circle cx="320" cy="340" r="9" fill="#37474F"/>'+T(320,362,"raised tactile dot marks the zone",12,"#444")
s+=R(660,70,480,300,"#ECEFF1","#37474F",4,18)+T(900,92,"FRONT / SIDE VIEW",13,"#37474F",bold=True)
for cx,lab in ((740,"Speaker L"),(1060,"Speaker R")):
    s+=f'<circle cx="{cx}" cy="170" r="52" fill="#455A64"/><circle cx="{cx}" cy="170" r="30" fill="#263238"/>'+T(cx,250,lab,13,"#222")
    s+=f'<circle cx="{cx}" cy="170" r="30" fill="none" stroke="#607D8B" stroke-width="3"><animate attributeName="r" values="30;70" dur="2s" repeatCount="indefinite"/><animate attributeName="opacity" values="0.9;0" dur="2s" repeatCount="indefinite"/></circle>'
# buttons with tactile shapes
s+=R(810,150,56,40,"#37474F")+T(838,176,"-",22,"#fff",bold=True)+f'<circle cx="900" cy="170" r="20" fill="#37474F"/>'+T(900,176,"+",22,"#fff",bold=True)+'<polygon points="960,148 984,190 936,190" fill="#37474F"/>'+T(960,184,"L",16,"#fff",bold=True)
s+=T(900,268,"VOL - (square)   VOL + (round)   LANG (triangle)",12,"#222")+T(900,286,"distinct shapes by touch, same order as the GPIOs: D25, D26, D27",11,"#555")
s+=R(700,300,90,50,"#212121")+T(745,330,"SWITCH",12,"#fff")+f'<circle cx="830" cy="325" r="10" fill="#1E88E5"><animate attributeName="opacity" values="0.3;1;0.3" dur="2s" repeatCount="indefinite"/></circle>'+T(830,352,"power",11)
s+=R(900,300,80,50,"#90A4AE")+T(940,330,"USB-C",12,"#fff")+f'<circle cx="1005" cy="316" r="9" fill="#E53935"><animate attributeName="opacity" values="1;0.2;1" dur="6s" repeatCount="indefinite"/></circle><circle cx="1005" cy="338" r="9" fill="#43A047"><animate attributeName="opacity" values="0.2;1;0.2" dur="6s" repeatCount="indefinite"/></circle>'+T(1060,330,"charge LEDs",11,"#444")
s+=T(600,408,"Keep the PN532 antenna facing the tap zone and away from metal parts; keep wires to the I2C header short; insulate the cell and leave ventilation.",12,"#555")
save("enclosure-layout.svg",s,1200,430,"Enclosure layout animation","Top view with the NFC tap zone and pulsing rings, and a front view with two speakers, three differently shaped buttons, power switch, USB-C port and indicator LEDs.")
# ================= 11. troubleshooting flow =================
Td=14.0; s=T(600,34,"No sound? Follow the chain from the top",20,NAVY,bold=True)
chain=[("Blue LED on?","switch OFF / cell empty / MT3608 not 5.0 V"),("Serial: \"PN532 online\"?","DIP S1 ON, S2 OFF; SDA, SCL, IRQ, 3V3; try PN532_IRQ_PIN 0xFF"),("Serial: \"DFPlayer online\"?","TX/RX crossed, 1k resistor, FAT32 card, 5 V, boot delay"),
 ("Tag UID printed?","tag type NTAG, distance 1-4 cm, no metal"),("\"Valid tag ... playing\" printed?","write the Text record TML:nnn with a language code"),("No \"Audio file missing\"?","file name /NN/NNN.mp3, remove ._ files"),("Speaker still silent?","PAM8403 5V, DAC_L/DAC_R, L+/L-, R+/R- wiring, volume")]
for i,(q,fix) in enumerate(chain):
    y=70+i*78
    s+=R(160,y,330,52,NAVY)+T(325,y+32,q,15,"#fff",bold=True)
    s+=L(325,y+52,325,y+78,"#888",3) if i<len(chain)-1 else ""
    s+=L(490,y+26,560,y+26,"#C0392B",3)+R(560,y,520,52,"#FDECEA","#C0392B",2,8)+T(570,y+31,"No: "+fix,13,"#7f1d1d","start")
    a=i/(len(chain)+1)
    s+=f'<rect x="150" y="{y-6}" width="350" height="64" rx="12" fill="none" stroke="{TEAL}" stroke-width="6" opacity="0"><animate attributeName="opacity" dur="{Td}s" repeatCount="indefinite" values="0;0;1;0;0" keyTimes="0;{a:.4f};{a+0.01:.4f};{a+1/(len(chain)+1):.4f};1"/></rect>'
s+=T(100,100,"Yes",12,"#2E7D32","middle",True)
s+=dotpath("M325,96 L325,570","#2E7D32",Td,0.03,0.9,8)
s+=T(600,640,"Yes at every step means the chain is healthy; the first No is where to start. More checks: docs/testing-and-troubleshooting.md",12,"#555")
save("troubleshooting-flow.svg",s,1200,660,"Troubleshooting flow animation","A highlight walks down seven questions; each No answer lists the first things to check.")
