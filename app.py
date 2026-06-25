import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
import plotly.express as px


# ----------------------------
# LOAD
# ----------------------------
df = pd.read_csv("./processed/team_shooting_all.csv")
df2 = pd.read_csv("./processed/team_advanced.csv")
player_df = pd.read_csv("./processed/players_all.csv")

player_df["off_impact"] = (
    player_df["assists"] +
    player_df["off_reb"]
)

player_df["def_impact"] = (
    player_df["blocks"] +
    player_df["steals"]
)

player_df["def_reb"] = player_df["def_reb"]
player_df["points"] = player_df["points"]

# ----------------------------
# DISTANCE ZONES
# ----------------------------
DISTANCE_ZONES = {
    "rim_rate": (0, 4),
    "floater_rate": (5, 9),
    "mid_rate": (10, 16),
    "long_mid_rate": (17, 21),
    "three_rate": (22, 30),
}


# ----------------------------
# SYNTHETIC DISTANCES
# ----------------------------
def generate_distances(season_df, samples=12000):

    distances = []

    for _, row in season_df.iterrows():

        team_samples = samples // len(season_df)

        for zone, bounds in DISTANCE_ZONES.items():

            n = int(team_samples * row[zone])

            distances.extend(
                np.random.uniform(
                    bounds[0],
                    bounds[1],
                    n
                )
            )

    return np.array(distances)


dist97 = generate_distances(
    df[df["season"] == 1997]
)

dist26 = generate_distances(
    df[df["season"] == 2026]
)


# ----------------------------
# KDE
# ----------------------------
x = np.linspace(0, 30, 500)

kde97 = gaussian_kde(dist97)
kde26 = gaussian_kde(dist26)

density97 = kde97(x)
density26 = kde26(x)

# Normalize to percent of peak
global_max = max(
    density97.max(),
    density26.max()
)

density97 = (
    density97 /
    global_max
) * 100

density26 = (
    density26 /
    global_max
) * 100

heat97 = np.tile(
    density97,
    (80, 1)
)

heat26 = np.tile(
    density26,
    (80, 1)
)

# ----------------------------
# AVAILABLE YEARS
# ----------------------------
YEARS = [
    1997,
    2002,
    2007,
    2012,
    2017,
    2022,
    2026
]


# ----------------------------
# BUILD ALL HEATMAPS
# ----------------------------
heatmaps = {}
avg_dists = {}

all_densities = []

for season in YEARS:

    season_df = df[
        df["season"] == season
    ]

    distances = generate_distances(
        season_df
    )

    x = np.linspace(
        0,
        30,
        500
    )

    kde = gaussian_kde(
        distances
    )

    density = kde(x)

    all_densities.append(
        density.max()
    )

    heatmaps[season] = density

    avg_dists[season] = (
        season_df[
            "avg_dist"
        ].mean()
    )


# shared normalization
global_max = max(
    all_densities
)

for season in YEARS:

    density = (
        heatmaps[season]
        /
        global_max
    ) * 100

    heatmaps[season] = np.rot90(
        np.tile(
            density,
            (80, 1)
        )
    )


# ----------------------------
# TIMELINE
# ----------------------------
st.markdown(
    "## The Evolution of the WNBA"
)

st.markdown(
    "#### In honor of the WNBA's 30th season, this dashboard explores the evolution of the league over time."
)

st.markdown(
    "All data used in this dashboard has been sourced from Basketball Reference. If you have any questions, comments, feedback, or things you want added to this dashboard, please reach out to me!"
)

st.markdown(
    "The first visual below, explores how shot selection in the game has changed since the inaugural season in 1997. It notably highlights the famous disappearance of the midrange game, shifting from a peak of 50% of shots taken at specific areas in the midrange, down to a peak of 21% in 2026. You can play through an animation of the evolution over the years, or use the slider at the bottom to manually scrub through time. You can hover on the heatmap to get the percentage of shots taken at each distance from the rim. Please keep in mind that these shot locations are not based on true x, y coordinates from WNBA data, but rather simulated shots based on true historic rates for each range of shot."
)

