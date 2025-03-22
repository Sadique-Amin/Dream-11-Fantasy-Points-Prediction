import pandas as pd

def calculateBattingFantasy(df):
    df["Fantasy"] = df["Runs"] + 4 * df["Fours"] + 6 * df["Sixes"] + 4
    df.loc[df["Runs"] >= 25, "Fantasy"] += 4
    df.loc[df["Runs"] >= 50, "Fantasy"] += 8
    df.loc[df["Runs"] >= 75, "Fantasy"] += 12
    df.loc[df["Runs"] >= 100, "Fantasy"] += 16
    df.loc[(df["Runs"] == 0) & (df["IsOut"] == 1), "Fantasy"] -= 2
    df.loc[df["SR"] > 170, "Fantasy"] += 6
    df.loc[(df["SR"] <= 170) & (df["SR"] > 150), "Fantasy"] += 4
    df.loc[(df["SR"] <= 150) & (df["SR"] > 130), "Fantasy"] += 2
    df.loc[df["SR"] < 50, "Fantasy"] -= 6
    df.loc[(df["SR"] >= 50) & (df["SR"] < 60), "Fantasy"] -= 4
    df.loc[(df["SR"] >= 60) & (df["SR"] < 70), "Fantasy"] -= 2
    return df


def calculateBowlingFantasy(df):
    df["Fantasy"] = 4 + 25 * df["Wickets"] + 12 * df["Maidens"]
    df.loc[df["Wickets"] >= 3, "Fantasy"] += 4
    df.loc[df["Wickets"] >= 4, "Fantasy"] += 8
    df.loc[df["Wickets"] >= 5, "Fantasy"] += 12
    df.loc[df["Economy"] < 5, "Fantasy"] += 6
    df.loc[(df["Economy"] >= 5) & (df["Economy"] < 6), "Fantasy"] += 4
    df.loc[(df["Economy"] >= 6) & (df["Economy"] <= 7), "Fantasy"] += 2
    df.loc[df["Economy"] > 12, "Fantasy"] -= 6
    df.loc[(df["Economy"] <= 12) & (df["Economy"] > 11), "Fantasy"] -= 4
    df.loc[(df["Economy"] <= 11) & (df["Economy"] >= 10), "Fantasy"] -= 2
    return df


df = pd.read_csv("CleanedBowlingData.csv")
print(df.head())
print(calculateBowlingFantasy(df))
