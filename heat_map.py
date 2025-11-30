import pandas as pd
import plotly.graph_objects as go
import os

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Read risk data
risk_db = pd.read_csv(os.path.join(script_dir, "risk_table.csv"), skiprows=2)

impact_bins = [0, 16 / 3, 2 * 16 / 3, 16]
likelihood_bins = [0, 5 / 3, 2 * 5 / 3, 5]

# Create a 3x3 matrix for risk levels based on Impact and Likelihood categories
# 0: Low (Green), 1: Medium (Yellow), 2: High (Red)
# Rows: Likelihood (Low, Medium, High)
# Columns: Impact (Low, Medium, High)
risk_matrix_values = [
    [
        0,
        1,
        1,
    ],  # Low Likelihood: Low Impact -> Low, Medium Impact -> Medium, High Impact -> Medium
    [
        1,
        1,
        2,
    ],  # Medium Likelihood: Low Impact -> Medium, Medium Impact -> Medium, High Impact -> High
    [
        1,
        2,
        2,
    ],  # High Likelihood: Low Impact -> Medium, Medium Impact -> High, High Impact -> High
]

# Calculate bin centers for the heatmap
impact_centers = [
    impact_bins[0] + (impact_bins[1] - impact_bins[0]) / 2,
    impact_bins[1] + (impact_bins[2] - impact_bins[1]) / 2,
    impact_bins[2] + (impact_bins[3] - impact_bins[2]) / 2,
]

likelihood_centers = [
    likelihood_bins[0] + (likelihood_bins[1] - likelihood_bins[0]) / 2,
    likelihood_bins[1] + (likelihood_bins[2] - likelihood_bins[1]) / 2,
    likelihood_bins[2] + (likelihood_bins[3] - likelihood_bins[2]) / 2,
]

fig = go.Figure(
    data=go.Heatmap(
        z=risk_matrix_values,
        x=impact_centers,
        y=likelihood_centers,
        colorscale="RdYlGn_r",
        zsmooth="best",
        colorbar=dict(
            tickvals=[0, 1, 2],
            ticktext=["Low Risk", "Medium Risk", "High Risk"],
            title="Risk Level",
        ),
        showscale=False,
    )
)

# Add scatter plot for each risk
for index, row in risk_db.iterrows():
    fig.add_trace(
        go.Scatter(
            x=[row["Impact (1-16)"]],
            y=[row["Likelihood (1-5)"]],
            mode="markers+text",
            text=[row["Ref ID"]],
            textposition="top center",
            marker=dict(size=10),
            name=row["Risk Description"],
        )
    )

fig.update_layout(
    title="Risk Heat Map",
    xaxis_title="Impact",
    yaxis_title="Likelihood",
    xaxis=dict(showticklabels=False, showgrid=False, zeroline=False, range=[0, 16]),
    yaxis=dict(showticklabels=False, showgrid=False, zeroline=False, range=[0, 5]),
    showlegend=True,
)

fig.show()
