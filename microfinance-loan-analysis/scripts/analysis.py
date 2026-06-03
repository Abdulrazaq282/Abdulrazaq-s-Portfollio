"""
Microfinance Loan & Bank Marketing Analysis
Author: Abdulrazaq SHOLA
Description: Analysis of 45,000+ bank customers covering loan defaults,
             subscription behaviour, demographics, and campaign performance.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import numpy as np
import os

# ── Style ──────────────────────────────────────────────────────────────────────
sns.set_theme(style="darkgrid", palette="deep")
plt.rcParams.update({
    "figure.facecolor": "#0d1117",
    "axes.facecolor":   "#161b22",
    "axes.edgecolor":   "#30363d",
    "axes.labelcolor":  "#c9d1d9",
    "xtick.color":      "#8b949e",
    "ytick.color":      "#8b949e",
    "text.color":       "#c9d1d9",
    "grid.color":       "#21262d",
    "font.family":      "DejaVu Sans",
    "axes.titlesize":   13,
    "axes.titleweight": "bold",
    "figure.titlesize": 15,
    "figure.titleweight": "bold",
})

ACCENT  = "#58a6ff"
ACCENT2 = "#3fb950"
ACCENT3 = "#f78166"
ACCENT4 = "#d2a8ff"
PALETTE = [ACCENT, ACCENT2, ACCENT3, ACCENT4, "#ffa657", "#79c0ff", "#56d364", "#e3b341"]

DATA_PATH   = os.path.join(os.path.dirname(__file__), "..", "data", "loan_data.xlsx")
OUTPUT_DIR  = os.path.join(os.path.dirname(__file__), "..", "visuals")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def save(fig, name):
    path = os.path.join(OUTPUT_DIR, name)
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
    print(f"  ✓ {name}")
    plt.close(fig)

# ── Load data ─────────────────────────────────────────────────────────────────
df = pd.read_excel(DATA_PATH, sheet_name="Loan analytics")
df.columns = df.columns.str.strip()
df["subscribed"] = df["y/n"].map({"yes": 1, "no": 0})


# ── 1. Subscription Rate Overview ─────────────────────────────────────────────
sub_counts = df["y/n"].value_counts()
fig, ax = plt.subplots(figsize=(7, 7))
fig.suptitle("Term Deposit Subscription Rate")
wedges, texts, autotexts = ax.pie(
    sub_counts,
    labels=["Not Subscribed", "Subscribed"],
    autopct="%1.1f%%",
    colors=[ACCENT3, ACCENT2],
    startangle=90,
    wedgeprops={"edgecolor": "#0d1117", "linewidth": 2},
    textprops={"color": "#c9d1d9", "fontsize": 13},
)
for at in autotexts:
    at.set_fontsize(14)
    at.set_fontweight("bold")
ax.set_title(f"Only 11.7% of {len(df):,} customers subscribed to a term deposit",
             fontsize=11, color="#8b949e", pad=10)
save(fig, "01_subscription_rate.png")


# ── 2. Subscription Rate by Job ────────────────────────────────────────────────
job_sub = df.groupby("job")["subscribed"].agg(["mean", "count"]).reset_index()
job_sub.columns = ["job", "rate", "count"]
job_sub = job_sub[job_sub["count"] >= 100].sort_values("rate", ascending=True)
job_sub["rate_pct"] = job_sub["rate"] * 100

fig, ax = plt.subplots(figsize=(10, 6))
fig.suptitle("Subscription Rate by Job Type")
colors = [ACCENT2 if r == job_sub["rate_pct"].max() else ACCENT for r in job_sub["rate_pct"]]
bars = ax.barh(job_sub["job"], job_sub["rate_pct"], color=colors, edgecolor="none", zorder=3)
for bar, val in zip(bars, job_sub["rate_pct"]):
    ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2,
            f"{val:.1f}%", va="center", fontsize=10, color="#c9d1d9")
ax.set_xlabel("Subscription Rate (%)")
ax.set_xlim(0, 35)
ax.set_title("Students & retired customers are most likely to subscribe", fontsize=11, color="#8b949e", pad=8)
save(fig, "02_subscription_by_job.png")


# ── 3. Loan Default by Age Group ──────────────────────────────────────────────
age_order = ["Young Adult", "Adult", "Elder", "Senior", "Aged"]
age_default = df[df["age group"].isin(age_order)].groupby("age group").agg(
    total=("Id", "count"),
    defaults=("default", lambda x: (x == "yes").sum())
).reset_index()
age_default["default_rate"] = (age_default["defaults"] / age_default["total"] * 100).round(2)
age_default = age_default.set_index("age group").reindex([a for a in age_order if a in age_default.index]).reset_index()

fig, ax = plt.subplots(figsize=(10, 5))
fig.suptitle("Loan Default Rate by Age Group")
bars = ax.bar(age_default["age group"], age_default["default_rate"],
              color=PALETTE[:len(age_default)], edgecolor="none", zorder=3, width=0.5)
for bar, val, tot in zip(bars, age_default["default_rate"], age_default["total"]):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
            f"{val}%\n({tot:,})", ha="center", fontsize=10, color="#c9d1d9")
ax.set_ylabel("Default Rate (%)")
ax.set_ylim(0, age_default["default_rate"].max() * 1.4)
ax.set_title("Young Adults show highest default risk", fontsize=11, color="#8b949e", pad=8)
save(fig, "03_default_by_age_group.png")


# ── 4. Balance Distribution by Subscription ────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 5))
fig.suptitle("Account Balance Distribution: Subscribers vs Non-Subscribers")
for label, color, yn in [("Subscribed", ACCENT2, "yes"), ("Not Subscribed", ACCENT3, "no")]:
    data = df[df["y/n"] == yn]["balance"].dropna()
    data = data[data.between(data.quantile(0.01), data.quantile(0.99))]
    ax.hist(data, bins=50, alpha=0.6, color=color, label=label, edgecolor="none")
ax.set_xlabel("Account Balance (USD)")
ax.set_ylabel("Number of Customers")
ax.legend(facecolor="#161b22", edgecolor="#30363d")
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
ax.set_title("Subscribers tend to have higher account balances", fontsize=11, color="#8b949e", pad=8)
save(fig, "04_balance_distribution.png")


# ── 5. Campaign Effectiveness by Month ─────────────────────────────────────────
month_order = ["jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"]
month_sub = df.groupby("month")["subscribed"].agg(["mean", "count"]).reset_index()
month_sub.columns = ["month", "rate", "contacts"]
month_sub = month_sub[month_sub["month"].isin(month_order)]
month_sub["month"] = pd.Categorical(month_sub["month"], categories=month_order, ordered=True)
month_sub = month_sub.sort_values("month")
month_sub["rate_pct"] = month_sub["rate"] * 100

fig, ax1 = plt.subplots(figsize=(12, 5))
fig.suptitle("Campaign Performance by Month")
bars = ax1.bar(month_sub["month"].astype(str), month_sub["contacts"],
               color=ACCENT, alpha=0.5, zorder=2, label="Contacts")
ax1.set_ylabel("Customers Contacted", color=ACCENT)
ax1.tick_params(axis="y", labelcolor=ACCENT)
ax2 = ax1.twinx()
ax2.plot(month_sub["month"].astype(str), month_sub["rate_pct"],
         color=ACCENT2, marker="o", linewidth=2.5, markersize=8, zorder=4, label="Sub Rate")
ax2.set_ylabel("Subscription Rate (%)", color=ACCENT2)
ax2.tick_params(axis="y", labelcolor=ACCENT2)
ax2.set_facecolor("#161b22")
ax1.set_title("March has the highest conversion rate despite fewer contacts",
              fontsize=11, color="#8b949e", pad=8)
save(fig, "05_campaign_by_month.png")


# ── 6. Education vs Subscription ───────────────────────────────────────────────
edu_sub = df.groupby("education")["subscribed"].agg(["mean", "count"]).reset_index()
edu_sub.columns = ["education", "rate", "count"]
edu_sub = edu_sub[edu_sub["education"] != "unknown"].sort_values("rate", ascending=False)
edu_sub["rate_pct"] = edu_sub["rate"] * 100

fig, ax = plt.subplots(figsize=(8, 5))
fig.suptitle("Subscription Rate by Education Level")
bars = ax.bar(edu_sub["education"], edu_sub["rate_pct"],
              color=PALETTE[:len(edu_sub)], edgecolor="none", zorder=3, width=0.5)
for bar, val, cnt in zip(bars, edu_sub["rate_pct"], edu_sub["count"]):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2,
            f"{val:.1f}%\n({cnt:,})", ha="center", fontsize=10, color="#c9d1d9")
ax.set_ylabel("Subscription Rate (%)")
ax.set_ylim(0, edu_sub["rate_pct"].max() * 1.35)
ax.set_title("Tertiary-educated customers subscribe at the highest rate",
             fontsize=11, color="#8b949e", pad=8)
save(fig, "06_subscription_by_education.png")


print("\n✅ All 6 visualisations generated!")
print(f"   Saved to: {os.path.abspath(OUTPUT_DIR)}")
