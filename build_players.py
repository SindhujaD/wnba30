import pandas as pd


COLUMN_MAP = {
    "Name": "name",

    # game stats
    "G": "games",

    "GS": "games_start",

    "MP": "mins_played",

    # shooting
    "FG": "fields_made",

    "FGA": "fg_attempts",

    "FG%": "fg_pct",

    "3P": "3p_made",

    "3PA": "3p_attempts",

    "3P%": "3p_pct",

    "2P": "2p_made",

    "2PA": "2p_attempts",

    "2P%": "2p_pct",

    "FT": "ft_made",

    "FTA": "ft_attempts",

    "FT%": "ft_pct",

    # misc stats

    "ORB": "off_reb",

    "DRB": "def_reb",
    
    "TRB": "total_reb",

    "AST": "assists",
    
    "STL": "steals",
    
    "BLK": "blocks",
    
    "TOV": "turnovers",

    "PF": "fouls",
    
    "PTS": "points"


}


def load_team_file(path):

    df = pd.read_csv(
        path,
        header=0
    )


    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
    )

    df = df.rename(
        columns=COLUMN_MAP
    )

    print(df.columns.tolist())


    cols = [
        "name",
        # game stats
        "games",
        "games_start",
        "mins_played",

        # shooting
        "fields_made",
        "fg_attempts",
        "fg_pct",
        "3p_made",
        "3p_attempts",
        "3p_pct",
        "2p_made",
        "2p_attempts",
        "2p_pct",
        "ft_made",
        "ft_attempts",
        "ft_pct",

        # misc stats
        "off_reb",
        "def_reb",
        "total_reb",
        "assists",
        "steals",
        "blocks",
        "turnovers",
        "fouls",
        "points"
    ]

    return df[cols]


df_all = load_team_file(
    "raw/players.csv"
)

df_all.to_csv(
    "processed/players_all.csv",
    index=False
)

print(
    df_all.head()
)