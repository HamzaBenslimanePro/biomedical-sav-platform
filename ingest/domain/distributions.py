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