# ----------------------------
# INTERACTIVE ANIMATED HEATMAP
# ----------------------------
import plotly.graph_objects as go

distance_axis = np.linspace(
    30,
    0,
    next(iter(heatmaps.values())).shape[0]
)

frames = []

for season in YEARS:

    frames.append(
        go.Frame(
            name=str(season),

            data=[

                go.Heatmap(
                    z=heatmaps[season],

                    y=distance_axis,

                    colorscale="Magma",

                    zmin=0,
                    zmax=100,

                    hovertemplate=
                    (
                        "Distance: %{y:.1f} ft"
                        "<br>"
                        "Relative Frequency: %{z:.1f}%"
                        "<extra></extra>"
                    )
                )

            ]
        )
    )


fig = go.Figure()

fig.add_trace(

    go.Heatmap(

        z=heatmaps[2017],

        y=distance_axis,

        colorscale="Magma",

        zmin=0,
        zmax=100,

        colorbar=dict(
            title="Relative Shot Frequency (%)"
        ),

        hovertemplate=
        (
            "Distance: %{y:.1f} ft"
            "<br>"
            "Relative Frequency: %{z:.1f}%"
            "<extra></extra>"
        )
    )
)

fig.frames = frames


# ----------------------------
# COURT MARKERS
# ----------------------------
refs = [
    (0, "Rim"),
    (4, "RA"),
    (15, "FT"),
    (22, "3PT")
]

for ft, label in refs:

    fig.add_hline(
        y=ft,
        line_dash="dash",
        line_color="white"
    )

    fig.add_annotation(
        x=10,
        y=ft,
        text=label,
        showarrow=False
    )


# ----------------------------
# ANIMATION CONTROLS
# ----------------------------
fig.update_layout(

    template="plotly_dark",

    title=dict(
        text="WNBA Shot Evolution"
    ),

    height=850,

    dragmode="zoom",

    xaxis=dict(
        visible=False
    ),

    yaxis=dict(
        title="Shot Distance (ft)",
        autorange="reversed"
    ),

    updatemenus=[

        dict(

            type="buttons",

            showactive=False,

            buttons=[

                dict(

                    label="▶ Play",

                    method="animate",

                    args=[
                        None,
                        {
                            "frame": {
                                "duration": 1200,
                                "redraw": True
                            },

                            "fromcurrent": True
                        }
                    ]
                ),

                dict(

                    label="⏸ Pause",

                    method="animate",

                    args=[
                        [None],
                        {
                            "frame": {
                                "duration": 0
                            }
                        }
                    ]
                )

            ]
        )

    ],

    sliders=[

        {

            "currentvalue": {

                "prefix": "Season: "

            },

            "steps": [

                {

                    "label": str(y),

                    "method": "animate",

                    "args": [

                        [str(y)],

                        {

                            "mode": "immediate",

                            "frame": {

                                "duration": 300,

                                "redraw": True

                            }

                        }

                    ]

                }

                for y in YEARS

            ]

        }

    ]
)


st.plotly_chart(
    fig,
    use_container_width=True
)

# ----------------------------
# LEAGUE-WIDE AGGREGATES
# ----------------------------
league = (
    df2.groupby("season")
    .agg({
        "pace": "mean",
        "ft_per_fg_att": "mean",
        "shoot_pct": "mean",
        "age": "mean"
    })
    .reset_index()
)


# Convert shooting % → TS%
# Approximation:
league["ts_pct"] = (
    league["shoot_pct"]
    /
    2
) * 100


# Convert to %
league["ft_per_fg_att"] *= 100

