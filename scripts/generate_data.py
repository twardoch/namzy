#!/usr/bin/env python3
# this_file: scripts/generate_data.py
"""Generate stem packs, syllable rotations, bad-seam list, and per-language wordlist sources.

Design (issue #102):
- 10 disciplines, hand-curated, ≤2 syllables and ≤7 chars each, ~100 stems per pack.
- Syllable-based rotations: only "safe" CV-pair swaps + a few unambiguous letter swaps.
- Bad-seam list: reject candidates with double identical vowels, triple letters, etc.

Source of truth: this file. Outputs:
  data/{cities,rivers,colors,adjectives,nouns,verbs,names,trees,birds,gems,weather,myth}.txt
  data/rotations.txt
  data/badseams.txt
  namzy-ts/src/wordlist.ts
  namzy-py/src/namzy/_wordlist.py
  namzy-rs/src/wordlist.rs
  namzy-cpp/src/wordlist.{h,cpp}
"""
from __future__ import annotations
from pathlib import Path
from typing import Sequence

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

# ----------------------- Stem source pools -----------------------
# Hand-curated. The filter below keeps only ≤2-syllable, ≤7-char words.
# Goal: ≥80 surviving stems per pack.

CITIES = """paris tokyo milan rome oslo lima baku doha kiev riga sofia kabul
dakar cairo accra perth miami boston dallas denver vegas omaha tulsa fargo
salem mobile dover leeds york derby bath hull kent devon essex berlin munich
bremen bonn jena mainz madrid lisbon porto faro evora braga athens sparta
rhodes crete naxos delos rabat oran tunis sana mecca jeddah aden dubai amman
mosul basra herat lahore dhaka delhi agra pune surat patna hanoi manila cebu
davao medan beijing wuhan xian dalian taipei seoul busan daegu kobe sydney
hobart darwin cairns alice cuzco quito cali natal leon merida cancun austin
fresno durham eugene boise reno juneau topeka dublin galway cork bergen tromso
malmo turku kazan samara tomsk omsk perm minsk warsaw krakow brno linz graz
basel geneva lyon nantes nice dijon reims lille rouen calais cannes tours metz
brest naples turin genoa verona pisa siena parma bari aarhus tallinn vilnius
shanghai osaka kyoto pune patna ankara izmir bursa konya gdansk lodz prague
zurich bern oslo madrid sevilla bilbao toledo dakar lagos durban accra essen""".split()

RIVERS = """nile volga rhine seine thames tiber indus congo niger douro tagus
ebro loire elbe oder don ural lena amur chao jordan snake platte ohio red gila
fraser peace copper yampa green pearl james hudson mohawk fox iowa cedar grand
white salt trinity neches medina leon po arno reno taro ticino oglio adda
mincio piave brenta ems weser saale havel spree main neckar lech isar inn
drava sava tisza prut olt mures somes drin tay clyde forth tweed spey severn
trent avon dee esk wye usk lee suir nore boyne bann erne moy lagan parana
amazon mekong yukon ganges yangtze ob tweed elbe meuse rhone tarn lot var ain
aisne marne yonne saone tilt tay teme dove ouse swale ure tees coquet aire""".split()

COLORS = """azure amber coral ivory jade lilac mauve ochre olive pearl ruby
sepia teal umber plum cobalt cyan navy salmon beige linen mint peach rose sand
sky slate snow tan wine bronze copper gold brass cherry hazel honey lemon lime
cream cocoa mocha sage taupe fern flax ginger grape khaki orchid moss rust
sienna spruce jasper ash fawn dust gray char ink ebony frost silver claret
garnet jet onyx blush rouge crimson scarlet magenta indigo violet cobalt poppy
saffron citrus papaya melon thistle topaz quartz pewter saddle smoke fuchsia
chestnut buff brick coffee dune apricot dawn vine moss ember rust seal heliotrope
opal coral mango chia ivory pine bay umber sable opal opal cream khaki ochre""".split()

