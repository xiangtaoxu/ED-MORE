# Example 04, Tonzi Ranch — a blue-oak savanna and its grass (prototype)

Example 04's pipeline at a savanna: deciduous blue oaks over a C3 annual grass in the Sierra Nevada
foothills of California, the AmeriFlux tower US-Ton (23.5 m), 2010–2019. It is ED-MORE's first stand
with a plant that is not a tree: the grass has no stem, stands at its plant type's height and changes
only its leaf area ([`docs/science/plant_carbon_allocation.md`](../../../../docs/science/plant_carbon_allocation.md)
§2). **Status: prototype.**

The example:

1. builds the forcing from the tower's meteorology, with Vaira Ranch's where Tonzi measured nothing;
2. starts a frozen stand: oaks imputed from the site survey's stand averages, and the grass beneath and
   between them; its leaves follow the phenology fitted in example 02, part 3;
3. calibrates the fast parameters of both plant types against the tower;
4. compares the default and the calibrated runs with the tower, and each plant type's leaf area with
   MODIS and the clip LAI;
5. follows ten April days hour by hour: a canopy oak, the grass beneath it and the grass in the open,
   with their canopy air and soil.

## Run

```bash
cd examples/example04_column_biophysics/sites/tonzi
python run_site.py --ameriflux AMF_US-Ton_FLUXNET_2001-2025_v1.3_r1.zip --badm <base> --modis <modis>
python run_site.py ... --forcing-only          # the tower file and the forcing only
python run_site.py ... --calibrate --workers 60
```

`<base>` is the folder holding AmeriFlux's BASE-BADM zips of US-Ton and US-Var
(`AMF_US-Ton_BASE-BADM_27-5.zip`, `AMF_US-Var_BASE-BADM_27-5.zip`); they and the FLUXNET zip need an
AmeriFlux account. `<modis>` holds ORNL DAAC's MCD15A3H subset around the tower
(`us_california_tonzi_ranch_mcd15a3h_{Lai_500m,FparLai_QC}.csv`). Every step but the calibration takes
about 5 minutes on 32 cores with the dev build; with `--calibrate`, every step takes 10 minutes on 64
cores.

## The data

| Input | Source |
|---|---|
| Meteorology and fluxes | AmeriFlux US-Ton FLUXNET (ONEFlux v1.3_r1), CC-BY-4.0. Measured values only: [`prepare_tower.py`](prepare_tower.py) blanks the product's fills, and [`make_tower_forcing.py`](../../../../scripts/prepare_input/flux_tower/make_tower_forcing.py) fills the gaps by its own rules |
| Rain and pressure | US-Ton's BASE file (BASE-BADM 27-5; the FLUXNET product has none before 2021). Where Tonzi has none, or its file holds Vaira's readings, Vaira Ranch's (US-Var, 2.4 km away, 48 m lower) |
| Longwave | measured at Tonzi from 2014. Before, Vaira's less its mean excess over Tonzi's where both measure (10.4 W m⁻² over 2014–2019): half-hourly RMSE 12.1 W m⁻², against 21.8 for the forcing tool's own fill |
| Stand | an oak census imputed from the survey's stand averages (Kiang 2002, via Baldocchi, Xu & Kiang 2004, Agric. For. Meteorol. 123:13–39): 194 stems ha⁻¹ and 18 m² ha⁻¹ on 40 of 100 cells of 10 m. **Not measured trees** ([`make_tonzi_census.py`](make_tonzi_census.py)) |
| Traits | the oaks' and the grass's from the site literature, each value's source in [`pft_parameters.toml`](pft_parameters.toml) |
| Leaf area and phenology | the BADM's clip LAI (US-Ton understory, US-Var grassland), its oak and grass dates, PhenoCam's `tonzi_GR_1000` greenness (example 02, part 3) |
| The oaks' water | their leaf water potential, predawn and midday, in the dry summers of 2007–2008 (Osuna et al. 2015, Tree Physiol. 35:485; Miller et al. 2010, Water Resour. Res. 46:W10503), their sapwood area (Miller 2009, PhD dissertation, UC Berkeley, Fig. 5.4) and the water table at the tower's well (US-Ton's BASE file) |
| Satellite leaf area | MODIS MCD15A3H collection 6.1 (4-day, 500 m; Myneni, Knyazikhin & Park 2021, doi:10.5067/MODIS/MCD15A3H.061), ORNL DAAC's subset around the tower |

Cite US-Ton's BASE as Ma, Xu, Verfaillie & Baldocchi, doi:10.17190/AMF/1245971, and US-Var's as
doi:10.17190/AMF/1245984.

## 1. The model

[`ed_config_eval.toml`](ed_config_eval.toml) runs 2010–2019; the scoring starts in 2011.
- **The stand is frozen** (`demography_on = false`): only the leaves change. The census's 100 cells
  restructure to 10 patches and 63 cohorts.
  - **The oaks** are 194 stems at the site's basal area. Their diameters are drawn with the spread of blue
    oak at NEON's San Joaquin Experimental Range: the survey's mean diameter (19.9 cm) does not fit its
    stem count and basal area. Their height curve passes through the survey's mean and tallest (7.1 and
    13.0 m), and their leaf area gives the trees' LAI, 0.65.
  - **The grass** is one row per cell, with dbh 0, of tillers 0.3 m tall. A cell in the open carries
    Vaira's open-grassland peak LAI (2.55, the median over 2002–2014 of each year's largest clip), a cell
    under the oaks the Tonzi understory's (1.31). The tiller count, 2,000 m⁻² in the open, is a choice: no
    count was found for these swards, and in a frozen stand only the leaf area and root length it gives
    matter.
