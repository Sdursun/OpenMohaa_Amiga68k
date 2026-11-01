#!/usr/bin/env python3
"""
mklang.py: translations for OpenMoHAA on AmigaOS
(https://github.com/Sdursun/OpenMohaa_Amiga68k), Medal of Honor: Allied
Assault, Spearhead and Breakthrough. Python 3, no other modules needed.

The game shows translated subtitles, objectives, HUD messages and menu text
from a plain UTF-8 text file in the game folder:
    main/global/localization-<code>.txt
One file serves the base game and both expansions. Its first line names the
language for MOHAAPrefs:
    // OpenMoHAA language: Deutsch
Each entry is one line, the English exactly as the game has it (spaces
included: the game joins pieces such as "Press the USE key ( " + key),
then the translation:
    { "English" "Translation" }
or, in a file to share, a hash of the English instead of the English
("#" + 8 hex digits, made by "publish"), so that it holds no text of the
game. Empty translations and unchanged lines are ignored by the game.
Rules: no double quotes inside a string, at most 255 bytes a line once
converted, keep &&& (a value the game puts in) and the spaces at the start
and end. Characters: those of Windows-1252 (Western European languages)
and the Turkish letters; the game converts the UTF-8 when it loads the file.

The game's text is EA's: the English comes from your own installed game,
it is never shipped.

Translating:
  1. python mklang.py template localization-de.txt <path>/main <path>/mainta <path>/maintt
     every English string of the games, on both sides of each line
  2. change the first line to the language's name and translate the right
     side of the lines (leave the left side as it is)
  3. python mklang.py check localization-de.txt
  4. python mklang.py progress localization-de.txt localization-template.txt
  5. try it: copy it to the Amiga as main/global/localization-de.txt and
     choose it in MOHAAPrefs
  6. python mklang.py publish localization-de.txt localization-de.share.txt
     the file to share (hash keys, no text of the game); it works in the
     game the same way

Commands:
  template <out.txt> <game folder> [<game folder> ...]
      a working file: every English string of the given games (main
      mainta maintt) on both sides
  check <localization-xx.txt>
      lines the game would not take
  progress <localization-xx.txt> <localization-template.txt>
      how many of the template's strings the translation covers
  publish <localization-xx.txt> <out.txt>
      the file to share: each English text replaced by its hash
  hashtemplate <out.txt> <game folder> [...]
      the list of all strings as hashes with empty translations
      (localization-template.txt)
  extract <game folder> <strings.json>
      the English strings as JSON, with their kind (menu/HUD, subtitle,
      map message)
  totext <translation.json> <out.txt> <language name>
  tojson <localization-xx.txt> <out.json>
      {"English": "translation"} JSON to the text file and back
"""
import glob
import json
import os
import re
import sys
import zipfile

LOC = "global/localization.txt"
# the game's tokenizer takes 256 bytes with the terminating zero
MAXTOKEN = 255
ENTRY = re.compile(r'\{\s*"([^"]*)"\s*"([^"]*)"\s*\}')


def paks(folder):
    """the game folder's paks in load order, without ours"""
    return [p for p in sorted(glob.glob(os.path.join(folder, "*.pk3")), key=lambda p: os.path.basename(p).lower())
            if not os.path.basename(p).lower().startswith("zz_amiga")]


def files(folder, pattern):
    """{name: text} of the files matching pattern, the last pak's copy"""
    out = {}
    for pak in paks(folder):
        with zipfile.ZipFile(pak) as z:
            for name in z.namelist():
                if re.match(pattern, name, re.I):
                    out[name.lower()] = z.read(name).decode("latin-1")
    return out


def code_lines(text):
    for line in text.splitlines():
        s = line.strip()
        if s and not s.startswith("//"):
            yield line


SCRIPT_TEXT = re.compile(
    r'(?:add_objectives\s+\S+\s+\S+|iprintlnbold(?:_noloc)?|iprintln(?:_noloc)?|centerprint|'
    r'loc_convert_string|hint|settext)\s+"([^"]+)"', re.I)


