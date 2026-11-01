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
     main/  mainta/  maintt/   game data (yours, unchanged)
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

One file covers Allied Assault, Spearhead and Breakthrough. Choose the
language (and turn subtitles on) in MOHAAPrefs. A Turkish translation is
included. Pictures (briefing pages, some buttons) cannot be translated this
way.

### File names

The code is free (up to 11 characters); MOHAAPrefs takes the part between
`localization-` and `.txt`. Two-letter ISO 639-1 codes are the usual
choice:

| Language | File | First line (the name MOHAAPrefs shows) |
|---|---|---|
| German | `main/global/localization-de.txt` | `// OpenMoHAA language: Deutsch` |
| French | `main/global/localization-fr.txt` | `// OpenMoHAA language: Français` |
| Spanish | `main/global/localization-es.txt` | `// OpenMoHAA language: Español` |
| Italian | `main/global/localization-it.txt` | `// OpenMoHAA language: Italiano` |

### Examples

The English texts below are the game's own.

`localization-de.txt`
```
// OpenMoHAA language: Deutsch
{ "Health" "Gesundheit" }
{ "Game Saved" "Spiel gespeichert" }
{ "An objective has been added!" "Ein Ziel wurde hinzugefügt!" }
{ "German checkpoint, 200 yards." "Deutscher Kontrollpunkt, 200 Yards." }
{ "Press the USE key  ( &&& ) to grab items off tables." "Drücke die BENUTZEN-Taste  ( &&& ), um Gegenstände von Tischen zu nehmen." }
```

`localization-fr.txt`
```
// OpenMoHAA language: Français
{ "Health" "Santé" }
{ "Game Saved" "Partie sauvegardée" }
{ "An objective has been added!" "Un objectif a été ajouté !" }
{ "German checkpoint, 200 yards." "Poste de contrôle allemand, à 200 yards." }
{ "Press the USE key  ( &&& ) to grab items off tables." "Appuie sur la touche UTILISER  ( &&& ) pour prendre les objets sur les tables." }
```

`localization-es.txt`
```
// OpenMoHAA language: Español
{ "Health" "Salud" }
{ "Game Saved" "Partida guardada" }
{ "An objective has been added!" "¡Se ha añadido un objetivo!" }
{ "German checkpoint, 200 yards." "Control alemán, a 200 yardas." }
{ "Press the USE key  ( &&& ) to grab items off tables." "Pulsa la tecla USAR  ( &&& ) para coger objetos de las mesas." }
```

### Rules

- Save the file as **UTF-8**. Letters such as ä ö ü ß é è à ç ñ ¿ ¡ are in
  the game's own fonts. For Turkish the game adds the missing letters
  (ğ ı İ ş Ğ Ş) to its fonts itself.
- The English text on the left must be **exactly** the game's, spaces
  included ("key  (" above has two spaces, as in the game). Take it from a
  template rather than typing it (see below).
- `&&&` is a value the game puts in later (a key name, a number, a player
  name). Keep the same number of them; they may move in the sentence.
- Keep spaces at the start and end of a text: the game builds some
  sentences from pieces.
- No double quotes (`"`) inside a translation (use `'`), at most 255
  bytes a line.
- Lines you leave out stay in English.

### Translating the game

Translations can be made now, before the first release, on a PC (Windows,
Linux, macOS) with [Python 3](https://www.python.org/) and your own copy of
the game. The [`translation`](translation/) folder has what you need:

| File | What it is |
|---|---|
| [`mklang.py`](translation/mklang.py) | the translation tool (Python 3, nothing else needed) |
| [`localization-template.txt`](translation/localization-template.txt) | the list of every string of the three games (about 3,900), as hashes: it holds no text of the game, it is used to count your progress |

The English text comes from your own installed game; it is not in this
repository (it belongs to EA).

1. **Make your working file** from the game's folders (`main` is enough
   for Allied Assault; add `mainta` and `maintt` for the expansions):

   ```
   python mklang.py template localization-de.txt "C:\Games\MOHAA\main" "C:\Games\MOHAA\mainta" "C:\Games\MOHAA\maintt"
   ```

   Every line has the English on both sides:
   `{ "Game Saved" "Game Saved" }`.
2. **Translate**: put the language's name on the first line
   (`// OpenMoHAA language: Deutsch`) and change the right side of the
   lines. Leave the left side exactly as it is. Lines you do not change
   stay in English in the game.
3. **Check** it for lines the game would not take (too long, `&&&`
   missing, spaces):

   ```
   python mklang.py check localization-de.txt
   ```
4. **See how far you are**:

   ```
   python mklang.py progress localization-de.txt localization-template.txt
   localization-de.txt: 1250 of 3860 strings translated (32.4%)
   ```
5. **Try it** in the game: copy the file to the Amiga as
   `main/global/localization-de.txt` and choose the language in MOHAAPrefs.
6. **Share it**: turn it into a file without the game's English text and
   share that one (open an issue or a pull request here):

   ```
   python mklang.py publish localization-de.txt localization-de.share.txt
   ```

   ```
   // OpenMoHAA language: Deutsch
   { "#04e3c5d0" "Deutscher Kontrollpunkt, 200 Yards." }
   ```

   The game reads this form the same way: it matches each `#` key with
   the hash of the English text. Players put it in
   `main/global/localization-de.txt` too.

The included Turkish translation is shipped in this shared form.

**Where do the words behind the hashes come from?** From your own game.
You never translate hashes: `template` gives you the English, and to work
on a shared file (to correct or finish someone's translation),
`unhash` puts the English from your game back in front of each line.
Lines nobody has translated yet come with the English on both sides:

```
python mklang.py unhash localization-tr.txt localization-tr.work.txt "C:\Games\MOHAA\main" "C:\Games\MOHAA\mainta" "C:\Games\MOHAA\maintt"
```

```
{ "Game Saved" "Oyun Kaydedildi" }
{ "Health" "Sağlık" }
```

Then continue from step 2, and `publish` it again when you are done.

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
