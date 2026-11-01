# OpenMoHAA for AmigaOS 3.x (68k)

A port of [OpenMoHAA](https://github.com/openmoh/openmohaa), the open source
engine for **Medal of Honor: Allied Assault**, to classic AmigaOS 3.x with
RTG and 3D hardware acceleration. It plays the single player campaigns of
Allied Assault, **Spearhead** and **Breakthrough**.

The main target is an Amiga with a **PiStorm** (Raspberry Pi 4, Emu68) and
**PiStorm3D**. The same programs also run in WinUAE.

You need the original game data (see [Installation](#installation)). It is
not included and never will be.

## Two builds

| Program | Renderer | Library |
|---|---|---|
| `openmohaa` | OpenGL 1.x renderer | `minigl.library` |
| `openmohaa_ogle2` | OpenGL ES 2 renderer (GLSL shaders) | `ogles2.library` |

Both play the same game with the same data and settings. The MiniGL build
is the main one. The GLES2 build is newer and still experimental. It draws
the world from vertex buffers and has better lighting, but it is not yet
as fast on every system.

## Requirements

- AmigaOS 3.x
- 68040 or 68060 with FPU. In practice a PiStorm with Emu68; a real 68060
  is far too slow
- RTG with a 16 or 32 bit screen mode (P96 / CyberGraphX). PiStorm3D needs a
  32 bit (BGRA) mode
- `minigl.library` (PiStorm3D) or `ogles2.library` for the GLES2 build
- [openal.library](https://github.com/Sdursun/Openal_Amiga) and AHI for sound
- MUI 3.8 or newer for the settings program
- Plenty of Fast RAM: 1 GB recommended (tested with 1 GB and more)
- About 3 GB of disk space for the game data
- Not needed: a network stack. Multiplayer is not supported

## Installation

1. Copy the `main` folder of your Medal of Honor: Allied Assault installation
   (the PC version) into the OpenMoHAA folder on the Amiga.
   For the expansions also copy `mainta` (Spearhead) and `maintt`
   (Breakthrough).
2. Copy the files from the release archive into the same folder:

   ```
   OpenMoHAA/
     openmohaa              MiniGL build
     openmohaa_ogle2        GLES2 build
     MOHAA, Spearhead, Breakthrough (+ _ogle2)   start icons
     MOHAAPrefs             settings
     main/  mainta/  maintt/   game data (yours), plus the zz_amiga_*.pk3 files
   ```
3. Start the game from Workbench with the **MOHAA**, **Spearhead** or
   **Breakthrough** icon (or the `_ogle2` icons for the GLES2 build).

From a Shell:

```
cd OpenMoHAA
openmohaa                          ; Allied Assault
openmohaa +set com_target_game 1   ; Spearhead
openmohaa +set com_target_game 2   ; Breakthrough
```

The game needs a large stack. The start icons give it one; from a Shell use
`Stack 1048576` first.

## Settings: MOHAAPrefs

`MOHAAPrefs` sets what the game reads at startup:

- **Language** and **Subtitles** (see below)
- **Resolution**: 640x480 up to 1280x720 and 1920x1080
- **Screen depth**: 16 or 32 bit (PiStorm3D: 32)
- **Detail**: "Fast (Amiga)" sets the low detail values that cost the most
  CPU (model detail, entity lighting, shadows, effects). It is the
  biggest single speed-up
- **FPS limit**, **Buffering** (double/triple, MiniGL build)
- **Show FPS**, **Skip intro movie**
- **Sound quality**: 22 kHz mixing is faster and decodes the music at half
  rate
- **Check update**: looks for a newer release on this page

Every option has "Game setting", which leaves it to the game's own menus.
The settings are saved in `config/openmohaa` in the game folder, so they
move with the folder.

## Languages and subtitles

The game can show translated subtitles, objectives, HUD messages and menu
text. A translation is a plain UTF-8 text file in the game folder:

```
main/global/localization-<code>.txt
```

```
// OpenMoHAA language: Deutsch
{ "Health" "Gesundheit" }
{ "Game Saved" "Spiel gespeichert" }
```

The first line names the language for MOHAAPrefs. Each line holds the
English text exactly as the game has it, then the translation. One file
covers all three games. Western European languages work with the game's
own fonts. For Turkish, `zz_amiga_fonts.pk3` adds the Turkish letters.

A Turkish translation is included. Pictures (briefing pages, some buttons)
cannot be translated this way.

Want to translate the game? A tool makes a template with every English
string from your installed game. See the release notes, or open an issue.

## Performance

The game is CPU bound on the Amiga, so resolution matters much less than
detail. With the "Fast (Amiga)" detail the first mission ran more than
twice as fast as with the game's default PC settings in our tests. Model
detail (`r_lodscale`) is the setting that matters most: values above 1
draw every soldier at full detail even far away.

Loading a mission takes a while: the game data is large.

## Status

- Single player: Allied Assault, Spearhead, Breakthrough
- Multiplayer: not supported (single player only by design)
- Known limits: some pictures in menus and briefings stay in English;
  the GLES2 build is experimental

## Building

The port is built with the bebbo m68k-amigaos-gcc cross compiler.
The source is not published here yet.

## Credits

- [OpenMoHAA](https://github.com/openmoh/openmohaa) by the OpenMoHAA team
  (GPL v2), on which this port is based
- id Software for the Quake III Arena engine OpenMoHAA builds on
- [Openal_Amiga](https://github.com/Sdursun/Openal_Amiga) for sound
- PiStorm, Emu68 and PiStorm3D developers
- Medal of Honor: Allied Assault is © Electronic Arts. This project does
  not contain any of its data; you need your own copy of the game.

## License

The engine is GPL v2, like OpenMoHAA.
