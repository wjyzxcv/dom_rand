# import atexit
import pandas as pd
import numpy as np
import sqlite3 as sq

def cus_inp(mes, var_type, var_cond):
    output = None
    while output is None:
        print(mes)
        try:
            output = input()
            output = var_type(output)
            if not var_cond(output):
                raise ValueError()
        except ValueError:
            output = None
            print("Invalid input \n")
    return output

def main():
    #load db
    sq_con = sq.connect("d_db.db")
    d_table = pd.read_sql('''
                          SELECT *
                          FROM d_table
                          ''', sq_con)
    name_sets = pd.unique(d_table["Set"])
    n_sets = len(name_sets)
    df_name_sets = pd.DataFrame(name_sets)
    df_name_sets.columns = ["Set"]
    print("Available expansions: ")
    print(df_name_sets)
    mode = None
    while not mode == 'q':
        mode = cus_inp(
            "\n Select mode: \n a. Expansion \n b. Card \n c. Event \n d. Landmark \n e. Project \n f. Ways \n g. Allies \n l. list of expansions \n q. Quit",
            lambda x: x,
            lambda x: x in "abcdefgql"
            )
        if mode == "a":
            n_req = cus_inp(
                "\n Number of expansions: ",
                int,
                lambda x: x > 0 and x <= n_sets
                )
            print(np.random.choice(name_sets, n_req, replace = False))
        elif mode == "b":
            set_ind = cus_inp(
                "\n Index of expansion: ",
                int,
                lambda x: x in range(n_sets)
                )
            set_name = df_name_sets.iloc[set_ind,0]
            l_cards = d_table[d_table["Set"] == set_name]["Name"]
            n_cards = cus_inp(
                "\n Number of cards: ",
                int,
                lambda x: x > 0 and x <= len(l_cards)
                )
            print(l_cards.sample(n_cards).to_string())
        elif mode == "c":
            event_table = pd.read_sql('''
                                  SELECT *
                                  FROM event_table
                                  ''', sq_con)
            valid_exp = df_name_sets[df_name_sets["Set"].isin(["Empires", "Adventures", "Menagerie", "Promo"])]
            print("\n Valid Expansions: ")
            print(valid_exp.to_string())
            set_ind = cus_inp(
                "\n Index of expansion: ",
                int,
                lambda x: x in valid_exp.index
                )
            set_name = df_name_sets.iloc[set_ind,0]
            l_events = event_table[event_table["Set"] == set_name]["Name"]
            n_events = cus_inp(
                "\n Number of events: ",
                int,
                lambda x: x > 0 and x <= 2
                )
            print(l_events.sample(n_events).to_string())
        elif mode == "d":
            lm_table = pd.read_sql('''
                                  SELECT *
                                  FROM lm_table
                                  ''', sq_con)
            n_lms = cus_inp(
                "\n Number of landmarks: ",
                int,
                lambda x: x > 0 and x <= 2
                )
            print(lm_table["Name"].sample(n_lms).to_string())
        elif mode == "e":
            pj_table = pd.read_sql('''
                                  SELECT *
                                  FROM pj_table
                                  ''', sq_con)
            n_pjs = cus_inp(
                "\n Number of projects: ",
                int,
                lambda x: x > 0 and x <= 2
                )
            print(pj_table["Name"].sample(n_pjs).to_string())
        elif mode == "f":
            way_table = pd.read_sql('''
                                  SELECT *
                                  FROM way_table
                                  ''', sq_con)
            n_ways = cus_inp(
                "\n Number of ways: ",
                int,
                lambda x: x > 0 and x <= 2
                )
            print(way_table["Name"].sample(n_ways).to_string())
        elif mode == "l":
            print("Available expansions: ")
            print(df_name_sets)
        elif mode == "g":
            ally_table = pd.read_sql('''
                                  SELECT *
                                  FROM ally_table
                                  ''', sq_con)
            n_allies = cus_inp(
                "\n Number of Allies: ",
                int,
                lambda x: x > 0 and x <= 2
                )
            print(ally_table["Name"].sample(n_allies).to_string())
            
if __name__ == '__main__':
    main()