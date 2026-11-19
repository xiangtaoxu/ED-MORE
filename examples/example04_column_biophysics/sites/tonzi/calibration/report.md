# Fast calibration: tonzi

## Validation

**Passed**: the calibrated cost below the default's, and no target's RMSE more than 10% worse.

| target | default | calibrated | change |
|---|---|---|---|
| lw_up | 3.07 | 3.27 | +7% |
| le | 2.12 | 2.01 | -5% |
| h | 2.24 | 2.13 | -5% |
| gpp | 2.53 | 1.68 | -34% |
| ustar | 0.57 | 0.54 | -4% |

RMSE in units of each target's sigma. Cost: default 27383, calibrated 26584.4.

The full record with the slow tier on is the next check: run the calibrated configs (budgets closed; dry-season GPP and LE no worse than the default's).

## Keys

| key | kind | scope | MAP | 68 % | prior centre | prior z | sd ratio | note | prior source |
|---|---|---|---|---|---|---|---|---|---|
| vcmax25 | trait | plant_type | 63.1 | 54.98-71.65 | 113.3 | -0.71 | 0.11 |  | EEO: the coordination of the Rubisco- and light-limited rates at the site's grow |
| vcmax25_pft2 | trait | plant_type | 40.8 | 38.23-43.53 | 113.3 | -1.05 | 0.05 |  | EEO: the coordination of the Rubisco- and light-limited rates at the site's grow |
| stomatal_g1 | trait | plant_type | 2.855 | 2.458-3.314 | 4.45 | -1.20 | 0.39 |  | CLM5 medlynslope for deciduous broadleaf trees (Lin et al. 2015, Nature Climate  |
| stomatal_g1_pft2 | trait | plant_type | 3.134 | 2.718-3.607 | 1.92 | +0.95 | 0.27 |  | EEO: the least-cost optimum at the site's growing-season daytime climate (priors |
| stomatal_g0 | trait | plant_type | 0.006358 | 0.005553-0.007264 | 0.01 | -0.43 | 0.12 |  | the PFT file's value, a factor e either way: the residual conductance is poorly  |
| stomatal_g0_pft2 | trait | plant_type | 0.007552 | 0.002957-0.01712 | 0.01 | -0.27 | 0.85 |  | the PFT file's value, a factor e either way: the residual conductance is poorly  |
| z0m_ratio | effective | site | 0.1946 | 0.1832-0.2055 | 0.13 | +1.57 | 0.28 |  | the base value (ED2 0.13), +-0.04: closed canopies give z0/h of about 0.06-0.15  |
| wstress_sref_stomata | effective | plant_type | 4.432 | 3.74-5.127 | 0.6 | +3.11 | 0.37 |  | the PFT file's value, a factor 2 either way (Sabot et al. 2022 fit 0.5-5 across  |
| kappa | observation | observation | 0.8733 | 0.8319-0.9167 | 1 | -2.59 | 0.91 |  | the gap between the provider's night-time and daytime partitionings (RECO agains |

Fixed at their priors: wstress_sref_stomata_pft2 (dead: its gradient column is zero (a key the windows never use))

## Targets

| target | chi2/n | sigma scale | model/tower | n (cal) |
|---|---|---|---|---|
| lw_up | 1.00 | 2.94 | 1.029 | 2321 |
| le | 0.95 | 1.85 | 0.931 | 4780 |
| h | 1.06 | 1.89 | 0.968 | 677 |
| gpp | 0.35 | 2.61 | 1.041 | 941 |
| ustar | 0.29 | 1.00 | 0.919 | 1208 |

lw_up, model/tower by local hour: 0 h 1.04, 1 h 1.04, 2 h 1.04, 3 h 1.04, 4 h 1.04, 5 h 1.04, 6 h 1.03, 7 h 1.03, 8 h 1.02, 9 h 1.01, 10 h 1.00, 11 h 1.00, 12 h 1.00, 13 h 1.01, 14 h 1.02, 15 h 1.03, 16 h 1.04, 17 h 1.04, 18 h 1.05, 19 h 1.05, 20 h 1.05, 21 h 1.05, 22 h 1.05, 23 h 1.04
lw_up, by light: SW quartile 2 1.04, SW quartile 3 1.02, SW quartile 4 1.01

le, model/tower by local hour: 5 h -56.18, 6 h 1.40, 7 h 0.79, 8 h 0.66, 9 h 0.70, 10 h 0.72, 11 h 0.79, 12 h 0.87, 13 h 0.96, 14 h 1.09, 15 h 1.42, 16 h 1.70, 17 h 2.31, 18 h 2.30
le, by light: SW quartile 1 1.36, SW quartile 2 0.90, SW quartile 3 0.98, SW quartile 4 0.84

h, model/tower by local hour: 8 h 0.62, 9 h 0.75, 10 h 0.85, 11 h 0.91, 12 h 0.97, 13 h 0.98, 14 h 1.03, 15 h 1.12, 16 h 1.21, 17 h 1.46, 18 h 3.96
h, by light: SW quartile 1 1.52, SW quartile 2 0.94, SW quartile 3 0.92, SW quartile 4 0.94

gpp, model/tower by local hour: 6 h 1.17, 7 h 0.92, 8 h 0.91, 9 h 0.86, 10 h 0.95, 11 h 0.98, 12 h 1.02, 13 h 1.08, 14 h 1.14, 15 h 1.15, 16 h 1.28, 17 h 1.34, 18 h 1.45
gpp, by light: SW quartile 1 1.11, SW quartile 2 0.96, SW quartile 3 0.98, SW quartile 4 1.18

ustar, model/tower by local hour: 5 h 1.15, 6 h 0.75, 7 h 0.76, 8 h 0.75, 9 h 0.83, 10 h 0.89, 11 h 0.92, 12 h 0.95, 13 h 0.94, 14 h 0.96, 15 h 0.97, 16 h 0.96, 17 h 1.00, 18 h 1.12
ustar, by light: SW quartile 1 0.99, SW quartile 2 0.86, SW quartile 3 0.91, SW quartile 4 0.93

## kappa

kappa = 0.873: the tower's respiration 2.88 -> 3.30 umol m-2 s-1; GPP 4.96 -> 5.31 (1.88 -> 2.01 kgC m-2 yr-1), means over the records with GPP and its respiration measured, day and night; GPP gains the scaled respiration by day only.

## Uncertainty

Laplace, from the final gradient matrix.
- alternative gpp_ustar: the fit did not use the provider's threshold, or GPP's diagnostic finds no plateau
- alternative closure: the fit scored H and LE as measured ([closure].shares = "none"): no closure factor
- alternative partitioning (the provider's daytime partitioning (GPP_DT, RECO_DT)): largest linear shift 2.66 sd -- refitted: vcmax25 63.1->73.56, vcmax25_pft2 40.8->28.93, stomatal_g1 2.855->1.718, stomatal_g1_pft2 3.134->5.099, stomatal_g0 0.006358->0.005529, stomatal_g0_pft2 0.007552->0.003369, z0m_ratio 0.1946->0.1941, wstress_sref_stomata 4.432->2.969, kappa 0.8733->0.9479
