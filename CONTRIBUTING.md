# Contributing

<p align="center"><img src="images/animations/strip-contributing.svg" alt="Animated header: Contributing" width="100%"></p>


Contributions are welcome: tested wiring photos, translations of audio scripts (reviewed by a pharmacist), firmware fixes, documentation.

1. Open an issue describing the change. 2. Fork and branch. 3. Keep the connection table, wiring diagram (`diagrams/generate_wiring_diagram.py`), animations (`diagrams/generate_animated_svgs.py`; every Markdown file must embed one) and `config.example.h` consistent. 4. Run `g++ ... tests/ndef_parser_test.cpp` and `python3 tests/check_repo_links.py`. 5. State exactly what you tested on hardware; never claim untested results. 6. Only add images you own or that carry a redistributable licence, and record them in `docs/references.md`.

Do not submit medical advice content that has not been reviewed by a qualified professional.
