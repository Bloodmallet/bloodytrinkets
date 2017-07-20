import datetime
import subprocess
import sys

profiles = [
  ( "Death Knight - Frost - Patchwerk", "death_knight", "frost" ),
  ( "Death Knight - Unholy - Patchwerk", "death_knight", "unholy" ),
  ( "Demon Hunter - Havoc - Patchwerk", "demon_hunter", "havoc" ),
  ( "Druid - Balance - Patchwerk", "druid", "balance" ),
  ( "Druid - Feral - Patchwerk", "druid", "feral" ),
  ( "Hunter - Beast Mastery - Patchwerk", "hunter", "beast_mastery" ),
  ( "Hunter - Marksmanship - Patchwerk", "hunter", "marksmanship" ),
  ( "Hunter - Survival - Patchwerk", "hunter", "survival" ),
  ( "Mage - Arcane - Patchwerk", "mage", "arcane" ),
  ( "Mage - Fire - Patchwerk", "mage", "fire" ),
  ( "Mage - Frost - Patchwerk", "mage", "frost" ),
  ( "Monk - Windwalker - Patchwerk", "monk", "windwalker" ),
  ( "Paladin - Retribution - Patchwerk", "paladin", "retribution" ),
  ( "Priest - Shadow - Patchwerk", "Priest", "shadow" ),
  ( "Rogue - Assassination - Patchwerk", "rogue", "assassination" ),
  ( "Rogue - Outlaw - Patchwerk", "rogue", "outlaw" ),
  ( "Rogue - Subtlety - Patchwerk", "rogue", "subtlety" ),
  ( "Shaman - Elemental - Patchwerk", "shaman", "elemental" ),
  ( "Shaman - Enhancement - Patchwerk", "shaman", "enhancement" ),
  ( "Warlock - Affliction - Patchwerk", "warlock", "affliction" ),
  ( "Warlock - Demonology - Patchwerk", "warlock", "demonology" ),
  ( "Warlock - Destruction - Patchwerk", "warlock", "destruction" ),
  ( "Warrior - Arms - Patchwerk", "warrior", "arms" ),
  ( "Warrior - Fury - Patchwerk", "warrior", "fury" )
]

start = datetime.datetime.now()

for profile in profiles:
  with open("automator_input.py", "w") as ofile:
    ofile.write("graph_title = \"" + profile[0] + "\"\n")
    ofile.write("simc_settings = {}\n")
    ofile.write("simc_settings[\"class\"] = \"" + profile[1] + "\"\n")
    ofile.write("simc_settings[\"spec\"] = \"" + profile[2] + "\"\n")

  print("")

  command = "python bloodytrinkets.py"
  if sys.platform == 'win32':
    # call simulationcraft in the background. grab output for processing and get dps value
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    result = subprocess.run(
      command, 
      stdout=None, 
      stderr=subprocess.DEVNULL, 
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
      stderr=subprocess.DEVNULL, 
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


## Use this in settings to automate the process
# import automator_input
# graph_name = automator_input.graph_name
# simc_settings["class"] = automator_input.simc_settings["class"]
# simc_settings["spec"]  = automator_input.simc_settings["spec"]