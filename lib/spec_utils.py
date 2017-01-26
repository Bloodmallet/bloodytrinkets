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
      "sublety":       { "role": "melee", "stat": "agi" }
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
## @brief      Gets the role from class and spec.
##
## @param      class_name  The class name as string
## @param      spec_name   The specifier name as string
##
## @return     The role as string.
##
def get_role(class_name, spec_name):
  return __classes_data[class_name]["specs"][spec_name]["role"]


##
## @brief      Gets the main stat like agi, str or int.
##
## @param      class_name  The class name as string
## @param      spec_name   The specifier name as string
##
## @return     The main stat as string.
##
def get_stat(class_name, spec_name):
  return __classes_data[class_name]["specs"][spec_name]["stat"]


##
## @brief      Gets the dps talents. 0-no dps row, 1-dps row
##
## @param      class_name  The class name
##
## @return     The dps talents as string.
##
def get_dps_talents(class_name):
  return __classes_data[class_name]["talents"]


##
## @brief      Gets the specs of a class.
##
## @param      class_name  The class name
##
## @return     The specs as a list.
##
def get_specs(class_name):
  return __classes_data[class_name]["specs"].keys()


##
## @brief      Determines if class is a wow class.
##
## @param      class_name  The class name
##
## @return     True if class, False otherwise.
##
def is_class(class_name):
  if class_name in __classes_data.keys():
    return True
  else:
    return False


##
## @brief      Determines if specis of class.
##
## @param      class_name  The class name
## @param      spec_name   The specifier name
##
## @return     True if spec is of the provided class, False otherwise.
##
def is_spec(class_name, spec_name):
  if spec_name in __classes_data[class_name]["specs"].keys():
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
## @param      class_name  The class name
## @param      spec_name   The spec name
##
## @return     The dps talents as string.
##
def get_dps_talents(class_name, spec_name):
  return get_dps_talents(class_name)

##
## @brief      Gets the role and main stat
##
## @param      class_name  The class name as string
## @param      spec_name   The specifier name as string
##
## @return     list of [role, main_stat]
##
def get_spec_info(class_name, spec_name):
  return [get_role(class_name, spec_name), get_stat(class_name, spec_name)]


##
## @brief      Simple data check
##
## @return     True if data doesn't have obvious flaws, False otherwise.
##
def __validity_check():
  for wow_class in __classes_data:
    for spec in __classes_data[wow_class]["specs"]:
      if (__classes_data[wow_class]["specs"][spec]["role"] == "ranged" and __classes_data[wow_class]["specs"][spec]["stat"] == "str") or (__classes_data[wow_class]["specs"][spec]["role"] == "melee" and __classes_data[wow_class]["specs"][spec]["stat"] == "int"):
        return False
  return True