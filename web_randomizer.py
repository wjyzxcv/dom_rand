import pandas as pd
import numpy as np
import sqlite3 as sq
from flask import Flask, render_template, request, url_for

app = Flask(__name__)

def pd_df2html(df):
    return df.to_html(classes=["table table-bordered table-striped table-hover"],index=False, justify = "center").replace('<tr>', '<tr align="center">')


def dom_ran(mode, expan="0", n_cards="2"):
    n_cards = int(n_cards)
    expan = int(expan)
    #load db
    sq_con = sq.connect("d_db.db")
    d_table = pd.read_sql('''
                          SELECT *
                          FROM d_table
                          ''', sq_con)  
    name_sets = pd.unique(d_table["Set"])
    df_name_sets = pd.DataFrame(name_sets)
    df_name_sets.columns = ["Set"]
    if mode == "a":
        n_req = n_cards
        return pd_df2html(pd.DataFrame(np.random.choice(name_sets, n_req, replace = False), columns=["Expansions"]))
    elif mode == "b":
        set_ind = expan
        set_name = df_name_sets.iloc[set_ind,0]
        l_cards = d_table[d_table["Set"] == set_name]["Name"]
        n_cards = n_cards
        return pd_df2html(l_cards.sample(n_cards).to_frame())
    elif mode == "c":
        event_table = pd.read_sql('''
                                SELECT *
                                FROM event_table
                                ''', sq_con)
        valid_exp = df_name_sets[df_name_sets["Set"].isin(["Empires", "Adventures", "Menagerie", "Promo"])]
        set_ind = expan
        set_name = df_name_sets.iloc[set_ind,0]
        l_events = event_table[event_table["Set"] == set_name]["Name"]
        l_events = l_events.to_frame()
        n_events = n_cards
        return pd_df2html(l_events.sample(n_events))
    elif mode == "d":
        lm_table = pd.read_sql('''
                                SELECT *
                                FROM lm_table
                                ''', sq_con)
        n_lms = n_cards
        return pd_df2html(lm_table["Name"].to_frame().sample(n_lms))
    elif mode == "e":
        pj_table = pd.read_sql('''
                                SELECT *
                                FROM pj_table
                                ''', sq_con)
        n_pjs = n_cards
        return pd_df2html(pj_table["Name"].to_frame().sample(n_pjs))
    elif mode == "f":
        way_table = pd.read_sql('''
                                SELECT *
                                FROM way_table
                                ''', sq_con)
        n_ways = n_cards
        return pd_df2html(way_table["Name"].to_frame().sample(n_ways))
    elif mode == "g":
        ally_table = pd.read_sql('''
                                SELECT *
                                FROM ally_table
                                ''', sq_con)
        n_allies = n_cards
        return pd_df2html(ally_table["Name"].to_frame().sample(n_allies))
    elif mode == "ini":
        return df_name_sets["Set"].to_list()

@app.route('/', methods=["POST", "GET"])
def index():
    expan_list = dom_ran("ini")
    if request.method == "POST":
        inputs_mode = request.form["mode"]
        inputs_expan = request.form["expan"]
        inputs_n_cards = request.form["n_cards"]
        try:
            output_table = dom_ran(inputs_mode, inputs_expan, inputs_n_cards)
            outputs = ""
        except Exception as e:
            output_table = ""
            # outputs = e
            outputs = "Please input a number"
        return render_template("index.html", output_table = output_table, outputs = outputs, expan_list = expan_list)
    else:
        return render_template("index.html", output_table = "", outputs = "Welcome to my crappy Dominion Randomizer!", expan_list = expan_list)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)