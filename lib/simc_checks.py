## Lib to check simc_options input values


##
## @brief      Gets all fight styles.
##
## @return     The fight styles.
##
def get_fight_styles():
  return (
    "patchwerk",
    "lightmovement", 
    "heavymovement", 
    "hecticaddcleave", 
    "beastlord", 
    "helterskelter" )

##
## @brief      Validates the input fight styles.
##
## @param      fight_styles  The fight style like in SimC options
##
## @return     True if fight_style matches predetermined SimC-styles
##
def is_fight_style(fight_styles):
  fight_style_list = get_fight_styles()
  for fight_style in fight_styles:
    if not type(fight_style) is str:
      return False
    if not fight_style.lower() in fight_style_list:
      return False
  return True


##
## @brief      Determines if iteration is a number as a string and greater than
##             5000.
##
## @param      iterations  The iterations
##
## @return     True if iterations is string and greater than 5000, False
##             otherwise.
##
def is_iteration(iterations):
  if type(iterations) is str:
    if int(iterations) > 5000:
      return True
  return False


##
## @brief      Determines if target error is string and < 0.5 and >= 0.0.
##
## @param      target_error  The target error
##
## @return     True if target error is string and < 0.5 and >= 0.0, False
##             otherwise.
##
def is_target_error(target_error):
  if type(target_error) is str:
    if 0.5 > float(target_error) >= 0.0:
      return True
  return False
