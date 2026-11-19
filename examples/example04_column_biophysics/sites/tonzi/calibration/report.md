# Fast calibration: tonzi

## Validation

**Failed**: the calibrated cost below the default's, and no target's RMSE more than 10% worse.

| target | default | calibrated | change |
|---|---|---|---|
| lw_up | 2.88 | 2.95 | +2% |
| le | 2.32 | 2.42 | +5% |
| h | 2.74 | 2.60 | -5% |
| gpp | 2.55 | 2.58 | +1% |
| ustar | 0.58 | 0.54 | -6% |

RMSE in units of each target's sigma. Cost: default 27233.2, calibrated 27818.5.

The full record with the slow tier on is the next check: run the calibrated configs (budgets closed; dry-season GPP and LE no worse than the default's).

## Keys

| key | kind | scope | MAP | 68 % | prior centre | prior z | sd ratio | note | prior source |
|---|---|---|---|---|---|---|---|---|---|
| leaf_angle_mean | trait | plant_type | 58.8 | 47.16-67.68 | 63 | -0.39 | 0.91 |  | the PFT file's value, +-10 degrees; spherical leaves average 57.3. The range is  |
| leaf_angle_mean_pft2 | trait | plant_type | 51.73 | 40.52-61.68 | 63.24 | -0.98 | 0.82 |  | the PFT file's value, +-10 degrees; spherical leaves average 57.3. The range is  |
| vcmax25 | trait | plant_type | 49.31 | 43.32-55.87 | 113.3 | -0.90 | 0.10 |  | EEO: the coordination of the Rubisco- and light-limited rates at the site's grow |
| vcmax25_pft2 | trait | plant_type | 87.01 | 83.28-90.68 | 113.3 | -0.39 | 0.05 |  | EEO: the coordination of the Rubisco- and light-limited rates at the site's grow |
| stomatal_g1 | trait | plant_type | 0.9273 | 0.7929-1.127 | 1.92 | -1.76 | 0.56 |  | EEO: the least-cost optimum at the site's growing-season daytime climate (priors |
| stomatal_g1_pft2 | trait | plant_type | 3.43 | 2.995-3.917 | 1.92 | +1.12 | 0.26 |  | EEO: the least-cost optimum at the site's growing-season daytime climate (priors |
| stomatal_g0 | trait | plant_type | 0.002562 | 0.00188-0.003504 | 0.01 | -1.25 | 0.28 |  | the PFT file's value, a factor e either way: the residual conductance is poorly  |
| stomatal_g0_pft2 | trait | plant_type | 0.01083 | 0.00412-0.02378 | 0.01 | +0.08 | 0.91 |  | the PFT file's value, a factor e either way: the residual conductance is poorly  |
| z0m_ratio | effective | site | 0.1964 | 0.184-0.2083 | 0.13 | +1.62 | 0.31 |  | the base value (ED2 0.13), +-0.04: closed canopies give z0/h of about 0.06-0.15  |
| wstress_sref_stomata | effective | plant_type | 0.6416 | 0.3359-1.33 | 0.6 | +0.10 | 1.00 |  | the PFT file's value, a factor 2 either way (Sabot et al. 2022 fit 0.5-5 across  |
| kappa | observation | observation | 0.8934 | 0.858-0.93 | 1 | -2.16 | 0.76 |  | the gap between the provider's night-time and daytime partitionings (RECO agains |

Fixed at their priors: wstress_sref_stomata_pft2 (dead: its gradient column is zero (a key the windows never use))

## Targets

| target | chi2/n | sigma scale | model/tower | n (cal) |
|---|---|---|---|---|
| lw_up | 1.14 | 3.00 | 1.030 | 2321 |
| le | 0.85 | 2.18 | 0.709 | 4780 |
| h | 0.97 | 2.54 | 0.769 | 677 |
| gpp | 0.84 | 1.61 | 0.965 | 941 |
| ustar | 0.32 | 1.00 | 0.907 | 1208 |

lw_up, model/tower by local hour: 0 h 1.05, 1 h 1.05, 2 h 1.04, 3 h 1.04, 4 h 1.04, 5 h 1.04, 6 h 1.03, 7 h 1.02, 8 h 1.00, 9 h 0.99, 10 h 0.99, 11 h 0.99, 12 h 1.00, 13 h 1.01, 14 h 1.02, 15 h 1.03, 16 h 1.04, 17 h 1.05, 18 h 1.06, 19 h 1.06, 20 h 1.05, 21 h 1.05, 22 h 1.05, 23 h 1.05
lw_up, by light: SW quartile 2 1.05, SW quartile 3 1.02, SW quartile 4 1.00

le, model/tower by local hour: 5 h -55.50, 6 h 1.07, 7 h 0.61, 8 h 0.49, 9 h 0.52, 10 h 0.54, 11 h 0.59, 12 h 0.66, 13 h 0.73, 14 h 0.84, 15 h 1.11, 16 h 1.35, 17 h 1.79, 18 h 1.46
le, by light: SW quartile 1 1.03, SW quartile 2 0.67, SW quartile 3 0.75, SW quartile 4 0.65

h, model/tower by local hour: 8 h 0.44, 9 h 0.56, 10 h 0.65, 11 h 0.72, 12 h 0.77, 13 h 0.79, 14 h 0.83, 15 h 0.91, 16 h 1.00, 17 h 1.26, 18 h 3.29
h, by light: SW quartile 1 1.30, SW quartile 2 0.74, SW quartile 3 0.72, SW quartile 4 0.74

gpp, model/tower by local hour: 6 h 1.04, 7 h 0.84, 8 h 0.84, 9 h 0.79, 10 h 0.89, 11 h 0.93, 12 h 0.97, 13 h 1.02, 14 h 1.06, 15 h 1.06, 16 h 1.14, 17 h 1.16, 18 h 1.33
gpp, by light: SW quartile 1 1.00, SW quartile 2 0.89, SW quartile 3 0.93, SW quartile 4 1.10

ustar, model/tower by local hour: 5 h 1.14, 6 h 0.73, 7 h 0.74, 8 h 0.72, 9 h 0.80, 10 h 0.86, 11 h 0.90, 12 h 0.94, 13 h 0.93, 14 h 0.95, 15 h 0.96, 16 h 0.96, 17 h 1.02, 18 h 1.14
ustar, by light: SW quartile 1 1.01, SW quartile 2 0.84, SW quartile 3 0.89, SW quartile 4 0.92

## kappa

kappa = 0.893: the tower's respiration 2.88 -> 3.22 umol m-2 s-1; GPP 4.96 -> 5.25 (1.88 -> 1.99 kgC m-2 yr-1), means over the records with GPP and its respiration measured, day and night; GPP gains the scaled respiration by day only.

## Uncertainty

Laplace, from the final gradient matrix -- LOCAL ONLY (the linearity check failed).
- alternative gpp_ustar: the fit did not use the provider's threshold, or GPP's diagnostic finds no plateau
- alternative closure: the fit already used Bowen
- alternative partitioning (the provider's daytime partitioning (GPP_DT, RECO_DT)): largest linear shift 4.73 sd -- refitted: leaf_angle_mean 58.8->63.78, leaf_angle_mean_pft2 51.73->26.32, vcmax25 49.31->42.2, vcmax25_pft2 87.01->70.48, stomatal_g1 0.9273->1.057, stomatal_g1_pft2 3.43->4.52, stomatal_g0 0.002562->0.002415, stomatal_g0_pft2 0.01083->0.009785, z0m_ratio 0.1964->0.1972, wstress_sref_stomata 0.6416->0.5759, kappa 0.8934->0.9572