- **Two plant types**: blue oak (a tree) and a C3 annual grass (`growth_form = "grass"`), their capacity,
  leaf mass per area, stomata, leaf angles, hydraulics and roots from the site literature. The grass's
  Vcmax is a stand-in: none was found at leaf level.
- **The phenology** is fitted in [example 02, part 3](../../../example02_canopy_phenology/README.md#part-3--a-savanna-tonzi-ranch).
  The oaks flush on warmth and long days and drop their leaves on cold or drought. The grass grows and dies
  on water alone: its predawn leaf water potential summed above and below its turgor-loss point.
- **The oaks' water path is blue oak's.** Their sapwood area follows the relation measured on oaks
  felled at the site (Miller 2009), where the repository's gave 1.3–1.8 times as much, and their leaves
  blue oak's pressure–volume curve, with a turgor-loss point of −3.3 MPa (Meinzer et al. 2016). No leaf
  hydraulic conductance was found for blue oak: theirs, 3 mmol m⁻² s⁻¹ MPa⁻¹, and the leaf potential over
  which their stomata close, from −2.0 to −4.5 MPa, are fitted by hand to their measured midday potential
  and the tower's summer GPP by the hour. Their stomata narrow slowly as the predawn potential falls
  (Xu & Baldocchi 2003). The oaks of the default run (leaf-area weighted; predawn 4–6 h, midday 12–15 h):

  | oak leaf water potential [MPa], predawn / midday | measured | ED-MORE |
  |---|---|---|
  | May | −0.2 to −0.8 / −0.85 to −2.7 (Tonzi, 2007–2008) | −0.23 / −1.87 (2012–2015) |
  | early July of a dry summer | −1.3 to −2.6 / −2.9 to −4.0 (Tonzi, 2007–2008) | −2.91 / −4.00 (2012–2015) |
  | late August of a dry summer | −3.7 to −5.2 / −3.2 to −4.8 (Tonzi, 2007–2008) | −3.02 / −4.10 (2012–2015) |
  | July of a wet summer | −0.45 to −1.8 / −3.7 to −4.3 (Sierra foothills, 1978) | −0.92 / −3.11 (2011, 2017, 2019) |

  Tonzi's are Osuna et al. (2015) and Miller et al. (2010), read off their figures; no wet summer was
  measured at Tonzi, and the wet summer's are blue oaks in Sequoia's foothills (Baker, Rundel & Parsons
  1981, Madroño 28:1). With Harvard's broadleaves' leaf conductance and the repository's curve, the oaks'
  leaves stayed at −1 MPa at midday in a wet July and transpired through the afternoon.
- **The soil** is 1 m of loam over weathered rock, to a water table at 9 m (`water_bottom_bc =
  "aquifer"`), with a texture per layer. Tonzi's soil is about 1 m of very rocky silt loam over 4–8 m of
  saprolite and fractured greenstone, with the water table 7–12 m down, which the oaks draw most of their
  summer water from (Miller 2009). At the tower's well it rose to 2–4 m in the wet springs of 2011, 2017
  and 2019, and stayed at 7.5–9.3 m in 2013–2015. The rock holds a fifth of the loam's water (porosity
  0.15), between the loam and the fractured rock's specific yield, 0.04: fitted by hand to the tower's
  summer LE. Its conductivity is the slug tests' in the tower's well (Miller 2009). One loam to 9 m held
  five times the water at depth, and the oaks transpired 30–50 W m⁻² too much in the wet summers.
