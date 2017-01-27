# File containing all trinket items and functions for retrieval of a spec's possible trinkets
from lib.spec_utils import get_role_stat
from collections import defaultdict

# Ranged trinkets are usable by casters and hunters
ranged_trinkets = {}
ranged_trinkets["dungeon"] = [
  [ "Caged Horror",                       "136716", 840, 1200 ],
  [ "Chrono Shard",                       "137419", 840, 1200 ],
  [ "Corrupted Starlight",                "137301", 840, 1200 ],
  [ "Elementium Bomb Squirrel Generator", "137446", 840, 1200 ],
  [ "Eye of Skovald",           					"133641", 840, 1200 ],
  [ "Figurehead of the Naglfar",       		"137329", 840, 1200 ],
  [ "Horn of Valor",             					"133642", 840, 1200 ],
  [ "Moonlit Prism",             					"137541", 840, 1200 ],
  [ "Naraxas Spiked Tongue",        			"137349", 840, 1200 ],
  [ "Oakhearts Gnarled Root",       			"137306", 840, 1200 ],
  [ "Obelisk of the Void",         				"137433", 840, 1200 ],
  [ "Portable Manacracker",         			"137398", 840, 1200 ],
  [ "Stormsinger Fulmination Charge",   	"137367", 840, 1200 ]
]

ranged_trinkets["karazhan"] = [  
  [ "Arans Relaxed Ruby",          "142157", 860, 1200 ],
  [ "Deteriorated Construct Core", "142165", 860, 1200 ],
  [ "Mrrgrias_Favor",              "142160", 855, 1200 ] 
]

ranged_trinkets["emerald_nightmare"] = [  
  [ "Twisting Wind",                "139323", 835, 1200 ],
  [ "Unstable Horrorslime",         "138224", 835, 1200 ]
]

ranged_trinkets["nighthold"] = [  
  [ "Fury of the Burning Sky",        "140801", 860, 1200 ],
  [ "Icon of Rot",                    "140798", 860, 1200 ] 
]

ranged_trinkets["pvp"] = [   
  ["PVP Badge of Dominance",         "142779", 840, 1200],
  ["PVP Insignia of Dominance",       "142668", 840, 1200]
]


# Int trinkets are only usable by casters
int_trinkets = {}
int_trinkets["world"] = [
  [ "Devilsaur Shock-Baton",          "140030", 840, 1200 ],
  [ "Padawsen's Unlucky Charm",       "141536", 860, 1200 ],
  # 142507 is Brinewater Slime in a Bottle, used as a reference stat stick
  [ "Stat Stick (Crit)",              "142507,bonus_id=603", 865, 1200 ],
  [ "Stat Stick (Haste)",             "142507,bonus_id=604", 865, 1200 ],
  [ "Stat Stick (Mastery)",           "142507,bonus_id=605", 865, 1200 ],
  [ "Stat Stick (Versatility)",       "142507,bonus_id=607", 865, 1200 ],
  [ "Unstable Arcano Crystal",        "141482", 860, 1200 ]
]

int_trinkets["dungeon"] = [
  [ "Infernal Writ",                "137485", 840, 1200 ] 
]

int_trinkets["emerald_nightmare"] = [
  [ "Bough of Corruption",          "139323", 835, 1200 ],
  [ "Swarming Plaguehive",          "139321", 835, 1200 ],
  [ "Twisting Wind",                "139323", 835, 1200 ],
  [ "Unstable Horrorslime",         "138224", 835, 1200 ],
  [ "Wriggling Sinew",              "139326", 835, 1200 ] 
]

int_trinkets["nighthold"] = [
  [ "Erratic Metronome",              "140792", 855, 1200 ],
  [ "Pharameres Forbidden Guidance",  "140800", 860, 1200 ],
  [ "Star Gate",                      "140804", 860, 1200 ],
  [ "Whispers in the Dark",           "140809", 865, 1200 ]
]

int_trinkets["pvp"] = [ 
  ["PVP Insignia of Dominance",       "142668", 840, 1200],
  ["PVP Badge of Dominance",          "142779", 840, 1200]
]

int_trinkets["crafted"] = [
  [ "Darkmoon Deck: Hellfire",        "128709", 815, 865 ],
  [ "Infernal Alchemist Stone",       "127842", 815, 865 ]
]

# Melee trinkets usable by melee classes. Unfinished
melee_trinkets = {}
melee_trinkets["world"] = [
  [ "Darkmoon Deck: Dominion",        "128705", 815, 865],
  [ "The Devilsaur's Bite",           "140026", 805, 1200 ]
]

