# Desktop Packaging Plan for the Practice Exam App

## Goal

Package the existing Python + Qt app so it can be launched from a desktop environment on Windows or macOS without requiring users to run Python manually.

## Recommended approach

Use PyInstaller as the primary packaging tool because the app is already a Python script with a Qt GUI and a small set of data files.

### Why this fits this project
- The app is already structured as a single GUI entry point: [exam_gui.py](exam_gui.py)
- It relies on local JSON content in [courses](courses) and writable state in [saves](saves)
- PyInstaller can bundle Python, Qt, and the course assets into a desktop app bundle

## Key implementation work

### 1. Make file paths packaging-safe
The app currently uses paths relative to the script directory. That is fine for source execution, but packaged apps may run from a read-only bundle location.

Plan:
- update the app so writable files such as history and saved sessions are written to a platform-appropriate user data folder:
  - Windows: `%APPDATA%/PracticeExamGenerator`
  - macOS: `~/Library/Application Support/PracticeExamGenerator`
- keep course files bundled as read-only assets
- ensure the app can still discover and load JSON exams from the packaged app

### 2. Add app metadata and branding
- add an application icon for Windows and macOS
- set the app name, version, and description
- optionally add a small splash screen or startup window

### 3. Build the packaged app

#### Windows target
- build a Windows `.exe` app
- optionally create an installer with Inno Setup or WiX for a desktop shortcut and Start Menu entry

#### macOS target
- build a `.app` bundle
- optionally wrap it in a `.dmg` for easier installation
- sign and notarize for wider distribution if needed

## Proposed build workflow

### Phase 1 — Prepare the app
- confirm the app runs from the repository
- install packaging dependencies
- test the app with a local build before distribution

### Phase 2 — Create the packaging config
- add a PyInstaller spec file or build command
- include these assets:
  - [courses](courses)
  - [saves](saves)
  - [README.md](README.md)
  - the app icon files

### Phase 3 — Build for Windows
Example approach:
```bash
python -m pip install pyinstaller pyinstaller-hooks-contrib
pyinstaller --noconfirm --windowed --name "Practice Exam Generator" --icon app_icon.ico --add-data "courses:courses" --add-data "saves:saves" --add-data "README.md:." exam_gui.py
```

Then optionally package the output with Inno Setup to create:
- Desktop shortcut
- Start Menu entry
- uninstaller

### Phase 4 — Build for macOS
Example approach:
```bash
python -m pip install pyinstaller pyinstaller-hooks-contrib
pyinstaller --noconfirm --windowed --name "Practice Exam Generator" --icon app_icon.icns --add-data "courses:courses" --add-data "saves:saves" --add-data "README.md:." exam_gui.py
```

Then optionally create a DMG installer using `create-dmg` or a similar tool.

## Quality checklist

Before release, verify that the packaged app can:
- launch successfully from the desktop
- load existing courses from the bundled files
- import a new JSON exam file
- save and resume sessions
- create history records without crashing
- close and reopen without data loss

## Recommended delivery targets

### Minimum viable desktop release
- Windows `.exe` app
- macOS `.app` bundle

### Better release experience
- Windows installer with desktop shortcut
- macOS `.dmg` installer
- signed and notarized build for macOS

## Suggested timeline

- Day 1: make storage paths portable and add icon assets
- Day 2: create PyInstaller build configuration and test the app bundle
- Day 3: build Windows and macOS packages and validate them

## Recommendation

Start with PyInstaller for the first release. It is the fastest path to getting a desktop-launchable app for both Windows and macOS. If cross-platform packaging becomes a recurring need, the next step could be moving to Briefcase for a more structured app packaging workflow.
