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
import lib.simc_support.simc_checks as Simc_checks
import lib.simc_support.wow_lib     as Wow_lib



##
## @brief      Gets the dps for one trinket.
##
## @param      trinket_id   The trinket identifier
## @param      item_level   The item level
## @param      fight_style  The fight style
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
  if settings.simc_settings["use_second_trinket"]:
    argument += "trinket1=,id=" + settings.simc_settings["second_trinket"][0] + ",ilevel=" + settings.simc_settings["second_trinket"][1] + " "
  else:
    argument += "trinket1= "
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
##
## @return     Dictionary of all simmed trinkets with all their dps values as
##             strings {trinket_name s:{ilevel s:{dps s}}}. dps is "0" if to be
##             simmed itemlevel doesn't match available trinket itemlevel
##
def sim_all( trinkets, ilevels, fight_style ):
  sim_counter = 0
  sim_ceiling = 0

  ## calculate the max number of to be simmed values
  ## this number is larger than what will be simmed, because some trinkets
  ## aren't available at all itemlevels
  for source in trinkets:
    sim_ceiling += len( trinkets[source] )
  sim_ceiling *= len( ilevels )

  ## dictionary for all trinkets
  ## {trinket_name s:{ilevel s:{dps s}}}
  all_simmed = {}

  ## reminder of structure of trinkets:
  ## {source s:[[trinket_name s, id s, base_ilevel i, max_itemlevel i]]}
  ## source can be a dungeon etc
  for source in trinkets:
    for trinket in trinkets[source]:

      ## don't simulate a char with two identical trinkets
      if settings.simc_settings["use_second_trinket"] and trinket[1] == settings.simc_settings["second_trinket"][0]:
        continue

      ## if max trinket itemlevel is lower than lowest to sim ilevel, don't add
      ## it to the result
      if int( trinket[3] ) < int( ilevels[-1] ):
        continue

      ## handle legendaries
      if source == "legendary" and not settings.legendary:
        continue
      
      ## add a trinket to all simmed and make it a dictionary as well
      all_simmed[trinket[0]] = {}

      if source == "legendary" and settings.legendary:
        all_simmed[trinket[0]][settings.legendary_ilevel] = get_dps( trinket[1], settings.legendary_ilevel, fight_style )
      else:
        all_simmed[trinket[0]][settings.legendary_ilevel] = "0"

      ## get dps values from all normal trinkets for all necessary itemlevels
      for ilevel in ilevels:
        dps = "0"

        ## if the trinkets minimum itemlevel <= current itemlevel AND 
        ## trinket maximum itemlevel >= current itemlevel
        if trinket[2] <= int( ilevel ) and trinket[3] >= int( ilevel ):
          dps = get_dps( trinket[1], ilevel, fight_style )

        ## add data
        all_simmed[trinket[0]][ilevel] = dps
        sim_counter += 1

        ## create fancy progress bar:
        progress = "["
        ## progress is split in 10% steps
        for i in range(1,11):
          ## if sim_counter is less than a 10% step add a dot to the progress 
          ## bar
          if sim_ceiling * 10 * i / 100 > sim_counter:
            progress += "."
          else:
            progress += "="
        ## end of the progress bar
        progress += "]"

        ## print user feedback       
        sys.stdout.write( "Already simed: %s %d of %d\r" % ( progress, sim_counter, sim_ceiling ))
        sys.stdout.flush()
  return all_simmed



##
#-------------------------------------------------------------------------------------
# Program start
#-------------------------------------------------------------------------------------
##


## Check for errors in the data
error_collector = []
if not Simc_checks.is_iteration( settings.simc_settings["iterations"] ):
  error_collector.append("simc_settings[iterations] not strong or out of bounds")
if not Simc_checks.is_target_error( settings.simc_settings["target_error"] ):
  error_collector.append("simc_settings[target_error] not string or out of bounds")
if not Simc_checks.is_fight_style( settings.simc_settings["fight_styles"] ):
  error_collector.append("simc_settings[fight_styles] not a recognised fight style")
if not Wow_lib.is_class( settings.simc_settings["class"] ):
  error_collector.append("simc_settings[class] wrong name")
if not Wow_lib.is_spec( settings.simc_settings["spec"] ):
  error_collector.append("simc_settings[spec] not appropriate spec name")
## get all necessary trinkets for this class/spec at the same time
if Wow_lib.is_class_spec( settings.simc_settings["class"], settings.simc_settings["spec"] ):
  trinkets = Wow_lib.get_trinkets_for_spec( settings.simc_settings["class"], settings.simc_settings["spec"] )
else:
  error_collector.append("simc_settings[class] and simc_settings[spec] don't fit each other")

## Print errors and terminate
if error_collector:
  print("Some data got corrupted. The following errors were cought:")
  for error in error_collector:
    print(error)
  sys.exit("Program terminates due to errors in data.")

## Remind the user of his graph name input
print("Name of the graph: '" + settings.graph_name + "'")

## Print information about multiple fight styles, if that was choosen
if len(settings.simc_settings["fight_styles"]) > 1:
  print("Calculating multiple fight styles.")

## Generating baseline damage of a profile (no trinkets)
baseline = {"none": [["none", "", 840, 1200]]}
for fight_style in settings.simc_settings["fight_styles"]:

  print("Loading base dps value.")
  ## simulate baseline dps value from the empty trinket, minimum itemlevel and the current fight style
  base_dps = sim_all( baseline, [settings.ilevels[-1]], fight_style )
  if settings.output_screen:
    print( base_dps )

  ## simulate all trinkets for this fight style
  print("Loading dps-values for all trinkets.")
  sim_results = sim_all( trinkets, settings.ilevels, fight_style )

  ## output results
  if lib.output.output.print_manager( base_dps, sim_results, fight_style ):
    print("Output successful.")

print("Program exists flawless.")