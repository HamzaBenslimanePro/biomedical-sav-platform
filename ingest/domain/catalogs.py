"""Static reference data — what a hospital fleet actually contains.

Update here, never in the generators. Weights and catalogs live in
distributions.py so tuning a distribution never touches this file.
"""

MODALITIES = [
    "MRI", "CT", "NM", "RAD",
    "IVD_BIOCHEM", "IVD_HEMA", "IVD_IMMUNO",
]

STATUSES = ["OPERATIONAL", "DEGRADED", "DOWN", "DECOMMISSIONED"]

# Per-modality catalogue: manufacturer -> list of models.
# Kept deliberately short — the goal is credible, not exhaustive.
MODELS_BY_MODALITY: dict[str, dict[str, list[str]]] = {
    "MRI": {
        "Siemens Healthineers": ["MAGNETOM Vida", "MAGNETOM Aera", "MAGNETOM Sola"],
        "GE HealthCare": ["SIGNA Architect", "SIGNA Premier"],
        "Philips": ["Ingenia Elition", "Ingenia Ambition"],
    },
    "CT": {
        "Siemens Healthineers": ["SOMATOM Force", "SOMATOM go.Top", "SOMATOM Drive"],
        "GE HealthCare": ["Revolution CT", "Revolution Apex"],
        "Canon": ["Aquilion ONE"],
    },
    "NM": {
        "Siemens Healthineers": ["Symbia Intevo", "Biograph Vision"],
        "GE HealthCare": ["Discovery NM/CT 670"],
    },
    "RAD": {
        "Siemens Healthineers": ["Ysio Max", "Multix Impact"],
        "GE HealthCare": ["Optima XR240"],
        "Philips": ["DigitalDiagnost C90"],
        "Fujifilm": ["FDR D-EVO"],
    },
    "IVD_BIOCHEM": {
        "Roche": ["cobas 8000", "cobas 6000"],
        "Abbott": ["ARCHITECT c8000"],
        "Siemens Healthineers": ["Atellica CH 930"],
        "Beckman Coulter": ["AU5800"],
    },
    "IVD_HEMA": {
        "Sysmex": ["XN-9000", "XN-1000"],
        "Abbott": ["Alinity h-series"],
        "Beckman Coulter": ["DxH 800"],
    },
    "IVD_IMMUNO": {
        "Roche": ["cobas e 801"],
        "Abbott": ["ARCHITECT i2000SR"],
        "Siemens Healthineers": ["Atellica IM 1300"],
    },
}

# Moroccan hospital sites (matches UM6SS / Siemens Healthineers context).
SITE_CATALOG = [
    "SITE-CASA-01", "SITE-CASA-02", "SITE-RABAT-01", "SITE-RABAT-02",
    "SITE-MARRAKECH-01", "SITE-FES-01", "SITE-TANGER-01", "SITE-AGADIR-01",
]

# --- append to existing file ---------------------------------------------

SKILL_LEVELS = ["JUNIOR", "INTERMEDIATE", "SENIOR", "EXPERT"]