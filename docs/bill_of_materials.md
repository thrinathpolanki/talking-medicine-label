# Bill of Materials

<p align="center"><img src="../images/animations/strip-bom.svg" alt="Animated header: bill of materials" width="100%"></p>

Quantities follow the current circuit. No prices are listed because none were verified. "Photo" means a labelled photograph is in `images/components/` (licence unverified, see [references.md](references.md)).

| # | Part | Qty | Used for | Notes | Photo |
|---|---|---|---|---|---|
| 1 | ESP32 NodeMCU 30-pin, CP2102 | 1 | controller | pins labelled D21, D22, D4, D5, TX2, RX2, D25-D27 | yes |
| 2 | PN532 NFC/RFID V3 module | 1 | NFC reader | I2C mode, plus IRQ and RSTO wires | yes |
| 3 | DFPlayer Mini MP3-TF-16P | 1 | audio from microSD | 3.3 V UART | yes |
| 4 | PAM8403 amplifier module (HW-104) | 1 | drives two speakers | no volume pot | yes |
| 5 | TP4056 Type-C charger with protection | 1 | charging and cell protection | confirm DW01A + 8205A fitted | yes |
| 6 | MT3608 boost converter module | 1 | 5 V supply | adjust to 5.0 V first | yes |
| 7 | Li-ion cell | 1 | power | BOM says 18650; photo is marked INR21700-45E; confirm | yes |
| 8 | Battery holder for that cell | 1 | holds the cell | must match 18650 or 21700 | no |
| 9 | Slide switch, SPDT | 1 | main power | COM, OUT used, NC unused | yes |
| 10 | Tactile push button, 6 mm | 3 | volume down, volume up, language | | yes |
| 11 | LED red 5 mm | 1 | charging indicator | | yes |
| 12 | LED green 5 mm | 1 | fully-charged indicator | | yes |
| 13 | LED blue | 1 | power-on indicator | | yes |
| 14 | Resistor 1 kOhm | 4 | 3 LED limiters, 1 UART series | the supplied resistor photo reads 1 ohm: check bands | illustrative |
| 15 | Electrolytic capacitor 470 uF, 10 V or more | 1 | 5 V rail decoupling | observe polarity | no |
| 16 | Ceramic capacitor 100 nF | 1 | 5 V rail decoupling | | no |
| 17 | Mini speaker 8 ohm 0.5 W | 2 | left and right audio | cap the volume | yes |
| 18 | Prototype PCB (perfboard) | 1 | mounts and wires the parts | | yes |
| 19 | microSD card, 32 GB or less, FAT32 | 1 | audio storage | | no |
| 20 | NTAG213 (or larger) tag or sticker | 1 per medicine | stores TML code | not MIFARE Classic | no |
| 21 | Hook-up wire, headers, solder, heat-shrink | as needed | wiring and insulation | | no |
| 22 | Enclosure, non-conductive | 1 | housing | see [enclosure-and-layout.md](enclosure-and-layout.md) | no |
| 23 | USB-C cable and 5 V charger | 1 | charging | | no |
| 24 | Micro-USB cable | 1 | flashing the ESP32 | switch OFF while connected | no |

## Tools

Multimeter (essential for the MT3608 and continuity checks), soldering iron, wire cutters and strippers, small screwdriver, computer with Arduino IDE.

## Sourcing checklist

- [ ] Photograph every module when it arrives and compare its silkscreen with [pinout-reference.md](pinout-reference.md).
- [ ] Verify the TP4056 board has protection chips.
- [ ] Measure the cell's real size and capacity.
- [ ] Check the resistor colour bands.
- [ ] Format the microSD card and prepare the folders.
