import pulp
import pandas as pd

def select_dream_team(players_df):    
    # Add 10 points to Fielders
    fielding_players = {
        ("Virat Kohli", "IND"),
        ("Ravindra Jadeja", "IND"),
        ("Hardik Pandya", "IND"),
        ("Shubman Gill", "IND"),
        ("Glenn Maxwell", "AUS"),
        ("Travis Head", "AUS"),
        ("Rashid-Khan", "AFG"),
        ("Aiden Markram", "SA"),
        ("Mitchell Santner", "NZ"),
        ("Rachin Ravindra", "NZ"),
        ("Glenn Phillips", "NZ"),
        
    }

    # Define weak countries as a list
    restricted_countries = ["AFG", "BAN"]

    # Add 10 points to WK
    players_df.loc[players_df["Player Type"] == "WK", "Fantasy_Score"] += 10
    
    # Boost Fantasy Score for specific players
    players_df.loc[
        players_df[["Player Name", "Country"]].apply(tuple, axis=1).isin(fielding_players), 
        "Fantasy_Score"
    ] += 10

    players = players_df.to_dict('records')
    prob = pulp.LpProblem("Dream_11_Cricket_Team_Selection", pulp.LpMaximize)

    num_players = len(players)

    # Decision variables:
    x = pulp.LpVariable.dicts("Select", range(num_players), cat=pulp.LpBinary)
    c = pulp.LpVariable.dicts("Captain", range(num_players), cat=pulp.LpBinary)
    v = pulp.LpVariable.dicts("ViceCaptain", range(num_players), cat=pulp.LpBinary)

    # Constraints
    prob += pulp.lpSum([x[i] for i in range(num_players)]) == 11, "Total_players"
    prob += pulp.lpSum([players[i]["Credits"] * x[i] for i in range(num_players)]) <= 100, "Credit_limit"
    prob += pulp.lpSum([c[i] for i in range(num_players)]) == 1, "One_captain"
    prob += pulp.lpSum([v[i] for i in range(num_players)]) == 1, "One_vice_captain"

    for i in range(num_players):
        prob += c[i] <= x[i], f"Captain_if_selected_{i}"
        prob += v[i] <= x[i], f"ViceCaptain_if_selected_{i}"
        prob += c[i] + v[i] <= x[i], f"No_double_Designation_{i}"

    teams = set(player["Country"] for player in players)
        
    # At least 1 player from each Player Type category (except BOWL)
    for role in ["WK", "BAT", "ALL"]:
        prob += pulp.lpSum([x[i] for i in range(num_players) if players[i]["Player Type"] == role]) >= 1, f"Role_{role}_constraint"

    # Exactly 3 bowlers must be selected
    prob += pulp.lpSum([x[i] for i in range(num_players) if players[i]["Player Type"] == "BOWL"]) == 3, "Role_BOWL_constraint"

    # At least 1 bowler from each team
    for team in teams:
        prob += pulp.lpSum([x[i] for i in range(num_players) if players[i]["Country"] == team and players[i]["Player Type"] == "BOWL"]) >= 1, f"At_least_one_bowler_from_{team}"

   
    for team in teams:
        if team not in restricted_countries:
            prob += pulp.lpSum([x[i] for i in range(num_players) if players[i]["Country"] == team]) >= 5, f"Team_{team}_constraint"
    
    present_restricted = [country for country in restricted_countries if any(player["Country"] == country for player in players)]
    
    if len(present_restricted) == 2:
        for country in restricted_countries:
            prob += pulp.lpSum([x[i] for i in range(num_players) if players[i]["Country"] == country]) >= 5, f"{country}_Min_Limit"
    elif len(present_restricted) == 1:
        restricted_country = present_restricted[0]
        prob += pulp.lpSum([x[i] for i in range(num_players) if players[i]["Country"] == restricted_country]) <= 4, f"Restricted_{restricted_country}_Max_4"


    
    # Objective function: maximize points
    objective = pulp.lpSum([
        players[i]["Fantasy_Score"] * x[i] + players[i]["Fantasy_Score"] * c[i] + 0.5 * players[i]["Fantasy_Score"] * v[i]
        for i in range(num_players)
    ])
    prob += objective

    solver = pulp.PULP_CBC_CMD(msg=0)
    prob.solve(solver)

    if pulp.LpStatus[prob.status] == "Optimal":
        selected_players = []
        for i in range(num_players):
            if x[i].varValue == 1:
                designation = ""
                if c[i].varValue == 1:
                    designation = "(C)"
                elif v[i].varValue == 1:
                    designation = "(VC)"
                
                selected_players.append({
                    "Player Name": players[i]["Player Name"],
                    "Team": players[i]["Country"],
                    "Type": players[i]["Player Type"],
                    "Designation": designation
                })
        
        return pd.DataFrame(selected_players)
    else:
        return pd.DataFrame()


# team = select_dream_team(df)
# print(team)