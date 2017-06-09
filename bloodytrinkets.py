#!/usr/bin/env python3
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
def get_dps(trinket_id, item_level, fight_style):
  argument = [ settings.simc_settings["simc"] ]
  argument.append( "iterations="   + settings.simc_settings["iterations"] )
  argument.append( "target_error=" + settings.simc_settings["target_error"] )
  argument.append( "fight_style="  + fight_style )
  argument.append( "fixed_time=1" )
  argument.append( "default_actions=1" )
  if settings.simc_settings["ptr"]:
    argument.append( "ptr=1" )
  argument.append( "threads="      + settings.simc_settings["threads"] )
  if settings.simc_settings["c_profile"]:
    argument.append( settings.simc_settings["c_profile_path"] + settings.simc_settings["c_profile_name"] )
  else:
    argument.append( settings.simc_settings["class"] + "_" + settings.simc_settings["spec"] + "_" + settings.simc_settings["tier"] + ".simc" )
  argument.append( "trinket1=" )
  argument.append( "trinket2=,id=" + trinket_id + ",ilevel=" + item_level )

  # should prevent additional empty windows popping up...on win32 systems without breaking different OS
  if sys.platform == 'win32':
    # call simulationcraft in the background. grab output for processing and get dps value
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    simulation_output = subprocess.run(
      argument, 
      stdout=subprocess.PIPE, 
      stderr=subprocess.STDOUT, 
      universal_newlines=True, 
      startupinfo=startupinfo
    )

    while simulation_output.returncode != 0:
      simulation_output = subprocess.run(
        argument, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.STDOUT, 
        universal_newlines=True,
        startupinfo=startupinfo
      )
      
  else:
    simulation_output = subprocess.run(
      argument, 
      stdout=subprocess.PIPE, 
      stderr=subprocess.STDOUT, 
      universal_newlines=True
    )

    while simulation_output.returncode != 0:
      simulation_output = subprocess.run(
        argument, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.STDOUT, 
        universal_newlines=True
      )
  
  

  owndps = True
  dps = "DPS: 0.0"
  for line in simulation_output.stdout.splitlines():
    # needs this check to prevent grabbing the enemy dps
    if "DPS:" in line and owndps:
      dps = line
      owndps = False
  return dps.split()[1].split(".")[0]


##
## @brief      Sim all trinkets at all itemlevels when available.
##
## @param      trinkets     The trinkets dictionary {source s:{[trinket_name s,
##                          id s, base_ilevel i, max_itemlevel i]}}
## @param      ilevels      The ilevels list
## @param      fight_style  The fight style
## @param      simc_settings  The simc options dictionary {iterations s, target
##                            error s, fight style s, class s, spec s, tier s
##                            "T19M_NH"}
##
## @return     Dictionary of all simmed trinkets with all their dps values as
##             strings {trinket_name s:{ilevel s:{dps s}}}. dps is "0" if to be
##             simmed itemlevel don't match available trinket itemlevel
##
def sim_all( trinkets, ilevels, fight_style ):
  sim_counter = 0
  sim_ceiling = 0
  for source in trinkets:
    sim_ceiling += len( trinkets[source] )
  sim_ceiling *= len( ilevels )
  all_simmed = {}
  for source in trinkets:
    for trinket in trinkets[source]:
      # if max trinket itemlevel is lower than lowest to sim ilevel, don't add it to the result
      if int( trinket[3] ) < int( ilevels[-1] ):
        continue
      all_simmed[trinket[0]] = {}
      for ilevel in ilevels:
        dps = "0"
        if trinket[2] <= int( ilevel ) and trinket[3] >= int( ilevel ):
          dps = get_dps( trinket[1], ilevel, fight_style )
        elif source == "legendary" and ilevel == ilevels[0]:
          dps = get_dps( trinket[1], str(trinket[2]), fight_style )
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



error_collector = []
if not lib.simc_checks.is_iteration( settings.simc_settings["iterations"] ):
  error_collector.append("simc_settings[iterations] not strong or out of bounds")
if not lib.simc_checks.is_target_error( settings.simc_settings["target_error"] ):
  error_collector.append("simc_settings[target_error] not string or out of bounds")
if not lib.simc_checks.is_fight_style( settings.simc_settings["fight_styles"] ):
  error_collector.append("simc_settings[fight_styles] not a recognised fight style")
if not lib.spec_utils.is_class( settings.simc_settings["class"] ):
  error_collector.append("simc_settings[class] wrong name")
if not lib.spec_utils.is_spec( settings.simc_settings["spec"] ):
  error_collector.append("simc_settings[spec] not appropriate spec name")
if lib.spec_utils.is_class_spec( settings.simc_settings["class"], settings.simc_settings["spec"] ):
  trinkets = lib.trinkets.get_trinkets_for_spec( settings.simc_settings["class"], settings.simc_settings["spec"] )
else:
  error_collector.append("simc_settings[class] and simc_settings[spec] don't fit each other")

if error_collector:
  print("Some data got corrupted. The following errors were cought:")
  for error in error_collector:
    print(error)
  sys.exit("Program terminates due to errors in data.")


print("Name of the graph: '" + settings.graph_name + "'")

if len(settings.simc_settings["fight_styles"]) > 1:
  print("Calculating multiple fight styles.")

baseline = {"none": [["none", "", 840, 1200]]}
fight_style_counter = 0
for fight_style in settings.simc_settings["fight_styles"]:
  fight_style_counter += 1

  print("Loading base dps value.")
  base_dps = sim_all( baseline, [settings.ilevels[-1]], fight_style )
  if settings.output_screen:
    print( base_dps )

  print("Loading dps-values for all trinkets.")
  sim_results = sim_all( trinkets, settings.ilevels, fight_style )

  if lib.output.output.print_manager( base_dps, sim_results, fight_style ):
    print("Output successful.")

print("Program exists flawless.")