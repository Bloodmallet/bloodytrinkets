## File to manage outputs


## Library needed to get date and calculationtime for program
import lib.output.highcharts as highcharts
import lib.output.json_print as json
import settings


##
## @brief      Creates a filename with current date.
##
## @param      simc_settings  The simc options dictionary {iterations s, target
##                            error s, fight style s, class s, spec s, tier s
##                            "T19M_NH"}
##
## @return     Returns a filename which contains the current date
##
def __create_filename( fight_style, prefix="", suffix="" ):
  filename = "./results/"
  if prefix:
    filename += prefix + "_"
  filename += settings.simc_settings["class"] + "_"
  filename += settings.simc_settings["spec"] + "_"
  filename += fight_style
  if suffix:
    filename += "_" + suffix
  if settings.simc_settings["ptr"]:
    filename += "_ptr"
  return filename


##
## @brief      Gets the highest trinket dps.
##
## @param      sim_results  The simulation results
## @param      trinket      The trinket
##
## @return     The highest trinket dps.
##
def __get_highest_trinket_dps( sim_results, trinket ):
  if settings.legendary and sim_results[ trinket ][ settings.legendary_ilevel ] != "0":
    return sim_results[ trinket ][ settings.legendary_ilevel ]

  if sim_results[ trinket ][ settings.ilevels[ 0 ] ] != "0":
    return sim_results[ trinket ][ settings.ilevels[ 0 ] ]

  dps = "0"
  for ilevel in sim_results[ trinket ]:
    if int( sim_results[ trinket ][ ilevel ] ) > int( dps ):
      dps = sim_results[ trinket ][ ilevel ]
  return dps


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
## @param      base_ilevel  The lowest base ilevel
##
## @return     Dictionary of all simmed trinkets with all their normalised dps
##             values as strings {trinket_name s:{ilevel s:{dps s}}}. dps is "0"
##             if the simmed itemlevel doesn't match available trinket itemlevel
##
def __normalise_trinkets( base_dps, sim_results, base_ilevel ):
  normalized_results = {}
  for trinket in sim_results:
    normalized_results[ trinket ] = {}
    for ilevel in sim_results[ trinket ]:
      if not sim_results[ trinket ][ ilevel ] == "0":
        normalized_results[ trinket ][ ilevel ] = str( int( sim_results[ trinket ][ ilevel ] ) - int( base_dps[ "baseline" ][ base_ilevel ] ) )
      else:
        normalized_results[ trinket ][ ilevel ] = "0"
  return normalized_results


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
def __order_results(sim_results):

  current_best_dps = "-1"
  last_best_dps = "-1"
  name = ""
  trinket_list = []
  # gets highest dps value of all trinkets
  for trinket in sim_results:
    trinket_dps = __get_highest_trinket_dps( sim_results, trinket )
    if int( last_best_dps ) < int( trinket_dps ) :
      last_best_dps = trinket_dps
      name = trinket
  trinket_list.append( name )

  for outerline in sim_results:
    name = "error"
    current_best_dps = "-1"
    for trinket in sim_results:
      trinket_dps = __get_highest_trinket_dps( sim_results, trinket )
      if int( current_best_dps ) < int( trinket_dps ) and int( last_best_dps ) >= int( trinket_dps ) and not trinket in trinket_list:
        current_best_dps = trinket_dps
        name = trinket
    if not name == "error":
      trinket_list.append( name )
      last_best_dps = current_best_dps

  return trinket_list


def print_manager( base_dps_dic, sim_results, fight_style, prefix="", suffix="" ):
  filename = __create_filename( fight_style, prefix, suffix )

  for print_type in settings.output_types:
    print( "" )

    if print_type is "json":
      print( "JSON output " + prefix + " " + suffix )
      all_simulations = dict( sim_results )
      all_simulations[ "baseline" ] = dict( base_dps_dic[ "baseline" ] )

      if json.print_json( all_simulations, filename ):
        print( "  Generating json file: Done" )
      else:
        print( "  Generating json file: Failed" )

    elif print_type is "highchart":
      print( "HIGHCHART output " + prefix + " " + suffix )
      print( "  Ordering trinkets by dps." )

      ordered_trinket_names = __order_results( sim_results )

      if settings.output_screen:
        print( ordered_trinket_names )

      print( "  Normalising dps values." )
      normalized_results = __normalise_trinkets( base_dps_dic, sim_results, settings.ilevels[ -1 ] )

      if settings.output_screen:
        print( normalized_results )

      if highcharts.print_highchart( normalized_results, ordered_trinket_names, filename ):
        print( "  Generating highchart file: Done" )
      else:
        print( "  Generating highchart file: Failed" )
  return True
