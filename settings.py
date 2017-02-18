## File contains all settings for 
## 
## 

graph_colours = { 
  "865": "#4572a7", 
  "875": "#aa4643", 
  "885": "#89a54e", 
  "895": "#71588f", 
  "905": "#4198af", 
  "915": "#db843d", 
  "925": "#00E676" 
}
graph_name = "Icefury trinket sims 7.1.5"
# Defines itemlevels that shall be simed ordered from highest to lowest (graph output will have this order reversed)
ilevels = [ 
  "925", 
  "915", 
  "905", 
  "895", 
  "885", 
  "875", 
  "865"
]

output_screen = False
# "json", "highchart"
output_types = ["json", "highchart"]

simc_settings = {}
simc_settings["fight_style"]  = "patchwerk"
simc_settings["iterations"]   = "20000"
simc_settings["target_error"] = "0.1"
simc_settings["threads"]      = "6"
simc_settings["tier"]         = "T19M_NH"

simc_settings["class"] = "shaman"
simc_settings["spec"]  = "elemental"

# You want to use a custom profile? Set c_profile to True and add the relative path and name
simc_settings["c_profile"]      = False
simc_settings["c_profile_path"] = "example_dir/"
simc_settings["c_profile_name"] = "example_name.simc"
