# Utility file for class specialisations

spec_roles = {	
	"Death Knight": {
		"Frost": {
			"role": "melee",
			"stat": "str"
		},
		"Unholy": {
			"role": "melee",
			"stat": "str"
		}
	},
	"Demon Hunter": {
		"Havoc": {
			"role": "melee",
			"stat": "agi"
		}
	},
	"Druid": {
		"Feral": {
			"role": "melee",
			"stat": "agi"
		},
		"Balance": {
			"role": "ranged",
			"stat": "int"
		}
	},
	"Hunter": {
		"Beast Mastery": {
			"role": "ranged",
			"stat": "agi"
		},
		"Marksmanship": {
				"role": "ranged",
				"stat": "agi"
		},
		"Survival": {
				"role": "melee",
				"stat": "agi"
		}
	},
	"Mage": {
		"Arcane": {
				"role": "ranged",
				"stat": "int"
		},
		"Fire": {
				"role": "ranged",
				"stat": "int"
		},
		"Frost": {
				"role": "ranged",
				"stat": "int"
		}
	},
	"Monk": {
		"Windwalker": {
				"role": "melee",
				"stat": "agi"
		}
	},
	"Paladin": {
		"Retribution": {
				"role": "melee",
				"stat": "str"
		}
	},
	"Priest": {
		"Shadow": {
				"role": "ranged",
				"stat": "int"
		}
	}
}

def get_spec_info(class_name, spec_name):
	return spec_roles[class_name,spec_name]