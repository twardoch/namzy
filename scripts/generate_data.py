#!/usr/bin/env python3
# this_file: scripts/generate_data.py
"""Generate stem packs, rotation rules, and per-language wordlist sources.

Source of truth: this file. Outputs:
  data/{cities,rivers,colors,adjectives,nouns,verbs,names}.txt  (200 words each)
  data/rotations.txt
  namzy-ts/src/wordlist.ts
  namzy-py/src/namzy/_wordlist.py
  namzy-rs/src/wordlist.rs
  namzy-cpp/src/wordlist.cpp + wordlist.h
"""
from __future__ import annotations
from pathlib import Path
from typing import Sequence

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

# Stem packs. Each ~200 short, compact, portable, recognizable.
CITIES = """paris tokyo milan rome oslo lima baku doha kiev riga sofia kabul
dakar cairo accra perth miami boston dallas denver vegas omaha tulsa fargo
salem mobile tucson ottawa calgary dover leeds york derby oxford bristol
cardiff bath hull kent devon essex berlin munich bremen bonn jena mainz
madrid sevilla malaga bilbao toledo oviedo lisbon porto faro evora braga
athens sparta rhodes crete naxos delos rabat tangier oran tunis sana mecca
jeddah aden dubai manama beirut amman aleppo mosul basra shiraz tabriz herat
lahore dhaka mumbai delhi jaipur agra chennai pune surat bhopal indore
nagpur patna kandy galle lhasa hanoi manila cebu davao jakarta bandung medan
penang melaka beijing wuhan harbin chengdu ningbo xian dalian taipei seoul
busan daegu sapporo sendai nagoya kobe niigata sydney hobart darwin cairns
mackay alice auckland nelson napier cuzco quito bogota cali caracas recife
manaus natal asuncion santiago rosario havana nassau panama leon merida
oaxaca puebla cancun austin houston phoenix fresno oakland raleigh durham
nashville eugene boise reno juneau wichita topeka lincoln helena pierre
dublin galway cork bergen tromso aarhus malmo turku tampere kazan samara
tomsk omsk perm minsk vilnius tallinn warsaw krakow brno linz graz salzburg
basel geneva lyon nantes nice dijon reims lille rouen calais cannes tours
metz brest amiens orleans naples turin genoa verona pisa siena parma bari
""".split()

RIVERS = """nile amazon volga rhine danube seine thames tiber tigris ganges
indus mekong yukon hudson congo niger zambezi orinoco parana douro tagus ebro
loire elbe oder vistula dnieper don ural lena ob amur yangtze huang chao
brahma yamuna kaveri jordan euphrates orange limpopo senegal gambia okavango
murray darling colorado snake platte ohio missouri illinois arkansas red
brazos pecos rio gila salmon willamette sacramento klamath fraser nelson
churchill ottawa peace mackenzie liard skeena thompson saskatchewan athabasca
saint lawrence saguenay copper kobuk noatak yampa green colorado roanoke
savannah neuse cape pearl mobile alabama tombigbee chattahoochee suwannee
santee broad oconee black tar peedee yadkin catawba cumberland tennessee
kanawha shenandoah james potomac susquehanna delaware hudson connecticut
penobscot kennebec androscoggin merrimack thames housatonic genesee mohawk
oswego niagara maumee wabash cuyahoga muskingum scioto miami licking green
barren rock fox illinois sangamon iowa cedar des moines wapsipinicon skunk
chariton grand gasconade meramec current eleven black white cache buffalo
neosho verdigris cimarron washita canadian salt brazos colorado nueces frio
pecos llano san sabine trinity neches lavaca guadalupe medina concho leon
po arno tevere adige reno taro ticino oglio adda mincio piave brenta
ems weser saale havel spree main neckar lech isar inn drava sava morava
tisza prut siret olt mures somes argesh struma maritsa vardar drin
tay clyde forth tweed spey severn trent avon dee don esk wye usk
shannon liffey lee suir nore barrow boyne foyle bann erne moy lagan
""".split()

