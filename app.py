from flask import Flask, request, jsonify, render_template, send_file, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
import psycopg2
import re # regular expression
import logging
import csv
import pandas as pd
import random
# import requests # - use from flask import request
#from bokeh.plotting import figure
from bokeh.io import output_notebook, show, output_file
from bokeh.models import ColumnDataSource, HoverTool, Panel
from bokeh.models.widgets import Tabs

from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import file_html
from bokeh.embed import components

import numpy as np

app = Flask(__name__)

ENV = 'prod'

if ENV == 'dev': # for development
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:rewed23@localhost/premier_data" # local database which will hold all the tables
else: # for production
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://vaefvairxwnwzt:0a8da5b9a3953661db4fe3b888a682b1cec025d243d9f561291fc639649bd81a@ec2-34-206-252-187.compute-1.amazonaws.com:5432/d768c1mpisndrk" # for production taken from "heroku config --app <appname>"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)

# Product Class/Model with fields
class Player_Averages(db.Model): #SQLAlchemy.Model
    id = db.Column(db.Integer, primary_key=True) # id will automatically be included without needing to be specified in POST 
    Player = db.Column(db.String(200)) # unique=True
    Team = db.Column(db.String(200))
    Games = db.Column(db.Integer)
    One_Percenters = db.Column(db.Float)
    _50_Penalty = db.Column(db.Float)
    B50_Tackle_Eff = db.Column(db.Float)
    B50_Tackle_Ineff = db.Column(db.Float)
    Blocks = db.Column(db.Float)
    Chase = db.Column(db.Float)
    CL_Ball_Up = db.Column(db.Float)
    CL_Centre = db.Column(db.Float)
    CL_Throw_Ins = db.Column(db.Float)
    Deep_50_Entry = db.Column(db.Float)
    Deep_50_Mark = db.Column(db.Float)
    Deep_50_Rebound = db.Column(db.Float)
    Deep_Inside_50 = db.Column(db.Float)
    Disp_Count = db.Column(db.Float)
    Eff_Tack = db.Column(db.Float)
    F50_Tackle_Eff = db.Column(db.Float)
    F50_Tackle_Ineff = db.Column(db.Float)
    FP = db.Column(db.Float)
    Free_Against = db.Column(db.Float)
    Free_For = db.Column(db.Float)
    Handball_Eff = db.Column(db.Float)
    Handball_Ineff = db.Column(db.Float)
    Handball_Receive = db.Column(db.Float)
    Hard_Ball_Get = db.Column(db.Float)
    Hit_Out = db.Column(db.Float)
    Hit_Out_To_Advant = db.Column(db.Float)
    Ineff_Tack = db.Column(db.Float)
    Intercept_Mark = db.Column(db.Float)
    Intercept_Pos = db.Column(db.Float)
    Kick_Eff = db.Column(db.Float)
    Kick_Ineff = db.Column(db.Float)
    Loose_Ball_Get = db.Column(db.Float)
    Mark_Cont = db.Column(db.Float)
    Mark_Uncont = db.Column(db.Float)
    Mid_Tackle_Eff = db.Column(db.Float)
    Mid_Tackle_Ineff = db.Column(db.Float)
    Out_Of_Bounds = db.Column(db.Float)
    Pos_Cont = db.Column(db.Float)
    Score_Behind = db.Column(db.Float)
    Score_Goal = db.Column(db.Float)
    Score_Rush_Behind = db.Column(db.Float)
    Shallow_50 = db.Column(db.Float)
    Shallow_50_Mark = db.Column(db.Float)
    Shallow_50_Rebound = db.Column(db.Float)
    Shallow_Inside_50 = db.Column(db.Float)
    Shallow_Rebound = db.Column(db.Float)
    Smother = db.Column(db.Float)
    Spoil = db.Column(db.Float)
    Turnover_BCK = db.Column(db.Float)
    Turnover_FWD = db.Column(db.Float)
    Turnover_MID = db.Column(db.Float)


    def __init__(self, Player, Team, Games, One_Percenters, _50_Penalty, B50_Tackle_Eff, B50_Tackle_Ineff, Blocks, Chase, CL_Ball_Up, CL_Centre, CL_Throw_Ins, Deep_50_Entry, Deep_50_Mark, Deep_50_Rebound, Deep_Inside_50, Disp_Count, Eff_Tack, F50_Tackle_Eff, F50_Tackle_Ineff, FP, Free_Against, Free_For, Handball_Eff, Handball_Ineff, Handball_Receive, Hard_Ball_Get, Hit_Out, Hit_Out_To_Advant, Ineff_Tack, Intercept_Mark, Intercept_Pos, Kick_Eff, Kick_Ineff, Loose_Ball_Get, Mark_Cont, Mark_Uncont, Mid_Tackle_Eff, Mid_Tackle_Ineff, Out_Of_Bounds, Pos_Cont, Score_Behind, Score_Goal, Score_Rush_Behind, Shallow_50, Shallow_50_Mark, Shallow_50_Rebound, Shallow_Inside_50, Shallow_Rebound, Smother, Spoil, Turnover_BCK, Turnover_FWD, Turnover_MID):
        self.Player = Player
        self.Team = Team
        self.Games = Games
        self.One_Percenters = One_Percenters
        self._50_Penalty = _50_Penalty
        self.B50_Tackle_Eff = B50_Tackle_Eff
        self.B50_Tackle_Ineff = B50_Tackle_Ineff
        self.Blocks = Blocks
        self.Chase = Chase
        self.CL_Ball_Up = CL_Ball_Up
        self.CL_Centre = CL_Centre
        self.CL_Throw_Ins = CL_Throw_Ins
        self.Deep_50_Entry = Deep_50_Entry
        self.Deep_50_Mark = Deep_50_Mark
        self.Deep_50_Rebound = Deep_50_Rebound
        self.Deep_Inside_50 = Deep_Inside_50
        self.Disp_Count = Disp_Count
        self.Eff_Tack = Eff_Tack
        self.F50_Tackle_Eff = F50_Tackle_Eff
        self.F50_Tackle_Ineff = F50_Tackle_Ineff
        self.FP = FP
        self.Free_Against = Free_Against
        self.Free_For = Free_For
        self.Handball_Eff = Handball_Eff
        self.Handball_Ineff = Handball_Ineff
        self.Handball_Receive = Handball_Receive
        self.Hard_Ball_Get = Hard_Ball_Get
        self.Hit_Out = Hit_Out
        self.Hit_Out_To_Advant = Hit_Out_To_Advant
        self.Ineff_Tack = Ineff_Tack
        self.Intercept_Mark = Intercept_Mark
        self.Intercept_Pos = Intercept_Pos
        self.Kick_Eff = Kick_Eff
        self.Kick_Ineff = Kick_Ineff
        self.Loose_Ball_Get = Loose_Ball_Get
        self.Mark_Cont = Mark_Cont
        self.Mark_Uncont = Mark_Uncont
        self.Mid_Tackle_Eff = Mid_Tackle_Eff
        self.Mid_Tackle_Ineff = Mid_Tackle_Ineff
        self.Out_Of_Bounds = Out_Of_Bounds
        self.Pos_Cont = Pos_Cont
        self.Score_Behind = Score_Behind
        self.Score_Goal = Score_Goal
        self.Score_Rush_Behind = Score_Rush_Behind
        self.Shallow_50 = Shallow_50
        self.Shallow_50_Mark = Shallow_50_Mark
        self.Shallow_50_Rebound = Shallow_50_Rebound
        self.Shallow_Inside_50 = Shallow_Inside_50
        self.Shallow_Rebound = Shallow_Rebound
        self.Smother = Smother
        self.Spoil = Spoil
        self.Turnover_BCK = Turnover_BCK
        self.Turnover_FWD = Turnover_FWD
        self.Turnover_MID = Turnover_MID
        

