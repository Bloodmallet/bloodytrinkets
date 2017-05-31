## File contains all settings for 
## Bloodytrinkets
## 

graph_colours = { 
  "880": "#4572a7", 
  "890": "#aa4643", 
  "900": "#89a54e", 
  "910": "#71588f", 
  "920": "#4198af", 
  "930": "#db843d", 
  "940": "#00E676" 
}
graph_name = "Lightning Rod trinket sims 7.2.5"
# Defines itemlevels that shall be simed, ordered from highest to lowest (graph output will have this order reversed)
ilevels = [ 
  "940", 
  "930", 
  "920", 
  "910", 
  "900", 
  "890", 
  "880"
]

output_screen = False
# "json", "highchart"
output_types = ["json", "highchart"]

simc_settings = {}
simc_settings["simc"] = "../simc.exe"
simc_settings["fight_styles"] = ["patchwerk", "helterskelter"]
simc_settings["iterations"]   = "250000"
simc_settings["target_error"] = "0.1"
simc_settings["threads"]      = ""
simc_settings["tier"]         = "T19M_NH"

simc_settings["class"] = "shaman"
simc_settings["spec"]  = "elemental"

# You want to use a custom profile? Set c_profile to True and add the relative path and name
simc_settings["c_profile"]      = False
simc_settings["c_profile_path"] = "example_dir/"
simc_settings["c_profile_name"] = "example_name.simc"

simc_settings["ptr"] = True
