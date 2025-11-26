import pandas as pd
import plotly.graph_objects as go

risk_db = pd.DataFrame(
    {
        "Risk": ["R1", "R2", "R3", "R4"],
        "Likelihood": [0, 0, 0, 0],
        "Impact": [0, 0, 0, 0],
        "Priority": [0, 0, 0, 0],
    }
)

fig = go.Figure(data=go.Scatter(x=risk_db["Impact"], y=risk_db["Likelihood"], mode="markers"))
impact_bins = [0, 16 / 3, 2 * 16 / 3, 16]
likelihood_bins = [0, 5 / 3, 2 * 5 / 3, 5]

# Create a 3x3 matrix for risk levels based on Impact and Likelihood categories
# 0: Low (Green), 1: Medium (Yellow), 2: High (Red)
# Rows: Likelihood (Low, Medium, High)
# Columns: Impact (Low, Medium, High)
risk_matrix_values = [
    [0, 1, 1],  # Low Likelihood: Low Impact -> Low, Medium Impact -> Medium, High Impact -> Medium
    [1, 1, 2],  # Medium Likelihood: Low Impact -> Medium, Medium Impact -> Medium, High Impact -> High
    [1, 2, 2],  # High Likelihood: Low Impact -> Medium, Medium Impact -> High, High Impact -> High
]

fig = go.Figure(
    data=go.Heatmap(
        z=risk_matrix_values,
        x=["Low Impact", "Medium Impact", "High Impact"],
        y=["Low Likelihood", "Medium Likelihood", "High Likelihood"],
        colorscale=[[0, "green"], [0.5, "yellow"], [1, "red"]],
        colorbar=dict(
            tickvals=[0, 1, 2],
            ticktext=["Low Risk", "Medium Risk", "High Risk"],
            title="Risk Level",
        ),
    )
)

fig.update_layout(
    title="Risk Heat Map",
    xaxis_title="Impact (0-16)",
    yaxis_title="Likelihood (0-5)",
    xaxis=dict(
        tickmode="array",
        tickvals=[0, 1, 2],
        ticktext=[
            f"0-{impact_bins[1]:.1f}",
            f"{impact_bins[1]:.1f}-{impact_bins[2]:.1f}",
            f"{impact_bins[2]:.1f}-{impact_bins[3]:.1f}",
        ],
    ),
    yaxis=dict(
        tickmode="array",
        tickvals=[0, 1, 2],
        ticktext=[
            f"0-{likelihood_bins[1]:.1f}",
            f"{likelihood_bins[1]:.1f}-{likelihood_bins[2]:.1f}",
            f"{likelihood_bins[2]:.1f}-{likelihood_bins[3]:.1f}",
        ],
    ),
)

fig.show()
