FROM zmkfirmware/zmk-build-arm:3.5-branch

WORKDIR /zmk-config-paw

# Copy config directory first, then run west init/update, then copy rest of source.
# This two-step copy reduces the number of times the Docker container has to be fully rebuilt,
# as west init/update layers can be cached when only keymap or other non-config files change.
COPY config ./config

COPY . .
RUN west init -l config 
RUN west update

ENV CMAKE_PREFIX_PATH=/zmk-config-paw/zephyr

# Install keymap-drawer
# Install pip3 if not available, then install keymap-drawer
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3-pip && \
    PIP_BREAK_SYSTEM_PACKAGES=1 pip3 install keymap-drawer && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Run build script
RUN ./build.sh

CMD ["/bin/sh", "-c", "cp /build/paw.svg /out/paw.svg && cp /build/paw_thick.svg /out/paw_thick.svg && cp /build/left/zephyr/zmk.uf2 /out/left.uf2 && cp /build/right/zephyr/zmk.uf2 /out/right.uf2"]
