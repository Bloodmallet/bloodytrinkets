# Project to automate trinket sims for dps specs

# params
#import argparse
# Library to use command line
import subprocess
# Library to get date and calcutiontime for program
import datetime
# Library to look for files and create them if needed
import os
# Library to print fancy one line output
import sys
# Bloodytrinkets lib imports
import lib.output.highcharts
import lib.output.json
import lib.simc_checks
import lib.spec_utils
import lib.trinkets
##
#-------------------------------------------------------------------------------------
# Options
#-------------------------------------------------------------------------------------
##

graph_colours = { "865": "#4572a7", "875": "#aa4643", "885": "#89a54e", "895": "#71588f", "905": "#4198af", "915": "#db843d", "925": "#00E676" }
graph_name = "Icefury trinket sims 7.1.5"
# Defines itemlevels that shall be simed ordered from highest to lowest (graph output will have this order reversed)
ilevels = [ "925", "915", "905", "895", "885", "875", "865" ]

output_screen = False
# "json" or "highchart"
output_type = "json" 

simc_settings = {}
simc_settings["fight_style"]  = "patchwerk"
simc_settings["iterations"]   = "20000"
simc_settings["target_error"] = "0.1"
simc_settings["tier"]         = "T19M_NH"

simc_settings["class"] = "shaman"
simc_settings["spec"]  = "elemental"

# You want to use a custom profile? Set c_profile to True and add the relative path and name
simc_settings["c_profile"]      = False
simc_settings["c_profile_path"] = "example_dir/"
simc_settings["c_profile_name"] = "example_name.simc"



##
#-------------------------------------------------------------------------------------
# Functions
#-------------------------------------------------------------------------------------
##

##
## @brief      Creates a filename with current date.
##
## @param      simc_settings  The simc options dictionary {iterations s, target
##                            error s, fight style s, class s, spec s, tier s
##                            "T19M_NH"}
##
## @return     Returns a filename which contains the current date
##
def create_filename(simc_settings):
  filename = ""
  filename += "{:%Y_%m_%d__%H_%M}".format(datetime.datetime.now())
  filename += "_" + simc_settings["fight_style"]
  filename += "_" + simc_settings["class"]
  filename += "_" + simc_settings["spec"]
  filename += "_" + simc_settings["tier"]
  return filename


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
def get_dps(trinket_id, item_level, simc_settings):
  argument = "../simc.exe "
  argument += "iterations=" + simc_settings["iterations"] + " "
  argument += "target_error=" + simc_settings["target_error"] + " "
  argument += "fight_style=" + simc_settings["fight_style"] + " "
  argument += "fixed_time=1 "
  argument += "default_actions=1 "
  if simc_settings["c_profile"]:
    argument += simc_settings["c_profile_path"] + simc_settings["c_profile_name"] + " "
  else:
    argument += simc_settings["class"] + "_" + simc_settings["spec"] + "_" + simc_settings["tier"] + ".simc "
  argument += "name=" + create_filename(simc_settings) + " "
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
## @brief      Reduces trinket dps to the actual gain those trinkets provide in
##             comparison to the baseline dps.
##
## @param      sim_results  Dictionary of all simmed trinkets with all their dps
##                          values as strings {trinket_name s:{ilevel s:{dps
##                          s}}}.
## @param      base_dps     Dictionary of the base-profile without trinkets
##                          values as strings {trinket_name s:{ilevel s:{dps
##                          s}}}.
## @param      base_ilevel  The base ilevel
##
## @return     Dictionary of all simmed trinkets with all their normalised dps
##             values as strings {trinket_name s:{ilevel s:{dps s}}}. dps is "0"
##             if to be simmed itemlevel don't match available trinket itemlevel
##
def normalise_trinkets(sim_results, base_dps, base_ilevel):
  for trinket in sim_results:
    for ilevel in sim_results[trinket]:
      if not sim_results[trinket][ilevel] == "0":
        sim_results[trinket][ilevel] = str(int(sim_results[trinket][ilevel]) - int(base_dps["none"][base_ilevel]))
  return sim_results


