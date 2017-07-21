import datetime
import subprocess
import sys

fight_styles = [ 
  ( "patchwerk", "0.1" ), 
  ( "hecticaddcleave", "0.2" ) 
]

use_second_trinket = "False"

profiles = [
  ( "death_knight", "frost",          "str" ),
  ( "death_knight", "unholy",         "str" ),
  ( "demon_hunter", "havoc",          "agi" ),
  ( "druid",        "balance",        "int" ),
  ( "druid",        "feral",          "agi" ),
  ( "hunter",       "beast_mastery",  "agi" ),
  ( "hunter",       "marksmanship",   "agi" ),
  ( "hunter",       "survival",       "agi" ),
  ( "mage",         "arcane",         "int" ),
  ( "mage",         "fire",           "int" ),
  ( "mage",         "frost",          "int" ),
  ( "monk",         "windwalker",     "agi" ),
  ( "paladin",      "retribution",    "str" ),
  ( "priest",       "shadow",         "int" ),
  ( "rogue",        "assassination",  "agi" ),
  ( "rogue",        "outlaw",         "agi" ),
  ( "rogue",        "subtlety",       "agi" ),
  ( "shaman",       "elemental",      "int" ),
  ( "shaman",       "enhancement",    "agi" ),
  ( "warlock",      "affliction",     "int" ),
  ( "warlock",      "demonology",     "int" ),
  ( "warlock",      "destruction",    "int" ),
  ( "warrior",      "arms",           "str" ),
  ( "warrior",      "fury",           "str" )
]

second_trinket = {
  # agi
  "agi": "( \"142506,bonus_id=607\", \"880\" )",
  # int
  "int": "( \"142507,bonus_id=607\", \"880\" )",
  # str
  "str": "( \"142508,bonus_id=607\", \"880\" )"  
}


start = datetime.datetime.now()

for fight_style in fight_styles:
  for profile in profiles:
    with open("automator_input.py", "w") as ofile:
      ofile.write("graph_title = \"" + profile[0].title() + " - " + profile[1].title() + " - " + fight_style[0].title() + "\"\n")
      ofile.write("simc_settings = {}\n")
      ofile.write("simc_settings[\"class\"] = \"" + profile[0] + "\"\n")
      ofile.write("simc_settings[\"spec\"] = \"" + profile[1] + "\"\n")
      ofile.write("simc_settings[\"fight_styles\"] = [\"" + fight_style[0] + "\"]\n")
      ofile.write("simc_settings[\"target_error\"] = \"" + fight_style[1] + "\"\n")
      ofile.write("simc_settings[\"use_second_trinket\"] = " + use_second_trinket + "\n")
      ofile.write("simc_settings[\"second_trinket\"] = " + second_trinket[profile[2]] + "\n")

    print("")

    command = "python bloodytrinkets.py"
    if sys.platform == 'win32':
      # call bloodytrinkets in the background
      startupinfo = subprocess.STARTUPINFO()
      startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

      result = subprocess.run(
        command, 
        stdout=None, 
        stderr=subprocess.STDOUT, 
        universal_newlines=True, 
        startupinfo=startupinfo
      )
      while result.returncode != 0:
        print(result)
        print("I keep trying")
        result = subprocess.run(
          command, 
          stdout=None, 
          stderr=subprocess.STDOUT, 
          universal_newlines=True,
          startupinfo=startupinfo
        )

    else:
      result = subprocess.run(
        command, 
        stdout=None, 
        stderr=subprocess.STDOUT, 
        universal_newlines=True
      )
      while result.returncode != 0:
        result = subprocess.run(
          command, 
          stdout=None, 
          stderr=subprocess.STDOUT, 
          universal_newlines=True
        )
end = datetime.datetime.now()
print( "Done after " + str( end - start ))


## Add this to settings to automate the process
# import automator_input
# graph_title = automator_input.graph_title
# simc_settings["class"] = automator_input.simc_settings["class"]
# simc_settings["spec"]  = automator_input.simc_settings["spec"]
# simc_settings["fight_styles"] = automator_input.simc_settings["fight_styles"]
# simc_settings["target_error"] = automator_input.simc_settings["target_error"]
# simc_settings["use_second_trinket"] = automator_input.simc_settings["use_second_trinket"]
# simc_settings["second_trinket"] = automator_input.simc_settings["second_trinket"]