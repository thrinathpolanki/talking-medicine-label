# References and Image Source Register

<p align="center"><img src="../images/animations/strip-references.svg" alt="Animated header: references and image register" width="100%"></p>


"Opened" = the page was opened/read during authoring. "Listed" = standard reference not opened in this session.

## Technical sources

| # | Source | URL | Status | Used for |
|---|---|---|---|---|
| 1 | ShillehTek PN532 V3 manual | https://shillehtek.com/blogs/shillehtek-product-manuals/pn532-nfc-rfid-reader-writer-module-v3-manual | Opened | I2C/SPI/UART DIP settings, 0x24, ESP32 wiring (3V3, GPIO21/22), current |
| 2 | DFPlayer Mini manual (DFR0299) | https://robu.in/wp-content/uploads/2017/06/DFR0299-DFPlayer-Mini-Manual.pdf | Opened | VCC 3.2-5 V, 3.3 V UART, 1 kOhm series resistor, DAC_L/DAC_R, folders, 2-3 s init |
| 3 | DFRobot DFPlayer wiki and library | https://wiki.dfrobot.com/DFPlayer_Mini_SKU_DFR0299 , https://github.com/DFRobot/DFRobotDFPlayerMini | Opened (search extracts) | `begin(stream, isACK, doReset)`, ESP32 serial example |
| 4 | enjoyneering DFPlayer library | https://github.com/enjoyneering/DFPlayer | Listed (alternative) | Not used |
| 5 | Envistia PAM8403 guide | https://envistiamall.com/blogs/learn/pam8403-stereo-audio-amplifier-with-volume-control-switch-user-guide | Opened | BTL warning, 2.5-5.5 V, DFPlayer hook-up, decoupling |
| 6 | PAM8403 datasheet (Diodes Inc.) | https://www.mouser.com/datasheet/2/115/PAM8403-247318.pdf | Link taken from source 5, not opened | Reference |
| 7 | Robu TP4056 Type-C module page | https://robu.in/?p=835842 | Opened (search extract) | IN/B/OUT pads, disconnect load while charging, LEDs |
| 8 | ShillehTek TP4056 Type-C manual | https://shillehtek.com/blogs/shillehtek-product-manuals/tp4056-1a-lipo-battery-charging-board-type-c-with-current-protection-manual | Opened (search extract) | DW01A + 8205A, 4.28 V / 2.5 V / about 3 A thresholds |
| 9 | MT3608 notes (Robu, Envistia) | https://robu.in/?p=29763 , https://support.envistiamall.com/kb/mt3608-2v-28v-2a-dc-dc-step-up-boost-power-supply-voltage-converter-module/ | Opened (search extracts) | 2-24 V in, 5-28 V out, 2 A max, pot direction |
| 10 | ESP32 30-pin pin guides | https://esp32.co.uk/esp32-nodemcu-30-pin-pinout-safe-gpios/ , https://www.emertxe.com/content/arduino/esp32-devkit-pinout.pdf | Opened (search extracts) | GPIO16/17 (RX2/TX2), 21/22 availability; board variants differ |
| 11 | NXP NTAG213/215/216 datasheet | https://nxp.com/docs/en/data-sheet/NTAG213_215_216.pdf | Opened (search extract) | 144 bytes user memory, pages 4-39 |
| 12 | Adafruit PN532 library | https://github.com/adafruit/Adafruit-PN532 | Listed | `ntag2xx_ReadPage`, I2C constructor |

## Author-supplied reference diagram

`images/circuit/reference-wiring-diagram.jpg` was supplied by the project author and is used as the reference for the final connections. The diagram embeds photographs of the components whose original sources and licences are **not recorded**. Before publishing the repository publicly, replace it with a version built from your own photographs or from images whose licence allows redistribution, or remove the file and keep the schematic SVG.

## Component photograph register

The photographs below were **supplied by the project author** (uploaded in one batch). The original URLs, authors and licences were not recorded, so every row is **licence unverified**. They look like supplier product images; do not publish the repository publicly with them until you have confirmed the rights or replaced them with your own photographs. The two-view images were assembled by placing two supplied photos side by side (no other editing).

| Component | Local file | Original URL | Author/source | Licence/permission | Revision shown |
|---|---|---|---|---|---|
| MT3608 boost (Micro-USB) | `images/components/mt3608-boost-converter.png` | not recorded | supplied by author | unverified | VIN+/VIN-/OUT+/OUT- silkscreen, 3296 trimmer |
| TP4056 Type-C | `images/components/tp4056-type-c-charger.png` | not recorded | supplied by author | unverified | Type-C, LED1/LED2 footprints |
| PAM8403 (two views) | `images/components/pam8403-amplifier-module.png` | not recorded | supplied by author | unverified | right view marked HW-104 |
| DFPlayer Mini (two views) | `images/components/dfplayer-mini-mp3-tf-16p.png` | not recorded | supplied by author | unverified | MP3-TF-16P V3.0 |
| ESP32 NodeMCU 30-pin | `images/components/esp32-nodemcu-30-pin.png` | not recorded | supplied by author | unverified | 30-pin, micro-USB, EN/BOOT buttons |
| PN532 V3 | `images/components/pn532-nfc-module-v3.png` | not recorded | supplied by author | unverified | red board, mode DIP switch, I2C header |
| Li-ion cell | `images/components/li-ion-cell-inr21700.png` | not recorded | supplied by author | unverified | marking reads INR21700-45E (a 21700 cell) |
| Slide switch | `images/components/slide-switch-spdt.png` | not recorded | supplied by author | unverified | three-lug SPDT |
| Resistor | `images/components/resistor-carbon-film.png` | not recorded | supplied by author | unverified | bands read 1 ohm, not 1 kOhm: illustrative only |
| Red LED | `images/components/led-red-5mm.png` | not recorded | supplied by author | unverified | 5 mm |
| Green LED | `images/components/led-green-5mm.png` | not recorded | supplied by author | unverified | 5 mm |
| Blue LED | `images/components/led-blue-rectangular.png` | not recorded | supplied by author | unverified | rectangular |
| Speaker | `images/components/speaker-8ohm-0.5w.png` | not recorded | supplied by author | unverified | marked 8 ohm 0.5 W |
| Prototype PCB | `images/components/perfboard-prototype-pcb.png` | not recorded | supplied by author | unverified | perfboard |
| Tactile push button | `images/components/push-button-tactile-6mm.png` | not recorded | supplied by author | unverified | 6 mm, four legs |
| NFC tag | pending | | | | |
| microSD card | pending | | | | |

Supplier product pages (copyright of each vendor; link only): ShillehTek PN532 https://shillehtek.com/products/pn532-nfc-rfid-reader-writer-module-v3 ; Robu MT3608 https://robu.in/?p=29763 ; Robu TP4056 https://robu.in/?p=835842 ; Envistia PAM8403 guide (source 5).
