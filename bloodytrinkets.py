#!/usr/bin/env python3
# Project to automate trinket sims for dps specs

# params

# data
import settings

import logging
import subprocess
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
def get_dps( trinket_id, item_level, fight_style, enchantment="", use_trinket_id=True, arguments=[] ):
  argument = [ settings.simc_settings[ "simc" ] ]
  argument.append( "iterations="   + settings.simc_settings[ "iterations" ] )
  argument.append( "target_error=" + settings.simc_settings[ "target_error" ] )
  argument.append( "fight_style="  + fight_style )
  argument.append( "fixed_time=1" )
  argument.append( "optimize_expressions=1" )
  argument.append( "default_actions=1" )
  # necessary for tank simulations, so those get hit (Q:Melekus)
  argument.append( "tmi_boss=TMI_Standard_Boss_T19M" )
  argument.append( "tmi_boss_type=T19M" )

  if settings.simc_settings[ "ptr" ]:
    argument.append( "ptr=1" )
  argument.append( "threads="      + settings.simc_settings[ "threads" ] )

  if settings.simc_settings[ "c_profile" ]:
    argument.append( settings.simc_settings[ "c_profile_path" ] + settings.simc_settings[ "c_profile_name" ] )
  else:
    if settings.simc_settings[ "tier" ][0] == "T":
      argument.append( "Tier" + settings.simc_settings[ "tier" ][1:] + "/" + settings.simc_settings[ "tier" ] + "_" + settings.simc_settings[ "class" ] + "_" + settings.simc_settings[ "spec" ] + ".simc" )
    else:
      argument.append( "PreRaid/" + settings.simc_settings[ "tier" ] + "_" + settings.simc_settings[ "class" ] + "_" + settings.simc_settings[ "spec" ] + ".simc" )

  if settings.simc_settings[ "use_second_trinket" ]:
    second_trinket_string = "trinket1=,id=" + settings.simc_settings[ "second_trinket" ][0] + ",ilevel=" + settings.simc_settings[ "second_trinket" ][1]
    if enchantment and not use_trinket_id:
      second_trinket_string += ",enchant=" + enchantment
    argument.append( second_trinket_string )
  else:
    argument.append( "trinket1=" )

  if use_trinket_id and trinket_id:
    argument.append( "trinket2=,id=" + trinket_id + ",ilevel=" + item_level + ",enchant=" + enchantment )
  else:
    argument.append( "trinket2=" )
  argument.append( "ready_trigger=1" )

  for parameter in arguments:
    argument.append( parameter )

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

    if simulation_output.returncode != 0:
      print("")
      print("ERROR: An Error occured during simulation. Please check the following output:")
      print("args: " + str(simulation_output.args))
      print("stdout: " + str(simulation_output.stdout))

    fail_counter = 0
    while simulation_output.returncode != 0 and fail_counter < 5:
      simulation_output = subprocess.run(
        argument,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        startupinfo=startupinfo
      )
      fail_counter += 1

  else:
    simulation_output = subprocess.run(
      argument,
      stdout=subprocess.PIPE,
      stderr=subprocess.STDOUT,
      universal_newlines=True
    )

    if simulation_output.returncode != 0:
      print("")
      print("ERROR: An Error occured during simulation. Please check the following output:")
      print("stdout: " + str(simulation_output.stdout))
      print("args: " + str(simulation_output.args))

    fail_counter = 0
    while simulation_output.returncode != 0 and fail_counter < 5:
      simulation_output = subprocess.run(
        argument,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True
      )
      fail_counter += 1

  if fail_counter >= 5:
    logging.critical( "Simulation failed 5 times.\nstdout: %s\nargs: %s", simulation_output.stdout, simulation_output.args )
    raise SystemExit( 0 )

  owndps = True
  dps = "DPS: 0.0"
  for line in simulation_output.stdout.splitlines():
    # needs this check to prevent grabbing the enemy dps
    if "DPS:" in line and owndps:
      dps = line
      owndps = False
  return dps.split()[1].split(".")[0]

#import random
#def get_dps( trinket_id, item_level, fight_style, enchantment="", use_trinket_id=True ):
#  string = item_level[:-1] + "5"
#  return string

