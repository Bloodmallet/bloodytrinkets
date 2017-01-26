# Project to automate trinket sims for dps specs

# Library to use command line
import subprocess
# Library to get date and calcutiontime for program
import datetime
# Library to look for files and create them if needed
import os
# params
#import argparse
# TODO: Recheck sys in 
import sys



##
#-------------------------------------------------------------------------------------
# Options
#-------------------------------------------------------------------------------------
##

graph_name = "Icefury trinket sims 7.1.5"

output = True

simc_options = {}
simc_options["fight_style"]  = "patchwerk"
simc_options["iterations"]   = "20000"
simc_options["target_error"] = "0.1"
simc_options["tier"]         = "T19M_NH"

simc_options["class"] = "shaman"
simc_options["spec"]  = "elemental"

simc_options["c_profile"]          = False
simc_options["c_profile_location"] = "example_dir/"
simc_options["c_profile_name"]     = "example_same.simc"

# Defines itemlevels that shall be simed ordered from lowest to highest
ilevels = [ "925", "915", "905", "895", "885", "875", "865" ]
colours = { "865": "#4572a7", "875": "#aa4643", "885": "#89a54e", "895": "#71588f", "905": "#4198af", "915": "#db843d", "925": "#00E676" }


##
#-------------------------------------------------------------------------------------
# Functions
#-------------------------------------------------------------------------------------
##

##
## @brief      Creates a filename with current date.
##
## @param      simc_options  The simc options dictionary {iterations s, target
##                           error s, fight style s, class s, spec s, tier s
##                           "T19M_NH"}
##
## @return     Returns a filename which contains the current date
##
def create_filename(simc_options):
  filename = ""
  filename += "{:%Y_%m_%d}".format(datetime.datetime.now())
  filename += "_" + simc_options["fight_style"]
  filename += "_" + simc_options["class"]
  filename += "_" + simc_options["spec"]
  filename += "_" + simc_options["tier"]
  return filename


