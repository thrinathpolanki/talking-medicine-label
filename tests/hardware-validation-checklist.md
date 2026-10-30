# Hardware Validation Checklist

<p align="center"><img src="../images/animations/checklist.svg" alt="Animated validation checklist ticking item by item" width="100%"></p>


Fill in on the real build. Blank = not done.

| # | Check | Expected | Measured / result | Date | Initials |
|---|---|---|---|---|---|
| 1 | Cell voltage | 3.0-4.2 V | | | |
| 2 | TP4056 has DW01A + 8205A fitted | Yes | | | |
| 3 | TP4056 charge LEDs | Red charging, green full | | | |
| 4 | MT3608 output (no load) | 5.0 V | | | |
| 5 | 5 V rail under load | 4.9-5.1 V | | | |
| 6 | ESP32 3V3 | 3.3 V | | | |
| 7 | PN532 I2C scan | 0x24 | | | |
| 8 | DFPlayer init message | "DFPlayer online" | | | |
| 9 | PAM8403 L- and R- to GND continuity | Open | | | |
| 10 | Tag English id 1 plays /01/001.mp3 | Correct audio | | | |
| 11 | Select Telugu with the language button, present tag id 1 | Plays /02/001.mp3 | | | |
| 12 | Same tag held: no repeat | Single playback | | | |
| 13 | Remove and re-present: replays | Yes | | | |
| 14 | Blank tag | "Not recognised" prompt | | | |
| 15 | Missing audio file | "Audio missing" prompt | | | |
| 16 | No SD card | Error pattern; no crash | | | |
| 17 | Loud playback: no ESP32 reset | No reset | | | |
| 18 | Charge with switch OFF; time to green | | | | |
| 19 | Real cell capacity (discharge test) | | | | |
| 20 | Library versions used | record | | | |
| 28 | PN532 IRQ (GPIO4) idles high, goes low when a reply is ready | 3.3 V idle | | | |
| 29 | PN532 RSTO (GPIO5) idles high (3.3 V); firmware only reads it | 3.3 V | | | |
| 27 | Switch: continuity COM to OUT in ON, open in OFF; NC unused | As stated | | | |
| 21 | Red LED lit while charging; green when full | As described | | | |
| 22 | Blue LED lit when switch ON | Lit | | | |
| 23 | Volume up/down buttons change loudness, limits reached | Min 3, max 15 | | | |
| 24 | Language button cycles English/Telugu with spoken confirmation | Yes | | | |
| 25 | Both speakers play; hum check with GND_in arrangement | No hum | | | |
| 26 | AC voltage across each speaker at VOLUME_MAX (1 kHz test file) | 2 V RMS or less (0.5 W into 8 ohm) | | | |
