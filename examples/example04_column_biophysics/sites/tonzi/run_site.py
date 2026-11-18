#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""ED-MORE example 04, the Tonzi Ranch site -- the coupled column at the US-Ton blue-oak savanna tower, end to end.

Steps (the tower file, the forcing and the census file are kept once made; --force remakes them):
  1. the tower file data/tonzi_tower.csv: the tower's measured meteorology and fluxes (AmeriFlux US-Ton,
     FLUXNET), its own rain gauge and barometer and its understory eddy covariance (US-Ton's BASE file),
     and Vaira Ranch's longwave, pressure and rain where US-Ton has none (US-Var's BASE file)
     (prepare_tower.py)
  2. the forcing file data/tonzi_forcing.nc (scripts/prepare_input/flux_tower/make_tower_forcing.py)
  3. the census file: the oaks imputed from the site survey's stand averages, and the grass
     (make_tonzi_census.py)
  4. the ten tower years from the census, with hourly output (ed_config_eval.toml)
  5. with --calibrate: the fast parameters fitted to the tower (calibration.toml, scripts/calibrate_fast)
  6. the calibrated run, when calibration/ed_config_calibrated.toml exists
  7. the runs against the tower (plot_evaluation.py), and the season of the oaks and the grass
     (plot_seasons.py)

The data: --ameriflux is the US-Ton FLUXNET zip (AMF_US-Ton_FLUXNET_2001-2025_v1.3_r1.zip) and --badm the
folder holding the BASE-BADM zips of US-Ton and US-Var (AMF_US-Ton_BASE-BADM_27-5.zip,
AMF_US-Var_BASE-BADM_27-5.zip), all from AmeriFlux with an account.

Usage:
  python run_site.py --ameriflux <zip> --badm <folder>       # every step but the calibration
  python run_site.py --forcing-only ...                       # steps 1-2
  python run_site.py --calibrate --workers 40 ...             # and redo the calibration

Needs numpy, pandas, netCDF4, matplotlib, and a built edmore (--edmore, or EDMORE_MAIN; default
../../../../build-dev/edmore).
"""
import argparse
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
TOOLS = os.path.join(ROOT, "scripts", "prepare_input")
CALIBRATE_FAST = os.path.join(ROOT, "scripts", "calibrate_fast", "calibrate_fast.py")
DATA = os.path.join(HERE, "data")
OUTPUT = os.path.join(HERE, "output")
CALIB = os.path.join(HERE, "calibration")
BADM = ("AMF_US-Ton_BASE-BADM_27-5.zip", "AMF_US-Var_BASE-BADM_27-5.zip")


def run(cmd, log=None):
    print("+", " ".join(cmd), flush=True)
    if log:
        with open(log, "w") as fh:
            status = subprocess.call(cmd, cwd=HERE, stdout=fh, stderr=subprocess.STDOUT)
        if status:
            raise SystemExit(f"ERROR: {cmd[0]} failed; see {log}")
    else:
        subprocess.check_call(cmd, cwd=HERE)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--ameriflux", default=os.environ.get("TONZI_AMERIFLUX"), help="the US-Ton FLUXNET zip")
    ap.add_argument("--badm", default=os.environ.get("TONZI_BADM"), help="the folder of the BASE-BADM zips")
    ap.add_argument("--edmore", default=os.environ.get("EDMORE_MAIN", os.path.join(ROOT, "build-dev", "edmore")))
    ap.add_argument("--forcing-only", action="store_true", help="stop after the forcing")
    ap.add_argument("--force", action="store_true", help="remake the tower file, the forcing and the census file")
    ap.add_argument("--calibrate", action="store_true", help="redo the fast-parameter fit (step 5)")
    ap.add_argument("--workers", type=int, default=os.cpu_count(), help="trials at once for --calibrate")
    args = ap.parse_args(argv)
    py = sys.executable
    os.makedirs(DATA, exist_ok=True)
    os.makedirs(OUTPUT, exist_ok=True)

    tower = os.path.join(DATA, "tonzi_tower.csv")
    forcing = os.path.join(DATA, "tonzi_forcing.nc")
    census = os.path.join(DATA, "tonzi_census_ed.csv")
    if args.force or not os.path.exists(tower):
        if not (args.ameriflux and args.badm):
            raise SystemExit("ERROR: the tower file needs --ameriflux and --badm (see the docstring)")
        run([py, "prepare_tower.py", "--ameriflux", args.ameriflux,
             "--ton-base", os.path.join(args.badm, BADM[0]), "--var-base", os.path.join(args.badm, BADM[1]),
             "--out", tower])
    if args.force or not os.path.exists(forcing):
        run([py, os.path.join(TOOLS, "flux_tower", "make_tower_forcing.py"), "--site", "tonzi_site.toml",
             "--out", forcing])
    if args.forcing_only:
        return

    if not os.path.exists(args.edmore):
        raise SystemExit(f"ERROR: no edmore at {args.edmore}; build ED-MORE or pass --edmore")
    if args.force or not os.path.exists(census):
        run([py, "make_tonzi_census.py", "--out", census, "--pft-file", "pft_parameters.toml"])
    run([args.edmore, "ed_config_eval.toml"], log=os.path.join(OUTPUT, "eval.log"))
    if args.calibrate:
        work = os.path.join(CALIB, "run")
        run([py, CALIBRATE_FAST, "fit", "--config", "calibration.toml", "--work", work,
             "--runner", args.edmore, "--workers", str(args.workers)])
        os.makedirs(CALIB, exist_ok=True)
        for name in ("fit.json", "report.md", "ed_config_calibrated.toml", "pft_parameters_calibrated.toml"):
            shutil.copyfile(os.path.join(work, name), os.path.join(CALIB, name))
    calibrated = os.path.join(CALIB, "ed_config_calibrated.toml")
    if not os.path.exists(calibrated):
        run([py, "plot_evaluation.py"])
        run([py, "plot_seasons.py", "--badm", args.badm or ""] if args.badm else [py, "plot_seasons.py"])
        return
    run([args.edmore, calibrated], log=os.path.join(OUTPUT, "cal.log"))
    run([py, "plot_evaluation.py", "--calibrated", os.path.join(OUTPUT, "cal-F-*.nc")])
    run([py, "plot_seasons.py", "--model", os.path.join(OUTPUT, "cal-D.nc")]
        + (["--badm", args.badm] if args.badm else []))


if __name__ == "__main__":
    main()
