#!/usr/bin/env python3
"""Build the Finder Quick Action on macOS; optionally package a release ZIP."""

import argparse
from pathlib import Path
import plistlib
import shutil
import subprocess
import uuid
import sys

root = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--archive', action='store_true', help='Create dist/open-in-codex.zip with Finder metadata preserved')
args = parser.parse_args()
if sys.platform != 'darwin':
    parser.error('Building the workflow requires macOS.')
name = 'Open in Codex'
script = (root / 'open-in-codex.zsh').read_text()
info = {
    'CFBundleIdentifier': 'local.finder.open-in-codex',
    'CFBundleName': name,
    'CFBundleVersion': '1.4.1',
    'NSServices': [{
        'NSMenuItem': {'default': name},
        'NSIconName': 'workflowCustomImage',
        'NSBackgroundColorName': 'background',
        'NSMessage': 'runWorkflowAsService',
        'NSRequiredContext': {'NSApplicationIdentifier': 'com.apple.finder'},
        'NSSendFileTypes': ['public.item'],
    }],
}
uuidstr = lambda: str(uuid.uuid4()).upper()
action = {
    'ActionBundlePath': '/System/Library/Automator/Run Shell Script.action',
    'ActionName': 'Run Shell Script',
    'ActionParameters': {'COMMAND_STRING': script, 'inputMethod': 1, 'shell': '/bin/zsh', 'source': '', 'CheckedForUserDefaultShell': True},
    'AMAccepts': {'Container': 'List', 'Optional': True, 'Types': ['com.apple.cocoa.string']},
    'AMProvides': {'Container': 'List', 'Types': ['com.apple.cocoa.string']},
    'AMActionVersion': '2.0.3',
    'AMParameterProperties': {key: {} for key in ['COMMAND_STRING', 'inputMethod', 'shell', 'source']},
    'AMRequiredResources': [],
    'BundleIdentifier': 'com.apple.RunShellScript',
    'Class Name': 'RunShellScriptAction',
    'InputUUID': uuidstr(), 'OutputUUID': uuidstr(), 'UUID': uuidstr(),
    'CanShowWhenRun': True, 'CanShowSelectedItemsWhenRun': False,
    'isViewVisible': True, 'ShowWhenRun': False,
}
workflow = {
    'AMDocumentVersion': '2', 'AMApplicationVersion': '2.10',
    'actions': [{'action': action, 'isViewVisible': True}], 'connectors': {},
    'workflowMetaData': {
        'serviceApplicationBundleID': 'com.apple.finder',
        'serviceApplicationPath': '/System/Library/CoreServices/Finder.app',
        'serviceInputTypeIdentifier': 'com.apple.Automator.fileSystemObject',
        'serviceOutputTypeIdentifier': 'com.apple.Automator.nothing',
        'serviceProcessesInput': 0,
        'workflowTypeIdentifier': 'com.apple.Automator.servicesMenu',
        'serviceName': name,
        'serviceIconName': 'workflowCustomImage',
        'serviceBackgroundColorName': 'background',
        'customImageFileData': (root / 'assets' / 'codex.tiff').read_bytes(),
        'customImageFileExtension': 'tiff',
        'presentationMode': 15,
    },
}
contents = root / f'{name}.workflow' / 'Contents'
contents.mkdir(parents=True, exist_ok=True)
resources = contents / 'Resources'
resources.mkdir(exist_ok=True)
# Remove stale variants so AppKit resolves exactly one image.
for old in resources.glob('workflowCustomImage*'):
    old.unlink()
shutil.copyfile(root / 'assets' / 'codex.tiff', resources / 'workflowCustomImage.tiff')
for filename, data in [('Info.plist', info), ('document.wflow', workflow)]:
    with (contents / filename).open('wb') as f:
        plistlib.dump(data, f, sort_keys=False)
# Finder's file icon is independent of the Quick Action menu image.
icon_file = contents.parent / 'Icon\r'
icon_file.touch()
resource_fork = (root / 'assets' / 'finder-icon.resourcefork').read_bytes()
Path(str(icon_file) + '/..namedfork/rsrc').write_bytes(resource_fork)
subprocess.run(['/usr/bin/xattr', '-wx', 'com.apple.FinderInfo', '0000000000000000040000000000000000000000000000000000000000000000', str(contents.parent)], check=True)
print(contents.parent)

if args.archive:
    dist = root / 'dist'
    dist.mkdir(exist_ok=True)
    archive = dist / 'open-in-codex.zip'
    archive.unlink(missing_ok=True)
    # Standard ZIP/Git cannot preserve Finder resource forks; ditto can.
    subprocess.run(['/usr/bin/ditto', '-c', '-k', '--sequesterRsrc', '--keepParent',
                    str(contents.parent), str(archive)], check=True)
    print(archive)
