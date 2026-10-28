/*
  Talking Medicine Label - ESP32 + PN532 (I2C) + DFPlayer Mini (UART2)
  CSP project firmware. NOT yet compiled or hardware-tested by the author of this
  repository snapshot - see README "Testing status".

  Buttons: GPIO25 volume down, GPIO26 volume up, GPIO27 language.
  Flow: poll PN532 -> read NTAG NDEF Text record "TML:<id>" with language code ->
        play /<languageFolder>/<id>.mp3 on the DFPlayer Mini. The same tag is not replayed
        while it stays in range (latch), and is re-armed once it has been removed.

  Libraries: Adafruit PN532 (+Adafruit BusIO), DFRobotDFPlayerMini. Board: "ESP32 Dev Module".
*/
#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_PN532.h>
#include <DFRobotDFPlayerMini.h>
#include "ndef_parser.h"

#if __has_include("config.h")
  #include "config.h"
#else
  #include "config.example.h"
#endif

// Forward declarations (used by the button handler defined before them)
void blink(uint8_t n, uint16_t onMs, uint16_t offMs);
void playSystem(uint8_t track);

Adafruit_PN532 nfc(PN532_IRQ_PIN, PN532_RESET_PIN, &Wire);
DFRobotDFPlayerMini dfp;
HardwareSerial& dfSerial = Serial2;

bool pn532Online = false;
bool dfOnline = false;

// Same-tag latch
bool     tagLatched = false;
uint8_t  latchedUid[7];
uint8_t  latchedLen = 0;
uint8_t  misses = 0;
uint32_t latchedAt = 0;
uint8_t  lastFolder = 0, lastTrack = 0;
uint8_t  volume = DFPLAYER_VOLUME;
uint8_t  activeLang = DEFAULT_LANGUAGE;   // index into langFolder[]
const uint8_t langFolder[3] = {FOLDER_EN, FOLDER_TE, FOLDER_HI};
const uint8_t langPrompt[3] = {SYS_LANG_EN, SYS_LANG_TE, SYS_LANG_HI};

struct Button { uint8_t pin; bool lastLevel; uint32_t changedAt; };
Button btnDown = {PIN_BTN_VOL_DOWN, HIGH, 0};
Button btnUp   = {PIN_BTN_VOL_UP,   HIGH, 0};
Button btnLang = {PIN_BTN_LANGUAGE, HIGH, 0};

// Returns true once per debounced press (falling edge, pull-up input).
bool buttonPressed(Button& b) {
  bool level = digitalRead(b.pin);
  if (level != b.lastLevel && millis() - b.changedAt > BTN_DEBOUNCE_MS) {
    b.lastLevel = level;
    b.changedAt = millis();
    return level == LOW;
  }
  return false;
}

void handleButtons() {
  if (buttonPressed(btnUp)) {
    volume = (volume + VOLUME_STEP > VOLUME_MAX) ? VOLUME_MAX : volume + VOLUME_STEP;
    if (dfOnline) dfp.volume(volume);
    Serial.printf("Volume %u\n", volume);
    if (volume == VOLUME_MAX) { blink(2, 80, 80); playSystem(SYS_VOLUME_LIMIT); }
  }
  if (buttonPressed(btnDown)) {
    volume = (volume < VOLUME_MIN + VOLUME_STEP) ? VOLUME_MIN : volume - VOLUME_STEP;
    if (dfOnline) dfp.volume(volume);
    Serial.printf("Volume %u\n", volume);
    if (volume == VOLUME_MIN) { blink(2, 80, 80); playSystem(SYS_VOLUME_LIMIT); }
  }
  if (buttonPressed(btnLang)) {
    activeLang = (activeLang + 1) % LANG_COUNT;
    Serial.printf("Language selected: %u (folder %u)\n", activeLang, langFolder[activeLang]);
    playSystem(langPrompt[activeLang]);   // spoken confirmation
  }
}

// ---------- helpers ----------
void blink(uint8_t n, uint16_t onMs, uint16_t offMs) {
  for (uint8_t i = 0; i < n; i++) {
    digitalWrite(PIN_STATUS_LED, HIGH); delay(onMs);
    digitalWrite(PIN_STATUS_LED, LOW);  delay(offMs);
  }
}

