import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np


def getMatchInfo(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }

    data = {"MatchLink": url}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return {}

    try:
        soup = bs(response.text, "lxml")
        tables = soup.find_all("table")
        if len(tables) < 5:
            raise IndexError("Insufficient table elements found on the webpage.")

        table = tables[4]
        table_features = ["Toss", "Series", "Match days"]
        rows = table.find_all("tr")
        table_data = {}

        for row in rows:
            columns = row.find_all("td")
            if columns and columns[0].text in table_features:
                table_data[columns[0].text] = columns[1].text.strip()

        data["TossWonTeam"] = table_data.get("Toss", "Unknown").split(", ")[0]

        if "field" in table_data.get("Toss", "").split(", ")[-1]:
            data["TossResult"] = "field"
        else:
            data["TossResult"] = "bat"

        data["Series"] = table_data.get("Series", "Unknown")
        match_days = table_data.get("Match days", "").lower()

        if "daynight" in match_days:
            data["MatchTime"] = "daynight"
        elif "day" in match_days:
            data["MatchTime"] = "day"
        else:
            data["MatchTime"] = "night"

        divs = soup.find("div", class_="ds-w-2/3")
        if not divs:
            raise ValueError("Match details section not found.")

        team_details = divs.find_all("div", class_="ci-team-score")
        if len(team_details) < 2:
            raise ValueError("Insufficient team score details found.")

        team1_details, team2_details = team_details[:2]

        data["Team1"] = team1_details.find("a").text.strip()
        data["Team2"] = team2_details.find("a").text.strip()
        data["Result"] = divs.find("p").text
        print(data["Result"])
        def extract_score_and_wickets(details):
            try:
                score_parts = details.find("strong").text.split("/")
                score = int(score_parts[0])
                wickets = int(score_parts[1]) if len(score_parts) > 1 else 10
            except (AttributeError, ValueError, IndexError):
                score, wickets = 0, 10
            return score, wickets

        data["Team1Score"], data["Team1Wickets"] = extract_score_and_wickets(team1_details)
        data["Team2Score"], data["Team2Wickets"] = extract_score_and_wickets(team2_details)

    except Exception as e:
        print(f"Error processing data: {e}")
        return {}

    return data



def getInfoMultiMatch():
    df = pd.read_csv("MatchLinks.csv")
    links = np.array(df["MatchLink"])
    i = 1
    data = []
    for link in links:
        data.append(getMatchInfo(link))
        print(f"{i} / {len(links)} completed")
        i += 1

    notFoundLinks = [d for d in data if not d]
    data = [d for d in data if d]
    df = pd.DataFrame(data)
    notDf = pd.DataFrame(notFoundLinks)
    notDf.to_csv("NotFoundMatches.csv", index=False)
    df.to_csv("MatchWiseInfo.csv", index=False)

    print(len(notFoundLinks), len(df))

getInfoMultiMatch()