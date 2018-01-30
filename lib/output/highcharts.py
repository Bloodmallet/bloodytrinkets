# File for handling all Highcharts

import datetime
import json
# Library to look for files and create them if needed
import os
import settings



##
## @brief      Gets the dps ilevel borders which helds dps values of a trinket.
##
## @param      trinket  The trinket with all ilevel dps values
##
## @return     The lowest ilevel and highest dps ilevel as string in a list
##             [lowest, highest].
##
def __get_dps_ilevel_borders(trinket):
  # this value should be greater than any possible ilevel value
  lowest_ilevel = "1200"
  highest_ilevel = settings.ilevels[ -1 ]

  for ilevel in trinket:
    if int(ilevel) < int(lowest_ilevel) and trinket[ilevel] != "0":
      lowest_ilevel = ilevel
    if int(ilevel) > int(highest_ilevel) and trinket[ilevel] != "0":
      highest_ilevel = ilevel

  return [lowest_ilevel, highest_ilevel]


##
## @brief      Generates js output for http://www.highcharts.com/ bars of
##             https://www.stormearthandlava.com/ele/trinkets/
##
## @param      trinket_list           The normalised trinkets dictionary
##                                    {trinket_name s:{ilevel s: dps s,}}
## @param      ordered_trinket_names  The ordered trinket names
## @param      filename               The filename
## TODO        Rewrite                Rewrite this whole function to use actual data types and
##                                    and convert that into json itself.
##
## @return     True if writing to file was successfull
##
def print_highchart( trinket_list, ordered_trinket_names, filename ):
  # let's create a real structure...
  categories = []
  for name in ordered_trinket_names:
    categories.append( name )

  # massage category names into wowhead links
  if settings.add_tooltips:
    new_categories_list = []

    import lib.simc_support.wow_lib as Wow_lib
    # get full trinket list, to compare to categories
    # {source s:[[trinket_name s, id s, base_ilevel i, max_itemlevel i, max_itemlevel_drop i],]}
    full_trinket_list = Wow_lib.get_trinkets_for_spec( settings.simc_settings[ "class" ], settings.simc_settings[ "spec" ] )

    for i in range( len( categories ) ):
      found = False
      for source in full_trinket_list:
        for trinket in full_trinket_list[ source ]:
          # if the original trinket name is in the category name like "Amanthuls +15"
          if trinket[ 0 ] in categories[ i ]:
            found = True
            categories[ i ] = "<a href=\"http://www.wowhead.com/item={item_id}\">{item_name}</a>".format( item_id=trinket[ 1 ], item_name=categories[ i ] )
            break
        if found:
          break

  # MEAN CALCULATION
  dps_sum = 0
  dps_counter = 0

  for trinket_name in ordered_trinket_names:
    lowest_dps_ilevel, highest_dps_ilevel = __get_dps_ilevel_borders(trinket_list[trinket_name])
    # add highest dps value to the mean
    dps_sum += int(trinket_list[trinket_name][highest_dps_ilevel])
    dps_counter += 1

  mean = dps_sum / dps_counter
  mean_text = "'mean: ' + Intl.NumberFormat().format(" + str( int( mean ) ) + ")"
  # MEAN CALCULATION END

  # data handle for all series
  series = []

  ## handle all normal itemlevels data for series
  ## add legendary itemlevel if legendaries are enabled
  if settings.legendary:
    ilevels = [ settings.legendary_ilevel ] + settings.ilevels
    settings.graph_colours[ settings.legendary_ilevel ] = settings.legendary_colour

  else:
    ilevels = settings.ilevels

  for i in range( 0, len( ilevels ) ):
    ilevel = ilevels[i]
    if i < len( ilevels ) - 1:
      next_ilevel = ilevels[ i + 1 ]
    else:
      next_ilevel = False

    series_ilevel_data = []

    for trinket_name in ordered_trinket_names:
      lowest_dps_ilevel, highest_dps_ilevel = __get_dps_ilevel_borders( trinket_list[ trinket_name ] )

      # if it's the lowest itemlevel, just print the values
      if ilevel == ilevels[ -1 ]:
        series_ilevel_data.append( int( trinket_list[ trinket_name ][ ilevel ] ) )
      else:
        # if a trinket doesn't have the current ilevel, or for some unknown reason the dps value couldn't be generated
        if trinket_list[ trinket_name ][ ilevel ] == "0":
          # if the dps of trinket wasn't saved from the sim-run, print the average of the former and later
          if int( ilevel ) > int( lowest_dps_ilevel ) and int( ilevel ) < int( highest_dps_ilevel ):
            series_ilevel_data.append(
              int(
                (
                  int( trinket_list[ trinket_name ][ ilevels[ i - 1 ] ] ) - int( trinket_list[ trinket_name ][ ilevels[ i + 1 ] ] )
                ) / 2.0
              )
            )
          else:
            series_ilevel_data.append( 0 )
        else:
          if int( trinket_list[ trinket_name ][ ilevel ] ) - int( trinket_list[ trinket_name ][ next_ilevel ]) < 0:
            series_ilevel_data.append( 0 )
          elif trinket_list[ trinket_name ][ next_ilevel ] == "0" and int( next_ilevel ) > int( lowest_dps_ilevel ):
            series_ilevel_data.append(
              int(
                (
                  int( trinket_list[ trinket_name ][ ilevel ] ) - int( trinket_list[ trinket_name ][ ilevels[ i + 2 ] ] )
                ) / 2.0
              )
            )
          else:
            series_ilevel_data.append(
                int( trinket_list[ trinket_name ][ ilevel ] ) - int( trinket_list[ trinket_name ][ next_ilevel ] )
            )

    # create series ilevel dictionars
    series_ilevel = {
      "name": ilevel,
      "color": settings.graph_colours[ ilevel ],
      "data": series_ilevel_data
    }

    # add dictionary to series
    series.append( series_ilevel )


  highcharts_data = {
    "chart": {
      "type": "bar"
    },
    "title": {
      "text": settings.graph_title,
      "useHTML": True
    },
    "subtitle": {
      "text": settings.graph_subtitle,
      "useHTML": True
    },
    "xAxis": {
      "categories": categories,
      "labels": {
        "useHTML": True,
      },
    },
    "yAxis": {
      "min": 0,
      "title": {
        "text": '\\u0394 Damage per second'
      },
      "labels": {
        "enabled": False,
      },
      "stackLabels": {
        "enabled": True,
        "style": {
          "textOutline": False,
        },
        "formatter": """'''function() {
          return Intl.NumberFormat().format(this.total);
        }'''""",
      },
      "plotLines": [{
        "color": "#0973DA",
        "value": mean,
        "width": 2,
        "zIndex": 2,
        "label": {
          "text": """'''{0}'''""".format(mean_text),
          "align": 'left',
          "verticalAlign": 'bottom',
          "rotation": 0,
          "x": 10,
          "y": -23,
          "style": {
            "color": "#0973DA"
          }
        }
      }]
    },
    "legend": {
      "align": "right",
      "x": 0,
      "verticalAlign": "bottom",
      "y": 0,
      "floating": False,
      "backgroundColor": "'''(Highcharts.theme && Highcharts.theme.background2) || 'white''''",
      "borderColor": '#CCC',
      "borderWidth": 1,
      "shadow": False,
      "reversed": True
    },
    "tooltip": {
      "headerFormat": "<b>{point.x}</b>",
      "formatter": """'''function() {
        var s = '<div style="background-color:#eee; padding:12px;"><b>'+ this.x +'</b>';
        var cumulative_amount = 0;
        for (var i = this.points.length - 1 ; i >= 0 ; i--) {
            cumulative_amount += this.points[i].y;
            if (this.points[i].y !== 0){
                s += '<br/><span style=\"color: ' + this.points[i].series.color + '; font-weight: bold;\">' + this.points[i].series.name +'</span>: ' + Intl.NumberFormat().format(cumulative_amount);
            }
        }
        s += '</div>';
        return s;
      }'''""",
      "shared": True,
      "backgroundColor": "#eee",
      "borderColor": "#bbb",
      "style": {
        "color": "black"
      },
      "useHTML": True
    },
    "plotOptions": {
      "series": {
        "borderColor": "#151515",
        "events": {
          "legendItemClick": "'''function() { return false; }'''"
        }
      },
      "bar": {
        "stacking": "normal",
        "dataLabels": {
          "enabled": False,
          "color": "'''(Highcharts.theme && Highcharts.theme.dataLabelsColor) || 'white''''"
        },
        "point": {
          "events": {
            "click": """'''function (event) {
                var chart = this.series.yAxis;
                chart.removePlotLine('helperLine');
                chart.addPlotLine({
                    value: this.stackY,
                    color: '#000',
                    width: 2,
                    id: 'helperLine',
                    zIndex: 5,
                    label: {
                      text: this.series.name + ' ' + this.category + ': ' + Intl.NumberFormat().format(this.stackY),
                      align: 'left',
                      verticalAlign: 'bottom',
                      rotation: 0,
                      y: -5
                    }
                });
              }'''"""
          }
        }
      }
    },
    "series": series
  }

  # write raw file
  with open( filename + "_raw.js", "w" ) as ofile:
    ofile.write( "Highcharts.chart('" + filename[10:] + "', \n" )
    json.dump( highcharts_data, ofile, indent=4, sort_keys=True )
    ofile.write( ");" )

  # create result file without quotes in inappropriate places
  with open( filename + "_raw.js", "r" ) as old:
    with open( filename + ".js", "w" ) as new:
      for line in old:
        # get rid of quotes for key ("key": "value")
        if "\":" in line:
          newline = line.split( "\":" )[ 0 ].replace( "\"", "" )
          line = newline + ":" + line.split("\":")[1]
        # get rid of quotes around our functions
        if "\"'''" in line or "'''\"" in line:
          newline = line.replace( "\"'''", "\\n" ).replace( "'''\"", "\\n" ).replace( "\\n", "" )
          new.write(newline)
        elif "\\\\u" in line:
          newline = line.replace( "\\\\u", "\\u" )
          new.write( newline )
        else:
          new.write( line )
  # delete raw file
  os.remove( filename + "_raw.js" )
  return True
