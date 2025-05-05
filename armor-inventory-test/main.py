person_armors = {
    "skyrim_armor_0": {
        "head": "Scaled Helmet",
        "chest": "Leather armor",
        "hands": "Worn Shrouded Gloves",
        "feet": "Ancient Falmer Boots",
    },
    "other_armor_0": {
        "head": "Scaled Helmet",
        "chest": "Hardened Leather Cuirass",
        "hands": "Worn Shrouded Gloves",
        "feet": "Ancient Falmer Boots",
    },
}

shop_inventories = {
    "skyrim_0": ["Scaled Bracers", "Linwe's gloves", "Chitin Bracers", "Glass Gauntlets", "Steel armor", "Fur Helmet", "Dragonscale Boots"],
    "generic": ["Bronzed Armguards", "Duskwoven Gloves", "Boneplated Bracers", "Crystalsteel Gauntlets", "Tempered Iron Armor","Wolffur Cap", "Skyhide Boots"],
}

formats = {
    "head": "a {body_part} on their head",
    "chest": "{body_part} on their chest",
    "hands": "{body_part}",
    "feet": "{body_part}",
}

order = ["chest", "head", "feet", "hands"]

person_wearing_format = "You are in a medieval fanstasy setting. The person you are talking to is wearing {person_armor}."
shop_format = "You have in your shop: {shop_inventory}.\n\nYou are a Smith. You want to sell the person you are talking to some gear."

#def comma_and_and_join(list):
#    list[-1] = f"and {list[-1]}"
#    return ", ".join(list)

def main():
    person_armor = person_armors["skyrim_armor_0"]
    #person_armor = [formats[body_part].format(body_part=person_armor[body_part]) for body_part in person_armor.keys()]
    #person_armor[-1] = f"and {person_armor[-1]}"
    #person_armor = ", ".join(person_armor)

    shop_inventory = shop_inventories["skyrim_0"]
    #shop_inventory[-1] = f"and {shop_inventory[-1]}"
    #shop_inventory = ", ".join(shop_inventory)

    output = f"{person_wearing_format.format(person_armor = person_armor)}\n\n{shop_format.format(shop_inventory = shop_inventory)}"

    #print(repr(output))
    print(output.replace("\n","\\n"))

if __name__ == "__main__":
    main()
