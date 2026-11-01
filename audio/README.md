// Host-side unit test for firmware/talking-medicine-label/ndef_parser.h
// Build: g++ -std=c++11 -Wall -Wextra -I firmware/talking-medicine-label tests/ndef_parser_test.cpp -o /tmp/ndef_test && /tmp/ndef_test
#include <cstdio>
#include <vector>
#include <string>
#include "ndef_parser.h"

static std::vector<uint8_t> textRecord(const std::string& lang, const std::string& text, bool utf16 = false) {
  std::vector<uint8_t> payload;
  payload.push_back((utf16 ? 0x80 : 0x00) | (uint8_t)lang.size());
  payload.insert(payload.end(), lang.begin(), lang.end());
  payload.insert(payload.end(), text.begin(), text.end());
  std::vector<uint8_t> rec = {0xD1, 0x01, (uint8_t)payload.size(), 'T'};
  rec.insert(rec.end(), payload.begin(), payload.end());
  std::vector<uint8_t> mem = {0x03, (uint8_t)rec.size()};
  mem.insert(mem.end(), rec.begin(), rec.end());
  mem.push_back(0xFE);
  mem.resize(64, 0x00);
  return mem;
}
static int fails = 0;
static void expect(const char* name, NdefStatus got, NdefStatus want) {
  bool ok = got == want; if (!ok) fails++;
  std::printf("%-34s %s (got %d, want %d)\n", name, ok ? "PASS" : "FAIL", got, want);
}
int main() {
  TmlRecord r;
  auto m = textRecord("en", "TML:007");
  expect("english id 7", parseTmlNdef(m.data(), m.size(), &r), NDEF_OK);
  if (std::string(r.lang) != "en" || r.medId != 7) { std::printf("FAIL fields\n"); fails++; }
  m = textRecord("te", "TML:255");  expect("telugu id 255", parseTmlNdef(m.data(), m.size(), &r), NDEF_OK);
  m = textRecord("EN", "TML:12");   expect("upper-case lang", parseTmlNdef(m.data(), m.size(), &r), NDEF_OK);
  if (std::string(r.lang) != "en") { std::printf("FAIL lowercase\n"); fails++; }
  m = textRecord("en", "TML:000");  expect("id 0 rejected", parseTmlNdef(m.data(), m.size(), &r), NDEF_BAD_ID);
  m = textRecord("en", "TML:256");  expect("id 256 rejected", parseTmlNdef(m.data(), m.size(), &r), NDEF_BAD_ID);
  m = textRecord("en", "TML:1x3");  expect("non-numeric id", parseTmlNdef(m.data(), m.size(), &r), NDEF_BAD_ID);
  m = textRecord("en", "XYZ:001");  expect("wrong prefix", parseTmlNdef(m.data(), m.size(), &r), NDEF_NOT_TML);
  m = textRecord("en", "TML:007", true); expect("utf16 rejected", parseTmlNdef(m.data(), m.size(), &r), NDEF_BAD_TEXT_ENCODING);
  std::vector<uint8_t> blank(64, 0); expect("blank tag", parseTmlNdef(blank.data(), blank.size(), &r), NDEF_NO_NDEF_TLV);
  std::vector<uint8_t> uri = {0x03,0x08,0xD1,0x01,0x04,'U',0x00,'a','b','c',0xFE}; uri.resize(64,0);
  expect("URI record rejected", parseTmlNdef(uri.data(), uri.size(), &r), NDEF_NOT_TEXT_RECORD);
  m = textRecord("en", "TML:007"); expect("truncated buffer", parseTmlNdef(m.data(), 8, &r), NDEF_TRUNCATED);
  std::printf(fails ? "\n%d FAILED\n" : "\nALL PASSED\n", fails);
  return fails ? 1 : 0;
}
