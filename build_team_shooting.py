import pandas as pd


COLUMN_MAP = {

    "Team": "team",

    "FG%": "fg_pct",

    "Dist.": "avg_dist",

    # Shot distribution
    "0-3": "rim_rate",

    "3-10": "floater_rate",

    "10-16": "mid_rate",

    "16-3P": "long_mid_rate",

    "3P": "three_rate",

    # Zone efficiency
    "0-3.1": "rim_fg",

    "3-10.1": "floater_fg",

    "10-16.1": "mid_fg",

    "16-3P.1": "long_mid_fg",

    "3P.1": "three_fg",

    # Assisted %
    "2P.2": "ast_2p",

    "3P.2": "ast_3p",

    # Corner 3
    "%3PA": "corner3_rate",

    "3P%": "corner3_pct"
}


def load_team_file(path, season):

    df = pd.read_csv(
        path,
        header=1
    )


    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
    )


    df["season"] = season

    df = df[
        ~df["Team"]
        .eq("League Average")
    ]

    df = df.rename(
        columns=COLUMN_MAP
    )

    print(df.columns.tolist())


    cols = [
        "season",
        "team",
        "fg_pct",
        "avg_dist",

        "rim_rate",
        "floater_rate",
        "mid_rate",
        "long_mid_rate",
        "three_rate",

        "rim_fg",
        "floater_fg",
        "mid_fg",
        "long_mid_fg",
        "three_fg",

        "ast_2p",
        "ast_3p",

        "corner3_rate",
        "corner3_pct"
    ]

    return df[cols]


df_1997 = load_team_file(
    "raw/shooting_team_1997.csv",
    1997
)

df_2002 = load_team_file(
    "raw/shooting_team_2002.csv",
    2002
)

df_2007 = load_team_file(
    "raw/shooting_team_2007.csv",
    2007
)

df_2012 = load_team_file(
    "raw/shooting_team_2012.csv",
    2012
)

df_2017 = load_team_file(
    "raw/shooting_team_2017.csv",
    2017
)

df_2022 = load_team_file(
    "raw/shooting_team_2022.csv",
    2022
)

df_2026 = load_team_file(
    "raw/shooting_team_2026.csv",
    2026
)

final = pd.concat(
    [df_1997, df_2002, df_2007, df_2012, df_2017, df_2022, df_2026]
)

final.to_csv(
    "processed/team_shooting_all.csv",
    index=False
)

print(
    final.head()
)