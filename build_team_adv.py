import pandas as pd


COLUMN_MAP = {

    "Team": "team",

    "Age": "age",

    # schedule records 

    "W": "wins",

    "L": "loss",

    "PW": "py_wins",

    "PL": "py_loss",

    "MOV": "marg_of_victory",

    "SOS": "stgth_of_sched",

    "SRS": "simp_rating_sys",

    # ratings

    "ORtg": "off_rtg",

    "DRtg": "def_rtg",

    "NRtg": "net_rtg",

    "Pace": "pace",

    # shooting

    "FTr": "ft_att_rate",

    "3PAr": "3pt_att_rate",

    "TS%": "shoot_pct",

    # offensive four factors

    "eFG%": "effect_fg",

    "TOV%": "turnover",

    "ORB%": "off_reb",

    "FT/FGA": "ft_per_fg_att",

    # defensive four factors

    "deFG%": "effect_fg_def",

    "dTOV%": "turnover_def",

    "DRB%": "def_reb",

    "dFT/FGA": "ft_per_fg_att_def",

    "Arena": "arena"
}

FRANCHISE_MAP = {
    "Utah Starzz": "Las Vegas Aces",
    "San Antonio Silver Stars": "Las Vegas Aces",
    "San Antonio Stars": "Las Vegas Aces",

    "Detroit Shock": "Dallas Wings",
    "Tulsa Shock": "Dallas Wings",
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
    
    # remove asterisks from team names
    df["Team"] = (
        df["Team"]
        .astype(str)
        .str.replace("*", "", regex=False)
        .str.strip()
    )

    df["Team"] = df["Team"].replace(FRANCHISE_MAP)

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
        "age",

        # schedule records 
        "wins",
        "loss",
        "py_wins",
        "py_loss",
        "marg_of_victory",
        "stgth_of_sched",
        "simp_rating_sys",

        # ratings
        "off_rtg",
        "def_rtg",
        "net_rtg",
        "pace",

        # shooting
        "ft_att_rate",
        "3pt_att_rate",
        "shoot_pct",

        # offensive four factors
        "effect_fg",
        "turnover",
        "off_reb",
        "ft_per_fg_att",

        # defensive four factors
        "effect_fg_def",
        "turnover_def",
        "def_reb",
        "ft_per_fg_att_def",
        "arena"
    ]

    return df[cols]


df_1997 = load_team_file(
    "raw/advanced_1997.csv",
    1997
)

df_2002 = load_team_file(
    "raw/advanced_2002.csv",
    2002
)

df_2007 = load_team_file(
    "raw/advanced_2007.csv",
    2007
)

df_2012 = load_team_file(
    "raw/advanced_2012.csv",
    2012
)

df_2017 = load_team_file(
    "raw/advanced_2017.csv",
    2017
)

df_2022 = load_team_file(
    "raw/advanced_2022.csv",
    2022
)

df_2026 = load_team_file(
    "raw/advanced_2026.csv",
    2026
)

final = pd.concat(
    [df_1997, df_2002, df_2007, df_2012, df_2017, df_2022, df_2026]
)

final.to_csv(
    "processed/team_advanced2.csv",
    index=False
)

print(
    final.head()
)