COLORS = """azure amber coral indigo ivory jade lilac mauve ochre olive pearl
ruby saffron scarlet sepia teal violet umber vermilion plum cobalt cyan
magenta crimson maroon navy salmon beige linen mint peach rose sand sky
slate snow tan wine bronze copper gold silver brass cherry chestnut hazel
honey lemon lime cream cocoa coffee mocha russet sage taupe burgundy claret
emerald fern flax ginger grape khaki ochre orchid orchard fuchsia magnolia
chartreuse moss myrtle pumpkin raspberry rust seagreen seashell sienna sky
sorrel spruce squash tangerine thistle topaz turquoise viridian wheat
zaffre puce mulberry damask carmine cerise garnet hyacinth jasmine lavender
melon mustard nutmeg paprika periwinkle persimmon pewter pomegranate poppy
quince rosewood ruche saddle sangria seafoam shamrock smoke spearmint sterling
sunflower terra tomato vanilla verdigris veronica wisteria xanadu zinnia
absinthe alabaster apricot aqua aquamarine asparagus avocado azalea bistre
bittersweet blush bordeaux brick buff bumblebee burgundy butter byzantium
canary cardinal celadon celeste chambray chamois cinnabar citrine clover
coquelicot daffodil dandelion eggshell electric emerald firebrick flame
glaucous goldenrod gunmetal heliotrope iceberg icterine isabelline imperial
jet juniper lavender lemonade lilac linen mahogany malachite mango maroon
melon midnight mocha moonbeam morello mulberry myrtle nutbrown obsidian ochre
opal opaline orchid oyster paisley papaya pastel pewter pink pistachio
platinum porcelain primrose prussian quartz quicksilver rouge sable sapphire
seal shadow slate snow spruce starlight sunset thunder umbra walnut whisper
""".split()

ADJECTIVES = """brave bright calm clever cool deep eager fair fine glad
grand happy keen kind lively merry neat noble proud quick quiet swift
warm wise witty young zest jolly lucky mighty smart snappy spry sunny
super tidy true vivid wild zippy able active alert ample apt artful
balmy bold breezy brisk chic chill cosy crisp dapper dashing dazzling
deft divine dreamy dynamic earnest easy elated elegant epic exact
fancy fluent fresh friendly funky gallant gentle gifted glossy graceful
hardy hearty honest hopeful humble jaunty jazzy jovial joyful jubilant
keen lavish legit liberal light limber lithe lovely loyal lucid lush
magic main mellow mild modest neat nifty nimble nimbly noble notable
peppy perky placid plucky plush polished polite posh prime pristine
pristine prompt pure quaint quirky radiant rapid rare regal reliable
robust rosy royal rugged sage sassy savvy serene sharp shiny silky
sincere sleek slick smooth snug solid sparkly spirited splendid spotless
spunky stable stately steady stellar stoic strong stunning stylish suave
subtle sturdy supple svelte tactful tender thrifty tidy timeless top
tough tranquil trendy trusty upbeat valiant velvet warmhearted welcoming
worthy zealous ace adept agile airy ardent astute beaming benign bonny
breezy buoyant candid charming cheery chipper choice classic clean cogent
comfy cordial cosmic cute daring dauntless dewy devout doughty dreamy ducky
fab famed fervid festive firm forthright frank fruitful genial genuine glowing
golden hale handy heady hopeful jocund kingly lithe luminous luxe magical""".split()

NOUNS = """harbor haven cove glade meadow grove orchard summit ridge peak
canyon vista oasis sanctum atrium plaza forum agora portal beacon torch
ember spark flame prism orbit comet nebula pulsar quasar zenith apex
crown laurel medal trophy gem jewel pearl charm token coin badge crest
emblem sigil banner pennant arrow anchor compass keystone cornerstone
pillar lantern lighthouse keep tower castle bastion citadel fortress
manor cottage cabin lodge chalet villa palace temple shrine altar
chapel cathedral basilica garden grotto fountain spring brook creek
falls rapids tide wave swell pearl shell coral reef harbor port pier
dock wharf marina island isle archipelago atoll cape ridge cliff bluff
mesa plateau valley vale dale fen heath moor savanna prairie tundra
delta lagoon estuary fjord strait sound channel bay gulf cove inlet
lakeshore beach dune cinder pumice basalt granite quartz crystal opal
agate amber jade onyx topaz garnet zircon spinel beryl peridot
tourmaline jasper malachite obsidian moonstone sunstone bloodstone amethyst
aquamarine turquoise lapis citrine carnelian chalcedony tigereye hematite
meadowlark falcon eagle hawk swan crane heron robin wren finch sparrow
sunbeam dawn dusk twilight starlight moonlight aurora rainbow zephyr breeze
gale storm thunder lightning whirlwind tempest meridian solstice equinox
talisman amulet charm scepter chalice goblet flute lyre harp drum bell
chime echo whisper melody chorus anthem hymn verse rhyme stanza ode lullaby
quill scroll parchment tome volume tale fable myth legend saga epic tale""".split()