ADJECTIVES = """brave bright calm clever cool deep eager fair fine glad grand
happy keen kind merry neat noble proud quick quiet swift warm wise witty young
jolly lucky mighty smart snappy spry sunny super tidy true vivid wild zippy
able active alert ample apt artful balmy bold breezy brisk chic chill cosy
crisp dapper deft divine dreamy easy elated epic exact fancy fluent fresh
funky gallant gentle gifted glossy hardy hearty honest hopeful humble jaunty
jazzy jovial joyful keen lavish light limber lithe lovely loyal lucid lush
mellow mild modest nifty nimble noble peppy perky placid plucky plush polite
posh prime prompt pure quaint quirky rapid rare regal robust rosy royal rugged
sassy savvy serene sharp shiny silky sleek slick smooth snug solid spry stable
steady stoic strong stylish suave subtle sturdy supple svelte tender thrifty""".split()

NOUNS = """harbor haven cove glade meadow grove summit ridge peak canyon vista
oasis sanctum atrium plaza forum agora portal beacon torch ember spark flame
prism orbit comet zenith apex crown laurel medal trophy gem jewel pearl charm
token coin badge crest emblem sigil banner arrow anchor compass keystone
pillar lantern keep tower castle bastion manor cottage cabin lodge chalet villa
palace temple shrine altar chapel garden grotto spring brook creek tide wave
swell shell coral reef port pier dock wharf isle atoll cape cliff bluff mesa
valley vale dale fen heath moor delta lagoon fjord sound channel bay gulf inlet
beach dune basalt granite quartz crystal opal agate jade onyx topaz beryl
jasper malachite citrine zircon spinel falcon eagle hawk swan crane heron robin
sunbeam rainbow zephyr breeze gale storm thunder amulet chalice flute lyre""".split()

VERBS = """soar glide drift float flow leap dash sprint march wander roam
voyage venture journey travel embark launch spark ignite kindle awaken arise
rise climb ascend bloom blossom flower grow expand evolve elevate enliven
inspire spark uplift nurture foster shelter guard protect uphold support
sustain anchor steady balance align tune compose craft fashion forge sculpt
shape mold weave thread knit stitch braid build raise discover unveil reveal
unfold open share spread gather collect compile unite bond join meld merge
blend fuse synthesize connect link bridge converge rally thrive prosper achieve
attain master prevail excel shine glow gleam glimmer sparkle radiate beam
flash flutter dart dive surge swirl spin twirl pivot hover linger swoop
cascade tumble vault bound bounce skip prance gambol caper romp frolic cavort""".split()

NAMES = """ada alex amy ana avi ben bea cam dan dee eli emma eva finn gus
hugo ian iris ivan jade jane juno kai kit lena liam lila luca lyra maya mia
milo nia noah nora oli omar otto piper quinn rex rio ron sage sam sara seth
sky theo tom uma vera vic will xander yael yuki zane zara alma anya beau cole
cora dane dora elsa enzo erin esme gabe gina hank iggy inez ivy jack joel juno
kade kara kira kyle lana lars leah leon lily luna mack maeve mads matt myra
nash neil niko odin oren orin pax pete raj rena rhys riya rome rosa ruth ryan
seth shay simon sloan stef tara teo tess thane tilda toby vance vita vlad walt
wes wren xenia yves zara zeke zion abe alan amir andi arlo asher aster august
bea beck beth blake bo bruno cael cain cal calla cara casey cass cato cyrus""".split()

TREES = """oak elm ash fir pine cedar maple birch beech alder hazel holly ivy
fern rowan larch yew bay palm aspen poplar willow olive lime hawthorn cherry
walnut chestnut hornbeam linden cypress juniper sycamore plane laurel mulberry
fig peach plum pear apple lemon mango mango orange almond cacao banyan baobab
mahogany teak ebony rose dogwood box quince spruce balsa sandal myrtle locust
poplar tamarack hickory pecan oak elm fir pine cedar maple birch beech ash
yew bay holly ivy elder fern rowan willow olive lime hawthorn cherry walnut
chestnut linden cypress sycamore plane laurel mulberry fig peach plum pear apple
lemon mango orange almond cacao baobab teak ebony rose dogwood box quince spruce""".split()