def plot_trend(
    data,
    y_col,
    title,
    ylabel
):

    fig, ax = plt.subplots(
        figsize=(10, 5)
    )

    ax.plot(
        data["season"],
        data[y_col],
        linewidth=3
    )

    ax.scatter(
        data["season"],
        data[y_col],
        s=70
    )

    # Vertical era markers
    years = [
        1997,
        2002,
        2007,
        2012,
        2017,
        2022,
        2026
    ]

    for yr in years:

        ax.axvline(
            yr,
            alpha=.15,
            linestyle="--"
        )

    ax.set_title(
        title,
        fontsize=18
    )

    ax.set_xlabel(
        "Season"
    )

    ax.set_ylabel(
        ylabel
    )

    ax.grid(
        alpha=.25
    )

    plt.tight_layout()

    return fig


st.divider()

st.subheader(
    "Pace of Play, Shooting Percentage, FT Rate, and Player Age over Time"
)

st.markdown(
    "In this section, I answered some questions that I was personally curious about. The first chart shows how true shooting accuracy, that is shot accuracy of all types of shots combined, has increased since the inception of the league. In 1997, we began with a true shooting rate of about 49%, and in 2026, the rate is nearly 56%."
)

def plot_trend_plotly(data, y_col, title, y_label):
    fig = px.line(
        data,
        x="season",
        y=y_col,
        markers=True,
        title=title
    )

    fig.update_traces(line=dict(width=3))

    timeline_years = [1997, 2002, 2007, 2012, 2017, 2022, 2026]

    for yr in timeline_years:
        fig.add_vline(x=yr, line_width=1, line_dash="dash", opacity=0.3)

    fig.update_layout(
        xaxis_title="Season",
        yaxis_title=y_label,
        hovermode="x unified",
        template="plotly_dark"
    )

    return fig

# ----------------------------
# TEAM TREND FUNCTION
# ----------------------------
def plot_team_trends_plotly(data, metric, title, ylabel, selected_teams):

    fig = px.line(
        data,
        x="season",
        y=metric,
        color="team",
        markers=True,
        title=title
    )

    fig.update_traces(line=dict(width=3))

    timeline_years = [1997, 2002, 2007, 2012, 2017, 2022, 2026]

    for yr in timeline_years:
        fig.add_vline(x=yr, line_width=1, line_dash="dash", opacity=0.25)

    fig.update_layout(
        xaxis_title="Season",
        yaxis_title=ylabel,
        hovermode="x unified",
        template="plotly_dark"
    )

    # filter teams AFTER creation (important)
    fig.for_each_trace(
        lambda trace: trace.update(
            visible=True if trace.name in selected_teams else False
        )
    )

    return fig

# ----------------------------
# TS%
# ----------------------------

ts_fig = plot_trend_plotly(
    league,
    "shoot_pct",
    "True Shooting Percentage",
    "TS%"
)

st.plotly_chart(ts_fig, use_container_width=True)


st.markdown(
    "This chart illustrates how the pace of the game has increased over time. This is not surprising to anyone who watches the game, especially as the game becomes more offensively focused. I am not sure what the sudden dip in the 2002 season is, but I would love to know any anecdotal information that fans may know about why the pace dipped so much that year. "
)

# ----------------------------
# PACE
# ----------------------------

pace_fig = plot_trend_plotly(
    league,
    "pace",
    "WNBA Pace Over Time",
    "Possessions per 40"
)

st.plotly_chart(pace_fig, use_container_width=True)


st.markdown(
    "The two charts below gave me no specific conclusions or takeaways, but it was interesting to see if there were any concrete trends in the amount of free throws taken or the age of the players. When I first looked at the chart for the players, I was shocked at what felt like a widely varying average age, just to discover the range is not even one year."
) 


# ----------------------------
# FT/FGA
# ----------------------------

ft_fig = plot_trend_plotly(
    league,
    "ft_per_fg_att",
    "Free Throws per 100 FG Attempts",
    "FT / 100 FGA"
)

st.plotly_chart(ft_fig, use_container_width=True)

# ----------------------------
# Age
# ----------------------------

age_fig = plot_trend_plotly(
    league,
    "age",
    "Average Age Over Time",
    "Age"
)

st.plotly_chart(age_fig, use_container_width=True)


# ----------------------------
# TEAM SELECTOR
# ----------------------------