VERBS = """soar glide drift float flow leap dash sprint march wander roam
explore voyage venture journey travel embark launch begin start spark
ignite kindle awaken arise rise climb ascend conquer summit triumph
flourish thrive prosper bloom blossom flower grow expand evolve elevate
empower energize inspire spark uplift cherish nurture foster shelter
guard protect uphold support sustain anchor steady balance harmonize
align tune compose craft fashion forge sculpt shape mold weave thread
knit stitch braid binds craft build raise rear render render shape
discover unveil reveal disclose unfold open share spread broadcast share
gather collect compile assemble unite bond join meld merge blend fuse
synthesize integrate connect link bridge weave converge gather rally
flourish blossom thrive prosper succeed achieve attain master conquer
prevail triumph excel shine glow gleam glimmer sparkle radiate beam
flash bloom flourish flutter dart dive surge swirl spin twirl pivot
balance hover linger glide pirouette swoop swivel cascade tumble vault
bound bounce skip prance gambol caper romp frolic cavort dance sway
glisten shimmer scintillate twinkle dazzle illuminate radiate brighten
amplify boost charge fortify embolden enliven enchant captivate beguile
mesmerize delight gladden enrich endow grant gift bestow yield deliver
render produce furnish supply provide cultivate plant sow reap harvest
till tend mind heal mend renew restore revive refresh rejuvenate awaken
quicken hasten propel thrust propel propel guide steer navigate course
chart map plot trace draft sketch outline design devise envision
imagine dream wish hope aspire strive seek pursue chase track hunt
gain win earn capture claim secure obtain procure attain reach grasp""".split()

NAMES = """ada alex amy ana avi ben bea cam dan dee eli emma eva finn gus
hugo ian iris ivan jade jane juno kai kit lena liam lila luca lyra maya
mia milo nia noah nora oli omar otto piper quinn rex rio ron sage sam
sara seth sky theo tom uma vera vic will xander yael yuki zane zara
alma anya beau cole cora dane dora elsa enzo erin esme finn gabe gina
hank hugo iggy inez ivy jack joel juno kade kara kira kyle lana lars
leah leon lily luna mack maeve mads matt myra nash neil niko nora odin
oren orin pax pete piper raj rena rhys riya rome rosa ruth ryan ryla
seth shay simon sloan stef tara teo tess thane tilda toby vance vera
vita vlad walt wes wren xenia yves zara zeke zion abe ada alan alma
amir andi anya arden aria ariel arlo asher aster atticus august aurora
bea beck beth blake blanche bo bridget bruno cael cain cal calla callie
camilo cara casey cass cato cecily celia celine cesar chase clio cole
colt cooper coral corin cyrus daisy dalia dane dario darby dax dee desmond
dexter diana dimitri dina dom drew dru dylan eden edith elena elias eliza
elif ellis elsa emery emil enzo eric esme estes evan ewan ezra fern fiona""".split()

# Pad/truncate to exactly 200
def fix200(lst: Sequence[str], label: str) -> list[str]:
    # dedupe preserving order
    seen = set()
    out = []
    for w in lst:
        w = w.strip().lower()
        if w and w.isalpha() and w not in seen:
            seen.add(w)
            out.append(w)
    if len(out) < 200:
        raise SystemExit(f"{label}: only {len(out)} stems, need 200")
    return out[:200]

PACKS = {
    "cities": fix200(CITIES, "cities"),
    "rivers": fix200(RIVERS, "rivers"),
    "colors": fix200(COLORS, "colors"),
    "adjectives": fix200(ADJECTIVES, "adjectives"),
    "nouns": fix200(NOUNS, "nouns"),
    "verbs": fix200(VERBS, "verbs"),
    "names": fix200(NAMES, "names"),
}

# Rotation rules: every letter -> a related letter (sounds/looks alike).
# Consonant -> consonant; vowel -> vowel. Applied to at most 1-2 random positions.
ROTATIONS = [
    ("a", "e"), ("e", "i"), ("i", "y"), ("o", "u"), ("u", "o"), ("y", "i"),
    ("b", "p"), ("c", "k"), ("d", "t"), ("f", "v"), ("g", "j"), ("h", "x"),
    ("j", "y"), ("k", "c"), ("l", "r"), ("m", "n"), ("n", "m"), ("p", "b"),
    ("q", "k"), ("r", "l"), ("s", "z"), ("t", "d"), ("v", "f"), ("w", "v"),
    ("x", "z"), ("z", "s"),
]