BIRDS = """robin finch wren hawk owl falcon swan crane lark raven dove jay
kestrel heron ibis kite eagle vulture buzzard merlin osprey peacock parrot
ostrich emu kiwi puffin gull tern petrel kingfisher cuckoo magpie thrush nightingale
blackbird sparrow martin swallow swift swiftlet plover snipe woodcock pheasant
quail partridge grouse turkey rooster hen duck goose teal mallard goose pelican
flamingo stork bittern cormorant guillemot razorbill auk loon grebe coot rail
moorhen pigeon dove starling jackdaw rook crow oriole tanager warbler tit chickadee
pipit lark wagtail bunting linnet siskin redpoll waxwing redwing fieldfare
shrike hoopoe bee-eater roller hornbill toucan macaw cockatoo lorikeet budgie""".split()

GEMS = """jade ruby opal onyx quartz beryl agate amber jasper pearl topaz
garnet zircon spinel lapis pyrite calcite mica gypsum barite kyanite
flint chert shale slate basalt granite marble coral bone ivory horn
antler ebony jade opal onyx quartz beryl agate amber jasper pearl topaz
garnet zircon spinel coral chert shale flint slate marble gypsum barite
mica calcite pyrite kyanite jade onyx opal ruby pearl beryl amber agate""".split()

WEATHER = """storm mist dawn dusk rain frost fog haze ice snow cloud breeze
gust gale tempest squall blizzard hail sleet drizzle thunder lightning rainbow
zephyr aurora twilight sunset sunrise moonbeam starlight noon meridian solstice
equinox horizon vapor steam cinder ash spray spume foam shower deluge monsoon
hurricane typhoon cyclone tornado vortex eddy current draft draught chill
warmth glow shimmer haze blaze flare flash bolt cosmos comet asteroid nebula
pulsar quasar galaxy planet star moon sun sky cloud rain storm mist dawn dusk
frost fog haze ice snow breeze gust gale squall hail sleet drizzle thunder""".split()

MYTH = """thor odin loki freya frigg hel baldr tyr atlas hera juno mars vesta
ceres leto niobe isis ra hathor osiris anubis horus apis ptah thoth bast set
seshat ammit khonsu sobek bes maat shiva vishnu rama sita kali durga indra
ganesh hanuman kuber surya soma agni vayu prana nataraj parvati lakshmi saraswati
mira yama zeus apollo ares poseidon hades demeter athena artemis hermes hephaestus
dionysus iris hebe hecate selene helios eos nyx erebus aether chaos gaia uranus
cronus rhea oceanus tethys phoebe themis mnemosyne pan triton nereus proteus
calypso circe medusa scylla charybdis pegasus chimera hydra cerberus minotaur""".split()

# ---------------------- Filtering ----------------------
def syllables(w: str) -> int:
    """Approximate syllable count via vowel-group runs."""
    groups, in_v = 0, False
    for c in w:
        v = c in "aeiouy"
        if v and not in_v:
            groups += 1
        in_v = v
    return max(1, groups)


def fit(pack: Sequence[str], label: str, min_count: int = 25, cap: int = 110) -> list[str]:
    """Filter one discipline pack down to short, pronounceable, unique stems.

    Keeps 3–7 letter, ≤2-syllable, alphabetic words, dropping duplicates within
    the pack. Raises if a pack cannot supply ``min_count`` survivors so a thinned
    source list fails loudly at generation time rather than silently shrinking.
    """
    seen: set[str] = set()
    out: list[str] = []
    for w in pack:
        w = w.strip().lower()
        if not w or not w.isalpha():
            continue
        if not (3 <= len(w) <= 7):
            continue
        if syllables(w) > 2:
            continue
        if w in seen:
            continue
        seen.add(w)
        out.append(w)
        if len(out) >= cap:
            break
    if len(out) < min_count:
        raise SystemExit(f"{label}: only {len(out)} short stems (need ≥{min_count})")
    return out


