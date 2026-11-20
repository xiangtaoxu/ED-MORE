#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""The Toolik stand, synthesised from the site's harvest and cover: one cohort per PFT on one patch, for
ed_config_eval.toml's census start, with the PFT file's allometry and the soil carbon's steady litter.

The PFTs (pft_parameters.toml): 1 the tussock sedge (Eriophorum vaginatum, Carex bigelowii), a grass; 2 the
evergreen dwarf shrubs (Rhododendron tomentosum, Vaccinium vitis-idaea, Empetrum nigrum, Cassiope tetragona);
3 the deciduous dwarf shrubs (Betula nana, Salix pulchra, Vaccinium uliginosum). Forbs are left out.

1. The leaf area. The ARC LTER MAT06 control plots' harvest (August 2012, knb-lter-arc.20158.2, 15
   quadrats in moist acidic tussock tundra 10 km from the tower): each group's green leaves (the
   graminoids' blades, the shrubs' new and old leaves) times its PFT's specific leaf area (the PFT
   file's sla, at 0.5 gC per g of leaf) is the harvest's leaf area. NEON's 1 m2 cover at TOOL
   (DP1.10058.001, 2019-2024, the run's years) splits that total among the PFTs: cover is the leaves'
   projection.
2. The shrubs' stems: each shrub PFT keeps the harvest's above-ground stems (new and old) per leaf area.
3. One cohort per shrub PFT, at its PFT's height cap (hgt_max) and at the diameter at the ground whose
   allometric height that is: Berner, Orndahl & Burns 2023's dwarf birch (Arctic Data Center,
   doi:10.18739/A2QV3C526): above-ground dry mass 21.09 BD^3.01 g, BD [cm] at the ground (n 43, R2 0.97);
   height 27.16 BD^0.526 cm, fitted here in log-log on its 43 stems (R2 0.27). No such allometry was
   found for evergreen dwarf shrubs, so both shrub PFTs take the birch's. A stem is that mass less its
   leaves, at the PFT's leaf share in MAT06; nplant = the PFT's stems over one stem's.
4. The sedge: one row of tillers, diameter 0, at its PFT's height. No count of tillers was found; in a
   frozen stand only the leaf area matters, so TILLERS is a choice and lai_b1 its leaf area over it.

It prints the values the PFT file holds (the allometry the census assumes) and the [soil_carbon] steady
litter input; a PFT file that differs is reported.

Usage:
  python make_toolik_census.py --data <toolik data> --out data/toolik_census_ed.csv [--pft-file pft_parameters.toml]
