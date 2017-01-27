# File for handling all Highcharts

##
## @brief      Generates js output for http://www.highcharts.com/ bars of
##             http://www.stormearthandlava.com/elemental-shaman-hub/elemental-trinket-sims/
##
## @param      trinket_list           The normalised trinkets dictionary
##                                    {trinket_name s:{ilevel s:{dps s}}}
## @param      ordered_trinket_names  The ordered trinket names
## @param      ilevels                The ilevels list
## @param      graph_colours          The graph_colours list for ilevels
## @param      graph_name             The graph name
## @param      simc_settings          The simc options dictionary {iterations s,
##                                    target error s, fight style s, class s,
##                                    spec s, tier s "T19M_NH"}
##
## @return     True if writing to file was successfull
##
def print_graph_data(trinket_list, ordered_trinket_names, ilevels, graph_colours, graph_name, simc_settings):
  with open(create_filename(simc_settings) + ".js", "w") as ofile:
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
      ofile.write("            color: '" + graph_colours[ilevel] + "',\n")
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