void playSystem(uint8_t track) {
#if ENABLE_SYSTEM_PROMPTS
  if (dfOnline) dfp.playFolder(FOLDER_SYSTEM, track);
#endif
}

uint8_t folderForLang(const char* lang) {
  if (!strncmp(lang, "en", 2)) return FOLDER_EN;
  if (!strncmp(lang, "te", 2)) return FOLDER_TE;
  if (!strncmp(lang, "hi", 2)) return FOLDER_HI;
  return 0;
}

bool initPn532() {
  for (uint8_t i = 0; i < INIT_RETRIES; i++) {
    nfc.begin();
    if (nfc.getFirmwareVersion()) {
      nfc.SAMConfig();
      nfc.setPassiveActivationRetries(0x02);  // do not block forever when no tag is present
      Serial.println(F("PN532 online."));
      return true;
    }
    delay(300);
  }
  Serial.println(F("PN532 NOT found: check DIP switches (I2C), SDA/SCL, 3V3, GND."));
  return false;
}

bool initDfPlayer() {
  for (uint8_t i = 0; i < INIT_RETRIES; i++) {
    if (dfp.begin(dfSerial, /*isACK=*/true, /*doReset=*/true)) {
      dfp.setTimeOut(500);
      dfp.volume(volume);
      dfp.EQ(DFPLAYER_EQ_NORMAL);
      dfp.outputDevice(DFPLAYER_DEVICE_SD);
      Serial.println(F("DFPlayer online."));
      return true;
    }
    delay(500);
  }
  Serial.println(F("DFPlayer NOT initialised: check TX/RX wiring, 1k resistor, 5V, microSD (FAT32)."));
  return false;
}

void handleDfEvents() {
  if (!dfOnline || !dfp.available()) return;
  uint8_t type = dfp.readType();
  int value = dfp.read();
  switch (type) {
    case DFPlayerError:
      if (value == FileMismatch || value == FileIndexOut) {
        Serial.printf("Audio file missing: /%02u/%03u.mp3\n", lastFolder, lastTrack);
        if (lastFolder != FOLDER_SYSTEM) playSystem(SYS_AUDIO_MISSING);
      } else if (value == Sleeping) {
        Serial.println(F("DFPlayer: no storage detected (SD card?)"));
      } else {
        Serial.printf("DFPlayer error code %d\n", value);
      }
      break;
    case DFPlayerCardRemoved:
      Serial.println(F("microSD removed."));
      dfOnline = false;
      break;
    case DFPlayerCardInserted:
    case DFPlayerCardOnline:
      Serial.println(F("microSD online."));
      break;
    case DFPlayerPlayFinished:
      Serial.println(F("Playback finished."));
      break;
    default: break;
  }
}

void playMedicine(uint8_t folder, uint8_t track) {
  lastFolder = folder; lastTrack = track;
  Serial.printf("Playing /%02u/%03u.mp3\n", folder, track);
  dfp.playFolder(folder, track);
}

// Reads 16 pages (64 bytes) of NTAG user memory starting at page 4.
bool readUserMemory(uint8_t* buf64) {
  for (uint8_t p = 0; p < 16; p++) {
    if (!nfc.ntag2xx_ReadPage(4 + p, buf64 + p * 4)) return false;
  }
  return true;
}