- **The oaks' roots reach the water table.** The share of their roots near it was fitted by hand to the
  tower's dry-season LE. In the drought summers their late-summer predawn potential stays near −3 MPa,
  above the −3.7 to −5.2 MPa measured in 2007–2008: the model's roots meet the water table, while the real
  oaks do not come to equilibrium with it (Miller 2009). The site's profile, 70 % of the roots above
  0.5 m, leaves them no root at the water table: the oaks then starve in the 2012–2015 drought, their
  storage emptied every autumn.
- **The momentum roughness is the landscape's.** At Vaira's 2 m sonic the aerodynamic canopy height is
  0.56–0.74 m in every month while the grass stands 0.04–0.55 m; `soil_rough` floors the canopy's height
  for its roughness at 0.65 m.

## 2. The calibration

[`calibration.toml`](calibration.toml) fits both plant types' capacity, stomata and leaf angles on the
grass's months (January–February), the oaks' (July–August) and April. **It fails its own validation**:
on the windows it held out its cost is 2 % above the default's (27,819 against 27,233), and LE's RMSE 5 %
([`calibration/report.md`](calibration/report.md)). The default run is the site's reference; the
calibrated one is kept for the diagnosis.

- **Both of the oaks' calibration windows fell in the 2014 drought** (14 July and 22 August): a window
  needs the longwave measured at Tonzi, from 2014 on, and of those summers 2014's were the best covered.
  By late August 2014 the oaks had nearly closed: from 9 to 16 h the tower's GPP was 1.5 µmol m⁻² s⁻¹
  and its LE 16 W m⁻², against the default's 2.4 and 34.
- **The fit can only scale the oaks down**: Medlyn g1 0.93 (prior 1.92) and Vcmax 49 (prior 113). Over
  the full record that halves their summer LE (dry-season bias −19.6 W m⁻², against −5.0 for the default):

  | June–August, 9–16 h | 2011 | 2012 | 2013 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 |
  |---|---|---|---|---|---|---|---|---|---|
  | LE [W m⁻²]: tower | 118 | 74 | 42 | 44 | 53 | 66 | 85 | 67 | 117 |
  | default | 110 | 48 | 42 | 39 | 45 | 64 | 69 | 70 | 103 |
  | calibrated | 67 | 31 | 26 | 28 | 29 | 29 | 27 | 28 | 59 |
  | GPP [µmol m⁻² s⁻¹]: tower | 6.6 | 5.3 | 3.8 | 3.1 | 2.7 | 3.5 | 4.5 | 4.3 | 7.0 |
  | default | 7.9 | 3.1 | 2.7 | 2.6 | 3.0 | 4.1 | 4.4 | 4.7 | 7.0 |
  | calibrated | 6.0 | 2.7 | 2.4 | 2.6 | 2.7 | 2.4 | 2.4 | 2.5 | 4.9 |

- **The drought windows ask for a drier late summer, not a smaller g1.** The real oaks were near closure
  in August 2014, at predawn potentials that reached −3.7 to −5.2 MPa in the dry summers of 2007–2008; the
  model's stay near −3 MPa on the water table (§1) and keep transpiring, so the fit lowers g1 and Vcmax
  for every summer. Until the late summer dries (Open), the default is the better run.

## 3. Against the tower