##
## @brief      Sim all trinkets at all itemlevels when available.
##
## @param      trinkets     The trinkets dictionary {source s:[[trinket_name s,
##                          id s, base_ilevel i, max_itemlevel i, max_itemlevel_drop i],]}
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
  # for all sources in trinkets
  for source in trinkets:
    # for all trinkets in each source
    for trinket in trinkets[ source ]:
      # for all itemlevels
      for ilevel in ilevels:
        # if a trinket's minimum itemlevel is lower or equal to the ilevel
        # and a trinket's maximum itemlevel is greater or equal to the ilevel
        # trinket_min_ilevel <= ilevel <= trinket_max_ilevel
        if trinket[ 2 ] <= int( ilevel ) and int( ilevel ) <= trinket[ 3 ]:
          sim_ceiling += 1

  ## dictionary for all trinkets
  ## {trinket_name s:{ilevel s:{dps s}}}
  all_simmed = {}

  ## reminder of structure of trinkets:
  ## {source s:[[trinket_name s, id s, base_ilevel i, max_itemlevel i],]}
  ## source can be a dungeon etc
  for source in trinkets:
    for trinket in trinkets[ source ]:

      ## don't simulate a char with two identical trinkets if allow_double_trinkets is not checked
      if settings.simc_settings[ "use_second_trinket" ] and not settings.simc_settings[ "allow_double_trinkets" ] and trinket[ 1 ] == settings.simc_settings[ "second_trinket" ][ 0 ]:
        continue

      ## if max trinket itemlevel is lower than lowest to sim ilevel, don't add
      ## it to the result
      if int( trinket[ 3 ] ) < int( ilevels[ -1 ] ):
        continue

      ## handle legendaries
      if source == "legendary" and not settings.legendary:
        continue

      ## add a trinket to all simmed and make it a dictionary as well
      all_simmed[ trinket[ 0 ] ] = {}

      ## special handling for pantheon trinkets
      if trinket[ 1 ] in ( "154172", "154174", "154177", "154176" ):
        all_simmed[ trinket[ 0 ] + " +10" ] = {}
        all_simmed[ trinket[ 0 ] + " +15" ] = {}
        all_simmed[ trinket[ 0 ] + " +20" ] = {}

      ## special handling of the baseline profile to simulate data for sockets too
      if trinket[ 1 ] == "":
        all_simmed[ trinket[ 0 ] ][ ilevels[ 0 ] ] = get_dps( trinket[ 1 ], ilevels[ 0 ], fight_style )

        if settings.simulate_gems:
          all_simmed[ trinket[ 0 ] ][ "10_crit_gems" ] = get_dps( "", ilevels[ 0 ], fight_style, enchantment="2000crit", use_trinket_id=False )
          all_simmed[ trinket[ 0 ] ][ "10_haste_gems" ] = get_dps( "", ilevels[ 0 ], fight_style, enchantment="2000haste", use_trinket_id=False )
          all_simmed[ trinket[ 0 ] ][ "10_mastery_gems" ] = get_dps( "", ilevels[ 0 ], fight_style, enchantment="2000mastery", use_trinket_id=False )
          all_simmed[ trinket[ 0 ] ][ "10_versatility_gems" ] = get_dps( "", ilevels[ 0 ], fight_style, enchantment="2000vers", use_trinket_id=False )
        continue


      ## get dps values from all trinkets for all necessary itemlevels
      for ilevel in ilevels:
        dps = "0"

        ## if the trinkets minimum itemlevel <= current itemlevel AND
        ## trinket maximum itemlevel >= current itemlevel
        ## trinket_min_ilevel <= ilevel <= trinket_max_ilevel
        if trinket[ 2 ] <= int( ilevel ) and int( ilevel ) <= trinket[ 3 ]:
          dps = get_dps( trinket[ 1 ], ilevel, fight_style )
          sim_counter += 1

        ## add data
        all_simmed[ trinket[ 0 ] ][ ilevel ] = dps

        # if pantheon trinket: add +10 +15 +20 versions
        if trinket[ 1 ] in ( "154172", "154174", "154177", "154176" ):
          dps = "0"
          if trinket[ 2 ] <= int( ilevel ) and int( ilevel ) <= trinket[ 3 ]:
            dps = get_dps( trinket[ 1 ], ilevel, fight_style, arguments=["legion.pantheon_trinket_users=am/am/am/am/am/am/am/am/am/am"] )
          all_simmed[ trinket[ 0 ] + " +10" ][ ilevel ] = dps

          dps = "0"
          if trinket[ 2 ] <= int( ilevel ) and int( ilevel ) <= trinket[ 3 ]:
            dps = get_dps( trinket[ 1 ], ilevel, fight_style, arguments=["legion.pantheon_trinket_users=am/am/am/am/am/am/am/am/am/am/am/am/am/am/am"] )
          all_simmed[ trinket[ 0 ] + " +15" ][ ilevel ] = dps

          dps = "0"
          if trinket[ 2 ] <= int( ilevel ) and int( ilevel ) <= trinket[ 3 ]:
            dps = get_dps( trinket[ 1 ], ilevel, fight_style, arguments=["legion.pantheon_trinket_users=am/am/am/am/am/am/am/am/am/am/am/am/am/am/am/am/am/am/am/am"] )
          all_simmed[ trinket[ 0 ] + " +20" ][ ilevel ] = dps


        ## create fancy progress bar:
        progress = "["
        ## progress is split in 10% steps
        for i in range( 1, 26 ):
          ## if sim_counter is less than a 10% step add a dot to the progress
          ## bar
          if sim_ceiling * 4 * i / 100 > sim_counter:
            progress += "."
          else:
            progress += "="
        ## end of the progress bar
        progress += "]"

        ## print user feedback
        sys.stdout.write( "Already simed: %s %d of %d\r" % ( progress, sim_counter, sim_ceiling ) )
        sys.stdout.flush()
  return all_simmed