##
## @brief      Gets the dps for one trinket.
##
## @param      trinket_id    The trinket identifier
## @param      item_level    The item level
## @param      simc_options  The simc options dictionary {iterations s, target
##                           error s, fight style s, class s, spec s, tier s
##                           "T19M_NH"}
##
## @return     The dps s.
##
def get_dps(trinket_id, item_level, simc_options):
  argument = "../simc.exe "
  argument += "iterations=" + simc_options["iterations"] + " "
  argument += "target_error=" + simc_options["target_error"] + " "
  argument += "fight_style=" + simc_options["fight_style"] + " "
  argument += "fixed_time=1 "
  argument += "default_actions=1 "
  if simc_options["c_profile"]:
    argument += simc_options["c_profile_location"] + simc_options["c_profile_name"] + " "
  else:
    argument += simc_options["class"] + "_" + simc_options["spec"] + "_" + simc_options["tier"] + ".simc "
  argument += "name=" + create_filename(simc_options) + " "
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
## @brief      Generates js output for http://www.highcharts.com/ bars of
##             http://www.stormearthandlava.com/elemental-shaman-hub/elemental-trinket-sims/
##
## @param      trinket_list           The trinkets dictionary {trinket_name
##                                    s:{ilevel s:{dps s}}}
## @param      ordered_trinket_names  The ordered trinket names
## @param      ilevels                The ilevels list
## @param      colours                The colours list for ilevels
## @param      graph_name             The graph name
## @param      simc_options           The simc options dictionary {iterations s,
##                                    target error s, fight style s, class s,
##                                    spec s, tier s "T19M_NH"}
##
## @return     True if writing to file was successfull
##
def output_graph_data(trinket_list, ordered_trinket_names, ilevels, colours, graph_name, simc_options):
  with open(create_filename(simc_options) + ".js", "w") as ofile:
    ofile.write("jQuery(function ($) {\n")
    ofile.write("    Highcharts.chart('if-container', {\n")
    ofile.write("        chart: {\n")
    ofile.write("            type: 'bar'\n")
    ofile.write("        },\n")
    ofile.write("        title: {\n")
    ofile.write("            text: '" + graph_name + "'\n")
    ofile.write("        },\n")
    ofile.write("        xAxis: {\n")
    ofile.write("      categories: [")
    for name in ordered_trinket_names:
      ofile.write('"' + name + '"')
      if not name == ordered_trinket_names[-1]:
        ofile.write(",")
    ofile.write("]\n")
    ofile.write("        },\n")
    ofile.write("        yAxis: {\n")
    ofile.write("            min: 0,\n")
    ofile.write("            title: {\n")
    #Δ
    ofile.write("                text: '\\u0394 Damage per second'\n")
    ofile.write("            },\n")
    ofile.write("            labels: {\n")
    ofile.write("                enabled: true\n")
    ofile.write("            },\n")
    ofile.write("            stackLabels: {\n")
    ofile.write("                enabled: false,\n")
    ofile.write("                style: {\n")
    ofile.write("                    fontWeight: 'bold',\n")
    ofile.write("                    color: (Highcharts.theme && Highcharts.theme.textColor) || 'white'\n")
    ofile.write("                }\n")
    ofile.write("            }\n")
    ofile.write("        },\n")
    ofile.write("        legend: {\n")
    ofile.write("            align: 'right',\n")
    ofile.write("            x: 0,\n")
    ofile.write("            verticalAlign: 'bottom',\n")
    ofile.write("            y: 0,\n")
    ofile.write("            floating: false,\n")
    ofile.write("            backgroundColor: (Highcharts.theme && Highcharts.theme.background2) || 'white',\n")
    ofile.write("            borderColor: '#CCC',\n")
    ofile.write("            borderWidth: 1,\n")
    ofile.write("            shadow: false,\n")
    ofile.write("            reversed: true\n")
    ofile.write("        },\n")
    ofile.write("        tooltip: {\n")
    ofile.write("            headerFormat: '<b>{point.x}</b>',\n")
    ofile.write("            formatter: function() {\n")
    ofile.write("                var s = '<b>'+ this.x +'</b>',\n")
    ofile.write("                cumulative_amount = 0;\n")
    ofile.write("                $.each(this.points.reverse(), function(i, point) {\n")
    ofile.write("                    cumulative_amount += point.y\n")
    ofile.write("                    if (point.y !== 0){\n")
    ofile.write("                        s += '<br/>'+ point.series.name +':\t' + cumulative_amount; \n")
    ofile.write("                    }\n")
    ofile.write("                });\n")
    ofile.write("                return s;\n")
    ofile.write("            },\n")
    ofile.write("            shared: true\n")
    ofile.write("        },\n")
    ofile.write("        plotOptions: {\n")
    ofile.write("            series: {\n")
    ofile.write("                borderColor: '#151515'\n")
    ofile.write("\n")
    ofile.write("            },\n")
    ofile.write("            bar: {\n")
    ofile.write("                stacking: 'normal',\n")
    ofile.write("                dataLabels: {\n")
    ofile.write("                    enabled: false,\n")
    ofile.write("                    color: (Highcharts.theme && Highcharts.theme.dataLabelsColor) || 'white'\n")
    ofile.write("                }\n")
    ofile.write("            }\n")
    ofile.write("        },\n")
    ofile.write("                series: [")
    for i in range(0, len(ilevels)):
      ilevel = ilevels[i]
      if i < len(ilevels) - 1:
        next_ilevel = ilevels[i + 1]
      else:
        next_ilevel = False
      if not ilevel == ilevels[0]:
        ofile.write(", ")
      ofile.write("{\n")
      ofile.write("            name: '" + ilevel + "',\n")
      ofile.write("            color: '" + colours[ilevel] + "',\n")
      ofile.write("            data: [")
      for trinket_name in ordered_trinket_names:
        if ilevel == ilevels[-1]:
          ofile.write(trinket_list[trinket_name][ilevel])
        else:
          if trinket_list[trinket_name][ilevel] == "0":
            ofile.write("0")
          else:
            ofile.write(str(int(trinket_list[trinket_name][ilevel]) - int(trinket_list[trinket_name][next_ilevel])))
        if not trinket_name == ordered_trinket_names[-1]:
          ofile.write(",")
      ofile.write("]\n")
      ofile.write("        }")
    ofile.write("]\n")
    ofile.write("    });\n")
    ofile.write("});")
    return True
  return False


