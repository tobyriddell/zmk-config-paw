#!/bin/bash

set -ex

# Build left and right firmware
west build -d /build/left  -p -b nice_nano_v2 -s /zmk-config-paw/zmk/app -- -DSHIELD=paw_left  -DZMK_CONFIG=/zmk-config-paw/config
west build -d /build/right -p -b nice_nano_v2 -s /zmk-config-paw/zmk/app -- -DSHIELD=paw_right -DZMK_CONFIG=/zmk-config-paw/config

# Generate keymap diagrams
# Parse keymap file to YAML, then draw SVG diagram
keymap parse -z config/boards/shields/paw/paw.keymap -o paw.yaml && \
keymap draw -d config/paw_physical_layout.dtsi paw.yaml -o /build/paw.svg && \
python3 thicken_svg.py /build/paw.svg /build/paw_thick.svg