##
## @brief      Generates dps values for the max_itemlevel_drop itemlevel of all
##             trinkets. Prunes after the top 20 results.
##
## @param      trinkets     The trinkets dictionary {source s:[[trinket_name s,
##                          id s, base_ilevel i, max_itemlevel i, max_itemlevel_drop i],]}
## @param      ilevels      The ilevels list
## @param      fight_style  The fight style
##
## @return     Dictionary of all remaining trinkets after pruning.
##             {trinket_name s:{ilevel s:{dps s}}}
##
def prune_trinkets( trinkets, ilevels, fight_style ):

  # [ ( name, ilevel, dps ), ]
  full_list = []

  counter = 0
  ceiling = 0

  for source in trinkets:
    ceiling += len( trinkets[ source ] )

  for source in trinkets:
    for trinket in trinkets[ source ]:
      dps = "0"
      # look for the drop itemlevel in ilevels list
      if str( trinket[ 4 ] ) in ilevels:
        dps = get_dps( trinket[ 1 ], str( trinket[ 4 ] ), fight_style)
        full_list.append( ( trinket[ 0 ], str( trinket[ 4 ] ), dps ) )
      elif str( trinket[ 4 ] - 5 ) in ilevels:
        # tricky...simming with original itemlevel but printing the reduced one
        dps = get_dps( trinket[ 1 ], str( trinket[ 4 ] ), fight_style)
        full_list.append( ( trinket[ 0 ], str( trinket[ 4 ] - 5 ), dps ) )
      # if max_itemlevel_drop is smaller than the lowest to be simmed itemlevel
      elif trinket[ 4 ] < int( ilevels[ -1 ] ):
        # ignore trinket
        pass
      # if highest drop itemlevel is higher than all to be simmed itemlevels
      elif trinket[ 4 ] > int( ilevels[ 0 ] ):
        # magic: select a lower itemlevel in range of ilevels. if not possible, ignore trinket
        pass
      else:
        pass
      counter += 1
      sys.stdout.write( "Already simed: %d of %d\r" % ( counter, ceiling ) )
      sys.stdout.flush()

  sorted_full_list = sorted( full_list, key=lambda trinket: int( trinket[ 2 ] ), reverse=True )

  # prune
  logging.info( "Trinket list length before pruning: %d", len( sorted_full_list ) )
  del sorted_full_list[ settings.prune_count: ]
  logging.info( "Trinket list length after pruning: %d", len( sorted_full_list ) )

  results = {}

  for trinket in sorted_full_list:
    results[ trinket[ 0 ] ] = {}
    for ilevel in ilevels:
      if ilevel == trinket[ 1 ]:
        results[ trinket[ 0 ] ][ trinket[ 1 ] ] = trinket[ 2 ]
      else:
        results[ trinket[ 0 ] ][ ilevel ] = "0"

  return results