def write_data():
    DATA.mkdir(exist_ok=True)
    for name, words in PACKS.items():
        (DATA / f"{name}.txt").write_text("\n".join(words) + "\n")
    rot = "\n".join(f"{a} {b}" for a, b in ROTATIONS) + "\n"
    (DATA / "rotations.txt").write_text(rot)

def unified() -> list[str]:
    seen = set()
    out = []
    for words in PACKS.values():
        for w in words:
            if w not in seen:
                seen.add(w)
                out.append(w)
    return out

# ---------------- TypeScript ----------------
def write_ts():
    stems = unified()
    f = ROOT / "namzy-ts" / "src" / "wordlist.ts"
    body = "// this_file: src/wordlist.ts\n// AUTO-GENERATED by scripts/generate_data.py. Do not edit.\n\n"
    body += "export const STEMS: readonly string[] = [\n"
    for i in range(0, len(stems), 8):
        body += "  " + ", ".join(f'"{w}"' for w in stems[i:i+8]) + ",\n"
    body += "];\n\n"
    body += "export const ROTATIONS: readonly (readonly [string, string])[] = [\n"
    for a, b in ROTATIONS:
        body += f'  ["{a}", "{b}"],\n'
    body += "];\n"
    f.write_text(body)

# ---------------- Python ----------------
def write_py():
    stems = unified()
    f = ROOT / "namzy-py" / "src" / "namzy" / "_wordlist.py"
    body = "# this_file: src/namzy/_wordlist.py\n# AUTO-GENERATED by scripts/generate_data.py. Do not edit.\n\nSTEMS: list[str] = [\n"
    for i in range(0, len(stems), 8):
        body += "    " + ", ".join(f'"{w}"' for w in stems[i:i+8]) + ",\n"
    body += "]\n\nROTATIONS: list[tuple[str, str]] = [\n"
    for a, b in ROTATIONS:
        body += f'    ("{a}", "{b}"),\n'
    body += "]\n"
    f.write_text(body)

# ---------------- Rust ----------------
def write_rs():
    stems = unified()
    f = ROOT / "namzy-rs" / "src" / "wordlist.rs"
    body = "//! this_file: src/wordlist.rs\n//! AUTO-GENERATED by scripts/generate_data.py. Do not edit.\n\n"
    body += f"pub static STEMS: &[&str] = &[\n"
    for i in range(0, len(stems), 8):
        body += "    " + ", ".join(f'"{w}"' for w in stems[i:i+8]) + ",\n"
    body += "];\n\n"
    body += "pub static ROTATIONS: &[(char, char)] = &[\n"
    for a, b in ROTATIONS:
        body += f"    ('{a}', '{b}'),\n"
    body += "];\n"
    f.write_text(body)

# ---------------- C++ ----------------
def write_cpp():
    stems = unified()
    h = ROOT / "namzy-cpp" / "src" / "wordlist.h"
    c = ROOT / "namzy-cpp" / "src" / "wordlist.cpp"
    h.write_text("""// this_file: src/wordlist.h
// AUTO-GENERATED by scripts/generate_data.py. Do not edit.
#pragma once
#include <QStringList>
#include <QVector>
#include <QPair>
#include <QChar>

namespace namzy {
const QStringList& stems();
const QVector<QPair<QChar, QChar>>& rotations();
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
        body += "        " + ", ".join(f'QStringLiteral("{w}")' for w in stems[i:i+8]) + ",\n"
    body += """    };
    return s;
}

const QVector<QPair<QChar, QChar>>& rotations() {
    static const QVector<QPair<QChar, QChar>> r = {
"""
    for a, b in ROTATIONS:
        body += f"        {{ QChar('{a}'), QChar('{b}') }},\n"
    body += """    };
    return r;
}

} // namespace namzy
"""
    c.write_text(body)

def main():
    write_data()
    write_ts()
    write_py()
    write_rs()
    write_cpp()
    print(f"unified stems: {len(unified())}")
    print(f"rotations: {len(ROTATIONS)}")
    for name, w in PACKS.items():
        print(f"  {name}: {len(w)}")

if __name__ == "__main__":
    main()
