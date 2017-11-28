# File to handle JSON output of results

import datetime
import json
# Library to look for files and create them if needed
import os
import settings

##
## @brief      Prints all data to json file
##
## @param      trinket_list   The trinkets dictionary {trinket_name s:{ilevel
##                            s:{dps s}}}
## @param      ilevels        The ilevels
## @param      graph_name     The graph name
## @param      simc_settings  The simc options dictionary {iterations s, target
##                            error s, fight style s, class s, spec s, tier s
##                            "T19M_NH"}
## @param      ordered_trinket_names  The ordered trinket names
##
## @return     True after json output
##
def print_json(trinket_list, filename):
  sim_data = {}
  sim_data["title"] = settings.graph_title
  sim_data["subtitle"] = settings.graph_subtitle
  sim_data["Simulated itemlevels"] = settings.ilevels
  sim_data["Simc setting"] = settings.simc_settings
  sim_data["Date"] = "{:%Y_%m_%d__%H_%M}".format(datetime.datetime.now())
  sim_data["trinkets"] = trinket_list
  sim_data["legendary_activated"] = settings.legendary
  sim_data["legendary_ilevel_colour"] = setting.legendary_colour
  sim_data["legendary_ilevel"] = settings.legendary_ilevel
  sim_data["simulate_gems"] = settings.simulate_gems
  with open(filename + ".json", "w") as ofile:
    ofile.write(json.dumps(sim_data, sort_keys=True, indent=4))
    return True
  return False