def strings(folder):
    """{English: kind} of a game folder; the keys are the game's bytes
    (Windows-1252) read as Latin-1"""
    out = {}

    def add(s, kind):
        if s.strip() and s not in out:
            out[s] = kind

    for name, text in files(folder, re.escape(LOC) + "$").items():
        for m in ENTRY.finditer(text):
            add(m.group(1), "loc")
    for name, text in files(folder, r".*\.scr$").items():
        for line in code_lines(text):
            for m in re.finditer(r'(?:force)?subtitle\s+"([^"]*)"', line, re.I):
                add(m.group(1), "sub")
            for m in SCRIPT_TEXT.finditer(line):
                add(m.group(1), "map")
    return out


def game_text(s):
    """the game's bytes (read as Latin-1) as the Windows-1252 text they are,
    for a UTF-8 file; the game converts it back when it loads the file"""
    return s.encode("latin-1").decode("cp1252", errors="replace")


def extract(folder, out):
    found = strings(folder)
    with open(out, "w", encoding="utf-8") as f:
        json.dump([{"en": s, "kind": k} for s, k in found.items()], f, ensure_ascii=False, indent=1)
    kinds = {}
    for k in found.values():
        kinds[k] = kinds.get(k, 0) + 1
    print("%s: %d strings %s" % (out, len(found), kinds))


HEADER = """// OpenMoHAA language: %s
// A translation of Medal of Honor: Allied Assault, Spearhead and
// Breakthrough for OpenMoHAA. Put it in the game folder as
// main/global/localization-<code>.txt and choose it in MOHAAPrefs.
// One entry a line: { "English, exactly as the game has it" "translation" }
// No double quotes inside a string, at most 255 bytes, keep &&& and the
// spaces at the start and end. UTF-8.
"""


def write_text(path, name, pairs):
    with open(path, "w", encoding="utf-8", newline="\r\n") as f:
        f.write(HEADER % name)
        for en, tr in pairs:
            f.write('{ "%s" "%s" }\n' % (en, tr))
    print("%s: %d entries" % (path, len(pairs)))


def template(out, folders):
    found = {}
    for folder in folders:
        for s in strings(folder):
            found.setdefault(s, None)
    write_text(out, "(name of the language)", [(game_text(s), game_text(s)) for s in found])


# a double quote would end the string (the game converts the rest; a
# backslash stays, the game's own file has "\n" in some entries)
REPLACE = {'"': "'"}


def totext(translation, out, name):
    with open(translation, encoding="utf-8") as f:
        tr = json.load(f)
    pairs = []
    for en, text in tr.items():
        if not text or text == en:
            continue
        for a, b in REPLACE.items():
            text = text.replace(a, b)
        pairs.append((game_text(en), text))
    write_text(out, name, pairs)


def read_text(path):
    with open(path, encoding="utf-8-sig") as f:
        # comments as the game's tokenizer skips them (the header has an example)
        text = "\n".join(l for l in f.read().splitlines() if not l.lstrip().startswith("//"))
    return [(m.group(1), m.group(2)) for m in ENTRY.finditer(text)]


def tojson(path, out):
    pairs = read_text(path)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(dict(pairs), f, ensure_ascii=False, indent=1)
    print("%s: %d entries" % (out, len(pairs)))


def font_bytes(s):
    """the bytes the game makes of a string when it loads the file"""
    out = bytearray()
    turkish = {"Ğ": 0xD0, "ğ": 0xF0, "İ": 0xDD, "ı": 0xFD, "Ş": 0xDE, "ş": 0xFE}
    for ch in s:
        if ch in turkish:
            out.append(turkish[ch])
        else:
            try:
                out += ch.encode("cp1252")
            except UnicodeEncodeError:
                out += b"?"
    return bytes(out)


