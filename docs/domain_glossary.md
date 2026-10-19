# Domain Glossary — Biomedical SAV

> Purpose: make synthetic data credible. The AI must not generate generic
> e-commerce-style data. Every field here must be reflected in the generator.

## Service vocabulary
- **PM (Préventif):** scheduled maintenance per manufacturer interval.
- **CM (Correctif):** unplanned intervention following a failure or user report.
- **MTTR:** mean time to repair = mean(closed_at − opened_at), CM only, in hours.
- **MTBF:** mean time between failures = mean interval between consecutive CM events
  on the same asset, in hours.
- **PM compliance:** PM closed within due window / PM due.
- **SAV Back-Office:** remote diagnostic and ticket-routing team.
- **Downtime:** time during which the asset is not clinically usable.

## Modalities
MRI, CT, NM (nuclear medicine), RAD (radiology), and IVD analyzers:
IVD_BIOCHEM (clinical chemistry), IVD_HEMA (hematology), IVD_IMMUNO (immunoassay).

## Typical failure codes (examples — extend as needed)
- HVL_OVERTEMP — high-voltage generator over-temperature
- DET_CALIB_DRIFT — detector calibration drift
- TUBE_ARC — X-ray tube arcing
- PUMP_OCCLUSION — fluidic pump occlusion (IVD)
- REAGENT_PROBE_ERR — reagent probe misalignment (IVD)
- FLUIDIC_LEAK — fluidic circuit leak
- GANTRY_ENCODER_ERR — gantry encoder fault (CT/MRI)
- CRYO_COMPRESSOR_DEGRADED — cryogenic compressor degradation (MRI)

## Realistic distributions to encode in the generator
- PM : CM ratio ≈ 3 : 1.
- MTTR (CM): 2–48h, log-normal-ish. MTTR (PM): 1–4h.
- Older assets have higher CM rates (e.g. linear or exponential aging effect).
- Expert technicians resolve faster than juniors (factor ~0.6–1.3 on MTTR).
- Some PMs are late → this is what the PM compliance KPI measures.
- A subset of assets should show repeat failures (same failure code twice in 30 days)
  — this is the pattern that predictive maintenance in P4 will later target.
