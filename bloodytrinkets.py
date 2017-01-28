# Project to automate trinket sims for dps specs

# params
#import argparse
# Library to use command line
import subprocess
import settings
# Library to print fancy one line output
import sys
# Bloodytrinkets lib imports
import lib.output.output
import lib.simc_checks
import lib.spec_utils
import lib.trinkets



##
## @brief      Gets the dps for one trinket.
##
## @param      trinket_id     The trinket identifier
## @param      item_level     The item level
## @param      simc_settings  The simc options dictionary {iterations s, target
##                            error s, fight style s, class s, spec s, tier s
##                            "T19M_NH"}
##
## @return     The dps s.
##
def get_dps(trinket_id, item_level):
  argument = "../simc.exe "
  argument += "iterations=" + settings.simc_settings["iterations"] + " "
  argument += "target_error=" + settings.simc_settings["target_error"] + " "
  argument += "fight_style=" + settings.simc_settings["fight_style"] + " "
  argument += "fixed_time=1 "
  argument += "default_actions=1 "
  argument += "threads=" + settings.simc_settings["threads"] + " "
  if settings.simc_settings["c_profile"]:
    argument += settings.simc_settings["c_profile_path"] + settings.simc_settings["c_profile_name"] + " "
  else:
    argument += settings.simc_settings["class"] + "_" + settings.simc_settings["spec"] + "_" + settings.simc_settings["tier"] + ".simc "
  argument += "trinket1= "
  argument += "trinket2=,id=" + trinket_id + ",ilevel=" + item_level + " "
  # call simulationcraft in the background. grab output for processing and getting dps value
  simulation_output = subprocess.run(argument, stdout=subprocess.PIPE, universal_newlines=True)
  owndps = True
  for line in simulation_output.stdout.splitlines():
    # needs this check to prevent grabbing the enemy dps
    if "DPS:" in line and owndps:
      dps = line
      owndps = False
  return dps.split()[1].split(".")[0]


##
## @brief      Sim all trinkets at all itemlevels when available.
##
## @param      trinkets       The trinkets dictionary {source s:{[trinket_name
##                            s, id s, base_ilevel i, max_itemlevel i]}}
## @param      ilevels        The ilevels list
## @param      simc_settings  The simc options dictionary {iterations s, target
##                            error s, fight style s, class s, spec s, tier s
##                            "T19M_NH"}
##
## @return     Dictionary of all simmed trinkets with all their dps values as
##             strings {trinket_name s:{ilevel s:{dps s}}}. dps is "0" if to be
##             simmed itemlevel don't match available trinket itemlevel
##
def sim_all( trinkets, ilevels ):
  sim_counter = 0
  sim_ceiling = 0
  for source in trinkets:
    sim_ceiling += len( trinkets[source] )
  sim_ceiling *= len( ilevels )
  all_simmed = {}
  for source in trinkets:
    for trinket in trinkets[source]:
      all_simmed[trinket[0]] = {}
      for ilevel in ilevels:
        dps = "0"
        if trinket[2] <= int( ilevel ) and trinket[3] >= int( ilevel ):
          dps = get_dps( trinket[1], ilevel )
        elif source == "legendary" and ilevel == ilevels[-1]:
          dps = get_dps( trinket[1], trinket[2] )
        all_simmed[trinket[0]][ilevel] = dps
        sim_counter += 1
        sys.stdout.write( "Already simed: %d of %d\r" % ( sim_counter, sim_ceiling ))
        sys.stdout.flush()
  return all_simmed



##
#-------------------------------------------------------------------------------------
# Program start
#-------------------------------------------------------------------------------------
##


baseline = {"none": [["none", "", 840, 1200]]}
error_collector = []
if not lib.simc_checks.is_iteration(settings.simc_settings["iterations"]):
  error_collector.append("simc_settings[iterations] not strong or out of bounds")
if not lib.simc_checks.is_target_error(settings.simc_settings["target_error"]):
  error_collector.append("simc_settings[target_error] not string or out of bounds")
if not lib.simc_checks.is_fight_style(settings.simc_settings["fight_style"]):
  error_collector.append("simc_settings[fight_style] not a recognised fight style")
if not lib.spec_utils.is_class(settings.simc_settings["class"]):
  error_collector.append("simc_settings[class] wrong name")
if not lib.spec_utils.is_spec(settings.simc_settings["spec"]):
  error_collector.append("simc_settings[spec] not appropriate spec name")
if lib.spec_utils.is_class_spec(settings.simc_settings["class"], settings.simc_settings["spec"]):
  trinkets = lib.trinkets.get_trinkets_for_spec(settings.simc_settings["class"], settings.simc_settings["spec"])
else:
  error_collector.append("simc_settings[class] and simc_settings[spec] don't fit each other")

if error_collector:
  print("Some data got corrupted. The following errors were cought:")
  for error in error_collector:
    print(error)
  sys.exit("Program termintes due to errors in data.")


print("Name of the graph: '" + settings.graph_name + "'")

print("Loading base dps value.")
base_dps = sim_all( baseline, [settings.ilevels[-1]] )
if settings.output_screen:
  print( base_dps )

print("Loading dps-values for all trinkets.")
sim_results = sim_all( trinkets, settings.ilevels  )

if lib.output.output.print_manager( base_dps, sim_results ):
  print("Program ends.")
