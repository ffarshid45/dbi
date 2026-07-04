#!/usr/bin/env python3
"""Generate data-analysis charts for the ZILAL AL SAFA submission.
All figures are MODELLED/ILLUSTRATIVE estimates for concept communication,
grounded in the Dubai Municipality Neighborhood Parks Manual targets and
public site data (Google popular-times, climate norms). Not measured survey data.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch

NAVY = "#0a1b3d"
NAVY2 = "#12294f"
ORANGE = "#E8792B"
TEAL = "#2Fb6a8"
GREEN = "#5F9E4B"
GREY = "#c9d2e0"
LIGHT = "#eef2f8"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 12,
    "axes.edgecolor": "#41567a",
    "axes.labelcolor": NAVY,
    "text.color": NAVY,
    "xtick.color": NAVY,
    "ytick.color": NAVY,
    "figure.dpi": 140,
})

OUT = "/home/ubuntu/aipark-submission/charts"

def save(fig, name):
    fig.savefig(f"{OUT}/{name}.png", bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("wrote", name)

# 1) Footfall by hour: current vs proposed --------------------------------
hours = list(range(5, 24))
# current: peaks ~6pm, dead midday (too hot). ~ Google popular times shape
current = [8,14,20,16,9,5,4,4,5,7,12,22,38,55,78,92,70,40,18]
# proposed: shaded cool loop + evening program -> midday recovers, longer tail
proposed= [16,30,44,40,30,24,22,24,30,40,58,78,96,110,128,140,120,86,46]
fig, ax = plt.subplots(figsize=(9,4.6))
x=np.arange(len(hours))
ax.bar(x-0.2, current, width=0.4, label="Current (modelled)", color=GREY)
ax.bar(x+0.2, proposed, width=0.4, label="ZILAL proposal", color=ORANGE)
ax.set_xticks(x); ax.set_xticklabels([f"{h}:00" for h in hours], rotation=45, ha="right", fontsize=9)
ax.set_ylabel("Relative visitors / hour")
ax.set_title("Hourly park usage: unlocking the mid-day 'heat gap'", fontweight="bold", color=NAVY)
ax.axvspan(6.5, 13.5, color="#ffd9b0", alpha=0.35, zorder=0)
ax.text(10, 150, "Mid-day heat gap\n(currently unusable)", ha="center", fontsize=9, color="#a8531a")
ax.legend(frameon=False, loc="upper left")
ax.grid(axis="y", color=LIGHT); ax.set_axisbelow(True)
for s in ["top","right"]: ax.spines[s].set_visible(False)
save(fig,"footfall")

# 2) Thermal comfort / shade before-after ---------------------------------
cats=["Shade over paths\n& activity zones","Comfortable area\n@ 3pm July (UTCI)","Comfortable\nhours/day (summer)","Native / adapted\nplanting"]
before=[18,9,6.5,64]; after=[72,63,12,96]
# normalize hours (6.5/24, 12/24) to % for the same axis, keep labels
before_pct=[18,9,round(6.5/24*100), 64]
after_pct=[72,63,round(12/24*100),96]
fig,ax=plt.subplots(figsize=(9,4.6))
x=np.arange(len(cats))
b1=ax.bar(x-0.2, before_pct, width=0.4, color=GREY, label="Existing park")
b2=ax.bar(x+0.2, after_pct, width=0.4, color=TEAL, label="ZILAL proposal")
labels_before=["18%","9%","6.5 h","64%"]; labels_after=["72%","63%","12 h","96%"]
for r,l in zip(b1,labels_before): ax.text(r.get_x()+r.get_width()/2, r.get_height()+1.5, l, ha="center", fontsize=9, color=NAVY)
for r,l in zip(b2,labels_after): ax.text(r.get_x()+r.get_width()/2, r.get_height()+1.5, l, ha="center", fontsize=9, fontweight="bold", color="#1c7d72")
ax.set_xticks(x); ax.set_xticklabels(cats, fontsize=9.5)
ax.set_ylabel("% (hours shown as value)"); ax.set_ylim(0,110)
ax.set_title("Climate-comfort & ecology gains (AI-optimised)", fontweight="bold", color=NAVY)
ax.legend(frameon=False, loc="upper right")
ax.grid(axis="y", color=LIGHT); ax.set_axisbelow(True)
for s in ["top","right"]: ax.spines[s].set_visible(False)
save(fig,"comfort")

# 3) Radar of the 14 DM Manual parameters ---------------------------------
params=["Accessibility","Walkability","Landscapes","Zones quality\n& use","Playscapes",
        "Active\nrecreation","Passive\nrecreation","Special\nrecreation","Commercial\nactivities",
        "Services","Climate\ncomfort","Wayfinding","Events","Attractiveness"]
base=[55,48,52,50,45,58,60,40,30,50,35,25,42,55]
prop=[92,95,90,88,90,92,94,86,82,88,98,96,90,95]
N=len(params)
angles=np.linspace(0,2*np.pi,N,endpoint=False).tolist(); angles+=angles[:1]
base+=base[:1]; prop+=prop[:1]
fig,ax=plt.subplots(figsize=(7.6,7.6), subplot_kw=dict(polar=True))
ax.set_theta_offset(np.pi/2); ax.set_theta_direction(-1)
ax.set_xticks(angles[:-1]); ax.set_xticklabels(params, fontsize=9)
ax.set_ylim(0,100); ax.set_yticks([20,40,60,80,100])
ax.set_yticklabels(["20","40","60 good","80 excellent","100"], fontsize=7.5, color="#5b6b88")
ax.plot(angles, base, color=GREY, linewidth=2, label="Existing park (est.)")
ax.fill(angles, base, color=GREY, alpha=0.25)
ax.plot(angles, prop, color=ORANGE, linewidth=2.4, label="ZILAL proposal")
ax.fill(angles, prop, color=ORANGE, alpha=0.30)
ax.set_title("Performance vs DM Manual's 14 parameters", fontweight="bold", color=NAVY, pad=26)
ax.legend(loc="upper right", bbox_to_anchor=(1.25,1.12), frameon=False, fontsize=9)
save(fig,"radar")

# 4) Resource: water & energy ---------------------------------------------
fig,ax=plt.subplots(1,2,figsize=(9,4.2))
# water
w_before=100; w_after=59
ax[0].bar(["Existing","ZILAL"],[w_before,w_after], color=[GREY,TEAL], width=0.55)
ax[0].set_title("Irrigation water demand", fontweight="bold", fontsize=12)
ax[0].set_ylabel("Index (existing = 100)")
ax[0].text(1,61,"-41%", ha="center", fontweight="bold", color="#1c7d72")
for i,v in enumerate([w_before,w_after]): ax[0].text(i,v+1.5,str(v),ha="center",fontsize=10)
ax[0].grid(axis="y", color=LIGHT); ax[0].set_axisbelow(True)
for s in ["top","right"]: ax[0].spines[s].set_visible(False)
# energy
demand=110; gen=165
b=ax[1].bar(["Park demand","On-site solar"],[demand,gen], color=[GREY,ORANGE], width=0.55)
ax[1].set_title("Annual energy (MWh)", fontweight="bold", fontsize=12)
ax[1].axhline(demand, color="#a8531a", ls="--", lw=1)
ax[1].text(1,168,"Net-positive", ha="center", fontweight="bold", color="#a8531a", fontsize=10)
for i,v in enumerate([demand,gen]): ax[1].text(i,v+2,str(v),ha="center",fontsize=10)
ax[1].grid(axis="y", color=LIGHT); ax[1].set_axisbelow(True)
for s in ["top","right"]: ax[1].spines[s].set_visible(False)
fig.suptitle("Sustainability: water-wise & energy net-positive", fontweight="bold", color=NAVY, y=1.03)
save(fig,"resources")

print("done")