"""
import argparse
import glob
import json
import math
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "..", "scripts", "prepare_input", "census"))
import make_census as mc                # noqa: E402

C_PER_DRY = 0.5                         # [gC/g] as ED-MORE's C2B
SEDGE, EVERGREEN, DECIDUOUS = 1, 2, 3
MAT06 = os.path.join("arc_lter", "knb-lter-arc.20158.2_MAT06_biomass_2012", "2012lgMAT06_abovebiomass.csv")
GROUP_PFT = {"Graminoids": SEDGE, "Evergreen": EVERGREEN, "Deciduous": DECIDUOUS}
LEAF_TISSUES = {"Graminoids": ("blade",), "Evergreen": ("new leaves", "old leaves"), "Deciduous": ("new leaves",)}
STEM_TISSUES = ("new stems", "old stems")
# NEON's species by PFT, by genus (or species where a genus spans two).
FORM = {"Eriophorum": SEDGE, "Carex": SEDGE, "Luzula": SEDGE, "Calamagrostis": SEDGE, "Arctagrostis": SEDGE,
        "Hierochloe": SEDGE, "Poa": SEDGE,
        "Rhododendron": EVERGREEN, "Ledum": EVERGREEN, "Vaccinium vitis-idaea": EVERGREEN, "Empetrum": EVERGREEN,
        "Cassiope": EVERGREEN, "Andromeda": EVERGREEN, "Loiseleuria": EVERGREEN, "Dryas": EVERGREEN,
        "Diapensia": EVERGREEN,
        "Betula": DECIDUOUS, "Salix": DECIDUOUS, "Vaccinium uliginosum": DECIDUOUS, "Arctostaphylos": DECIDUOUS}
COVER_YEARS = range(2019, 2025)
BERNER_MASS = (21.09, 3.01)             # [g], [-] above-ground dry mass = a BD^b, BD [cm] at the ground
BERNER_HEIGHT = (27.16, 0.526)          # [cm], [-] height = a BD^b
TILLERS = 1000.0                        # [tillers m-2] the sedge's, a choice (see 4.)


def harvest(data):
    """MAT06's control plots [g dry m-2]: each PFT's green leaves and above-ground stems."""
    d = pd.read_csv(os.path.join(data, MAT06), encoding="latin-1")
    d = d[d["Treatment"] == "CT"]
    leaves, stems = {}, {}
    for group, pft in GROUP_PFT.items():
        g = d[d["Growth Form"] == group]
        leaves[pft] = float(g[g["Tissue"].isin(LEAF_TISSUES[group])]["Average g/m2"].sum())
        stems[pft] = float(g[g["Tissue"].isin(STEM_TISSUES)]["Average g/m2"].sum())
    return leaves, stems


def pft_of(name):
    if not isinstance(name, str):
        return None
    for key, pft in FORM.items():
        if name.startswith(key):
            return pft
    return None


def cover_shares(data):
    """Each PFT's share of the vascular cover: the mean over COVER_YEARS of each year's mean cover per
    1 m2 subplot."""
    files = sorted(glob.glob(os.path.join(data, "neon", "DP1.10058.001", "*", "*div_1m2Data*")))
    c = pd.concat([pd.read_csv(f, low_memory=False) for f in files])
    c = c[c["taxonID"].notna()].copy()
    c["year"] = c["endDate"].str[:4].astype(int)
    c = c[c["year"].isin(COVER_YEARS)]
    c["pft"] = c["scientificName"].map(pft_of)
    c["subplot"] = c["plotID"] + "_" + c["subplotID"].astype(str) + "_" + c["eventID"].astype(str)
    per = c.dropna(subset=["pft"]).groupby(["year", "subplot", "pft"])["percentCover"].sum().unstack(fill_value=0.0)
    yearly = per.groupby(level="year").mean()
    mean = yearly.mean()
    return {int(p): float(mean[p] / mean.sum()) for p in mean.index}, yearly.round(1)


def shrub_allometry(leaf_share, rho, hgt_max):
    """The birch's laws as the PFT file holds them (D [cm], H [m], AGB [kgC]): height exp(b1Ht) D^b2Ht,
    stem AGB agb_c1 rho^agb_c2 (D^2 H)^agb_c2 = the above-ground mass less the leaves, and the leaf area
    following the above-ground mass, lai_b2 = agb_c2; the cohort's diameter at the height cap."""
    (a, b), (ha, hb) = BERNER_MASS, BERNER_HEIGHT
    b1ht, b2ht = math.log(ha / 100.0), hb
    c2 = b / (2.0 + hb)
    c1 = 1.0e-3 * C_PER_DRY * (1.0 - leaf_share) * a / (rho ** c2 * math.exp(b1ht * c2))
    diameter = (100.0 * hgt_max / ha) ** (1.0 / hb)
    stem = 1.0e-3 * C_PER_DRY * (1.0 - leaf_share) * a * diameter ** b        # [kgC per plant]
    return dict(b1Ht=b1ht, b2Ht=b2ht, agb_c1=c1, agb_c2=c2, lai_b2=c2), diameter, stem


