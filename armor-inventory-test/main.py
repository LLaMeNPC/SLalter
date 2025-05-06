person_armors = {
    "skyrim": { ## only two skyrim_0 gloves are better
        "head": {"name": "Elven Helmet", "armor": 14},
        "chest": {"name": "Ancient Falmer Cuirass", "armor": 38},
        "hands": {"name": "Nightingale Gloves", "armor": 10},
        "feet": {"name": "Ancient Falmer Boots", "armor": 11},
    },
    "generic": { ## only two skyrim_0 gloves are better
        "head": {"name": "Ironbark Helm", "armor": 14},
        "chest": {"name": "Tempered Iron Armor", "armor": 38},
        "hands": {"name": "Hide Gloves", "armor": 10},
        "feet": {"name": "Wyrmscale Boots", "armor": 11},
    },
}

shop_inventories = {
    "skyrim": [
        {"name": "Scaled Bracers", "armor": 9, "body_part": "hands"},
        {"name": "Deathbrand Gauntlets", "armor": 11, "body_part": "hands"},
        {"name": "Chitin Bracers", "armor": 8.5, "body_part": "hands"},
        {"name": "Glass Gauntlets", "armor": 11, "body_part": "hands"},
        {"name": "Steel armor", "armor": 31, "body_part": "chest"},
        {"name": "Fur Helmet", "armor": 11, "body_part": "head"},
        {"name": "Dragonscale Boots", "armor": 12, "body_part": "feet"},
    ],
    "generic": [
        {"name": "Bronzed Armguards", "armor": 9, "body_part": "hands"},
        {"name": "Duskwoven Gloves", "armor": 11, "body_part": "hands"},
        {"name": "Boneplated Bracers", "armor": 8.5, "body_part": "hands"},
        {"name": "Crystalsteel Gauntlets", "armor": 11, "body_part": "hands"},
        {"name": "Hardened Leather Cuirass", "armor": 31, "body_part": "chest"},
        {"name": "Wolffur Cap", "armor": 11, "body_part": "head"},
        {"name": "Skyhide Boots", "armor": 12, "body_part": "feet"},
    ],
}

formats = {
    "head": "a {body_part} on their head",
    "chest": "{body_part} on their chest",
    "hands": "{body_part}",
    "feet": "{body_part}",
}

person_wearing_format = "The person you are talking to is wearing {person_armor}."
shop_format = "You have in your shop: {shop_inventory}.\n\nYou are a Smith who sells armor. You are talking to a potential customer."
#tmp = "Do not use the numbers given"

def print_full_json_format(person_armor, shop_inventory):
    output = f"{person_wearing_format.format(person_armor = person_armor)}\n\n{shop_format.format(shop_inventory = shop_inventory)}"
    print(output.replace("\n","\\n"))

def print_simple_json_format(person_armor, shop_inventory):
    person_armor = {body_part: armor_info["name"] for body_part, armor_info in person_armor.items()} # simplify / remove armor points
    shop_inventory = [armor_info["name"] for armor_info in shop_inventory] # simplify to only name / remove armor points and body part

    output = f"{person_wearing_format.format(person_armor = person_armor)}\n\n{shop_format.format(shop_inventory = shop_inventory)}"
    print(output.replace("\n","\\n"))

def print_readable_format(person_armor, shop_inventory):
    person_armor = {body_part: armor_info["name"] for body_part, armor_info in person_armor.items()} # simplify / remove armor points
    person_armor = [formats[body_part].format(body_part=person_armor[body_part]) for body_part in person_armor.keys()]
    person_armor[-1] = f"and {person_armor[-1]}"
    person_armor = ", ".join(person_armor)

    shop_inventory = [armor_info["name"] for armor_info in shop_inventory] # simplify to only name / remove armor points and body part
    shop_inventory[-1] = f"and {shop_inventory[-1]}"
    shop_inventory = ", ".join(shop_inventory)

    output = f"{person_wearing_format.format(person_armor = person_armor)}\n\n{shop_format.format(shop_inventory = shop_inventory)}"
    print(output.replace("\n","\\n"))

def main():
    person_armor = person_armors["generic"]
    person_armor = {body_part: armor_info["name"] for body_part, armor_info in person_armor.items()} # simplify / remove armor points
    person_armor = [formats[body_part].format(body_part=person_armor[body_part]) for body_part in person_armor.keys()]
    person_armor[-1] = f"and {person_armor[-1]}"
    person_armor = ", ".join(person_armor)

    shop_inventory = shop_inventories["generic"]
    #shop_inventory = [{"name": armor_info["name"], "armor": armor_info["armor"]} for armor_info in shop_inventory] # remove body part
    shop_inventory = [armor_info["name"] for armor_info in shop_inventory] # simplify to only name / remove armor points and body part
    shop_inventory[-1] = f"and {shop_inventory[-1]}"
    shop_inventory = ", ".join(shop_inventory)

    output = f"{person_wearing_format.format(person_armor = person_armor)}\n\n{shop_format.format(shop_inventory = shop_inventory)}"

    #print(repr(output))
    print(output.replace("\n","\\n"))

if __name__ == "__main__":
    #main()
    print_readable_format(person_armors["skyrim"], shop_inventories["skyrim"])
