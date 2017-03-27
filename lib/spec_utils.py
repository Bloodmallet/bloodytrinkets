## Utility file for class specialisations
## Contains wow class names, spec names, dps talent rows

__classes_data = {
  "death_knight": {
    "talents": "1110011",
    "specs": {
      "frost":  { "role": "melee", "stat": "str" },
      "unholy": { "role": "melee", "stat": "str" }
    }
  },
  "demon_hunter": {
    "talents": "1110111",
    "specs": {
      "havoc": { "role": "melee", "stat": "agi" }
    }
  },
  "druid": {
    "talents": "1000111",
    "specs": { 
      "balance": { "role": "ranged", "stat": "int" },
      "feral":   { "role": "melee",  "stat": "agi" }
    }
  },
  "hunter": {
    "talents": "1101011",
    "specs": {
      "bm": { "role": "ranged", "stat": "agi" },
      "mm": { "role": "ranged", "stat": "agi" },
      "sv": { "role": "melee",  "stat": "agi" }
    }
  },
  "mage": {
    "talents": "1011011",
    "specs": {
      "arcane": { "role": "ranged", "stat": "int" },
      "fire":   { "role": "ranged", "stat": "int" },
      "frost":  { "role": "ranged", "stat": "int" }
    }
  },
  "monk": {
    "talents": "1010011",
    "specs": {
      "windwalker": { "role": "melee", "stat": "agi" }
    }
  },
  "paladin": {
    "talents": "1101001",
    "specs": {
      "retribution": { "role": "melee", "stat": "str" }
    }
  },
  "priest": {
    "talents": "1001111",
    "specs": {
      "shadow": { "role": "ranged", "stat": "int" }
    }
  },
  "rogue": {
    "talents": "1110111",
    "specs": {
      "assassination": { "role": "melee", "stat": "agi" },
      "outlaw":        { "role": "melee", "stat": "agi" },
      "subtlety":       { "role": "melee", "stat": "agi" }
    }
  },
  "shaman": {
    "talents": "1001111",
    "specs": {
      "elemental":   { "role": "ranged", "stat": "int" },
      "enhancement": { "role": "melee",  "stat": "agi" }
    }
  },
  "warlock": {
    "talents": "1101011",
    "specs": {
      "affliction":  { "role": "ranged", "stat": "int" },
      "demonology":  { "role": "ranged", "stat": "int" },
      "destruction": { "role": "ranged", "stat": "int" }
    }
  },
  "warrior": {
    "talents": "1010111",
    "specs": {
      "arms": { "role": "melee", "stat": "str" },
      "fury": { "role": "melee", "stat": "str" }
    }
  }
}


##
## @brief      Gets the wow classes.
##
## @return     The classes.
##
def get_classes():
  classes = []
  for wow_class in __classes_data:
    classes.append(wow_class)
  return classes

##
## @brief      Gets the role from class and spec.
##
## @param      wow_class  The class name as string
## @param      wow_spec   The specifier name as string
##
## @return     The role as string.
##
def get_role(wow_class, wow_spec):
  return __classes_data[wow_class]["specs"][wow_spec]["role"]


##
## @brief      Gets the main stat like agi, str or int.
##
## @param      wow_class  The class name as string
## @param      wow_spec   The specifier name as string
##
## @return     The main stat as string.
##
def get_stat(wow_class, wow_spec):
  return __classes_data[wow_class]["specs"][wow_spec]["stat"]


##
## @brief      Gets the dps talents. 0-no dps row, 1-dps row
##
## @param      wow_class  The class name
##
## @return     The dps talents as string.
##
def get_dps_talents(wow_class):
  return __classes_data[wow_class]["talents"]


##
## @brief      Gets the specs of a class.
##
## @param      wow_class  The class name
##
## @return     The specs as a list.
##
def get_specs(wow_class):
  spec_collection = []
  for spec in __classes_data[wow_class]["specs"]:
    spec_collection.append(spec)
  return spec_collection


##
## @brief      Determines if class is a wow class.
##
## @param      wow_class  The class name
##
## @return     True if class, False otherwise.
##
def is_class(wow_class):
  if wow_class in get_classes():
    return True
  else:
    return False


##
## @brief      Determines if specis of class.
##
## @param      wow_spec   The specifier name
##
## @return     True if spec exists in wow, False otherwise.
##
def is_spec(wow_spec):
  spec_list = []
  for wow_class in __classes_data:
    spec_list = spec_list + get_specs(wow_class)
  if wow_spec in spec_list:
    return True
  else:
    return False


##
#-------------------------------------------------------------------------------------
# Higher functions
#-------------------------------------------------------------------------------------
##


##
## @brief      Function for people who don't paying attention to parameters
##
## @param      wow_class  The class name
## @param      wow_spec   The spec name
##
## @return     The dps talents as string.
##
def get_dps_talents(wow_class, wow_spec):
  return get_dps_talents(wow_class)


##
## @brief      Gets the role and main stat.
##
## @param      wow_class  The class name as string
## @param      wow_spec   The specifier name as string
##
## @return     List of [role, main_stat]
##
def get_role_stat(wow_class, wow_spec):
  return [get_role(wow_class, wow_spec), get_stat(wow_class, wow_spec)]


##
## @brief      Gets the role, main_stat and dps_talent_rows.
##
## @param      wow_class  The wow class
## @param      wow_spec   The wow specifier
##
## @return     The specifier information.
##
def get_spec_info(wow_class, wow_spec):
 return [get_role(wow_class, wow_spec), get_stat(wow_class, wow_spec), get_dps_talents(wow_class)]


##
## @brief      Gets the main stat and role
##
## @param      wow_class  The class name as string
## @param      wow_spec   The specifier name as string
##
## @return     List of [main_stat, role]
##
def get_stat_role(wow_class, wow_spec):
  return [get_stat(wow_class, wow_spec), get_role(wow_class, wow_spec)]


##
## @brief      Determines if class and spec are correct and fit each other.
##
## @param      wow_class  The wow class
## @param      wow_spec   The wow specifier
##
## @return     True if class specifier, False otherwise.
##
def is_class_spec(wow_class, wow_spec):
  if is_class(wow_class):
    if is_spec(wow_spec):
      if wow_spec in get_specs(wow_class):
        return True
  return False


##
## @brief      Determines if dps talent combination fits data.
##
## @param      talent_combination  The talent combination
## @param      wow_class           The wow class
##
## @return     True if dps talent combination fits, False otherwise.
##
def is_dps_talent_combination(talent_combination, wow_class):
  for i in range(0, 7):
    if talent_combination[i] == "0" and __classes_data[wow_class]["talents"][i] == "1":
      return False
    elif not talent_combination[i] == "0" and __classes_data[wow_class]["talents"][i] == "0":
      return False
  return True


##
## @brief      Simple data check
##
## @return     True if data doesn't have obvious flaws, False otherwise.
##
def __validity_check():
  for wow_class in __classes_data:
    for spec in get_specs(wow_class):
      if (get_role(wow_class, wow_spec) == "ranged" and get_stat(wow_class, wow_spec) == "str") or (get_role(wow_class, wow_spec) == "melee" and get_stat(wow_class, wow_spec) == "int"):
        return False
  return True