void processNewTag(const uint8_t* uid, uint8_t uidLen) {
  Serial.print(F("Tag UID: "));
  for (uint8_t i = 0; i < uidLen; i++) Serial.printf("%02X", uid[i]);
  Serial.println();

  if (uidLen != 7) {  // NTAG21x have 7-byte UIDs; 4-byte = MIFARE Classic etc. (unsupported)
    Serial.println(F("Unsupported tag type (expected NTAG21x)."));
    playSystem(SYS_TAG_UNRECOGNISED);
    return;
  }
  uint8_t mem[64];
  if (!readUserMemory(mem)) {
    Serial.println(F("Read failed - hold the tag steady."));
    playSystem(SYS_NFC_ERROR);
    tagLatched = false;  // allow an immediate retry on the next poll
    return;
  }
  TmlRecord rec;
  NdefStatus st = parseTmlNdef(mem, sizeof(mem), &rec);
  if (st != NDEF_OK) {
    Serial.printf("Tag content invalid (parser status %u).\n", (unsigned)st);
    playSystem(SYS_TAG_UNRECOGNISED);
    return;
  }
  uint8_t tagFolder = folderForLang(rec.lang);
  if (!tagFolder) {
    Serial.printf("Language '%s' not supported.\n", rec.lang);
    playSystem(SYS_TAG_UNRECOGNISED);
    return;
  }
  uint8_t folder = LANGUAGE_FROM_TAG ? tagFolder : langFolder[activeLang];
  Serial.printf("Valid tag: tag language=%s id=%u, playing folder %u\n", rec.lang, rec.medId, folder);
  playMedicine(folder, (uint8_t)rec.medId);
}

void armReplay() { tagLatched = false; misses = 0; }

// ---------- Arduino entry points ----------
void setup() {
  Serial.begin(115200);
  pinMode(PIN_STATUS_LED, OUTPUT);
  pinMode(PIN_BTN_VOL_DOWN, INPUT_PULLUP);
  pinMode(PIN_BTN_VOL_UP, INPUT_PULLUP);
  pinMode(PIN_BTN_LANGUAGE, INPUT_PULLUP);
  btStop();  // Wi-Fi is never started; Bluetooth stopped to reduce current draw
  Serial.println(F("\nTalking Medicine Label - starting"));

  Wire.begin(PIN_I2C_SDA, PIN_I2C_SCL);
  Wire.setClock(I2C_CLOCK_HZ);
  dfSerial.begin(DFPLAYER_BAUD, SERIAL_8N1, PIN_DFPLAYER_RX, PIN_DFPLAYER_TX);

  delay(DFPLAYER_BOOT_DELAY_MS);
  pn532Online = initPn532();
  dfOnline = initDfPlayer();
  if (!pn532Online) blink(3, 150, 150);
  if (!dfOnline)    blink(2, 600, 300);
  if (pn532Online && dfOnline) { playSystem(SYS_READY); blink(1, 300, 0); }
}

void loop() {
  handleDfEvents();
  handleButtons();

  // Recover from init failures / PN532 dropouts.
  static uint32_t lastCheck = 0;
  if (millis() - lastCheck > (pn532Online ? PN532_RECHECK_MS : 5000UL)) {
    lastCheck = millis();
    if (!pn532Online || !nfc.getFirmwareVersion()) pn532Online = initPn532();
    if (!dfOnline) dfOnline = initDfPlayer();
  }
  if (!pn532Online) return;

  static uint32_t lastPoll = 0;
  if (millis() - lastPoll < TAG_POLL_INTERVAL_MS) return;
  lastPoll = millis();

  uint8_t uid[7] = {0};
  uint8_t uidLen = 0;
  bool found = nfc.readPassiveTargetID(PN532_MIFARE_ISO14443A, uid, &uidLen, TAG_POLL_TIMEOUT_MS);

  if (!found) {
    if (tagLatched && ++misses >= TAG_LOST_MISSES) { armReplay(); Serial.println(F("Tag removed - ready.")); }
    return;
  }
  misses = 0;

  if (tagLatched && uidLen == latchedLen && !memcmp(uid, latchedUid, uidLen)) {
#if REPLAY_AFTER_MS > 0
    if (millis() - latchedAt > REPLAY_AFTER_MS) { latchedAt = millis(); processNewTag(uid, uidLen); }
#endif
    return;  // same tag still in range: do not repeat
  }

  tagLatched = true;
  latchedLen = uidLen;
  memcpy(latchedUid, uid, uidLen);
  latchedAt = millis();
  digitalWrite(PIN_STATUS_LED, HIGH);
  processNewTag(uid, uidLen);
  digitalWrite(PIN_STATUS_LED, LOW);
}
