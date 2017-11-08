## File contains all settings for
## Bloodytrinkets
##

import datetime

# graph_colours needs colours for all ilevels!
graph_colours = {
  "910": "#4572a7",
  "920": "#aa4643",
  "930": "#89a54e",
  "940": "#71588f",
  "950": "#4198af",
  "960": "#db843d",
  "970": "#00e676"
}
# Defines itemlevels that shall be simed, ordered from highest to lowest (graph
# output will have this order reversed)
ilevels = [
  "970",
  "960",
  "950",
  "940",
  "930",
  "920",
  "910"
]

legendary = True
legendary_colour = "#ffeb3b"
legendary_ilevel = "1000"

output_screen = False
# "json", "highchart"
output_types = ["json", "highchart"]

simc_settings = {}
simc_settings["simc"]         = "../simc.exe"
simc_settings["fight_styles"] = ["patchwerk", "helterskelter"]
simc_settings["iterations"]   = "250000"
simc_settings["target_error"] = "0.1"
simc_settings["threads"]      = "8"
simc_settings["tier"]         = "T21"

graph_title = "Shaman - Elemental - Patchwerk"
graph_subtitle = "UTC " + datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M") + " SimC build: 43201b2"
simc_settings["class"] = "shaman"
simc_settings["spec"]  = "elemental"

# Be aware that this feature basically makes the trinket disappear in the graph
# but has the benefit of showing a bit more realistic trinket values
simc_settings["use_second_trinket"] = True
simc_settings["second_trinket"] = ( "141482", "880" )     # ( id s, ilevel s),
                                                          # this is a int-vers stat stick
simc_settings["allow_double_trinkets"] = True             # True, allows two identical trinkets to be simmed
                                                          # False, prevents identical trinkets to be simmed

# You want to use a custom profile? Set c_profile to True and add a relative
# path and name
simc_settings["c_profile"]      = False
simc_settings["c_profile_path"] = "example_dir/"
simc_settings["c_profile_name"] = "example_name.simc"

simc_settings["ptr"] = False
