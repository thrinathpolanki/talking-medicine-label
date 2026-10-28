# Audio (microSD card)

<p align="center"><img src="../images/animations/audio-chain.svg" alt="Animated audio path from microSD through DFPlayer Mini and PAM8403 to left and right speakers" width="100%"></p>

![DFPlayer Mini MP3-TF-16P V3.0, two views](../images/components/dfplayer-mini-mp3-tf-16p.png)

*DFPlayer Mini photographs supplied by the project author (licence unverified; see `docs/references.md`).*


```mermaid
flowchart TD
  SD["microSD (FAT32, 32 GB or less)"] --> F1["/01 English"]
  SD --> F2["/02 Telugu"]
  SD --> F3["/03 Hindi (planned)"]
  SD --> F99["/99 System prompts"]
  F1 --> A1["001.mp3 = medicine ID 1"]
  F1 --> A2["002.mp3 = medicine ID 2"]
  F99 --> S1["001 ready"]
  F99 --> S2["002 tag not recognised"]
  F99 --> S3["003 audio missing"]
  F99 --> S4["004 hold tag steady"]
  F99 --> S5["005-007 language names"]
  F99 --> S6["008 volume limit beep"]
```

Folders are two digits (01-99) and files three digits (001-255), matching the DFPlayer `playFolder(folder, file)` command (manual section 3.4.4). The firmware plays `/<folder>/<id>.mp3`.

`/99/005.mp3` = "English", `006` = "Telugu" (spoken in Telugu), `007` = "Hindi" (only if enabled), `008` = short beep at the volume limits. The language button speaks 005/006 so the user knows which language is active.

**Recording guidelines:** mono mp3 (the same signal plays on both speakers), 44.1 kHz, 128 kbps; speak medicine name, strength, when/how to take, key warning, and "follow your doctor's advice"; have a pharmacist review. Telugu recordings should be by a native speaker. The `/99` prompts are required when `ENABLE_SYSTEM_PROMPTS` is 1. This repository ships **no audio files**.

**SD tips:** copy files into the folders in numeric order; on macOS run `dot_clean /Volumes/<card>` to delete `._` files; no sub-folders inside language folders.