def steady_litter(cohorts, pft_file):
    """The four steady-state litter streams [kgC m-2 day-1]: each shrub cohort by make_census.py's
    litter_input (one plant per 1/nplant m2), the sedge's by the same routing with no wood."""
    with open(pft_file, "rb") as fh:
        mort_gamma = mc.tomllib.load(fh)["pft"]["mort_gamma"]
    streams = {"labile_grnd": 0.0, "labile_soil": 0.0, "struct_grnd": 0.0, "struct_soil": 0.0}
    for pft, diameter, nplant, _ in cohorts:
        pp = mc.pft_params(pft_file, pft)
        if pft == SEDGE:
            leaf_c = nplant * pp["lai_b1"] / pp["sla"]
            kept = 1.0 - pp["retained"]
            leaf_l = leaf_c * pp["leaf_turnover"] * kept / mc.YR_DAY
            root_l = pp["root_to_leaf"] * leaf_c * pp["fineroot_turnover"] * kept / mc.YR_DAY
            fl, agf = pp["f_labile_leaf"], pp["aboveground_frac"]
            streams["labile_grnd"] += leaf_l * fl * agf
            streams["labile_soil"] += leaf_l * fl * (1.0 - agf) + root_l * fl
            streams["struct_grnd"] += leaf_l * (1 - fl) * agf
            streams["struct_soil"] += leaf_l * (1 - fl) * (1.0 - agf) + root_l * (1 - fl)
        else:
            one, _ = mc.litter_input(np.asarray([diameter]), 1.0 / nplant, pp, float(mort_gamma[pft - 1]))
            for k, v in one.items():
                streams[k] += v
    return streams


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--data", required=True, help="the Toolik data folder (arc_lter/, neon/)")
    ap.add_argument("--out", required=True)
    ap.add_argument("--pft-file", default=os.path.join(HERE, "pft_parameters.toml"))
    args = ap.parse_args(argv)

    leaves, stems = harvest(args.data)
    shares, yearly = cover_shares(args.data)
    pp = {p: mc.pft_params(args.pft_file, p) for p in (SEDGE, EVERGREEN, DECIDUOUS)}
    area_harvest = {p: leaves[p] * 1.0e-3 * C_PER_DRY * pp[p]["sla"] for p in pp}       # [m2 m-2]
    total = sum(area_harvest.values())
    lai = {p: total * shares[p] for p in pp}

    cohorts, pft_values = [], {"lai_b1": {}, "lai_b2": {}, "wai_b1": {}}
    cohorts.append((SEDGE, 0.0, TILLERS, pp[SEDGE]["hgt_max"]))
    pft_values["lai_b1"][SEDGE] = lai[SEDGE] / TILLERS
    pft_values["lai_b2"][SEDGE] = 0.0
    pft_values["wai_b1"][SEDGE] = 0.0
    for p in (EVERGREEN, DECIDUOUS):
        leaf_share = leaves[p] / (leaves[p] + stems[p])
        allom, diameter, stem = shrub_allometry(leaf_share, pp[p]["rho"], pp[p]["hgt_max"])
        stems_c = stems[p] * lai[p] / area_harvest[p] * 1.0e-3 * C_PER_DRY            # [kgC m-2]
        nplant = stems_c / stem
        height = pp[p]["hgt_max"]
        cohorts.append((p, diameter, nplant, height))
        pft_values[f"pft{p}"] = {k: round(v, 6) for k, v in allom.items()}
        pft_values["lai_b1"][p] = lai[p] / (nplant * (diameter * diameter * height) ** allom["lai_b2"])
        pft_values["lai_b2"][p] = allom["lai_b2"]
        pft_values["wai_b1"][p] = 0.01 * height                                       # [m2 per cm of stem]
        for key in ("b1Ht", "b2Ht", "agb_c1", "agb_c2"):
            have = pp[p][key]
            if not math.isclose(have, allom[key], rel_tol=1.0e-4):
                print(f"NOTE: the PFT file's {key} for PFT {p} is {have}, the census assumes {allom[key]:.6g}")

    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "w") as fh:
        fh.write("# The Toolik stand (NEON TOOL), written by make_toolik_census.py: one cohort per PFT synthesised from\n"
                 "# MAT06's harvest and NEON's cover (NOT measured plants). height is for reference.\n")
        fh.write("site_id,patch_id,cohort_id,diameter,height,pft,nplant,patch_area\n")
        for i, (p, diameter, nplant, height) in enumerate(cohorts, start=1):
            fh.write(f"1,1,{i},{diameter:.4f},{height:.3f},{p},{nplant:.6g},1.0\n")

    summary = {"harvest_leaves_g_m2": leaves, "harvest_stems_g_m2": stems,
               "harvest_leaf_area": {p: round(v, 3) for p, v in area_harvest.items()}, "harvest_lai": round(total, 3),
               "cover_shares": {p: round(v, 3) for p, v in shares.items()},
               "lai": {p: round(v, 3) for p, v in lai.items()},
               "cohorts": [{"pft": p, "diameter_cm": round(d, 4), "nplant_m2": round(n, 3), "height_m": h}
                           for p, d, n, h in cohorts],
               "pft_file": {"lai_b1": {p: float(f"{v:.6g}") for p, v in pft_values["lai_b1"].items()},
                            "lai_b2": {p: round(v, 6) for p, v in pft_values["lai_b2"].items()},
                            "wai_b1": pft_values["wai_b1"], "wai_b2": 1.0,
                            **{k: v for k, v in pft_values.items() if k.startswith("pft")}}}
    print(f"wrote {args.out}: {len(cohorts)} cohorts")
    print("NEON cover by PFT [%], mean per 1 m2 subplot:\n" + yearly.to_string())
    print(json.dumps(summary, indent=1))
    print("[soil_carbon] steady-state litter input:")
    for k, v in steady_litter(cohorts, args.pft_file).items():
        print(f"  spinup_{k} = {v:.6e}")


if __name__ == "__main__":
    main()
