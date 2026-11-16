# AISLING FX-1 for the M-VAVE FM-1

<img src="docs/card-fx1.png" width="240" height="240" alt="AISLING FX-1: a gold 8-bit harp on green, with FX beside it">

**[Download 1.1](https://github.com/stephencummins/fx1-aisling/releases/tag/v1.1)** · **[Manual](docs/FX1.md)** ·
**[Controls](docs/img/fx1-controls.svg)** · **[AISLING](https://aisling.stephen8n.com/)**

By CU_STE · [www.stephen8n.com](https://www.stephen8n.com)

## What?

AISLING FX-1 turns an M-VAVE FM-1 into an effects box for a computer. Connect the FM-1 to the computer with a USB
cable and choose **AISLING FX-1** as the computer's sound output: whatever the computer plays (a song, a track in your
music software, a browser tab) comes in over the cable, goes through AISLING's filter, its echo and its plate reverb
and the effects on its keys, and comes out of the FM-1's 3.5 mm socket. The same sound goes back up the cable too, so
the computer can record it. It needs no driver: it is a standard USB audio device, 44.1 kHz, 16-bit, stereo.

It is [AISLING](https://github.com/stephencummins/fm1-aisling) with its voices taken out: no harps, no drone, no flute,
only what the computer sends. The same source builds both; `--fx` builds this one.

**Status: 1.1.** FX-1 1.0 has run on one FM-1 (the first flash chip) with a Mac playing through it:
no gaps, no lost packets, and it sounds right. The 1.0 package has gone on over AISLING 1.4 and over the stock
firmware (V16), and AISLING 1.4 back over it. 1.1 is 1.0 with a light screen to choose (the Journey page's Screen:
Dark, or Light, the same colours deeper, on white; saved) and the knob strip's dividers moved clear of the names;
the sound is 1.0's. 1.1 has gone on one FM-1 over AISLING 1.4.1 and its screen looked right; sound has not been played through 1.1 yet.
Not yet known: the latency, a long session, a newer
FM-1, other computers. The [manual](docs/FX1.md#8-what-has-been-tried) keeps the list.

**Saved settings.** FX-1 is AISLING underneath, so it saves where AISLING does, in AISLING's own format, and reads
what AISLING saved: it starts on the piece AISLING was playing, with that piece's echo and reverb, and a save in FX-1
stores its settings as that piece's. It doesn't save by itself: hold GLO (or SAVE) for half a second. It doesn't read
what NACHTFAHRT, DUB-1 or AMB-1 saved (it starts on AISLING's own recipes), and they save in the same place in the
FM-1's memory, so a save in FX-1 replaces theirs, and theirs replaces FX-1's. Installing another firmware may lose
what FX-1 saved. FX-1 uses no samples.

**MIDI.** FX-1 sends no notes and no clock. With Setup's MIDI out on, an effect you play sends its CC on channel 16.
What comes in is as in AISLING: CC 74 the Filter, CC 16 to 19 the page's four knobs, each effect's own CC, and a
program change chooses a piece (and with it the echo's and the reverb's settings).

## In short

| | |
|---|---|
| MASTER | The level at the 3.5 mm socket (the stream back to the computer doesn't follow it) |
| HOME's knobs | **Filter** (off in the middle; low-pass down, high-pass up) · **Echo** · **Reverb** · **Dry** (0: only the echo and the plate, for a send and return; 100 at every start) |
| FX | The Space page (Echo, Echo time, Feedback, Reverb); again, the Echo page (Blur, Tone, Width, Size) |
| SEL | PERFORM: 17 of its 27 keys are effects on the computer's sound while held; the knobs Filter, Wet, Chorus |
| Black keys | Shimmer, Freeze, Macalla and Fras, while held |
| REC | A tap: hold (the echo and the plate repeat what they have); held: the effects grid on the white keys |
| PLAY | Play / rest: the sound comes through either way; playing, the Filter and the echo drift a little by themselves |
| PRESETS | The piece underneath: its echo and reverb settings and its tempo, which the echo's time counts in |
| GLO | Setup (MIDI out, Save, the sleep timer). Held: save |

The voices' pages (ENV, ARP, LFO, SEQ, SAVE, EDIT) are still there and change nothing you can hear. The screen shows
the sound coming in: its state (NO COMPUTER, NOTHING SENT YET, OPEN, NO PACKETS, PLAYING), the level left and right,
and the stream's counts. The [manual](docs/FX1.md) has every control, key and count.

## Installing

Install it from Chrome or Edge on [its install page](https://aisling.stephen8n.com/fx1/install/). Or download
`aislingfx-1.1.fwsc` from [the 1.1 release](https://github.com/stephencummins/fx1-aisling/releases/tag/v1.1)
and install it over AISLING, another firmware or the stock one with the command-line installer, which is in this
repository (Python 3 with mido and python-rtmidi; the FM-1 connected by USB):

```
git clone https://github.com/stephencummins/fx1-aisling
pip3 install mido python-rtmidi
python3 fx1-aisling/tools/fm1_install.py aislingfx-1.1.fwsc
```

Its identity is FM-1_391 and six digits (1.1 is FM-1_391010100), so The Firmware Hub and AISLING's web installer
don't take it for AISLING. To go back, install AISLING from its [web installer](https://aisling.stephen8n.com/install/),
or the stock firmware ([Back to stock](https://aisling.stephen8n.com/install/#stock)).

## Building and testing

The toolchain is AISLING's, NACHTFAHRT's and DUB-1's (see [BUILDING.md](BUILDING.md)):

```
tests/run_tests.sh      # the engine, the platform, the app in a simulator, FX-1's own tests
./build.sh --fx         # build/aislingfx-dev.fwsc (--release 1.1 --fx: build/aislingfx-1.1.fwsc)
./build.sh              # without --fx: AISLING, byte for byte
```

`build/host/amb_host_fx SCRIPT OUTDIR` (from `host/build_host.sh`) runs FX-1 on a computer from a script
(`tests/scenarios-fx/`), with audio and screenshots coming out; `AMB_FXSTATE` sets the stream's state.

## Credits

AISLING FX-1 is by CU_STE ([www.stephen8n.com](https://www.stephen8n.com)). It is AISLING's own code with a second
USB sound stream, the one coming in, and the voices left out; everything else is AISLING's, and comes from where
AISLING's does. AISLING is a fork of [NACHTFAHRT](https://github.com/FartyPants/fm1-nachtfahrt) by FartyPants
(GPL-3.0-only), a fork of [DUB-1](https://github.com/sbegueria/fm1-dub), a fork of
[AMB-1](https://github.com/charlesvestal/fm1-amb) by Charles Vestal (GPL-3.0-only): the echo chain, the plate, the
pieces system, the UI and the platform come from there. The reverb is Jon Dattorro's plate ("Effect Design, Part 1",
JAES 1997), as in [FoMni-1](https://github.com/charlesvestal/fm1-fomni); Shimmer's octave shifter follows OCT UP and
its SHIMMER in [Felucca](https://github.com/hugelton/Felucca)'s performance layer (Leo Kuroshita, Hügelton
Instruments; also in [Skiff](https://github.com/illuminus5/skiff)); the granular cloud (Freeze) follows the design of
CLOUD in [JIANT](https://github.com/juanjiant-bit/JIANT) (GPL-3.0). The platform (hardware layer, USB, update loader,
storage, installer) is [Felucca](https://github.com/hugelton/Felucca)'s
by Leo Kuroshita (Hügelton Instruments), by way of [X0X](https://github.com/charlesvestal/fm1-x0x), FoMni-1, AMB-1,
DUB-1 and NACHTFAHRT. The sleep timer is an idea from [ZEN-1](https://github.com/aceyprime/zen-1) (aceyprime) and
[Penumbra](https://github.com/MadMooneyham/Penumbra) (Lunar Eclipse Forge), and program change and MIDI CCs for the
knobs from Penumbra. AISLING's [README](https://github.com/stephencummins/fm1-aisling#credits) has its full credits,
for the voices this build leaves out. GPL-3.0-only; see [LICENSING.md](LICENSING.md).

M-VAVE and FM-1 are trademarks of their owners. AISLING FX-1 is not affiliated with M-VAVE, Hügelton Instruments or
NACHTFAHRT's author.
