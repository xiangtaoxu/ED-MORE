# Fast calibration: tonzi

## Validation

**Passed**: the calibrated cost below the default's, and no target's RMSE more than 10% worse.

| target | default | calibrated | change |
|---|---|---|---|
| lw_up | 2.91 | 2.91 | +0% |
| le | 3.59 | 2.41 | -33% |
| h | 3.09 | 2.66 | -14% |
| gpp | 3.23 | 2.25 | -30% |
| ustar | 0.64 | 0.55 | -15% |

RMSE in units of each target's sigma. Cost: default 35222.7, calibrated 26747.

The full record with the slow tier on is the next check: run the calibrated configs (budgets closed; dry-season GPP and LE no worse than the default's).

## Keys

| key | kind | scope | MAP | 68 % | prior centre | prior z | sd ratio | note | prior source |
|---|---|---|---|---|---|---|---|---|---|
| leaf_angle_mean | trait | plant_type | 47.59 | 36.02-58.61 | 63 | -1.27 | 0.87 |  | the PFT file's value, +-10 degrees; spherical leaves average 57.3. The range is  |
| leaf_angle_mean_pft2 | trait | plant_type | 47.61 | 36.67-58.05 | 63.24 | -1.28 | 0.81 |  | the PFT file's value, +-10 degrees; spherical leaves average 57.3. The range is  |
| vcmax25 | trait | plant_type | 60.77 | 54.05-67.85 | 113.3 | -0.74 | 0.10 |  | EEO: the coordination of the Rubisco- and light-limited rates at the site's grow |
| vcmax25_pft2 | trait | plant_type | 75.5 | 72.4-78.61 | 113.3 | -0.54 | 0.04 |  | EEO: the coordination of the Rubisco- and light-limited rates at the site's grow |
| stomatal_g1 | trait | plant_type | 0.7636 | 0.6736-0.9033 | 1.92 | -2.48 | 0.64 | beyond 2 prior sd, pushed by gpp: diagnose it (plan §5.1) or relabel it effective | EEO: the least-cost optimum at the site's growing-season daytime climate (priors |
| stomatal_g1_pft2 | trait | plant_type | 4.132 | 3.773-4.514 | 1.92 | +1.49 | 0.18 |  | EEO: the least-cost optimum at the site's growing-season daytime climate (priors |
| stomatal_g0 | trait | plant_type | 0.00269 | 0.002131-0.003401 | 0.01 | -1.21 | 0.21 |  | the PFT file's value, a factor e either way: the residual conductance is poorly  |
| stomatal_g0_pft2 | trait | plant_type | 0.003952 | 0.001449-0.01039 | 0.01 | -0.87 | 0.90 |  | the PFT file's value, a factor e either way: the residual conductance is poorly  |
| z0m_ratio | effective | site | 0.1976 | 0.185-0.2095 | 0.13 | +1.65 | 0.32 |  | the base value (ED2 0.13), +-0.04: closed canopies give z0/h of about 0.06-0.15  |
| kappa | observation | observation | 0.84 | 0.8076-0.8739 | 1 | -3.32 | 0.74 |  | the gap between the provider's night-time and daytime partitionings (RECO agains |

Fixed at their priors: wstress_sref_stomata (dead: its gradient column is zero (a key the windows never use)); wstress_sref_stomata_pft2 (dead: its gradient column is zero (a key the windows never use))

## Targets

| target | chi2/n | sigma scale | model/tower | n (cal) |
|---|---|---|---|---|
| lw_up | 1.13 | 3.00 | 1.029 | 2321 |
| le | 1.01 | 1.97 | 0.738 | 4780 |
| h | 1.01 | 2.55 | 0.750 | 677 |
| gpp | 0.90 | 1.53 | 0.993 | 941 |
| ustar | 0.33 | 1.00 | 0.899 | 1208 |

lw_up, model/tower by local hour: 0 h 1.05, 1 h 1.05, 2 h 1.04, 3 h 1.04, 4 h 1.04, 5 h 1.04, 6 h 1.02, 7 h 1.02, 8 h 1.00, 9 h 0.99, 10 h 0.99, 11 h 0.99, 12 h 1.00, 13 h 1.01, 14 h 1.02, 15 h 1.03, 16 h 1.04, 17 h 1.05, 18 h 1.06, 19 h 1.06, 20 h 1.05, 21 h 1.05, 22 h 1.05, 23 h 1.05
lw_up, by light: SW quartile 2 1.05, SW quartile 3 1.02, SW quartile 4 1.00

le, model/tower by local hour: 5 h -49.03, 6 h 1.08, 7 h 0.64, 8 h 0.51, 9 h 0.55, 10 h 0.57, 11 h 0.62, 12 h 0.68, 13 h 0.75, 14 h 0.87, 15 h 1.16, 16 h 1.39, 17 h 1.81, 18 h 1.36
le, by light: SW quartile 1 1.06, SW quartile 2 0.71, SW quartile 3 0.78, SW quartile 4 0.67

h, model/tower by local hour: 8 h 0.42, 9 h 0.54, 10 h 0.64, 11 h 0.71, 12 h 0.76, 13 h 0.77, 14 h 0.80, 15 h 0.87, 16 h 0.97, 17 h 1.24, 18 h 3.45
h, by light: SW quartile 1 1.25, SW quartile 2 0.71, SW quartile 3 0.70, SW quartile 4 0.73

gpp, model/tower by local hour: 6 h 1.07, 7 h 0.88, 8 h 0.88, 9 h 0.82, 10 h 0.92, 11 h 0.96, 12 h 1.00, 13 h 1.06, 14 h 1.10, 15 h 1.09, 16 h 1.14, 17 h 1.13, 18 h 1.22
gpp, by light: SW quartile 1 1.01, SW quartile 2 0.93, SW quartile 3 0.97, SW quartile 4 1.10

ustar, model/tower by local hour: 5 h 1.14, 6 h 0.72, 7 h 0.71, 8 h 0.70, 9 h 0.79, 10 h 0.86, 11 h 0.90, 12 h 0.93, 13 h 0.92, 14 h 0.94, 15 h 0.95, 16 h 0.95, 17 h 1.01, 18 h 1.15
ustar, by light: SW quartile 1 0.99, SW quartile 2 0.83, SW quartile 3 0.88, SW quartile 4 0.92

## kappa

kappa = 0.840: the tower's respiration 2.88 -> 3.43 umol m-2 s-1; GPP 4.96 -> 5.42 (1.88 -> 2.05 kgC m-2 yr-1), means over the records with GPP and its respiration measured, day and night; GPP gains the scaled respiration by day only.

## Uncertainty

Laplace, from the final gradient matrix -- LOCAL ONLY (the linearity check failed).
- alternative gpp_ustar: the fit did not use the provider's threshold, or GPP's diagnostic finds no plateau
- alternative closure: the fit already used Bowen
- alternative partitioning (the provider's daytime partitioning (GPP_DT, RECO_DT)): largest linear shift 5.15 sd -- refitted: leaf_angle_mean 47.59->63.87, leaf_angle_mean_pft2 47.61->27.06, vcmax25 60.77->48.66, vcmax25_pft2 75.5->58.86, stomatal_g1 0.7636->0.9583, stomatal_g1_pft2 4.132->5.169, stomatal_g0 0.00269->0.002074, stomatal_g0_pft2 0.003952->0.005832, z0m_ratio 0.1976->0.2022, kappa 0.84->0.9393