st.subheader(
    "Team Offensive and Defensive Rating over Time"
)

st.markdown(
    "This section allows you to select one or more teams to explore their offensive and defensive ratings over time. You can select multiple teams to compare their performance across seasons. The general trend I noticed was that, similar to true shooting percentage, the whole league has gotten better at the game over time. Also, the statistics for the Aces and the Wings includes the data from previous names and locations of those franchises."
) 

default_teams = [
    "Phoenix Mercury",
    "New York Liberty",
    "Los Angeles Sparks"
]

available_teams = sorted([
    t.replace("*", "")
    for t in df2["team"].unique()
])

selected_teams = st.multiselect(
    "Select teams",
    options=available_teams,
    default=default_teams
)


if len(selected_teams) > 0:

    # ----------------------------
    # OFFENSIVE RATING
    # ----------------------------

    off_fig = plot_team_trends_plotly(
        df2,
        "off_rtg",
        "Offensive Rating Over Time",
        "Off Rtg",
        selected_teams
    )

    st.plotly_chart(off_fig, use_container_width=True)


    # ----------------------------
    # DEFENSIVE RATING
    # ----------------------------

    def_fig = plot_team_trends_plotly(
        df2,
        "def_rtg",
        "Defensive Rating Over Time",
        "Def Rtg",
        selected_teams
    )

    st.plotly_chart(def_fig, use_container_width=True)

else:

    st.info(
        "Select at least one team."
    )


st.divider()
st.header("Player Impact Analysis")

# off scatter

st.subheader("Offensive Impact: Points vs Playmaking/Boards")
st.markdown(
    "In this last section, I tried to see the general correlation between points scored and other offensive impact in assists and offensive rebounds and the correlation between defensive rebounds and defensive impact in steals and blocks. All of the players plotted below ranked in the top 5 in at least one of those categories during their career. If you want to see a specfiic player, but they are not on there, feel free to reach out to me and I will add them in."
) 

selected_player_off = st.selectbox(
    "Search player (offense)",
    options=sorted(player_df["name"].unique())
)

fig_off = px.scatter(
    player_df,
    x="points",
    y="off_impact",
    hover_name="name",
    hover_data={
        "points": True,
        "assists": True,
        "off_reb": True,
        "def_reb": True,
        "blocks": True,
        "steals": True,
        "games": True
    },
    opacity=0.5,
    title="Points vs Offensive Impact"
)

fig_off.update_traces(marker=dict(size=7))

highlight_off = player_df[
    player_df["name"] == selected_player_off
]

fig_off.add_scatter(
    x=highlight_off["points"],
    y=highlight_off["off_impact"],
    mode="markers+text",
    marker=dict(size=10, color="orange"),
    text=highlight_off["name"],
    textposition="top center",
    name="Selected Player"
)

fig_off.update_layout(
    dragmode="zoom",
    template="plotly_dark"
)

st.plotly_chart(fig_off, use_container_width=True)


# def scatter


st.subheader("Defensive Impact: Stocks vs Defensive Rebounding")

selected_player_def = st.selectbox(
    "Search player (defense)",
    options=sorted(player_df["name"].unique())
)

fig_def = px.scatter(
    player_df,
    x="def_impact",
    y="def_reb",
    hover_name="name",
    hover_data={
        "blocks": True,
        "steals": True,
        "def_reb": True,
        "points": True,
        "games": True
    },
    opacity=0.5,
    title="Defensive Impact vs Defensive Rebounding"
)

fig_def.update_traces(marker=dict(size=7))

highlight_def = player_df[
    player_df["name"] == selected_player_def
]

fig_def.add_scatter(
    x=highlight_def["def_impact"],
    y=highlight_def["def_reb"],
    mode="markers+text",
    marker=dict(size=10, color="orange"),
    text=highlight_def["name"],
    textposition="top center",
    name="Selected Player"
)

fig_def.update_layout(
    dragmode="zoom",
    template="plotly_dark"
)

st.plotly_chart(fig_def, use_container_width=True)