##
## @brief      Sim all trinkets at all itemlevels when available.
##
## @param      trinkets      The trinkets dictionary {source s:{[trinket_name s,
##                           id s, base_ilevel i, max_itemlevel i]}}
## @param      ilevels       The ilevels list
## @param      simc_options  The simc options dictionary {iterations s, target
##                           error s, fight style s, class s, spec s, tier s
##                           "T19M_NH"}
## @param      output        Enables os disables "x / y" lines
##
## @return     Dictionary of all simmed trinkets with all their dps values as
##             strings {trinket_name s:{ilevel s:{dps s}}}. dps is "0" if to be
##             simmed itemlevel don't match available trinket itemlevel
##
def sim_all(trinkets, ilevels, simc_options, output):
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
          dps = get_dps(trinket[1], ilevel, simc_options)
        all_simmed[trinket[0]][ilevel] = dps
        sim_counter += 1
        if output:
          sys.stdout.write("Already simed: %d of %d\r" % (sim_counter, sim_ceiling))
          sys.stdout.flush()
          # TODO: Recheck here @ import sys
          #print(str(sim_counter) + "/" + str(sim_ceiling))
  return all_simmed


##
## @brief      Validates the input fight style.
##
## @param      fight_style  The fight style like in SimC options
##
## @return     True if fight_style matches predetermined SimC-styles
##
def validate_fight_style(fight_style):
  fight_style_list = ("patchwerk",
                      "lightmovement", 
                      "heavymovement", 
                      "hecticaddcleave", 
                      "beastlord", 
                      "helterskelter")
  if fight_style in fight_style_list:
      return True
  return False


##
## @brief      Validates the input wow_class
##
## @param      wow_class    The wow class you want to check
## @param      wow_classes  The wow classes that are available as a dictionary
##                          {name s:{talents s, specs s:(spec_names)}}
##
## @return     True if wow_class is an actual wow class
##
def validate_class(wow_class, wow_classes):
  if wow_class in wow_classes:
    return True
  return False




##
#-------------------------------------------------------------------------------------
# Data
#-------------------------------------------------------------------------------------
# Don't touch this unless you have to add data
baseline = {"none": [["none", "", 840, 1200]]}
trinkets = {}
trinkets["world"] = [ [ "Devilsaur Shock-Baton",    "140030", 840, 1200 ],
                      [ "Padawsen's Unlucky Charm", "141536", 860, 1200 ],
                      [ "Unstable Arcano Crystal",  "141482", 860, 1200 ] ]
trinkets["dungeon"] = [ [ "Caged Horror",           "136716", 840, 1200 ],
                        [ "Chrono Shard",           "137419", 840, 1200 ],
                        [ "Corrupted Starlight",    "137301", 840, 1200 ],
                        [ "Eye of Skovald",         "133641", 840, 1200 ],
                        [ "Figurehead of the Naglfar", "137329", 840, 1200 ],
                        [ "Horn of Valor",          "133642", 840, 1200 ],
                        [ "Infernal Writ",          "137485", 840, 1200 ],
                        [ "Moonlit Prism",          "137541", 840, 1200 ],
                        [ "Naraxas Spiked Tongue",  "137349", 840, 1200 ],
                        [ "Oakhearts Gnarled Root", "137306", 840, 1200 ],
                        [ "Obelisk of the Void",    "137433", 840, 1200 ],
                        [ "Portable Manacracker",   "137398", 840, 1200 ],
                        [ "Stormsinger Fulmination Charge", "137367", 840, 1200 ],
                        [ "Squirrel Generator",     "137446", 840, 1200 ] ]
