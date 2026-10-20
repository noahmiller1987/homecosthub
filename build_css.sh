#!/bin/sh
# Compile the site's Tailwind CSS into web/styles.css (replaces the cdn.tailwindcss.com
# runtime script, which Tailwind documents as not for production: ~300 KB of render-blocking
# JS that builds styles in the browser on every page view).
# The standalone CLI (v3.4.17, matches the CDN's v3) is downloaded on first run, not committed.
set -e
cd "$(dirname "$0")"
BIN=tools/tailwindcss
if [ ! -x "$BIN" ]; then
  mkdir -p tools
  curl -sL -o "$BIN" "https://github.com/tailwindlabs/tailwindcss/releases/download/v3.4.17/tailwindcss-macos-$(uname -m | sed 's/x86_64/x64/')"
  chmod +x "$BIN"
fi
nice -n 19 "$BIN" -c tailwind.config.js -i src/input.css -o web/styles.css --minify