![ED-MORE against the US-Ton tower: the wet and the dry season's mean diurnal cycles and the mean seasonal cycle of GPP, NEE, LE, H and net radiation](evaluation.png)

Means over the tower's measured hours ([`plot_evaluation.py`](plot_evaluation.py)), every hour of the day
weighted alike, 2011–2019. The bias in the panels is against the tower as the calibration scores it
(GPP with the tower's respiration over the fitted kappa, H and LE with the energy-closure gap shared);
the tower closes its energy balance to 0.87 of the available energy (the daily median).

| run | GPP [µmol m⁻² s⁻¹] tower / model | LE [W m⁻²] | H [W m⁻²] | net radiation [W m⁻²] |
|---|---|---|---|---|
| default | 2.85 / 3.23 | 31.9 / 35.9 | 57.8 / 46.5 | 103.3 / 78.9 |
| calibrated | 2.85 / 3.32 | 31.9 / 27.4 | 57.8 / 52.8 | 103.3 / 78.0 |

- **The grass's season is right in timing, and its spring too productive.** From December to February
  the monthly GPP and LE are within 0.8 µmol m⁻² s⁻¹ and 4 W m⁻² of the tower's. In April and May, with
  the oaks leafing out over the grass at its peak, GPP runs 2.5–2.6 µmol m⁻² s⁻¹ and LE 15–21 W m⁻² high.
- **The oaks' summer follows the tower.** From June to August the monthly GPP is within
  0.9 µmol m⁻² s⁻¹ and LE within 4 W m⁻² of the tower's; in September and October LE runs 7–9 W m⁻² high.
  Their day closes through the afternoon, a little flatter than the tower's: lower at the peak, higher
  late in the afternoon.

  | June–August, local hour | 7 | 9 | 11 | 13 | 15 | 16 | 17 |
  |---|---|---|---|---|---|---|---|
  | LE [W m⁻²], wet summers: tower | 59 | 98 | 119 | 120 | 100 | 77 | 53 |
  | default | 54 | 86 | 101 | 101 | 95 | 86 | 69 |
  | drought summers: tower | 31 | 55 | 61 | 57 | 43 | 33 | 22 |
  | default | 34 | 48 | 48 | 43 | 38 | 35 | 32 |
  | GPP [µmol m⁻² s⁻¹], wet summers: tower | 7.5 | 7.5 | 6.6 | 5.6 | 5.3 | 5.0 | 4.0 |
  | default | 8.7 | 8.4 | 7.1 | 6.0 | 5.4 | 5.2 | 4.4 |
  | drought summers: tower | 5.8 | 5.5 | 4.2 | 3.2 | 3.0 | 2.8 | 2.3 |
  | default | 5.7 | 4.7 | 3.3 | 2.3 | 2.0 | 1.9 | 1.9 |

  Wet summers are 2011, 2017 and 2019, drought summers 2012–2015.
- **Net radiation is 39–46 W m⁻² short in summer**: from June to August the stand reflects 0.19 of the
  shortwave against the tower's 0.15, and the ground, bare under the dead grass, is hotter: 11 W m⁻² more
  longwave. The ground's albedo is the repository's default.

## 4. Leaf area

![The mean seasonal cycle of the oaks' and the grass's leaf area, 2011–2019, against MODIS MCD15A3H and the clip LAI](lai.png)

Each plant type's daily leaf area in the default run, the mean seasonal cycle over 2011–2019
([`plot_lai.py`](plot_lai.py)), against MODIS MCD15A3H (the median of the 3 × 3 pixels of 500 m around
the tower, good retrievals only) and the BADM's clips, each on its day of the year. A MODIS pixel holds
oaks, the grass between them and the grass beneath them; the clips are of the grass alone.

| months | ED-MORE, oaks + grass | MODIS | clips, Tonzi understory | clips, Vaira grassland |
|---|---|---|---|---|
| March–April (the grass at its peak) | 0.26 + 1.23 = 1.49 | 1.65 | 1.01 | 1.52 |
| July–August (the oaks alone) | 0.65 + 0.05 = 0.70 | 0.92 | – | – |
| December–January (the grass filling) | 0.01 + 0.44 = 0.45 | 0.62 | 0.71 | 0.96 |

- **The grass fills over the winter** after the first big rain and dies in May and June. Its peak follows
  the year's rain, from 1.34 in 2013 to 2.04 in 2017, and in March–April it sits between the understory's
  clips and Vaira's open grassland.
- **The stand's spring is about two weeks late.** The mean cycle peaks on 6 May at 2.1, MODIS's on
  20 April at 2.0, and it falls to half three weeks after MODIS's (19 June against 28 May): the model's
  grass peaks and dies late.
- **The summer and the winter are low against MODIS** by about 0.2: the oaks' 0.65 is the survey's LAI, and
  the 500 m pixel also holds standing dead grass and branches, which the retrieval does not tell from
  leaves. In December–January the grass is below both clip records.

## 5. Ten days inside the column

![Ten April days at hourly resolution: shortwave and rain; air, canopy-air and leaf temperature; canopy-air CO2; gross assimilation and leaf water potential of a canopy oak, the grass beneath it and the grass in the open; soil moisture and temperature under the oaks and in the open](window.png)

18–27 April 2016, local time, every hour: the default run to the window's start, writing its state, and a
restart from it with every patch's canopy air and soil and every cohort's leaves written each hour
([`output_window.toml`](output_window.toml), [`plot_window.py`](plot_window.py)). The restart continues
the run exactly. The grass is near its peak and the oaks are in leaf; four warm, clear days, 13.5 mm of
rain on the 22nd, a cooler week, and 31 mm on the 27th. Two patches: the largest under the oaks (14 % of
the site, LAI 2.4) with its tallest oak cohort (10 m) and the grass beneath it, and the largest in the
open (60 %, LAI 1.7), the grass alone.

- **The open is the warmer.** At midday on the warm days its canopy air is 2.0 °C above the forcing's air
  (0.6 under the oaks), and its soil 2.5 cm down reaches 38 °C (32 under the oaks).
- **The light sets the assimilation:** at midday on the clear days 23 µmol m⁻² s⁻¹ for the canopy oak's
  leaves, 13 for the open grass's and 10 for the shaded grass's.
- **The leaves' water potential** falls each afternoon and recovers each night: on the warm days to
  −2.3 MPa for the canopy oak, −1.4 for the open grass, which draws on the drier topsoil, and −1.1 for
  the shaded grass.
- **The canopy air's CO₂** falls to 385–400 µmol mol⁻¹ by day (lower in brief dips at dawn and dusk) and
  rises to 400–420 at night; the swing is the wider in the open.
- **The storms wet the top 10 cm** from 0.14–0.17 to 0.30–0.37 m³ m⁻³; only the second reaches
  22.5 cm. At 45 and 80 cm the soil dries through the ten days, faster in the open (0.175 to 0.149 m³ m⁻³
  at 45 cm, against 0.187 to 0.169 under the oaks).

## Open

- **The census is imputed.** The survey's tree list (Kiang 2002) would replace it.
- **The oaks' late summer in a drought** (§1, §2): their predawn potential stays near −3 MPa against
  −3.7 to −5.2 MPa measured, on roots that meet a water table held at 9 m. The water table measured at
  the tower's well (2–9 m) as the column's bottom, and the oaks' loss of capacity over the summer (blue
  oak's Vcmax falls by more than 60 %, Xu & Baldocchi 2003, Osuna et al. 2015), are the next steps; the
  calibration's drought windows need them.
- **The ground's albedo and temperature** under the dead grass: the summer net radiation. MODIS's
  MCD43A3 albedo over the tower is the check.
- **The grass's germination** is its weakest timing (example 02, part 3), and its leaves are one big
  leaf at the bottom of the canopy; standing dead grass is not represented.
- **The fitted water path**: the oaks' leaf conductance and stomatal closure, and the weathered rock's
  water, are fitted by hand to the measured leaf potentials and the tower; a measured blue-oak leaf
  conductance and the saprolite's retention curve would replace them.

## Files

| File | What it is |
|---|---|
| [`run_site.py`](run_site.py) | the steps above |
| [`prepare_tower.py`](prepare_tower.py), [`tonzi_site.toml`](tonzi_site.toml) | the tower file and its declaration |
| [`make_tonzi_census.py`](make_tonzi_census.py) | the imputed oaks, the grass, and the steady litter input for the soil carbon |
| [`ed_config_eval.toml`](ed_config_eval.toml), [`pft_parameters.toml`](pft_parameters.toml), [`output_variables.toml`](output_variables.toml) | the default run |
| [`calibration.toml`](calibration.toml), [`calibration/`](calibration) | the calibration and its results |
| [`output_window.toml`](output_window.toml) | the ten-day window's hourly variables |
| [`plot_evaluation.py`](plot_evaluation.py), [`plot_lai.py`](plot_lai.py), [`plot_window.py`](plot_window.py) | the figures |