trinkets["karazhan"] = [[ "Arans Relaxed Ruby", "142157", 860, 1200 ],
                        [ "Deteriorated Construct Core", "142165", 860, 1200 ],
                        [ "Mrrgrias_Favor", "142160", 855, 1200 ] ]
trinkets["emerald_nightmare"] = [[ "Bough of Corruption",  "139323", 860, 1200 ],
                                 [ "Swarming Plaguehive",  "139321", 860, 1200 ],
                                 [ "Twisting Wind",        "139323", 860, 1200 ],
                                 [ "Unstable Horrorslime", "138224", 860, 1200 ],
                                 [ "Wriggling Sinew",      "139326", 860, 1200 ] ]
trinkets["trial_of_valor"] = [[ "Brinewater Slime in a Bottle Crit",        "142507,bonus_id=603", 865, 1200 ],
                              [ "Brinewater Slime in a Bottle Haste",       "142507,bonus_id=604", 865, 1200 ],
                              [ "Brinewater Slime in a Bottle Mastery",     "142507,bonus_id=605", 865, 1200 ],
                              [ "Brinewater Slime in a Bottle Versatility", "142507,bonus_id=607", 865, 1200 ] ]
trinkets["nighthold"] = [ [ "Erratic Metronome",        "140792", 870, 1200 ],
                          [ "Fury of the Burning Sky",  "140801", 875, 1200 ],
                          [ "Icon of Rot",              "140798", 875, 1200 ],
                          [ "Pharameres Forbidden Guidance", "140800", 875, 1200 ],
                          [ "Star Gate",                "140804", 875, 1200 ],
                          [ "Whispers in the Dark",     "140809", 875, 1200 ] ]
trinkets["pvp"] = [       ["PVP Insignia of Dominance", "142668", 840, 1200],
                          ["PVP Badge of Dominance", "142779", 840, 1200] ]

# TODO: create wow lib
wow_classes = { "shaman":       {"talents": "1001111", "specs": ("elemental", "enhancement")              },
                "mage":         {"talents": "1011011", "specs": ("fire", "frost", "arcane")               },
                "druid":        {"talents": "1000111", "specs": ("balance", "feral")                      },
                "priest":       {"talents": "1001111", "specs": ("shadow")                                },
                "warlock":      {"talents": "1101011", "specs": ("affliction", "destruction", "demonology")  },
                "hunter":       {"talents": "1101011", "specs": ("mm", "sv", "bm")                        },
                "death_knight": {"talents": "1110011", "specs": ("unholy", "frost")                       },
                "demon_hunter": {"talents": "1110111", "specs": ("havoc")                                 },
                "monk":         {"talents": "1010011", "specs": ("windwalker")                            },
                "paladin":      {"talents": "1101001", "specs": ("retribution")                           },
                "rogue":        {"talents": "1110111", "specs": ("assassination", "sublety", "outlaw")    },
                "warrior":      {"talents": "1010111", "specs": ("arms", "fury")                          } }


##
#-------------------------------------------------------------------------------------
# Program start
#-------------------------------------------------------------------------------------
##

print("Name of the graph: '" + graph_name + "'")
print("Loading base dps value.")
base_dps = sim_all(baseline, [ilevels[-1]], simc_options, False)
#if output:
#  print(base_dps)

print("Loading dps-values for all trinkets.")
sim_results = sim_all(trinkets, ilevels, simc_options, output)

print("Ordering trinkets by dps.")
ordered_trinket_names = order_results(sim_results, ilevels)
#if output:
#  print(ordered_trinket_names)

print("")
print("Normalising dps values.")
sim_results = normalise_trinkets(sim_results, base_dps, ilevels[-1])
#if output:
#  print(sim_results)

print("Printing results to file.")
if output_graph_data(sim_results, ordered_trinket_names, ilevels, colours, graph_name, simc_options):
  print("Output successful")
else:
  print("Output failed")
