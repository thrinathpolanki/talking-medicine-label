// ndef_parser.h - Hardware-independent parser for the Talking Medicine Label tag format.
//
// The tag stores ONE short NDEF "Text" record (NFC Forum well-known type "T"):
//   language code : "en", "te", "hi", ... (stored in the standard NDEF text-record field)
//   text          : "TML:" + medicine ID as 1-3 decimal digits (1..255), e.g. "TML:007"
//
// This file has no Arduino dependencies so it can be unit-tested on a PC
// (see tests/ndef_parser_test.cpp).
#pragma once
#include <stdint.h>
#include <stddef.h>
#include <string.h>

struct TmlRecord {
  char     lang[9];   // lower-case language code from the NDEF record, NUL-terminated
  uint16_t medId;     // 1..255
};

enum NdefStatus : uint8_t {
  NDEF_OK = 0,
  NDEF_NO_NDEF_TLV,        // blank tag or no NDEF message TLV (0x03)
  NDEF_TRUNCATED,          // data ends before the message does
  NDEF_UNSUPPORTED_LAYOUT, // not a single short record (we deliberately keep tags simple)
  NDEF_NOT_TEXT_RECORD,    // e.g. a URI record
  NDEF_BAD_TEXT_ENCODING,  // UTF-16 flag set or invalid language-code length
  NDEF_NOT_TML,            // text does not start with "TML:"
  NDEF_BAD_ID              // ID missing, not numeric, or outside 1..255
};

// mem = raw bytes starting at NTAG page 4 (first user-memory page).
inline NdefStatus parseTmlNdef(const uint8_t* mem, size_t len, TmlRecord* out) {
  size_t i = 0;
  while (i < len && mem[i] == 0x00) i++;                 // skip NULL TLVs
  if (i >= len || mem[i] != 0x03) return NDEF_NO_NDEF_TLV;
  i++;
  if (i >= len) return NDEF_TRUNCATED;
  size_t tlvLen = mem[i++];
  if (tlvLen == 0xFF) return NDEF_UNSUPPORTED_LAYOUT;    // 3-byte length form: too long for this format
  if (tlvLen == 0)    return NDEF_NO_NDEF_TLV;           // empty message
  if (i + tlvLen > len || tlvLen < 4) return NDEF_TRUNCATED;

  const uint8_t* r = mem + i;
  const uint8_t hdr = r[0];
  const bool mb = hdr & 0x80, me = hdr & 0x40, cf = hdr & 0x20, sr = hdr & 0x10, il = hdr & 0x08;
  const uint8_t tnf = hdr & 0x07;
  if (!mb || !me || cf || !sr || il) return NDEF_UNSUPPORTED_LAYOUT;
  if (tnf != 0x01 || r[1] != 1 || r[3] != 'T') return NDEF_NOT_TEXT_RECORD;

  const size_t payLen = r[2];
  if (3 + 1 + payLen > tlvLen || payLen < 1) return NDEF_TRUNCATED;
  const uint8_t* p = r + 4;
  const uint8_t status = p[0];
  if (status & 0x80) return NDEF_BAD_TEXT_ENCODING;      // UTF-16 not supported
  const size_t langLen = status & 0x3F;
  if (langLen < 2 || langLen > 8 || 1 + langLen >= payLen) return NDEF_BAD_TEXT_ENCODING;

  for (size_t k = 0; k < langLen; k++) {
    uint8_t c = p[1 + k];
    if (c >= 'A' && c <= 'Z') c = c - 'A' + 'a';
    out->lang[k] = (char)c;
  }
  out->lang[langLen] = '\0';

  const uint8_t* t = p + 1 + langLen;
  const size_t tl = payLen - 1 - langLen;
  if (tl < 5 || memcmp(t, "TML:", 4) != 0) return NDEF_NOT_TML;
  if (tl > 7) return NDEF_BAD_ID;
  uint16_t id = 0;
  for (size_t k = 4; k < tl; k++) {
    if (t[k] < '0' || t[k] > '9') return NDEF_BAD_ID;
    id = (uint16_t)(id * 10 + (t[k] - '0'));
  }
  if (id < 1 || id > 255) return NDEF_BAD_ID;
  out->medId = id;
  return NDEF_OK;
}
