"""Statistical distributions — the credibility of the synthetic data lives here.

Every weight is a deliberate choice documented by its comment. If you change a
number, change the comment. Tests assert the weights sum to 100.
"""

# Realistic hospital fleet: RAD most common, MRI rarest (cost + footprint),
# IVD split across three subtypes. Sums to 100.
MODALITY_WEIGHTS = {
    "MRI": 6,
    "CT": 10,
    "NM": 4,
    "RAD": 35,
    "IVD_BIOCHEM": 15,
    "IVD_HEMA": 15,
    "IVD_IMMUNO": 15,
}

# Default status weights (mid-age assets). Sums to 100.
STATUS_WEIGHTS = {
    "OPERATIONAL": 85,
    "DEGRADED": 8,
    "DOWN": 3,
    "DECOMMISSIONED": 4,
}

# Install-year buckets — skews recent, long tail of old assets. Sums to 100.
# Reference date is 2026: "0-2" means installed 2024-2026 (likely warranty active).
INSTALL_AGE_WEIGHTS = {
    "0-2": 25,
    "3-5": 30,
    "6-10": 30,
    "11-15": 15,
}

# Warranty duration (months) by modality. Medtech norm is 1-3 years.
WARRANTY_MONTHS_BY_MODALITY = {
    "MRI": 24,
    "CT": 24,
    "NM": 24,
    "RAD": 12,
    "IVD_BIOCHEM": 12,
    "IVD_HEMA": 12,
    "IVD_IMMUNO": 12,
}

# CM rate per asset per year, weighted by age. Realistic for imaging + IVD:
# ~4 CM/asset/year for a mid-age asset under service contract.
CM_RATE_PER_ASSET_YEAR = {
    "young": 2.5,   # < 3 years
    "mid":   4.0,   # 3–10 years
    "old":   6.0,   # > 10 years
}

# PM rate per asset per year, per manufacturer interval.
# Imaging: quarterly. IVD: monthly. This drives the PM:CM ratio.
PM_RATE_PER_ASSET_YEAR = {
    "MRI": 4, "CT": 4, "NM": 4, "RAD": 4,      # quarterly
    "IVD_BIOCHEM": 12, "IVD_HEMA": 12, "IVD_IMMUNO": 12,  # monthly
}

PM_OUTCOMES = {"on_time": 80, "late": 15, "missed": 5}

# Technician skill distribution. Junior-heavy is realistic for a 50-tech pool.
SKILL_WEIGHTS = {"JUNIOR": 20, "INTERMEDIATE": 40, "SENIOR": 30, "EXPERT": 10}

# Hire-year buckets (weighted toward recent). Sums to 100.
HIRE_YEAR_WEIGHTS = {"0-2": 25, "3-5": 25, "6-10": 30, "11-15": 20}