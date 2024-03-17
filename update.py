import pandas as pd

import sqlite3 as sq

# %% get card info and clean up
d_tables = pd.read_html("https://wiki.dominionstrategy.com/index.php/List_of_cards")
d_table = d_tables[0]
d_table = d_table.iloc[:, :5]
# remove 1E cards
d_table = d_table[~d_table["Set"].str.contains("1E")]
d_table["Set"] = d_table["Set"].str.rstrip(", 2E")
# make tables for event, landmark, project, ways, boon, and hex
event_table = d_table[d_table["Types"] == "Event"]
event_table.reset_index(drop=True, inplace=True)
d_table = d_table[~(d_table["Types"] == "Event")]
lm_table = d_table[d_table["Types"] == "Landmark"]
lm_table.reset_index(drop=True, inplace=True)
d_table = d_table[~(d_table["Types"] == "Landmark")]
pj_table = d_table[d_table["Types"] == "Project"]
pj_table.reset_index(drop=True, inplace=True)
d_table = d_table[~(d_table["Types"] == "Project")]
way_table = d_table[d_table["Types"] == "Way"]
way_table.reset_index(drop=True, inplace=True)
d_table = d_table[~(d_table["Types"] == "Way")]
boon_table = d_table[d_table["Types"] == "Boon"]
boon_table.reset_index(drop=True, inplace=True)
d_table = d_table[~(d_table["Types"] == "Boon")]
hex_table = d_table[d_table["Types"] == "Hex"]
hex_table.reset_index(drop=True, inplace=True)
d_table = d_table[~(d_table["Types"] == "Hex")]
ally_table = d_table[d_table["Types"] == "Ally"]
ally_table.reset_index(drop=True, inplace=True)
d_table = d_table[~(d_table["Types"] == "Ally")]
trait_table = d_table[d_table["Types"] == "Trait"]
trait_table.reset_index(drop=True, inplace=True)
d_table = d_table[~(d_table["Types"] == "Trait")]
# filter out cards
d_table = d_table[
    ~d_table["Name"].isin(
        [
            "Plunder",
            "Emporium",
            "Bustling Village",
            "Rocks",
            "Fortune",
            "Avanto",
            "Copper",
            "Silver",
            "Potion",
            "Gold",
            "Platinum",
            "Estate",
            "Duchy",
            "Province",
            "Curse",
            "Colony",
        ]
    )
]
d_table = d_table[
    ~d_table["Types"].str.contains(
        "Prize|Ruins|Shelter|Heirloom|Castle|Knight|Artifact|Zombie|Townsfolk|Augur|Odyssey|Wizard|Fort|Clash|Loot|State"
    )
]
d_table = d_table[~d_table["Text"].str.contains("This is not in the Supply.")]
#.append depreciated
# d_table.append(["Castle", "Empires", "Victory", "NaN", "NaN"])
# d_table.append(["Knight", "Dark Ages", "Action", "NaN", "NaN"])
# d_table.append(["Townsfolk", "Allies", "Action", "NaN", "NaN"])
# d_table.append(["Augur", "Allies", "Action", "NaN", "NaN"])
# d_table.append(["Odyssey", "Allies", "Action", "NaN", "NaN"])
# d_table.append(["Wizard", "Allies", "Action", "NaN", "NaN"])
# d_table.append(["Fort", "Allies", "Action", "NaN", "NaN"])
# d_table.append(["Clash", "Allies", "Action", "NaN", "NaN"])
d_table = pd.concat([d_table, pd.DataFrame({"Name":"Castle", "Set":"Empires", "Types":"Victory", "Cost":"NaN", "Text":"NaN"}, index=[0])])
d_table = pd.concat([d_table, pd.DataFrame({"Name":"Knight", "Set":"Dark Ages", "Types":"Action", "Cost":"NaN", "Text":"NaN"}, index=[0])])
d_table = pd.concat([d_table, pd.DataFrame({"Name":"Townsfolk", "Set":"Allies", "Types":"Action", "Cost":"NaN", "Text":"NaN"}, index=[0])])
d_table = pd.concat([d_table, pd.DataFrame({"Name":"Augur", "Set":"Allies", "Types":"Action", "Cost":"NaN", "Text":"NaN"}, index=[0])])
d_table = pd.concat([d_table, pd.DataFrame({"Name":"Odyssey", "Set":"Allies", "Types":"Action", "Cost":"NaN","Text":"NaN"}, index=[0])])
d_table = pd.concat([d_table, pd.DataFrame({"Name":"Wizard", "Set":"Allies", "Types":"Action", "Cost":"NaN", "Text":"NaN"}, index=[0])])
d_table = pd.concat([d_table, pd.DataFrame({"Name":"Fort", "Set":"Allies", "Types":"Action", "Cost":"NaN", "Text":"NaN"}, index=[0])])
d_table = pd.concat([d_table, pd.DataFrame({"Name":"Clash", "Set":"Allies", "Types":"Action", "Cost":"NaN", "Text":"NaN"}, index=[0])])
d_table.reset_index(drop=True, inplace=True)


# %% save table to db
sq_con = sq.connect("d_db.db")
d_table.to_sql("d_table", sq_con, if_exists="replace")
event_table.to_sql("event_table", sq_con, if_exists="replace")
lm_table.to_sql("lm_table", sq_con, if_exists="replace")
pj_table.to_sql("pj_table", sq_con, if_exists="replace")
way_table.to_sql("way_table", sq_con, if_exists="replace")
boon_table.to_sql("boon_table", sq_con, if_exists="replace")
hex_table.to_sql("hex_table", sq_con, if_exists="replace")
ally_table.to_sql("ally_table", sq_con, if_exists="replace")
trait_table.to_sql("trait_table", sq_con, if_exists="replace")

# %% test
r_table = pd.read_sql(
    """
                      SELECT *
                      FROM d_table
                      """,
    sq_con,
)
