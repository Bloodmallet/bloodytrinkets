import datetime
import subprocess
import sys

simc_build = "<a href=\\\"https://github.com/simulationcraft/simc/commit/c56773bf9e4845bb68b68dccb8ce6015ee67375a\\\" target=\\\"blank\\\">c56773b</a>"

fight_styles = [
  ( "patchwerk", "0.1" ),
  ( "beastlord", "0.25" )
]

use_second_trinket = "True"

profiles = [
  ( "death_knight", "blood",          "str" ),
  ( "death_knight", "frost",          "str" ),
  ( "death_knight", "unholy",         "str" ),
  ( "demon_hunter", "havoc",          "agi" ),
  #( "demon_hunter", "vengeance",      "agi" ),
  ( "druid",        "balance",        "int" ),
  ( "druid",        "feral",          "agi" ),
  #( "druid",        "guardian",       "agi" ),
  ( "hunter",       "beast_mastery",  "agi" ),
  ( "hunter",       "marksmanship",   "agi" ),
  ( "hunter",       "survival",       "agi" ),
  ( "mage",         "arcane",         "int" ),
  ( "mage",         "fire",           "int" ),
  ( "mage",         "frost",          "int" ),
  ( "monk",         "brewmaster",     "agi" ),
  ( "monk",         "windwalker",     "agi" ),
  ( "paladin",      "protection",     "str" ),
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
  ( "warrior",      "fury",           "str" ),
  #( "warrior",      "protection",     "str" )
]

second_trinket = {
  # agi
  "agi": "( \"142506,bonus_id=607\", \"910\" )",
  # int
  "int": "( \"142507,bonus_id=607\", \"910\" )",
  # str
  "str": "( \"142508,bonus_id=607\", \"910\" )"
}


start = datetime.datetime.utcnow()

for fight_style in fight_styles:
  for profile in profiles:
    with open("automator_input.py", "w") as ofile:
      ofile.write("graph_title = \"" + profile[0].title() + " - " + profile[1].title() + " - " + fight_style[0].title() + "\"\n")
      ofile.write("graph_subtitle = \"UTC " + start.strftime("%Y-%m-%d %H:%M") + " SimC build: " + simc_build + "\"\n")
      ofile.write("simc_settings = {}\n")
      ofile.write("simc_settings[\"class\"] = \"" + profile[0] + "\"\n")
      ofile.write("simc_settings[\"spec\"] = \"" + profile[1] + "\"\n")
      ofile.write("simc_settings[\"fight_styles\"] = [\"" + fight_style[0] + "\"]\n")
      ofile.write("simc_settings[\"target_error\"] = \"" + fight_style[1] + "\"\n")
      ofile.write("simc_settings[\"use_second_trinket\"] = " + use_second_trinket + "\n")
      ofile.write("simc_settings[\"second_trinket\"] = " + second_trinket[profile[2]] + "\n")

    print("")
    print(datetime.datetime.utcnow())

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
end = datetime.datetime.utcnow()
print( "Done after " + str( end - start ))


## Add this to settings to automate the process
# import automator_input
# graph_title = automator_input.graph_title
# graph_subtitle = automator_input.graph_subtitle
# simc_settings["class"] = automator_input.simc_settings["class"]
# simc_settings["spec"]  = automator_input.simc_settings["spec"]
# simc_settings["fight_styles"] = automator_input.simc_settings["fight_styles"]
# simc_settings["target_error"] = automator_input.simc_settings["target_error"]
# simc_settings["use_second_trinket"] = automator_input.simc_settings["use_second_trinket"]
# simc_settings["second_trinket"] = automator_input.simc_settings["second_trinket"]
