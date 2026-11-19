# Fast calibration: tonzi

## Validation

**Passed**: the calibrated cost below the default's, and no target's RMSE more than 10% worse.

| target | default | calibrated | change |
|---|---|---|---|
| lw_up | 2.88 | 2.91 | +1% |
| le | 2.10 | 1.96 | -7% |
| h | 2.20 | 2.07 | -6% |
| gpp | 2.55 | 2.74 | +7% |
| ustar | 0.58 | 0.54 | -6% |

RMSE in units of each target's sigma. Cost: default 25987.9, calibrated 25756.

The full record with the slow tier on is the next check: run the calibrated configs (budgets closed; dry-season GPP and LE no worse than the default's).

## Keys

| key | kind | scope | MAP | 68 % | prior centre | prior z | sd ratio | note | prior source |
|---|---|---|---|---|---|---|---|---|---|
| leaf_angle_mean | trait | plant_type | 41.86 | 30.76-53.63 | 63 | -1.70 | 0.88 |  | the PFT file's value, +-10 degrees; spherical leaves average 57.3. The range is  |
| leaf_angle_mean_pft2 | trait | plant_type | 46.45 | 35.92-56.71 | 63.24 | -1.37 | 0.78 |  | the PFT file's value, +-10 degrees; spherical leaves average 57.3. The range is  |
| vcmax25 | trait | plant_type | 39.97 | 36.54-43.71 | 113.3 | -1.06 | 0.07 |  | EEO: the coordination of the Rubisco- and light-limited rates at the site's grow |
| vcmax25_pft2 | trait | plant_type | 89.95 | 86.07-93.74 | 113.3 | -0.35 | 0.05 |  | EEO: the coordination of the Rubisco- and light-limited rates at the site's grow |
| stomatal_g1 | trait | plant_type | 1.542 | 1.344-1.786 | 4.45 | -2.88 | 0.42 | beyond 2 prior sd, pushed by le: diagnose it (plan §5.1) or relabel it effective | CLM5 medlynslope for deciduous broadleaf trees (Lin et al. 2015, Nature Climate  |
| stomatal_g1_pft2 | trait | plant_type | 2.93 | 2.601-3.297 | 1.92 | +0.82 | 0.23 |  | EEO: the least-cost optimum at the site's growing-season daytime climate (priors |
| stomatal_g0 | trait | plant_type | 0.006541 | 0.005283-0.008053 | 0.01 | -0.41 | 0.20 |  | the PFT file's value, a factor e either way: the residual conductance is poorly  |
| stomatal_g0_pft2 | trait | plant_type | 0.005101 | 0.001744-0.01368 | 0.01 | -0.64 | 0.96 |  | the PFT file's value, a factor e either way: the residual conductance is poorly  |
| z0m_ratio | effective | site | 0.1994 | 0.1872-0.2111 | 0.13 | +1.69 | 0.31 |  | the base value (ED2 0.13), +-0.04: closed canopies give z0/h of about 0.06-0.15  |
| wstress_sref_stomata | effective | plant_type | 0.6298 | 0.3431-1.246 | 0.6 | +0.07 | 0.94 |  | the PFT file's value, a factor 2 either way (Sabot et al. 2022 fit 0.5-5 across  |
| kappa | observation | observation | 0.8833 | 0.8488-0.919 | 1 | -2.38 | 0.74 |  | the gap between the provider's night-time and daytime partitionings (RECO agains |

Fixed at their priors: wstress_sref_stomata_pft2 (dead: its gradient column is zero (a key the windows never use))

## Targets

| target | chi2/n | sigma scale | model/tower | n (cal) |
|---|---|---|---|---|
| lw_up | 1.13 | 3.00 | 1.030 | 2321 |
| le | 0.91 | 1.94 | 0.865 | 4780 |
| h | 1.00 | 2.08 | 0.899 | 677 |
| gpp | 0.88 | 1.55 | 0.972 | 941 |
| ustar | 0.31 | 1.00 | 0.910 | 1208 |

lw_up, model/tower by local hour: 0 h 1.05, 1 h 1.05, 2 h 1.04, 3 h 1.04, 4 h 1.04, 5 h 1.04, 6 h 1.02, 7 h 1.02, 8 h 1.00, 9 h 0.99, 10 h 0.99, 11 h 0.99, 12 h 1.00, 13 h 1.01, 14 h 1.02, 15 h 1.03, 16 h 1.04, 17 h 1.05, 18 h 1.06, 19 h 1.06, 20 h 1.05, 21 h 1.05, 22 h 1.05, 23 h 1.05
lw_up, by light: SW quartile 2 1.05, SW quartile 3 1.02, SW quartile 4 1.00

le, model/tower by local hour: 5 h -55.77, 6 h 1.39, 7 h 0.73, 8 h 0.58, 9 h 0.63, 10 h 0.66, 11 h 0.72, 12 h 0.80, 13 h 0.89, 14 h 1.01, 15 h 1.36, 16 h 1.66, 17 h 2.27, 18 h 2.37
le, by light: SW quartile 1 1.30, SW quartile 2 0.81, SW quartile 3 0.89, SW quartile 4 0.80

h, model/tower by local hour: 8 h 0.53, 9 h 0.66, 10 h 0.77, 11 h 0.85, 12 h 0.91, 13 h 0.92, 14 h 0.96, 15 h 1.05, 16 h 1.15, 17 h 1.43, 18 h 3.69
h, by light: SW quartile 1 1.46, SW quartile 2 0.85, SW quartile 3 0.84, SW quartile 4 0.89

gpp, model/tower by local hour: 6 h 1.00, 7 h 0.81, 8 h 0.83, 9 h 0.80, 10 h 0.90, 11 h 0.94, 12 h 0.98, 13 h 1.03, 14 h 1.07, 15 h 1.07, 16 h 1.14, 17 h 1.18, 18 h 1.41
gpp, by light: SW quartile 1 1.00, SW quartile 2 0.89, SW quartile 3 0.94, SW quartile 4 1.11

ustar, model/tower by local hour: 5 h 1.12, 6 h 0.73, 7 h 0.74, 8 h 0.72, 9 h 0.80, 10 h 0.87, 11 h 0.91, 12 h 0.95, 13 h 0.93, 14 h 0.95, 15 h 0.96, 16 h 0.96, 17 h 1.02, 18 h 1.13
ustar, by light: SW quartile 1 1.01, SW quartile 2 0.84, SW quartile 3 0.89, SW quartile 4 0.93

## kappa

kappa = 0.883: the tower's respiration 2.88 -> 3.26 umol m-2 s-1; GPP 4.96 -> 5.28 (1.88 -> 2.00 kgC m-2 yr-1), means over the records with GPP and its respiration measured, day and night; GPP gains the scaled respiration by day only.

## Uncertainty

Laplace, from the final gradient matrix -- LOCAL ONLY (the linearity check failed).
- alternative gpp_ustar: the fit did not use the provider's threshold, or GPP's diagnostic finds no plateau
- alternative closure: the fit scored H and LE as measured ([closure].shares = "none"): no closure factor
- alternative partitioning (the provider's daytime partitioning (GPP_DT, RECO_DT)): largest linear shift 5.05 sd -- refitted: leaf_angle_mean 41.86->46.89, leaf_angle_mean_pft2 46.45->21.82, vcmax25 39.97->34.65, vcmax25_pft2 89.95->70.92, stomatal_g1 1.542->1.474, stomatal_g1_pft2 2.93->3.878, stomatal_g0 0.006541->0.00403, stomatal_g0_pft2 0.005101->0.007421, z0m_ratio 0.1994->0.1973, wstress_sref_stomata 0.6298->2.922, kappa 0.8833->0.9625