# what we want to show from get requests?
class Player_Averages_Schema(ma.Schema): #Marshmallow.Schema
    class Meta:
        fields = ('id', 'Player', 'Team', 'Games', 'One_Percenters', '_50_Penalty', 'B50_Tackle_Eff', 'B50_Tackle_Ineff', 'Blocks', 'Chase', 'CL_Ball_Up', 'CL_Centre', 'CL_Throw_Ins', 'Deep_50_Entry', 'Deep_50_Mark', 'Deep_50_Rebound', 'Deep_Inside_50', 'Disp_Count', 'Eff_Tack', 'F50_Tackle_Eff', 'F50_Tackle_Ineff', 'FP', 'Free_Against', 'Free_For', 'Handball_Eff', 'Handball_Ineff', 'Handball_Receive', 'Hard_Ball_Get', 'Hit_Out', 'Hit_Out_To_Advant', 'Ineff_Tack', 'Intercept_Mark', 'Intercept_Pos', 'Kick_Eff', 'Kick_Ineff', 'Loose_Ball_Get', 'Mark_Cont', 'Mark_Uncont', 'Mid_Tackle_Eff', 'Mid_Tackle_Ineff', 'Out_Of_Bounds', 'Pos_Cont', 'Score_Behind', 'Score_Goal', 'Score_Rush_Behind', 'Shallow_50', 'Shallow_50_Mark', 'Shallow_50_Rebound', 'Shallow_Inside_50', 'Shallow_Rebound', 'Smother', 'Spoil', 'Turnover_BCK', 'Turnover_FWD', 'Turnover_MID')

