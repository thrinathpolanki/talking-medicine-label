# Limitations and Future Work

<p align="center"><img src="../images/animations/strip-limitations.svg" alt="Animated header: limitations and future work" width="100%"></p>


## Current limitations
- Not tested on hardware or compiled in Arduino IDE (see README testing status).
- No automatic translation or text-to-speech: audio is prerecorded per medicine and language.
- Tags must be written in the TML format; MIFARE Classic and 4-byte-UID tags are rejected.
- Audio is not generated from tag content; a missing file produces only the "audio missing" prompt.
- No battery-level indication. Volume and language use three buttons without audible volume feedback except limit beeps.
- Read range about 3-7 cm.
- Battery capacity and converter headroom unverified.

## Proposed (not implemented)
More Indian languages, repeat button, battery-level voice alert, sleep mode, better enclosure, tag authentication (NTAG password), UID fallback table, optional offline TTS.
