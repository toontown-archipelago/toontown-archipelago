# This is the PRC configuration file for settings that are
# used by both developer & production instances of Toontown Online.

# Window settings
win-origin -2 -2
show-frame-rate-meter #t
frame-rate-meter-text-pattern %0.f FPS
frame-rate-meter-update-interval 0.001

# Notify settings
notify-level-gobj error
notify-level-collide warning
notify-level-chan warning
notify-level-gobj warning
notify-level-loader warning
notify-integrate false
notify-timestamp false
default-directnotify-level info

# Server settings
ttoff-specific-login true

# Resources settings
model-path /
default-model-extension .bam

# Display settings
depth-bits 24

# GUI settings
direct-wtext false
on-screen-debug-font ImpressBT.ttf

# Chat settings
parent-password-set true
allow-secret-chat true
force-avatar-understandable true
force-player-understandable true

# Toon News settings
want-news-page false
want-news-tab false

# Gameplay settings
want-legacy-heads false
want-gardening true
want-cogdominiums true
want-emblems true

# Misc. settings
respect-prev-transform true
language english
vfs-case-sensitive false
inactivity-timeout 180
merge-lod-bundles false
early-event-sphere true
server-data-folder backups/
isclient-check false
model-cache-dir
texture-anisotropic-degree 16

# Panda Config
load-display pandagl
audio-library-name p3fmod_audio

# Astron
dc-file astron/dclass/tto.dc

# Debugging
console-output true
want-dev false

# Mounting Phase
vfs-mount resources/phase_3.mf /
vfs-mount resources/phase_3.5.mf /
vfs-mount resources/phase_4.mf /
vfs-mount resources/phase_5.mf /
vfs-mount resources/phase_5.5.mf /
vfs-mount resources/phase_6.mf /
vfs-mount resources/phase_7.mf /
vfs-mount resources/phase_8.mf /
vfs-mount resources/phase_9.mf /
vfs-mount resources/phase_10.mf /
vfs-mount resources/phase_11.mf /
vfs-mount resources/phase_12.mf /
vfs-mount resources/phase_13.mf /
vfs-mount resources/phase_14.mf /