PACKS = {
    "cities":     fit(CITIES,     "cities"),
    "rivers":     fit(RIVERS,     "rivers"),
    "colors":     fit(COLORS,     "colors"),
    "adjectives": fit(ADJECTIVES, "adjectives"),
    "nouns":      fit(NOUNS,      "nouns"),
    "verbs":      fit(VERBS,      "verbs"),
    "names":      fit(NAMES,      "names"),
    "trees":      fit(TREES,      "trees"),
    "birds":      fit(BIRDS,      "birds"),
    "gems":       fit(GEMS,       "gems"),
    "weather":    fit(WEATHER,    "weather"),
    "myth":       fit(MYTH,       "myth"),
}

# ---------------------- Syllable rotations ----------------------
# Each rule is (src, dst). The algorithm finds every position in the candidate
# where `src` occurs as a substring and applies the rewrite to exactly one
# randomly-selected occurrence. Pairs are reversible (a→b is balanced by b→a).
# All pairs preserve length and pronounceability.

# Safe open-CV-syllable swaps: consonant followed by vowel.
_CV_SWAPS = []
_CONSONANTS = list("bcdfghjklmnprstvwz")
# Vowel rotation cycle. We use ONLY adjacent vowel swaps (no e<->a leap).
_VOWEL_PAIRS = [("a", "o"), ("o", "a"), ("i", "y"), ("y", "i"),
                ("e", "i"), ("i", "e"), ("o", "u"), ("u", "o")]
for c in _CONSONANTS:
    for v1, v2 in _VOWEL_PAIRS:
        _CV_SWAPS.append((c + v1, c + v2))

# Unambiguous letter swaps (no syllable disruption):
_LETTER_SWAPS = [
    ("k", "q"), ("q", "k"),
    ("c", "k"), ("k", "c"),   # safe before a/o/u — bad-seam filter handles edge cases
    ("ph", "f"), ("f", "ph"),
    ("x", "ks"), ("ks", "x"),
]

ROTATIONS: list[tuple[str, str]] = _CV_SWAPS + _LETTER_SWAPS

# ---------------------- Bad-seam patterns ----------------------
# Reject candidates whose junction (or anywhere) matches any of these.
# Junction = the 4 chars centered on `len(first)`.
BAD_SEAMS = [
    "aa", "ee", "ii", "oo", "uu", "yy",  # double identical vowels at the seam
    "iy", "yi",                          # ambiguous /aɪ/ sound at seam
]
# Plus: reject any tripled letter (e.g., "sss", "lll") -- enforced in code.


# ---------------------- File writers ----------------------
def unified() -> list[str]:
    """Flatten every pack into one deduplicated stem list (~950 stems).

    Order follows ``PACKS`` insertion order; a stem shared by two packs (e.g. a
    color that is also a gem) appears once, at its first occurrence. This is the
    single list every language implementation bundles.
    """
    seen: set[str] = set()
    out: list[str] = []
    for words in PACKS.values():
        for w in words:
            if w not in seen:
                seen.add(w)
                out.append(w)
    return out


def write_data() -> None:
    DATA.mkdir(exist_ok=True)
    for name, words in PACKS.items():
        (DATA / f"{name}.txt").write_text("\n".join(words) + "\n")
    (DATA / "rotations.txt").write_text("\n".join(f"{a} {b}" for a, b in ROTATIONS) + "\n")
    (DATA / "badseams.txt").write_text("\n".join(BAD_SEAMS) + "\n")


def _q(s: str) -> str:
    return f'"{s}"'


def write_ts() -> None:
    stems = unified()
    body = '// this_file: src/wordlist.ts\n'
    body += '// AUTO-GENERATED by scripts/generate_data.py. Do not edit.\n\n'
    body += 'export const STEMS: readonly string[] = [\n'
    for i in range(0, len(stems), 8):
        body += "  " + ", ".join(_q(w) for w in stems[i:i + 8]) + ",\n"
    body += "];\n\n"
    body += 'export const ROTATIONS: readonly (readonly [string, string])[] = [\n'
    for a, b in ROTATIONS:
        body += f"  [{_q(a)}, {_q(b)}],\n"
    body += "];\n\n"
    body += 'export const BAD_SEAMS: readonly string[] = [\n'
    for s in BAD_SEAMS:
        body += f"  {_q(s)},\n"
    body += "];\n"
    (ROOT / "namzy-ts" / "src" / "wordlist.ts").write_text(body)


