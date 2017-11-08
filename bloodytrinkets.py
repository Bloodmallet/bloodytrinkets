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
## @param      trinket_id      The trinket identifier for the trinket for the
##                             chart
## @param      item_level      The item level
## @param      fight_style     The fight style
## @param      enchantment     The enchantment if one is interested in using
##                             that, used for gem simulation in this case
## @param      use_trinket_id  Decided whether the trinket_id is used or not,
##                             important for gem simulation
##
## @return     The dps s.
##
def get_dps(trinket_id, item_level, fight_style, enchantment="", use_trinket_id=True):
  argument = [ settings.simc_settings["simc"] ]
  argument.append( "iterations="   + settings.simc_settings["iterations"] )
  argument.append( "target_error=" + settings.simc_settings["target_error"] )
  argument.append( "fight_style="  + fight_style )
  argument.append( "fixed_time=1" )
  argument.append( "optimize_expressions=1" )
  argument.append( "default_actions=1" )
  # necessary for tank simulations, so those get hit (Q:Melekus)
  argument.append( "tmi_boss=TMI_Standard_Boss_T19M" )
  argument.append( "tmi_boss_type=T19M" )

  if settings.simc_settings["ptr"]:
    argument.append( "ptr=1" )
  argument.append( "threads="      + settings.simc_settings["threads"] )

  if settings.simc_settings["c_profile"]:
    argument.append( settings.simc_settings["c_profile_path"] + settings.simc_settings["c_profile_name"] )
  else:
    if settings.simc_settings["tier"][0] == "T":
      argument.append( "Tier" + settings.simc_settings["tier"][1:] + "/" + settings.simc_settings["tier"] + "_" + settings.simc_settings["class"] + "_" + settings.simc_settings["spec"] + ".simc" )
    else:
      argument.append( "PreRaid/" + settings.simc_settings["tier"] + "_" + settings.simc_settings["class"] + "_" + settings.simc_settings["spec"] + ".simc" )

  if settings.simc_settings["use_second_trinket"]:
    second_trinket_string = "trinket1=,id=" + settings.simc_settings["second_trinket"][0] + ",ilevel=" + settings.simc_settings["second_trinket"][1]
    if enchantment and not use_trinket_id:
      second_trinket_string += ",enchant=" + enchantment
    argument.append( second_trinket_string )
  else:
    argument.append( "trinket1=" )

  if use_trinket_id:
    argument.append( "trinket2=,id=" + trinket_id + ",ilevel=" + item_level + ",enchant=" + enchantment )
  else:
    argument.append( "trinket2=" )
  argument.append( "ready_trigger=1" )

  #print(argument)

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

      ## don't simulate a char with two identical trinkets if allow_double_trinkets is not checked
      if settings.simc_settings["use_second_trinket"] and not settings.simc_settings["allow_double_trinkets"] and trinket[1] == settings.simc_settings["second_trinket"][0]:
        sim_counter += 1
        continue

      ## if max trinket itemlevel is lower than lowest to sim ilevel, don't add
      ## it to the result
      if int( trinket[3] ) < int( ilevels[-1] ):
        sim_counter += 1
        continue

      ## handle legendaries
      if source == "legendary" and not settings.legendary:
        sim_counter += 1
        continue

      ## add a trinket to all simmed and make it a dictionary as well
      all_simmed[trinket[0]] = {}

      # special handling of the baseline profile to simulate data for sockets too
      if trinket[1] == "":
        all_simmed[trinket[0]][ilevels[0]] = get_dps( trinket[1], ilevels[0], fight_style )
        #print("Base: " + all_simmed[trinket[0]][ilevels[0]])
        all_simmed[trinket[0]]["10_crit_gems"] = get_dps( "", ilevels[0], fight_style, enchantment="2000crit", use_trinket_id=False )
        #print("Crit: " + all_simmed[trinket[0]]["10_crit_gems"])
        all_simmed[trinket[0]]["10_haste_gems"] = get_dps( "", ilevels[0], fight_style, enchantment="2000haste", use_trinket_id=False )
        #print("Haste: " + all_simmed[trinket[0]]["10_haste_gems"])
        all_simmed[trinket[0]]["10_mastery_gems"] = get_dps( "", ilevels[0], fight_style, enchantment="2000mastery", use_trinket_id=False )
        #print("Mastery: " + all_simmed[trinket[0]]["10_mastery_gems"])
        all_simmed[trinket[0]]["10_versatility_gems"] = get_dps( "", ilevels[0], fight_style, enchantment="2000vers", use_trinket_id=False )
        #print("Vers: " + all_simmed[trinket[0]]["10_versatility_gems"])
        continue

      if source == "legendary" and settings.legendary:
        all_simmed[trinket[0]][settings.legendary_ilevel] = get_dps( trinket[1], settings.legendary_ilevel, fight_style )
        sim_counter += 1
      elif source == "none" and trinket[0] == "baseline" and trinket[1] == "":
        # don't add a 0 dps value to the baseline for legendary itemlevel
        pass
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
        for i in range(1,26):
          ## if sim_counter is less than a 10% step add a dot to the progress
          ## bar
          if sim_ceiling * 4 * i / 100 > sim_counter:
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
print("Name of the graph: '" + settings.graph_title + "'")

## Print information about multiple fight styles, if that was choosen
if len(settings.simc_settings["fight_styles"]) > 1:
  print("Calculating multiple fight styles.")

## Generating baseline damage of a profile (no trinkets)
baseline = {"none": [["baseline", "", 840, 1200]]}
for fight_style in settings.simc_settings["fight_styles"]:

  print("Loading base dps value.")
  ## simulate baseline dps value from the empty trinket, minimum itemlevel and the current fight style
  base_dps = sim_all( baseline, [settings.ilevels[-1]], fight_style )
  if settings.output_screen:
    print( base_dps )

  print("")
  ## simulate all trinkets for this fight style
  print("Loading dps-values for all trinkets.")
  sim_results = sim_all( trinkets, settings.ilevels, fight_style )

  ## output results
  if lib.output.output.print_manager( base_dps, sim_results, fight_style ):
    print("Output successful.")

print("Program exits flawless.")