def check(path):
    bad = 0
    for en, tr in read_text(path):
        problems = []
        if len(font_bytes(tr)) > MAXTOKEN:
            problems.append("longer than %d bytes" % MAXTOKEN)
        if en.count("&&&") != tr.count("&&&"):
            problems.append("&&& count differs")
        if (en[:1] == " ") != (tr[:1] == " ") or (en[-1:] == " ") != (tr[-1:] == " "):
            problems.append("leading/trailing spaces differ")
        if b"?" in font_bytes(tr) and "?" not in tr:
            problems.append("characters the fonts do not have")
        if problems:
            bad += 1
            print("%s: %s" % (", ".join(problems), en))
    print("%s: %d entries with problems" % (path, bad))


def loc_hash(data):
    """FNV-1a 32 over the game's bytes, as the game computes it"""
    h = 2166136261
    for b in data:
        h = ((h ^ b) * 16777619) & 0xFFFFFFFF
    return h


def publish(path, out):
    with open(path, encoding="utf-8-sig") as f:
        name = "?"
        for line in f:
            m = re.search(r"language:\s*(.+)", line)
            if m:
                name = m.group(1).strip()
                break
    seen = {}
    pairs = []
    for en, tr in read_text(path):
        if not tr or tr == en:
            continue
        h = loc_hash(font_bytes(en))
        if h in seen and seen[h] != en:
            sys.exit("hash collision: %r and %r" % (seen[h], en))
        seen[h] = en
        pairs.append(("#%08x" % h, tr))
    with open(out, "w", encoding="utf-8", newline="\r\n") as f:
        f.write("// OpenMoHAA language: %s\n" % name)
        f.write("// Keyed by a hash of the English text (mklang.py publish).\n")
        for key, tr in pairs:
            f.write('{ "%s" "%s" }\n' % (key, tr))
    print("%s: %d entries" % (out, len(pairs)))


def hashtemplate(out, folders):
    found = {}
    for folder in folders:
        for s in strings(folder):
            found.setdefault(s, None)
    with open(out, "w", encoding="utf-8", newline="\r\n") as f:
        f.write("// OpenMoHAA language: (template)\n")
        f.write("// Every string of Allied Assault, Spearhead and Breakthrough, as a hash\n")
        f.write("// of the English text (the game's text is not in this file). Use it\n")
        f.write("// with \"mklang.py progress\"; translate with \"mklang.py template\".\n")
        for s in found:
            f.write('{ "#%08x" "" }\n' % loc_hash(s.encode("latin-1")))
    print("%s: %d strings" % (out, len(found)))


def key_hash(key):
    """the hash of an English key or of a "#" key"""
    if re.match(r"^#[0-9a-fA-F]{8}$", key):
        return int(key[1:], 16)
    return loc_hash(font_bytes(key))


def progress(path, template):
    wanted = [key_hash(k) for k, _ in read_text(template)]
    done = {key_hash(k) for k, tr in read_text(path) if tr and tr != k}
    n = sum(1 for h in wanted if h in done)
    print("%s: %d of %d strings translated (%.1f%%)" % (path, n, len(wanted), 100.0 * n / max(len(wanted), 1)))


def main():
    a = sys.argv[1:]
    if len(a) >= 3 and a[0] == "extract":
        extract(a[1], a[2])
    elif len(a) >= 3 and a[0] == "template":
        template(a[1], a[2:])
    elif len(a) >= 4 and a[0] == "totext":
        totext(a[1], a[2], a[3])
    elif len(a) >= 3 and a[0] == "tojson":
        tojson(a[1], a[2])
    elif len(a) >= 2 and a[0] == "check":
        check(a[1])
    elif len(a) >= 3 and a[0] == "hashtemplate":
        hashtemplate(a[1], a[2:])
    elif len(a) >= 3 and a[0] == "progress":
        progress(a[1], a[2])
    elif len(a) >= 3 and a[0] == "publish":
        publish(a[1], a[2])
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
