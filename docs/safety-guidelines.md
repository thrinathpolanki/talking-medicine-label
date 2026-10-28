# Safety Guidelines

<p align="center"><img src="../images/animations/strip-safety.svg" alt="Animated header with a pulsing warning sign: safety guidelines" width="100%"></p>


**Medical:** The device only repeats information recorded by a competent person. Always confirm a medicine with the pharmacist or doctor if unsure. Wrong recordings can cause harm: have each recording reviewed and re-check labels when prescriptions change.

**Electrical:**
- Li-ion cells can ignite when shorted, over-discharged, punctured or charged with the wrong charger. Use only the protected TP4056 path.
- Fuse or at least current-limit your build during development (bench supply with current limit).
- Set the MT3608 to 5.0 V before connecting loads.
- Never short the PAM8403 outputs or connect them to ground.
- The supplied speakers are rated 0.5 W: an unrestricted PAM8403 can overdrive and burn them out. Keep the firmware volume cap and verify about 2 V RMS or less across each speaker.
- Disconnect the battery before rewiring.
- Keep the build in a non-conductive enclosure with insulated joints.
- Dispose of cells at recycling points.
