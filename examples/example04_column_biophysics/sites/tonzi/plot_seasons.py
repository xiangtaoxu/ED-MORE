#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""plot_seasons.py -- the two seasons of the Tonzi savanna in ED-MORE: the grass's, December to May, and the oaks',
April to October.

Three rows, day by day:
  1. the leaf area of the oaks and of the grass (the site's), with the clip LAI of the AmeriFlux BADM (direct
     harvests): the Tonzi understory (LAI_U) and Vaira's open grassland 2.4 km away (LAI_TOT);
  2. the daily GPP of the stand against the top tower's (GPP_NT_VUT_REF), and of the grass against the
     understory eddy covariance's (about 2 m above the ground, the PI's partitioning; tower file columns
     GPP_UNDER), each a daily mean of the days the tower measured at least half of;
  3. the predawn leaf water potential of the oaks and of the grass (leaf-area weighted over their cohorts),
     the cue of the grass's phenology and of the oaks' drought.
The BADM's clip LAI is read with example 02's Tonzi reader (--badm, the folder of the BASE-BADM zips).

Usage: python plot_seasons.py [--model output/eval-D.nc] [--out seasons.png] [--badm <folder>]
"""
import argparse
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from netCDF4 import Dataset  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "example02_canopy_phenology", "tonzi_stand"))
import evaluation as ev  # noqa: E402  (the example's colours)
OAK, GRASS = "#5a7d2a", "#c9a227"
UTC_OFFSET_H = -8


def model_days(path):
    """The daily file: the site's LAI and GPP by PFT, and each PFT's leaf-area weighted predawn potential."""
    with Dataset(path) as ds:
        t = pd.to_datetime(dict(year=ds["year"][:], month=ds["month"][:], day=ds["day"][:]))
        lai = np.asarray(ds["mean_lai_pft_py"][:], dtype=float).squeeze()
        gpp = np.asarray(ds["mean_gpp_pft_py"][:], dtype=float).squeeze()
        pft = np.asarray(ds["pft_co"][:], dtype=float).squeeze()
        lai_co = np.asarray(ds["mean_lai_co"][:], dtype=float).squeeze()
        psi = np.asarray(ds["mean_dmax_psi_leaf_co"][:], dtype=float).squeeze()
    out = pd.DataFrame({"lai_oak": lai[:, 0], "lai_grass": lai[:, 1], "gpp_oak": gpp[:, 0], "gpp_grass": gpp[:, 1]},
                       index=t)
    for k, name in ((1, "oak"), (2, "grass")):
        w = np.where(pft == k, np.maximum(np.nan_to_num(lai_co), 1e-9), 0.0)
        out[f"psi_{name}"] = np.nansum(w * np.nan_to_num(psi), axis=1) / np.maximum(w.sum(axis=1), 1e-30)
    return out


def tower_days(path):
    """The top tower's and the understory's daily GPP, on local days with at least half the half hours."""
    d = pd.read_csv(path, na_values=[-9999], usecols=["TIMESTAMP_START", "GPP_NT_VUT_REF", "NEE_VUT_REF_QC",
                                                      "GPP_UNDER", "NEE_UNDER_QC"])
    d.index = pd.to_datetime(d["TIMESTAMP_START"].astype(str), format="%Y%m%d%H%M")
    top = d["GPP_NT_VUT_REF"].where(d["NEE_VUT_REF_QC"] == 0)
    under = d["GPP_UNDER"].where(d["NEE_UNDER_QC"] == 0)
    keep = lambda s: s.resample("D").mean().where(s.resample("D").count() >= 24)  # noqa: E731
    return pd.DataFrame({"top": keep(top), "under": keep(under)})


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default=os.path.join(HERE, "output", "eval-D.nc"))
    ap.add_argument("--tower", default=os.path.join(HERE, "data", "tonzi_tower.csv"))
    ap.add_argument("--badm", default=None, help="the folder of the BASE-BADM zips, for the clip LAI")
    ap.add_argument("--out", default=os.path.join(HERE, "seasons.png"))
    args = ap.parse_args(argv)
    m = model_days(args.model)
    t = tower_days(args.tower).reindex(m.index)
    plt.rcParams.update({"axes.edgecolor": ev.MUTED, "axes.labelcolor": ev.INK, "xtick.color": ev.MUTED,
                         "ytick.color": ev.MUTED, "axes.grid": True, "grid.color": ev.GRID, "grid.linewidth": 0.6,
                         "axes.spines.top": False, "axes.spines.right": False, "axes.axisbelow": True})
    fig, ax = plt.subplots(3, 1, figsize=(13, 9.5), sharex=True)
    a = ax[0]
    a.plot(m.index, m["lai_oak"], color=OAK, lw=1.4, label="oaks (model)")
    a.plot(m.index, m["lai_grass"], color=GRASS, lw=1.4, label="grass (model)")
    if args.badm:
        import prepare_observations as po                  # example 02's BADM reader
        for name, var, marker in (("US-Ton", "LAI_U", "o"), ("US-Var", "LAI_TOT", "s")):
            zip_name = f"AMF_{name}_BASE-BADM_27-5.zip"
            groups = po.badm(os.path.join(args.badm, zip_name))
            rows = [(pd.Timestamp(v["LAI_DATE"][:8]), float(v[var])) for kind, v in groups.values()
                    if kind == "GRP_LAI" and var in v and len(v.get("LAI_DATE", "")) >= 8]
            s = pd.Series(dict(rows)).sort_index()
            s = s[(s.index >= m.index[0]) & (s.index <= m.index[-1])]
            label = "Tonzi understory clips" if name == "US-Ton" else "Vaira open-grassland clips"
            a.plot(s.index, s.values, marker, color=ev.TOWER, ms=4, mfc="white" if marker == "s" else ev.TOWER,
                   ls="none", label=label)
    a.set_ylabel("LAI (m² m⁻²)")
    a.legend(loc="upper right", frameon=False, ncol=4, fontsize=9)
    a = ax[1]
    a.plot(t.index, t["top"], color=ev.TOWER, lw=1.0, label="top tower")
    a.plot(m.index, m["gpp_oak"] + m["gpp_grass"], color=ev.MODEL, lw=1.0, label="model, the stand")
    a.plot(t.index, t["under"], color=ev.TOWER, lw=1.0, ls=":", label="understory tower")
    a.plot(m.index, m["gpp_grass"], color=GRASS, lw=1.0, label="model, the grass")
    a.set_ylabel("GPP, daily mean (µmol m⁻² s⁻¹)")
    a.legend(loc="upper right", frameon=False, ncol=4, fontsize=9)
    a = ax[2]
    a.plot(m.index, m["psi_oak"], color=OAK, lw=1.2, label="oaks")
    a.plot(m.index, m["psi_grass"], color=GRASS, lw=1.2, label="grass")
    a.set_ylabel("predawn leaf ψ (MPa)")
    a.legend(loc="lower right", frameon=False, ncol=2, fontsize=9)
    fig.suptitle("ED-MORE at Tonzi Ranch: the grass's season and the oaks', day by day", color=ev.INK, fontsize=12)
    fig.tight_layout()
    fig.savefig(args.out, dpi=120)
    print(f"figure: {args.out}")


if __name__ == "__main__":
    main()
