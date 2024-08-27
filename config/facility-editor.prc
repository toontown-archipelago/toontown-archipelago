# Server settings
version v0.11.1 Alpha

server-version tt-ap-edition

# Developer settings
want-dev false
schellgames-dev false

# Logging
console-output true
notify-level-gobj error
notify-level-collide warning
notify-level-chan warning
notify-level-gobj warning
notify-level-loader warning
notify-integrate false
notify-timestamp false
default-directnotify-level info

# Window settings
load-display pandagl
window-title Toontown: Archipelago [Facility Editor Alpha]
win-origin -2 -2
depth-bits 24
frame-rate-meter-text-pattern %0.f FPS
frame-rate-meter-update-interval 0.001

# Audio settings
audio-library-name p3openal_audio

# Astron
dc-file astron/dclass/ttap.dc

# Server settings
ttoff-specific-login true

# Resources
model-path resources/

# GUI settings
direct-wtext false
on-screen-debug-font ImpressBT.ttf

# Chat settings
parent-password-set true
allow-secret-chat true
want-whitelist false
force-avatar-understandable true
force-player-understandable true

# Toon News settings
want-news-page false
want-news-tab false

# Gameplay settings
want-gardening true
want-emblems true

# Misc. settings
respect-prev-transform true
language english
vfs-case-sensitive false
inactivity-timeout 180
merge-lod-bundles false
early-event-sphere true
server-data-folder backups/
model-cache-dir
texture-anisotropic-degree 16
# Harfbuzz is good for handling non-latin text.
# However, this causes odd spacing on Cog nametags, so let's disable it.
text-use-harfbuzz #f
