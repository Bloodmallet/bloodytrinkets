## File to manage outputs
 

## Library needed to get date and calculationtime for program
import datetime
import lib.output.highcharts as highcharts
import lib.output.json as json
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
def __create_filename(fight_style):
  # old format
  #filename = ""
  #filename += "{:%Y_%m_%d__%H_%M}".format(datetime.datetime.now())
  #filename += "_" + fight_style
  #filename += "_" + settings.simc_settings["class"]
  #filename += "_" + settings.simc_settings["spec"]
  #filename += "_" + settings.simc_settings["tier"]
  # 
  # format to use for automated website
  filename = ""
  filename += settings.simc_settings["class"] + "_"
  filename += settings.simc_settings["spec"]
  # TODO: add fightstyle to automated system
  return filename


##
## @brief      Gets the highest trinket dps.
##
## @param      sim_results  The simulation results
## @param      trinket      The trinket
##
## @return     The highest trinket dps.
##
def __get_highest_trinket_dps(sim_results, trinket):
  if not sim_results[trinket][settings.ilevels[0]] == "0":
    return sim_results[trinket][settings.ilevels[0]]
  dps = "0"
  for ilevel in settings.ilevels:
    if int( sim_results[trinket][ilevel] ) > int( dps ):
      dps = sim_results[trinket][ilevel]
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
## @param      base_ilevel  The base ilevel
##
## @return     Dictionary of all simmed trinkets with all their normalised dps
##             values as strings {trinket_name s:{ilevel s:{dps s}}}. dps is "0"
##             if the simmed itemlevel doesn't match available trinket itemlevel
##
def __normalise_trinkets(base_dps, sim_results, base_ilevel):
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
def __order_results(sim_results):
  highest_ilevel = settings.ilevels[0]
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
      if int( current_best_dps ) < int( trinket_dps ) and int( last_best_dps ) > int( trinket_dps ):
        current_best_dps = trinket_dps
        name = trinket
    if not name == "error": 
      trinket_list.append( name )
      last_best_dps = current_best_dps

  return trinket_list


def print_manager(base_dps_dic, sim_results, fight_style):
  filename = __create_filename(fight_style)
  for print_type in settings.output_types:
    print("")

    if print_type is "json":
      print("Initiating json output.")
      if json.print_json(sim_results, filename):
        print("Generating json file: Done")
      else:
        print("Generating json file: Failed")

    elif print_type is "highchart":
      print("Initiating highchart output")
      print("Ordering trinkets by dps.")
      ordered_trinket_names = __order_results(sim_results)
      if settings.output_screen:
        print(ordered_trinket_names)
      print("Normalising dps values.")
      sim_results = __normalise_trinkets(base_dps_dic, sim_results, settings.ilevels[-1])
      if settings.output_screen:
        print(sim_results)
      if highcharts.print_highchart(sim_results, ordered_trinket_names, filename):
        print("Generating highchart file: Done")
      else:
        print("Generating highchart file: Failed")
  return True