# Product schema
player_average_schema = Player_Averages_Schema(many=False) #strict=True
players_average_schema = Player_Averages_Schema(many=True) #strict=True


# logging
# create and configure logger
LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename = "log.log", 
                    level=logging.DEBUG, 
                    format=LOG_FORMAT) 
logger = logging.getLogger() # logger without a name (root logger)
print(logger.level)


def hist_hover(dataframe, column, colors=["SteelBlue", "Tan"], bins=30, log_scale=False, show_plot=False):

    # build histogram data with Numpy
    hist, edges = np.histogram(dataframe[column], bins = bins)
    hist_df = pd.DataFrame({column: hist,
                            "left": edges[:-1],
                            "right": edges[1:]})
    hist_df["interval"] = ["%d to %d" % (left, right) for left, 
                        right in zip(hist_df["left"], hist_df["right"])]

    # bokeh histogram with hover tool
    if log_scale == True:
        hist_df["log"] = np.log(hist_df[column])
        src = ColumnDataSource(hist_df)
        plot = figure(plot_height = 600, plot_width = 600,
            title = "Histogram of {}".format(column.capitalize()),
            x_axis_label = column.capitalize(),
            y_axis_label = "Log Count")    
        plot.quad(bottom = 0, top = "log",left = "left", 
            right = "right", source = src, fill_color = colors[0], 
            line_color = "black", fill_alpha = 0.7,
            hover_fill_alpha = 1.0, hover_fill_color = colors[1])
    else:
        src = ColumnDataSource(hist_df)
        
        plot = figure(plot_height = 600, plot_width = 600,
            title = "Histogram of {}".format(column.capitalize()),
            x_axis_label = column.capitalize(),
            y_axis_label = "Count")    
        plot.quad(bottom = 0, top = column,left = "left", 
            right = "right", source = src, fill_color = colors[0], 
            line_color = "black", fill_alpha = 0.7,
            hover_fill_alpha = 1.0, hover_fill_color = colors[1])
    # hover tool
    hover = HoverTool(tooltips = [('Interval', '@interval'),
                            ('Count', str("@" + column))])
    plot.add_tools(hover)
    # output
    if show_plot == True:
        show(plot)
    else:
        return plot


def histotabs(dataframe, features, log_scale=False, show_plot=False):
    hists = []
    for f in features:
        h = hist_hover(dataframe, f, log_scale=log_scale, show_plot=show_plot)
        p = Panel(child=h, title=f.capitalize())
        hists.append(p)
    t = Tabs(tabs=hists)
    return t




# get all player averages
@app.route('/players_averages', methods=['GET'])
def get_players_averages():
    logger.info("get_players_averages()")
    all_players_averages = Player_Averages.query.all() 
    result = players_average_schema.dump(all_players_averages) # ma schema


    # loop to change float to 2 decimal places
    for dict_value in result:
        for k, v in dict_value.items():
            # error handling because not all columns are numbers such as 'player', 'teams', 'games'
            try:
                dict_value[k] = float(str(v)[:4])
            except:
                continue

    # TODO - order dictionary by list values
    #L = ['Player', 'Team', 'Games', 'One_Percenters', '_50_Penalty', 'B50_Tackle_Eff', 'B50_Tackle_Ineff', 'Blocks', 'Chase', 'CL_Ball_Up', 'CL_Centre', 'CL_Throw_Ins', 'Deep_50_Entry', 'Deep_50_Mark', 'Deep_50_Rebound', 'Deep_Inside_50', 'Disp_Count', 'Eff_Tack', 'F50_Tackle_Eff', 'F50_Tackle_Ineff', 'FP', 'Free_Against', 'Free_For', 'Handball_Eff', 'Handball_Ineff', 'Handball_Receive', 'Hard_Ball_Get', 'Hit_Out', 'Hit_Out_To_Advant', 'Ineff_Tack', 'Intercept_Mark', 'Intercept_Pos', 'Kick_Eff', 'Kick_Ineff', 'Loose_Ball_Get', 'Mark_Cont', 'Mark_Uncont', 'Mid_Tackle_Eff', 'Mid_Tackle_Ineff', 'Out_Of_Bounds', 'Pos_Cont', 'Score_Behind', 'Score_Goal', 'Score_Rush_Behind', 'Shallow_50', 'Shallow_50_Mark', 'Shallow_50_Rebound', 'Shallow_Inside_50', 'Shallow_Rebound', 'Smother', 'Spoil', 'Turnover_BCK', 'Turnover_FWD', 'Turnover_MID']            
    
    df = pd.DataFrame(result) # convert to dataframe

    df = df[['Player', 'Team', 'Games', 'One_Percenters', '_50_Penalty', 'B50_Tackle_Eff', 'B50_Tackle_Ineff', 'Blocks', 'Chase', 'CL_Ball_Up', 'CL_Centre', 'CL_Throw_Ins', 'Deep_50_Entry', 'Deep_50_Mark', 'Deep_50_Rebound', 'Deep_Inside_50', 'Disp_Count', 'Eff_Tack', 'F50_Tackle_Eff', 'F50_Tackle_Ineff', 'FP', 'Free_Against', 'Free_For', 'Handball_Eff', 'Handball_Ineff', 'Handball_Receive', 'Hard_Ball_Get', 'Hit_Out', 'Hit_Out_To_Advant', 'Ineff_Tack', 'Intercept_Mark', 'Intercept_Pos', 'Kick_Eff', 'Kick_Ineff', 'Loose_Ball_Get', 'Mark_Cont', 'Mark_Uncont', 'Mid_Tackle_Eff', 'Mid_Tackle_Ineff', 'Out_Of_Bounds', 'Pos_Cont', 'Score_Behind', 'Score_Goal', 'Score_Rush_Behind', 'Shallow_50', 'Shallow_50_Mark', 'Shallow_50_Rebound', 'Shallow_Inside_50', 'Shallow_Rebound', 'Smother', 'Spoil', 'Turnover_BCK', 'Turnover_FWD', 'Turnover_MID']]
    
    result = df.to_dict('records') # convert back to list of dictionaries
    
    print(result[0])
    return result # no need for result.data # no need for jsonify(result) because being used in python