melee_trinkets["dungeon"] = [
  [ "Chaos Talisman",           "137459", 805, 1200 ],
  [ "Chrono Shard",             "137419", 840, 1200 ],
  [ "Faulty Countermeasure",    "137539", 805, 1200 ],
  [ "Giant Ornamental Pearl",   "137369", 805, 1200 ],
  [ "Horn of Valor",            "133642", 805, 1200 ],
  [ "Hunger of the Pack",       "136975", 805, 1200 ],
  [ "Mark of Dargrul",          "137357", 805, 1200 ],
  [ "Memento of Angerboda",     "133644", 805, 1200 ],
  [ "Nightmare Egg Shell",      "137312", 805, 1200 ],
  [ "Spiked Counterweight",     "136715", 805, 1200 ],
  [ "Terrorbound Nexus",        "137406", 840, 1200 ],
  [ "Tiny Oozeling in a Jar",   "137439", 805, 1200 ],
  [ "Windscar Whetstone",       "137486", 840, 1200 ]
]

melee_trinkets["emerald_nightmare"] = [
  [ "Nature's Call",             "139334", 835, 1200 ],
  [ "Ravaged Seed Pod",          "139320", 835, 1200 ],
  [ "Spontaneous Appendages",    "139325", 835, 1200 ]
]

melee_trinkets["nighthold"] = [
  [ "Convergence of Fates",       "140806", 860, 1200 ],
  [ "Draught of Souls",           "140808", 865, 1200 ],
  [ "Entwined Elemental Foci",    "140796", 860, 1200 ]
]

# Unfinished
agi_trinkets = {}
agi_trinkets["world"] = [
  [ "Ley Spark",               "140027", 805, 1200 ],
  [ "Six-Feather Fan",         "141585", 810, 1200 ],
    # 142506 is Eye of Guarm, used as a reference stat stick
  [ "Stat Stick (Crit)",              "142506,bonus_id=603", 865, 1200 ],
  [ "Stat Stick (Haste)",             "142506,bonus_id=604", 865, 1200 ],
  [ "Stat Stick (Mastery)",           "142506,bonus_id=605", 865, 1200 ],
  [ "Stat Stick (Versatility)",       "142506,bonus_id=607", 865, 1200 ],
  [ "Thrice-Accursed Compass", "141537", 860, 1200 ],
  [ "Unstable Arcano Crystal",        "141482", 860, 1200 ]
]

agi_trinkets["dungeon"] = [
  [ "Tempered Egg of Serpentrix",  "137373", 805, 1200 ],
  [ "Tirathon's Betrayal",         "137537", 805, 1200 ]
]

agi_trinkets["emerald_nightmare"] = [
  [ "Bloodythirsty Instinct",       "139239", 835, 1200 ]
]

agi_trinkets["nighthold"] = [
  [ "Arcanogolem Digit",           "140794", 855, 1200 ],
  [ "Nightblooming Frond",         "140802", 860, 1200 ]
]

# Unfinished
str_trinkets = {}
str_trinkets["world"] = []
str_trinkets["dungeon"] = []
str_trinkets["emerald_nightmare"] = [
  [ "Ursoc's Rending Pawn",         "139328", 835, 1200 ]
]
str_trinkets["nighthold"] = [
  [ "Claw of the Crystalline Scorpid",   "140790", 855, 1200 ],
  [ "Might of Krosus",                   "140799", 860, 1200 ]
]

##
## @brief      Selects the relevant trinket dictionaries for a given spec
##
## @param      role  The specialisation name as string
## @param      stat  The specialisation's main stat (str/int/agi) as a string
##
## @return     A group of trinkets relevant to the role as a dictionary of lists
## @return     A group of trinkets relevant to the main stat as a dictionary of lists
def __get_relevant_trinkets(role,stat):
  # Inelegant solution. No good way to do this.
  if role == "ranged":
    role_trinkets = ranged_trinkets
  else:
    role_trinkets = melee_trinkets

  if stat == "int":
    stat_trinkets = int_trinkets
  elif stat == "agi":
    stat_trinkets = agi_trinkets
  else:
    stat_trinkets = str_trinkets
  return (role_trinkets, stat_trinkets)

##
## @brief      Combines role and stat trinket
##
## @param      role_trinkets  The trinkets relevant to role (ranged/melee) as a dict of lists
## @param      stat_trinkets  The trinkets relevant to a spec's stat (int/str/agi) as a dict of lists
##
## @return     A group of trinkets relevant to the spec as a dictionary of lists
##
def __combine_trinket_dicts(role_trinkets,stat_trinkets):  
  # Populate a new trinkets dict with role trinkets
  trinkets = role_trinkets

  for source in stat_trinkets:
    if trinkets.get(source) is not None:
      # Append int/str/agi trinkets to existing list in the newly created dict
      trinkets[source] = trinkets[source] + stat_trinkets[source]
    else:
      # Just set the int/str/agi trinket list to the newly created dict's source key  
      trinkets[source] = stat_trinkets[source]
  return trinkets


##
## @brief      Uses class and spec names to return a dict of relevant trinkets
##
## @param      class_name  The class name as string
## @param      spec_name   The specifier name as string
##
## @return     Relevant trinkets as a dict of lists
##
def get_trinkets_for_spec(class_name, spec_name):
  spec_info = get_role_stat(class_name, spec_name)
  role_trinkets, stat_trinkets = __get_relevant_trinkets(spec_info[0], spec_info[1])
  combined_trinkets = __combine_trinket_dicts(role_trinkets, stat_trinkets)
  return combined_trinkets