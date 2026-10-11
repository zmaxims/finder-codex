# Codex — Open Here — Finder Quick Action

Launch Codex CLI in a selected folder directly from Finder. The Quick Action
opens a new **iTerm2** window, changes to the folder, and starts Codex.

**Right-click → Quick Actions → Codex — Open Here**

- Select a file to open its parent folder.
- Select multiple items to open each unique folder once.
- Includes a full-color Codex icon with Retina support.
- Once installed, the action works independently of the source folder.

## Requirements

- macOS with Finder and Automator. The original action and icon were confirmed working on macOS 27.0.1; other versions have not been tested.
- [iTerm2](https://iterm2.com/), installed as `iTerm`.
- Codex CLI at `/opt/homebrew/bin/codex`.
- Python 3, only when building from source.

If Codex is installed elsewhere, replace `/opt/homebrew/bin/codex` in
`open-in-codex.zsh` with the absolute path to your executable before building.

## Installation

### From a release

1. Download `open-in-codex.zip` from [Releases](https://github.com/zmaxims/finder-codex/releases).
2. Extract it using macOS Archive Utility.
3. Double-click `Codex — Open Here.workflow` in Finder to install it.
4. Select a folder and choose **Quick Actions → Codex — Open Here**.

Version 1.4.0 uses the original Russian name, `Открыть в Codex.workflow`.
Version 1.4.1 uses `Open in Codex.workflow`; version 1.4.2 uses `Codex — Open Here.workflow`.

On first launch, macOS may ask for permission to control iTerm. This allows
the action to create a terminal window and send the launch command.

### From source

Download or clone this repository, open its folder in a terminal, and run:

```sh
python3 build.py
```

Double-click the generated `Codex — Open Here.workflow` in Finder.
Rebuild and reinstall after changing the script or icons.

### Upgrading from an earlier action

Install `Codex — Open Here.workflow`, then move the old
`~/Library/Services/Открыть в Codex.workflow` or
`~/Library/Services/Open in Codex.workflow` to the Bin to avoid duplicate menu items.

## How it works

Finder passes the selected paths to an Automator Quick Action. Its embedded
shell script resolves the folders, removes duplicates, and uses AppleScript to
create a separate iTerm window for each folder. Each window runs `cd` followed
by Codex CLI. Paths are shell-quoted to support spaces and apostrophes.

The action expects selected files or folders. To launch Codex in the folder
you are currently viewing, go up one level and select that folder. The action
may not appear when right-clicking empty space in Finder.

## Troubleshooting

- Check that the workflow is installed at `~/Library/Services/Codex — Open Here.workflow`.
- In **Quick Actions → Customise…**, make sure the action is enabled.
- If Finder shows an old icon, relaunch Finder and open the menu again.
- If iTerm opens but Codex does not start, check the CLI path in the source script.

The menu uses a multi-resolution `workflowCustomImage.tiff`. The workflow file
has a separate Finder icon stored in a resource fork. Git and ordinary ZIP
packaging do not preserve that metadata; use the builder's release archive.

## Building a release

```sh
python3 build.py --archive
```

Output: `dist/open-in-codex.zip`. The builder uses the system `ditto` utility to
preserve the Finder icon and macOS metadata. Upload this ZIP to a GitHub Release.
GitHub's automatic source archives are intended for building from source.

## Project files

| File | Purpose |
| --- | --- |
| `open-in-codex.zsh` | Single source of the launch script |
| `build.py` | Builds the workflow and release archive |
| `assets/codex.png` | Original icon image |
| `assets/codex.tiff` | Multi-resolution menu image |
| `assets/finder-icon.resourcefork` | Finder workflow file icon |
| `CHANGELOG.md` | Release history |

## Uninstalling

In Finder, choose **Go → Go to Folder…**, enter `~/Library/Services`,
and move `Codex — Open Here.workflow` to the Bin.

## License

Original source code and documentation are licensed under [MIT](LICENSE).
Logos are excluded; see [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
This is an independent project, not an official OpenAI product.
