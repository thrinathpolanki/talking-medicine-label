// config.example.h - Hardware and behaviour configuration.
// Optional: copy to "config.h" (git-ignored) to keep personal changes out of version control.
// The sketch uses config.h if it exists, otherwise this file.
//
// GPIO numbers are ESP32 GPIO numbers (not board silkscreen "D" numbers).
// They match docs/circuit-connections.md. If you change a pin, change the wiring too.
#pragma once

// ---- PN532 NFC reader (I2C mode: set DIP switch S1=ON, S2=OFF, power OFF while switching) ----
#define PIN_I2C_SDA          21     // ESP32 GPIO21 -> PN532 SDA/TXD
#define PIN_I2C_SCL          22     // ESP32 GPIO22 -> PN532 SCL/RXD
#define I2C_CLOCK_HZ         100000 // conservative 100 kHz; PN532 is not reliable with long wires at 400 kHz
#define PN532_IRQ_PIN        0xFF   // 0xFF = IRQ/RESET pins not used (polling over I2C)
#define PN532_RESET_PIN      0xFF

// ---- DFPlayer Mini on ESP32 UART2 ----
#define PIN_DFPLAYER_RX      16     // ESP32 RX2 <- DFPlayer TX
#define PIN_DFPLAYER_TX      17     // ESP32 TX2 -> 1 kOhm -> DFPlayer RX
#define DFPLAYER_BAUD        9600   // module default
#define DFPLAYER_VOLUME      9      // start-up volume 0..30 (module default is 30 - far too loud)
#define DFPLAYER_BOOT_DELAY_MS 2000 // module needs ~1.5-3 s after power-up (DFPlayer manual, section 3.3.1)

// ---- Indicators and optional controls ----
#define PIN_STATUS_LED       2      // on-board LED on most 30-pin DevKit boards (verify on yours)
// Three push buttons, each wired GPIO -> button -> GND (internal pull-up, active LOW).
#define PIN_BTN_VOL_DOWN     25     // each press lowers the volume by VOLUME_STEP
#define PIN_BTN_VOL_UP       26     // each press raises the volume by VOLUME_STEP
#define PIN_BTN_LANGUAGE     27     // each press selects the next language
#define BTN_DEBOUNCE_MS      40
#define VOLUME_STEP          2
#define VOLUME_MIN           3      // never fully silent, so the user can always hear prompts
#define VOLUME_MAX           15     // supplied speakers are 8 ohm 0.5 W: calibrate so the amplifier stays near 2 V RMS (docs/power-management.md)

// ---- Tag polling / re-detection behaviour ----
#define TAG_POLL_INTERVAL_MS 250    // time between presence checks
#define TAG_POLL_TIMEOUT_MS  150    // per-check wait for a tag
#define TAG_LOST_MISSES      4      // consecutive misses (~1 s) before the tag counts as removed
#define REPLAY_AFTER_MS      0      // 0 = never replay while the same tag stays in range;
                                    // >0 = replay after this many ms (e.g. 30000)
#define PN532_RECHECK_MS     30000  // periodic PN532 health check
#define INIT_RETRIES         3

// ---- Audio layout on the microSD card (see audio/README.md) ----
// Folder numbers per language, files 001.mp3..255.mp3 = medicine IDs 1..255.
#define FOLDER_EN            1      // /01/001.mp3 ...
#define FOLDER_TE            2      // /02/001.mp3 ... (Telugu)
#define FOLDER_HI            3      // /03/001.mp3 ... (Hindi - planned, files not supplied)
// Languages the language button cycles through, in order: 0 = English, 1 = Telugu, 2 = Hindi.
#define LANG_COUNT           2      // set to 3 once Hindi recordings exist
#define DEFAULT_LANGUAGE     0
// 0 = the language button decides the playback language (tag language only has to be valid)
// 1 = use the language stored on the tag (the button is then only a prompt-language toggle)
#define LANGUAGE_FROM_TAG    0
#define FOLDER_SYSTEM        99     // /99/001.mp3 .. system prompts below
#define ENABLE_SYSTEM_PROMPTS 1     // 1 = speak error/ready prompts (requires the files in /99/)
#define SYS_READY            1      // "Device ready"
#define SYS_TAG_UNRECOGNISED 2      // "This tag is not recognised"
#define SYS_AUDIO_MISSING    3      // "Audio for this medicine is missing"
#define SYS_NFC_ERROR        4      // "Tag could not be read, hold it steady and try again"
#define SYS_LANG_EN          5      // "English"
#define SYS_LANG_TE          6      // "Telugu" (spoken in Telugu)
#define SYS_LANG_HI          7      // "Hindi"  (only needed if LANG_COUNT is 3)
#define SYS_VOLUME_LIMIT     8      // short beep at minimum/maximum volume (optional file)
