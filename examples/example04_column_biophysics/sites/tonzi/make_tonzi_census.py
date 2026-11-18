#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""The Tonzi stand: an oak census imputed from the site survey's stand averages, and the grass beneath.

The tree list of the ground survey at the US-Ton tower is not published. Its stand averages are (Kiang
2002, a 100 x 100 m plot and a 200 m transect, as reported by Baldocchi, Xu & Kiang 2004, Agric. For.
Meteorol. 123:13-39, section 2.1): 194 stems per hectare, a mean DBH of 0.199 m, a basal area of
18 m2 per hectare, a mean height of 7.1 m and a maximum of 13.0 m, with blue oak covering 40 % of the
land around the tower. These stems are NOT measured trees.

The three DBH figures do not fit one stand: 194 stems with 18 m2/ha need a quadratic mean DBH of
34.4 cm, and a mean of 19.9 cm would then need a DBH coefficient of variation of 1.4. Blue oak at NEON's
San Joaquin Experimental Range, 70 live stems of 5 cm and more, has 0.42. The stem count and the basal
area are kept: the site's above-ground tree carbon (4.24 kgC m-2, AmeriFlux BADM, 2001-03) and the
reported heights both point to the larger stems.

The stand, on 1 ha of 10 m cells (one patch each; ED-MORE fuses them before the first step):
  1. Oaks. 194 stems at the mid-quantiles, (i - 0.5)/194, of a Weibull with SJER's coefficient of
     variation, rescaled to 18 m2/ha exactly, dealt in snake order by size to the 40 treed cells. Each
     stem is one cohort row of one plant per cell.
  2. The height curve for the PFT file: a power law H = A D^b through the stems' mean height (7.1 m)
     and the largest stem's 13.0 m, printed as height_allometry = "power", b1Ht = ln A, b2Ht = b.
  3. The oaks' leaf area: the PFT file's lai_b1, printed, that gives the stems the site's tree LAI,
     0.65 (Baldocchi et al. 2004, p. 16), with the PFT file's lai_b2.
  4. Grass. One grass row in every cell, with dbh 0: a grass's size is its PFT's height. The tillers
     per m2 set its leaf area, and the per-tiller leaf area is the PFT file's lai_b1 (lai_b2 = 0):
     a cell in the open carries Vaira's open-grassland peak LAI, a cell under the oaks the Tonzi
     understory's. No count of tillers was found for these swards; in a frozen stand only the leaf
     area and the root length they give matter, so the density is a choice.
  5. With --pft-file, the stand's steady litter input for [soil_carbon], routed as make_census.py
     routes it: each PFT's leaf fall and fine-root turnover, the oaks' wood at their background
     mortality (the PFT file's mort_gamma; there is no repeated census), the grass's whole canopy
     each year.

Usage: python make_tonzi_census.py --out data/tonzi_census_ed.csv [--pft-file pft_parameters.toml]
"""
import argparse
import json
import math
import os
import statistics as st
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "..", "scripts", "prepare_input", "census"))
import make_census as mc                # noqa: E402
import numpy as np                      # noqa: E402

STEMS_PER_HA = 194.0          # Baldocchi, Xu & Kiang 2004, sect. 2.1
BASAL_AREA_M2_HA = 18.0       # same
HEIGHT_MEAN_M = 7.1           # same
HEIGHT_MAX_M = 13.0           # same
TREE_COVER = 0.40             # same: the oaks' cover around the tower
DBH_CV = 0.418                # NEON DP1.10098.001 at SJER: 70 live blue oak stems >= 5 cm, each one's latest record
PLOT_M, CELL_M = 100.0, 10.0  # [m] the survey's plot, and the stand's cells
OAK_PFT, GRASS_PFT = 1, 2
GRASS_HEIGHT_M = 0.3          # [m] the grass PFT's hgt_max (pft_parameters.toml), written for reference only
# The grass's peak leaf area: the median over water years of each year's largest clip LAI (AmeriFlux BADM,
# direct harvests): Vaira's open grassland 2.55 (LAI_TOT, 2002-2014), the Tonzi understory 1.31 (LAI_U, 2001-2014).
LAI_OPEN, LAI_UNDER_OAK = 2.55, 1.31
TILLERS_OPEN = 2000.0         # [tillers m-2] in the open, a choice (see 4.); the under-oak density follows
OAK_LAI = 0.65                # the trees' LAI (Baldocchi et al. 2004, p. 16)
OAK_LAI_B2 = 0.6410495        # the PFT file's lai_b2 for the oaks (the repository's, ED2's BAAD fit)


def weibull_shape_for_cv(cv):
    """The Weibull shape whose coefficient of variation is cv (bisection; the CV falls as the shape rises)."""
    def wcv(k):
        g1, g2 = math.gamma(1 + 1 / k), math.gamma(1 + 2 / k)
        return math.sqrt(g2 / g1 ** 2 - 1)
    lo, hi = 0.2, 20.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        lo, hi = (mid, hi) if wcv(mid) > cv else (lo, mid)
    return 0.5 * (lo + hi)


def power_through_mean_and_max(dbh, h_mean, h_max):
    """H = A D^b through (largest D, h_max) whose mean over the stems is h_mean; returns A and b."""
    dmax = max(dbh)
    lo, hi = 1e-3, 5.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        lo, hi = (mid, hi) if st.mean((d / dmax) ** mid for d in dbh) > h_mean / h_max else (lo, mid)
    b = 0.5 * (lo + hi)
    return h_max / dmax ** b, b


def oak_stems():
    """The 194 stems' DBH [cm], largest first, at exactly the reported basal area."""
    n = int(round(STEMS_PER_HA * (PLOT_M / 100.0) ** 2))
    k = weibull_shape_for_cv(DBH_CV)
    qmd_cm = 100.0 * math.sqrt(BASAL_AREA_M2_HA / (STEMS_PER_HA * math.pi / 4))
    scale = qmd_cm / math.sqrt(math.gamma(1 + 2 / k))
    dbh = [scale * (-math.log(1 - (i - 0.5) / n)) ** (1 / k) for i in range(1, n + 1)]
    ba = sum(math.pi / 4 * (d / 100) ** 2 for d in dbh) / (PLOT_M / 100.0) ** 2
    return sorted((d * math.sqrt(BASAL_AREA_M2_HA / ba) for d in dbh), reverse=True)


def steady_litter(dbh, cells, pft_file):
    """The four steady-state litter streams [kgC m-2 day-1] of the stand: the oaks by make_census.py's
    litter_input, the grass's by the same routing with no wood."""
    oak = mc.pft_params(pft_file, OAK_PFT)
    with open(pft_file, "rb") as fh:
        mort_gamma = float(mc.tomllib.load(fh)["pft"]["mort_gamma"][OAK_PFT - 1])
    area = PLOT_M * PLOT_M
    streams, _ = mc.litter_input(np.asarray(dbh), area, oak, mort_gamma)
    grass = mc.pft_params(pft_file, GRASS_PFT)
    leaf_c = sum(n * CELL_M ** 2 for _, n in cells) * grass["lai_b1"] / grass["sla"] / area
    kept = 1.0 - grass["retained"]
    leaf_l = leaf_c * grass["leaf_turnover"] * kept / mc.YR_DAY
    root_l = grass["root_to_leaf"] * leaf_c * grass["fineroot_turnover"] * kept / mc.YR_DAY
    fl, agf = grass["f_labile_leaf"], grass["aboveground_frac"]
    streams["labile_grnd"] += leaf_l * fl * agf
    streams["labile_soil"] += leaf_l * fl * (1.0 - agf) + root_l * fl
    streams["struct_grnd"] += leaf_l * (1 - fl) * agf
    streams["struct_soil"] += leaf_l * (1 - fl) * (1.0 - agf) + root_l * (1 - fl)
    return streams


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", required=True)
    ap.add_argument("--pft-file", help="the site's PFT file, for the steady litter input of [soil_carbon]")
    args = ap.parse_args(argv)

    dbh = oak_stems()
    a, b = power_through_mean_and_max(dbh, HEIGHT_MEAN_M, HEIGHT_MAX_M)
    ncell = int(round((PLOT_M / CELL_M) ** 2))
    ntree = int(round(TREE_COVER * ncell))
    deal = []
    while len(deal) < len(dbh):
        deal += list(range(ntree)) + list(range(ntree - 1, -1, -1))
    tiller_leaf_area = LAI_OPEN / TILLERS_OPEN                       # [m2 per tiller] the PFT's lai_b1
    tillers_under = LAI_UNDER_OAK / tiller_leaf_area

    rows = []
    for d, cell in zip(dbh, deal):
        rows.append((cell + 1, round(d, 2), round(min(a * d ** b, HEIGHT_MAX_M), 2), OAK_PFT, 1.0 / CELL_M ** 2))
    for cell in range(ncell):
        rows.append((cell + 1, 0.0, GRASS_HEIGHT_M, GRASS_PFT, tillers_under if cell < ntree else TILLERS_OPEN))
    rows.sort(key=lambda r: (r[0], -r[1]))

    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "w") as fh:
        fh.write("# The Tonzi (US-Ton) stand, written by make_tonzi_census.py: oaks imputed from the survey's stand\n"
                 "# averages (NOT measured trees) and one grass row (dbh 0) per 10 m cell. height is for reference.\n")
        fh.write("site_id,patch_id,cohort_id,dbh,height,pft,nplant,patch_area\n")
        for i, (cell, d, h, pft, n) in enumerate(rows, start=1):
            fh.write(f"1,{cell},{i},{d},{h},{pft},{n:.6g},{CELL_M * CELL_M}\n")

    hts = [min(a * d ** b, HEIGHT_MAX_M) for d in dbh]
    oak_lai_b1 = OAK_LAI * PLOT_M ** 2 / sum((d * d * h) ** OAK_LAI_B2 for d, h in zip(dbh, hts))
    summary = {
        "oak_stems": len(dbh), "basal_area_m2_ha": round(sum(math.pi / 4 * (d / 100) ** 2 for d in dbh), 3),
        "mean_dbh_cm": round(st.mean(dbh), 2), "dbh_range_cm": [round(min(dbh), 2), round(max(dbh), 2)],
        "mean_height_m": round(st.mean(hts), 2), "treed_cells": ntree, "open_cells": ncell - ntree,
        "pft_file": {"height_allometry": "power", "b1Ht": round(math.log(a), 5), "b2Ht": round(b, 5),
                     "hgt_max": HEIGHT_MAX_M, "oak_lai_b1": round(oak_lai_b1, 6), "oak_lai_b2": OAK_LAI_B2,
                     "grass_lai_b1": round(tiller_leaf_area, 8), "grass_lai_b2": 0.0},
        "grass_tillers_m2": {"open": TILLERS_OPEN, "under_oak": round(tillers_under, 1)},
        "grass_peak_lai": {"open": LAI_OPEN, "under_oak": LAI_UNDER_OAK,
                           "site": round(TREE_COVER * LAI_UNDER_OAK + (1 - TREE_COVER) * LAI_OPEN, 3)},
    }
    print(f"wrote {args.out}: {len(rows)} rows")
    print(json.dumps(summary, indent=1))
    if args.pft_file:
        cells = [(cell, tillers_under if cell < ntree else TILLERS_OPEN) for cell in range(ncell)]
        print("[soil_carbon] steady-state litter input:")
        for k, v in steady_litter(dbh, cells, args.pft_file).items():
            print(f"  spinup_{k} = {v:.6e}")


if __name__ == "__main__":
    main()