def write_py() -> None:
    stems = unified()
    body = "# this_file: src/namzy/_wordlist.py\n"
    body += "# AUTO-GENERATED by scripts/generate_data.py. Do not edit.\n\n"
    body += "STEMS: list[str] = [\n"
    for i in range(0, len(stems), 8):
        body += "    " + ", ".join(_q(w) for w in stems[i:i + 8]) + ",\n"
    body += "]\n\n"
    body += "ROTATIONS: list[tuple[str, str]] = [\n"
    for a, b in ROTATIONS:
        body += f"    ({_q(a)}, {_q(b)}),\n"
    body += "]\n\n"
    body += "BAD_SEAMS: list[str] = [\n"
    for s in BAD_SEAMS:
        body += f"    {_q(s)},\n"
    body += "]\n"
    (ROOT / "namzy-py" / "src" / "namzy" / "_wordlist.py").write_text(body)


def write_rs() -> None:
    stems = unified()
    body = "//! this_file: src/wordlist.rs\n"
    body += "//! AUTO-GENERATED by scripts/generate_data.py. Do not edit.\n\n"
    # `#[rustfmt::skip]` keeps the fixed 8-per-row layout so `cargo fmt --check`
    # in CI does not fight the generator over how these tables are wrapped.
    body += "#[rustfmt::skip]\npub static STEMS: &[&str] = &[\n"
    for i in range(0, len(stems), 8):
        body += "    " + ", ".join(_q(w) for w in stems[i:i + 8]) + ",\n"
    body += "];\n\n"
    body += "#[rustfmt::skip]\npub static ROTATIONS: &[(&str, &str)] = &[\n"
    for a, b in ROTATIONS:
        body += f"    ({_q(a)}, {_q(b)}),\n"
    body += "];\n\n"
    body += "#[rustfmt::skip]\npub static BAD_SEAMS: &[&str] = &[\n"
    for s in BAD_SEAMS:
        body += f"    {_q(s)},\n"
    body += "];\n"
    (ROOT / "namzy-rs" / "src" / "wordlist.rs").write_text(body)


def write_cpp() -> None:
    stems = unified()
    (ROOT / "namzy-cpp" / "src" / "wordlist.h").write_text("""// this_file: src/wordlist.h
// AUTO-GENERATED by scripts/generate_data.py. Do not edit.
#pragma once
#include <QStringList>
#include <QVector>
#include <QPair>
#include <QString>

namespace namzy {
const QStringList& stems();
const QVector<QPair<QString, QString>>& rotations();
const QStringList& badSeams();
}
""")
    body = """// this_file: src/wordlist.cpp
// AUTO-GENERATED by scripts/generate_data.py. Do not edit.
#include "wordlist.h"

namespace namzy {

const QStringList& stems() {
    static const QStringList s = {
"""
    for i in range(0, len(stems), 8):
        body += "        " + ", ".join(f'QStringLiteral("{w}")' for w in stems[i:i + 8]) + ",\n"
    body += """    };
    return s;
}

const QVector<QPair<QString, QString>>& rotations() {
    static const QVector<QPair<QString, QString>> r = {
"""
    for a, b in ROTATIONS:
        body += f'        {{ QStringLiteral("{a}"), QStringLiteral("{b}") }},\n'
    body += """    };
    return r;
}

const QStringList& badSeams() {
    static const QStringList s = {
"""
    for sm in BAD_SEAMS:
        body += f'        QStringLiteral("{sm}"),\n'
    body += """    };
    return s;
}

} // namespace namzy
"""
    (ROOT / "namzy-cpp" / "src" / "wordlist.cpp").write_text(body)


def main() -> None:
    write_data()
    write_ts()
    write_py()
    write_rs()
    write_cpp()
    print(f"unified stems: {len(unified())}")
    print(f"rotations: {len(ROTATIONS)}")
    print(f"bad seams: {len(BAD_SEAMS)}")
    for name, w in PACKS.items():
        print(f"  {name}: {len(w)}")


if __name__ == "__main__":
    main()