##
## @brief      Generates a list ordered by max dps value of highest itemlevel
##             trinkets [trinket_name s]
##
## @param      sim_results  Dictionary of all simmed trinkets with all their dps
##                          values as strings {trinket_name s:{ilevel s:{dps
##                          s}}}.
## @param      ilevels      The ilevels list
##
## @return     Trinket list ordered ascending from lowest to highest dps for
##             highest available itemlevel
##
def order_results(sim_results, ilevels):
  highest_ilevel = ilevels[0]
  current_best_dps = "-1"
  last_best_dps = "-1"
  name = ""
  trinket_list = []
  # gets highest dps value of all trinkets
  for trinket in sim_results:
    if int(last_best_dps) < int(sim_results[trinket][highest_ilevel]) :
      last_best_dps = sim_results[trinket][highest_ilevel]
      name = trinket
  trinket_list.append(name)
  for outerline in sim_results:
    name = "error"
    current_best_dps = "-1"
    for trinket in sim_results:
      if int(current_best_dps) < int(sim_results[trinket][highest_ilevel]) and int(last_best_dps) > int(sim_results[trinket][highest_ilevel]):
        current_best_dps = sim_results[trinket][highest_ilevel]
        name = trinket
    if not name == "error": 
      trinket_list.append(name)
      last_best_dps = current_best_dps
  return trinket_list


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
def sim_all(trinkets, ilevels, simc_settings):
  sim_counter = 0
  sim_ceiling = 0
  for source in trinkets:
    sim_ceiling += len(trinkets[source])
  sim_ceiling *= len(ilevels)
  all_simmed = {}
  for source in trinkets:
    for trinket in trinkets[source]:
      all_simmed[trinket[0]] = {}
      for ilevel in ilevels:
        dps = "0"
        if trinket[2] <= int(ilevel) and trinket[3] >= int(ilevel):
          dps = get_dps(trinket[1], ilevel, simc_settings)
        all_simmed[trinket[0]][ilevel] = dps
        sim_counter += 1
        sys.stdout.write("Already simed: %d of %d\r" % (sim_counter, sim_ceiling))
        sys.stdout.flush()
  return all_simmed



##
#-------------------------------------------------------------------------------------
# Program start
#-------------------------------------------------------------------------------------
##


baseline = {"none": [["none", "", 840, 1200]]}
error_collector = []
filename = create_filename(simc_settings)
if not lib.simc_checks.is_iteration(simc_settings["iterations"]):
  error_collector.append("simc_settings[iterations] not strong or out of bounds")
if not lib.simc_checks.is_target_error(simc_settings["target_error"]):
  error_collector.append("simc_settings[target_error] not string or out of bounds")
if not lib.simc_checks.is_fight_style(simc_settings["fight_style"]):
  error_collector.append("simc_settings[fight_style] not a recognised fight style")
if not lib.spec_utils.is_class(simc_settings["class"]):
  error_collector.append("simc_settings[class] wrong name")
if not lib.spec_utils.is_spec(simc_settings["spec"]):
  error_collector.append("simc_settings[spec] not appropriate spec name")
if lib.spec_utils.is_class_spec(simc_settings["class"], simc_settings["spec"]):
  trinkets = lib.trinkets.get_trinkets_for_spec(simc_settings["class"], simc_settings["spec"])
else:
  error_collector.append("simc_settings[class] and simc_settings[spec] don't fit each other")

if error_collector:
  print("Some data got corrupted. The following errors were cought:")
  for error in error_collector:
    print(error)
  sys.exit("Program termintes due to errors in data.")

print("Name of the graph: '" + graph_name + "'")


print("Loading base dps value.")
base_dps = sim_all(baseline, [ilevels[-1]], simc_settings)
if output_screen:
  print(base_dps)

print("Loading dps-values for all trinkets.")
sim_results = sim_all(trinkets, ilevels, simc_settings)

if output_type == "highchart":
  print("Ordering trinkets by dps.")
  ordered_trinket_names = order_results(sim_results, ilevels)
  if output_screen:
    print(ordered_trinket_names)
  
  print("")
  print("Normalising dps values.")
  sim_results = normalise_trinkets(sim_results, base_dps, ilevels[-1])
  if output_screen:
    print(sim_results)
  
  print("Printing results to js file.")
  if lib.output.highcharts.print_highchart(sim_results, ordered_trinket_names, ilevels, graph_colours, graph_name, simc_settings, filename):
    print("Output successful.")
  else:
    print("Output failed.")
elif output_type == "json":
  print("Printing results to json file.")
  if lib.output.json.print_json(sim_results, ilevels, graph_name, simc_settings, filename):
    print("Output successful.")
  else:
    print("Output failed.")
else:
  print("The specified output_type was not recognised.")