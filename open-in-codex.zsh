#!/bin/zsh
/usr/bin/osascript - "$@" <<'APPLESCRIPT'
on run selectedPaths
    if (count of selectedPaths) is 0 then
        tell application "Finder" to set selectedPaths to {POSIX path of (target of front window as alias)}
    end if
    set openedFolders to {}
    repeat with selectedPath in selectedPaths
        set targetPath to contents of selectedPath
        set targetFolder to do shell script "if [ -d " & quoted form of targetPath & " ]; then printf '%s' " & quoted form of targetPath & "; else /usr/bin/dirname " & quoted form of targetPath & "; fi"
        if targetFolder is not in openedFolders then
            set end of openedFolders to targetFolder
            set launchCommand to "cd -- " & quoted form of targetFolder & " && /opt/homebrew/bin/codex"
            tell application "iTerm"
                set codexWindow to (create window with default profile)
                tell current session of codexWindow to write text launchCommand
                activate
            end tell
        end if
    end repeat
end run
APPLESCRIPT