# get single player
@app.route('/player_averages/<id>', methods=['GET'])
def get_player_averages(id):
    player_averages = Player_Averages.query.get(id) 
    return player_average_schema.jsonify(player_averages)

# export csv
@app.route('/export_csv', methods=['GET'])
def export_csv():
    players = get_players_averages()

    keys = players[0].keys()
    with open('player_averages.csv', 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(players)


    return send_file('player_averages.csv',
                     mimetype='text/csv',
                     attachment_filename='GNFL_player_averags.csv',
                     as_attachment=True)

    
    

@app.route('/', methods=['GET'])
def index():
    print('hello')
    players = get_players_averages()
    #sortedKeysAlphabetically=sorted(players[0].keys(), key=lambda x:x.lower())
    
    player_names = []
    for player in players:
        player_names.append(player['Player'])

    player1 = players[0]
    player2 = players[1]

    df = pd.read_csv("player_averages.csv")
    numeric_columns = list(df.columns)[2:] # excludes player and team columns
    script, div = components(histotabs(df.fillna(0, axis=1), numeric_columns, log_scale=False))
    #plot = file_html(plot, CDN, "my plot") This is for rendering whole html webpage app instead of speicfic script and div component

    return render_template('index.html', players = players, player_names = player_names, player1 = player1, player2 = player2, script = script, div = div)

@app.route('/comparison', methods=['GET']) # @app.route('/comparison', methods=['GET'])
def compare_players():
    player1_name = request.args.get('Player1') 
    player2_name = request.args.get('Player2')
    print(player1_name)
    print(player2_name)


    players = get_players_averages()
    
    player_names = []
    for player in players:
        player_names.append(player['Player'])
    

    if player1_name == "Player1":
        player1_name = random.choice(player_names)
    if player2_name == "Player2":
        player2_name = random.choice(player_names)



    for player in players:
        if player['Player'] == player1_name:
            player1_data = player
        if player['Player'] == player2_name:
            player2_data = player
   
   #url_for(contact) + '/#name_of_anchor_tag'
    #return redirect(url_for())

    df = pd.read_csv("player_averages.csv")
    numeric_columns = list(df.columns)[2:] # excludes player and team columns
    script, div = components(histotabs(df.fillna(0, axis=1), numeric_columns, log_scale=False))
    #plot = file_html(plot, CDN, "my plot") This is for rendering whole html webpage app instead of speicfic script and div component

    player_1_and_2_data = zip(player1_data, player2_data)
    return render_template('index.html', players = players, player_names = player_names, player1_data = player1_data, player2_data = player2_data, player_1_and_2_data = player_1_and_2_data, script = script, div = div, scrollToAnchor='comparison')


if __name__ == "__main__":
    app.run(debug=True, port=5000) # Running a Flask app in debug mode may allow an attacker to run arbitrary code through the Werkzeug debugger.