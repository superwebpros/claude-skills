# Persistent Dolt tunnel on macOS (launchd)

A LaunchAgent keeps the SSH tunnel to the beads Dolt remote running across logins, reboots, and network drops. launchd does not expand environment variables or `~` inside a plist, so the template has placeholders that you fill in once from the variables described in [../SKILL.md](../SKILL.md#configuration).

## 1. Write the plist

Save as `~/Library/LaunchAgents/com.example.dolt-tunnel.plist`. You can choose any reverse-DNS label, but keep the `Label` value and the filename in sync.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.example.dolt-tunnel</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/ssh</string>
        <string>-N</string>
        <string>-L</string>
        <string>BEADS_REMOTE_PORT:127.0.0.1:BEADS_REMOTE_PORT</string>
        <string>-i</string>
        <string>ABSOLUTE_PATH_TO_BEADS_REMOTE_SSH_KEY</string>
        <string>-o</string>
        <string>ServerAliveInterval=60</string>
        <string>-o</string>
        <string>ServerAliveCountMax=3</string>
        <string>-o</string>
        <string>ExitOnForwardFailure=yes</string>
        <string>BEADS_REMOTE_SSH_USER@BEADS_REMOTE_HOST</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardErrorPath</key>
    <string>/tmp/dolt-tunnel.err</string>
    <key>StandardOutPath</key>
    <string>/tmp/dolt-tunnel.out</string>
</dict>
</plist>
```

Replace the four placeholders with real values on the local machine only. The key path must be absolute, for example the expanded value of `$BEADS_REMOTE_SSH_KEY`. Never commit the filled-in plist.

## 2. Load, check, unload

```bash
launchctl load ~/Library/LaunchAgents/com.example.dolt-tunnel.plist
lsof -i :"$BEADS_REMOTE_PORT" | grep LISTEN      # should show ssh
cat /tmp/dolt-tunnel.err                          # look here if it is not listening

# To change the plist, unload, edit, and load again
launchctl unload ~/Library/LaunchAgents/com.example.dolt-tunnel.plist
```

If a tunnel is already running from an ad-hoc `ssh -fNL`, kill it first or the LaunchAgent fails with "address already in use". The `KeepAlive` setting restarts the failed agent, so it comes up on its own once the port is free.
