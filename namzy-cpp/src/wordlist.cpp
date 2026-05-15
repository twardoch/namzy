#include "wordlist.h"

namespace Wordlist {

const char* const GEO_WORDS[] = {
    "tokyo", "paris", "oslo", "berlin", "lagos",
    "lima", "boston", "vienna", "cairo", "kyoto",
    "seoul", "delhi", "rome", "milan", "lisbon",
    "athens", "dubai", "havana", "nairobi", "oslo",
    "bruges", "geneva", "zurich", "bruges", "venice",
    "prague", "dublin", "sydney", "denver", "austin",
    "phoenix", "tucson", "reno", "boise", "fargo",
    "tulsa", "tampa", "miami", "salem", "dover",
    "trenton", "helena", "juneau", "topeka", "albany"
};
const int GEO_COUNT = static_cast<int>(sizeof(GEO_WORDS) / sizeof(GEO_WORDS[0]));

const char* const COMMON_WORDS[] = {
    "river", "stone", "ember", "frost", "harbor",
    "willow", "copper", "marble", "anchor", "lantern",
    "cedar", "falcon", "thunder", "silver", "canyon",
    "meadow", "basalt", "cobalt", "summit", "valley",
    "bridge", "beacon", "ranger", "timber", "clover",
    "pebble", "ripple", "canopy", "chimney", "cinder",
    "comet", "dagger", "ferret", "glider", "haven",
    "jaguar", "kernel", "lancer", "mortar", "nebula",
    "osprey", "patrol", "quartz", "rafter", "sparrow"
};
const int COMMON_COUNT = static_cast<int>(sizeof(COMMON_WORDS) / sizeof(COMMON_WORDS[0]));

} // namespace Wordlist
