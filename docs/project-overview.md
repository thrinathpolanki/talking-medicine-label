# Project Overview

<p align="center"><img src="../images/animations/strip-overview.svg" alt="Animated header: project overview" width="100%"></p>
<p align="center"><img src="../images/animations/signal-flow.svg" alt="Animated signal flow from NFC tag to PN532, ESP32, DFPlayer Mini, PAM8403 and two speakers" width="100%"></p>


![Project banner](../images/project-overview/banner.svg)

The Talking Medicine Label is a small battery-powered device. A tag stuck on a medicine container stores a short code and a language. When the container is held near the reader, the device speaks a prerecorded instruction from its memory card.

```mermaid
flowchart LR
  A["Tag: TML:007, language te"] --> B["Reader"] --> C["ESP32 picks file 02/007.mp3"] --> D["Audio player"] --> E["Speaker"]
```

The device is an **aid**. Recordings must be prepared and checked by a qualified person (pharmacist or doctor). It never replaces prescriptions, pharmacist advice, or the doctor's instructions.

See the root [README](../README.md) for the full report.