##
#-------------------------------------------------------------------------------------
# Program start
#-------------------------------------------------------------------------------------
##

if __name__ == '__main__':

  logging.getLogger(__name__)
  logging.basicConfig( filename='log.log', filemode='a', level=logging.DEBUG )

  ## Check for errors in the data
  error_collector = []
  if not Simc_checks.is_iteration( settings.simc_settings[ "iterations" ] ):
    error_collector.append( "simc_settings[iterations] not strong or out of bounds" )
  if not Simc_checks.is_target_error( settings.simc_settings[ "target_error" ] ):
    error_collector.append( "simc_settings[target_error] not string or out of bounds" )
  if not Simc_checks.is_fight_style( settings.simc_settings[ "fight_styles" ] ):
    error_collector.append( "simc_settings[fight_styles] not a recognised fight style" )
  if not Wow_lib.is_class( settings.simc_settings[ "class" ] ):
    error_collector.append( "simc_settings[class] wrong name" )
  if not Wow_lib.is_spec( settings.simc_settings[ "spec" ] ):
    error_collector.append( "simc_settings[spec] not appropriate spec name" )
  ## get all necessary trinkets for this class/spec at the same time
  if Wow_lib.is_class_spec( settings.simc_settings[ "class" ], settings.simc_settings[ "spec" ] ):
    trinkets = Wow_lib.get_trinkets_for_spec( settings.simc_settings[ "class" ], settings.simc_settings[ "spec" ] )
  else:
    error_collector.append( "simc_settings[class] and simc_settings[spec] don't fit each other" )

  ## Print errors and terminate
  if error_collector:
    logging.error( "Data corruption. The following errors were cought: %s", str(error_collector) )
    sys.exit( "Program terminates due to errors in data." )

  ## Remind the user of his graph name input
  print( "Name of the graph: '" + settings.graph_title + "'" )

  ## Print information about multiple fight styles, if that was choosen
  if len( settings.simc_settings[ "fight_styles" ] ) > 1:
    print( "Calculating multiple fight styles." )

  ## Generating baseline damage of a profile (no trinkets)
  baseline = { "none": [ [ "baseline", "", 840, 1200], ] }
  for fight_style in settings.simc_settings[ "fight_styles" ]:

    print( "Loading base dps value." )
    ## simulate baseline dps value from the empty trinket, minimum itemlevel and the current fight style
    base_dps = sim_all( baseline, [ settings.ilevels[ -1 ] ], fight_style )
    if settings.output_screen:
      print( base_dps )

    # add legendary itemlevel to the itemlevel list if necessary
    if settings.legendary:
      ilevels = [ settings.legendary_ilevel ] + settings.ilevels
    else:
      ilevels = settings.ilevels

    if settings.full_chart:
      ## simulate all trinkets for this fight style
      print("Loading dps-values for all trinkets.")
      sim_results = sim_all( trinkets, ilevels, fight_style )

      ## output results
      if lib.output.output.print_manager( base_dps, sim_results, fight_style ):
        print("  Full output successful.")

    # sim fewer if charts shall be pruned
    elif settings.pruned_chart:
      print("Loading trinkets to prune.")
      # prunes and simualtes trinkets
      sim_results = prune_trinkets( trinkets, ilevels, fight_style )

      # output results
      if lib.output.output.print_manager( base_dps, sim_results, fight_style, suffix="pruned" ):
        print("  Pruned output successful.")

    else:
      print("At least one of full_chart or pruned_chart needs to be set to true.")
      logging.critical("No chart type detected.")
      sys.exit( "No chart type detected." )

    # generate pruned charts
    if settings.pruned_chart and settings.full_chart:

      pruned_results = []
      for source in trinkets:
        for trinket in trinkets[ source ]:
          # {source s:[[trinket_name s, id s, base_ilevel i, max_itemlevel i, max_itemlevel_drop i],]}

          try:
            if str( trinket[ 4 ] ) in sim_results[ trinket[ 0 ] ]:
              pruned_results.append( ( trinket[ 0 ], str( trinket[ 4 ] ), sim_results[ trinket[ 0 ] ][ str( trinket[ 4 ] ) ] ) )
            elif str( trinket[ 4 ] - 5 ) in sim_results[ trinket[ 0 ] ]:
              # tricky...simming with original itemlevel but printing the reduced one
              pruned_results.append( ( trinket[ 0 ], str( trinket[ 4 ] - 5 ), sim_results[ trinket[ 0 ] ][ str( trinket[ 4 ] - 5 ) ]  ) )
            else:
              pass
          except Exception as e:
            logging.warning("The following trinket won't have a chance to be in the charts: %s", e)

      sorted_full_list = sorted( pruned_results, key=lambda trinket: int( trinket[ 2 ] ), reverse=True )
      del sorted_full_list[ settings.prune_count: ]

      pruned_results = {}

      for trinket in sorted_full_list:
        pruned_results[ trinket[ 0 ] ] = {}
        for ilevel in ilevels:
          if ilevel == trinket[ 1 ]:
            pruned_results[ trinket[ 0 ] ][ trinket[ 1 ] ] = trinket[ 2 ]
          else:
            pruned_results[ trinket[ 0 ] ][ ilevel ] = "0"

      if lib.output.output.print_manager( base_dps, pruned_results, fight_style, suffix="pruned" ):
        print("Pruned output successful.")

    # generate softly pruned charts (titanforged max ilevel drops)
    if settings.pruned_titanforged_chart and settings.full_chart:

      pruned_results = []
      for source in trinkets:
        for trinket in trinkets[ source ]:
          # {source s:[[trinket_name s, id s, base_ilevel i, max_itemlevel i, max_itemlevel_drop i],]}

          try:
            if str( trinket[ 4 ] ) in sim_results[ trinket[ 0 ] ]:
              pruned_results.append( ( trinket[ 0 ], str( trinket[ 4 ] ), sim_results[ trinket[ 0 ] ][ str( trinket[ 4 ] ) ] ) )
            elif str( trinket[ 4 ] - 5 ) in sim_results[ trinket[ 0 ] ]:
              # tricky...simming with original itemlevel but printing the reduced one
              pruned_results.append( ( trinket[ 0 ], str( trinket[ 4 ] - 5 ), sim_results[ trinket[ 0 ] ][ str( trinket[ 4 ] - 5 ) ]  ) )
            else:
              pass
          except Exception as e:
            logging.warning("The following trinket won't have a chance to be in the charts: %s", e)

      sorted_full_list = sorted( pruned_results, key=lambda trinket: int( trinket[ 2 ] ), reverse=True )
      del sorted_full_list[ settings.prune_count: ]

      pruned_results = {}

      for trinket in sorted_full_list:
        pruned_results[ trinket[ 0 ] ] = {}

        for i in range( len( ilevels ) ):
          try:
            if ilevels[ i ] == trinket[ 1 ] or ilevels[ i + 1 ] == trinket[ 1 ] or ilevels[ i + 2 ] == trinket[ 1 ]:
              pruned_results[ trinket[ 0 ] ][ ilevels[ i ] ] = sim_results[ trinket[ 0 ] ][ ilevels[ i ] ]
            else:
              pruned_results[ trinket[ 0 ] ][ ilevels[ i ] ] = "0"
          except Exception as e:
            pruned_results[ trinket[ 0 ] ][ ilevels[ i ] ] = "0"

      if lib.output.output.print_manager( base_dps, pruned_results, fight_style, suffix="pruned_titanforged" ):
        print("Pruned titanforged output successful.")
    elif settings.pruned_titanforged_chart:
      logging.error("Pruned titfanforged output can not be generated without full chart data. (Enable full_chart)")

  print("Program exits flawless.")
