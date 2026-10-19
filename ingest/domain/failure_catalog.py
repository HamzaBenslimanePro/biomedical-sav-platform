"""Failure code reference catalog.

The reference table (FAILURE_CODES) matches the contract exactly:
(code, label, subsystem, severity). The modality mapping is separate because
the contract does not include a `modalities` column — the reference table is
generic (TUBE_ARC applies to both CT and RAD), and the mapping tells the
work_orders generator which codes are valid for which equipment type.

Pure data. Never import from a generator module.
"""

FAILURE_CODES: list[dict] = [
    # MRI — cryogenics, gradients, RF
    {"failure_code": "CRYO_COMPRESSOR_DEGRADED", "label": "Cryogenic compressor degraded", "subsystem": "Cryogenics", "severity": "CRITICAL"},
    {"failure_code": "GRADIENT_COIL_OVERTEMP",  "label": "Gradient coil over-temperature", "subsystem": "Gradient system", "severity": "HIGH"},
    {"failure_code": "RF_AMPLIFIER_FAULT",      "label": "RF amplifier fault",           "subsystem": "RF chain", "severity": "HIGH"},
    {"failure_code": "HELIUM_LEVEL_LOW",        "label": "Helium level below threshold", "subsystem": "Cryogenics", "severity": "CRITICAL"},
    # CT — tube, gantry, high-voltage
    {"failure_code": "TUBE_ARC",                "label": "X-ray tube arcing",           "subsystem": "X-ray tube", "severity": "HIGH"},
    {"failure_code": "GANTRY_ENCODER_ERR",      "label": "Gantry encoder fault",         "subsystem": "Gantry", "severity": "HIGH"},
    {"failure_code": "DETECTOR_CALIB_DRIFT",    "label": "Detector calibration drift",   "subsystem": "Detector", "severity": "MEDIUM"},
    {"failure_code": "HVL_OVERTEMP",            "label": "High-voltage generator over-temperature", "subsystem": "High-voltage", "severity": "HIGH"},
    {"failure_code": "SLIP_RING_NOISE",         "label": "Slip ring signal noise",       "subsystem": "Slip ring", "severity": "MEDIUM"},
    # NM — detector, gantry, radiopharmacy
    {"failure_code": "DETECTOR_PMT_DRIFT",      "label": "Detector PMT gain drift",      "subsystem": "Detector", "severity": "MEDIUM"},
    {"failure_code": "COLLIMATOR_ALIGN_ERR",    "label": "Collimator alignment error",   "subsystem": "Gantry", "severity": "LOW"},
    {"failure_code": "RADIOPHARM_DISPENSE_ERR", "label": "Radiopharmaceutical dispense error", "subsystem": "Fluidics", "severity": "HIGH"},
    # RAD — generator, mechanics, optics
    {"failure_code": "GENERATOR_FAULT",         "label": "High-voltage generator fault", "subsystem": "Generator", "severity": "HIGH"},
    {"failure_code": "BUCKY_MOTOR_FAULT",       "label": "Bucky motor fault",            "subsystem": "Mechanics", "severity": "LOW"},
    {"failure_code": "COLLIMATOR_LAMP_ERR",     "label": "Collimator lamp failure",      "subsystem": "Optics", "severity": "LOW"},
    # IVD — shared across subtypes (fluidics + thermal are universal)
    {"failure_code": "PUMP_OCCLUSION",          "label": "Fluidic pump occlusion",       "subsystem": "Fluidics", "severity": "MEDIUM"},
    {"failure_code": "REAGENT_PROBE_ERR",       "label": "Reagent probe misalignment",   "subsystem": "Fluidics", "severity": "MEDIUM"},
    {"failure_code": "FLUIDIC_LEAK",            "label": "Fluidic circuit leak",         "subsystem": "Fluidics", "severity": "MEDIUM"},
    {"failure_code": "TEMP_REGULATION_ERR",     "label": "Temperature regulation error", "subsystem": "Thermal", "severity": "HIGH"},
    # IVD_BIOCHEM
    {"failure_code": "PHOTOMETER_DRIFT",        "label": "Photometer drift",             "subsystem": "Optics", "severity": "LOW"},
    {"failure_code": "CUVETTE_WASH_FAULT",      "label": "Cuvette wash station fault",   "subsystem": "Fluidics", "severity": "MEDIUM"},
    # IVD_HEMA
    {"failure_code": "APERTURE_CLOG",           "label": "Aperture clog",                "subsystem": "Fluidics", "severity": "MEDIUM"},
    {"failure_code": "LYSE_REAGENT_ERR",        "label": "Lyse reagent error",           "subsystem": "Fluidics", "severity": "MEDIUM"},
    {"failure_code": "HGB_PHOTOMETER_ERR",      "label": "HGB photometer error",         "subsystem": "Optics", "severity": "MEDIUM"},
    # IVD_IMMUNO
    {"failure_code": "LUMINOMETER_DRIFT",       "label": "Luminometer drift",            "subsystem": "Optics", "severity": "MEDIUM"},
    {"failure_code": "WASH_STATION_FAULT",      "label": "Wash station fault",           "subsystem": "Fluidics", "severity": "MEDIUM"},
    {"failure_code": "CARRIER_HANDLING_ERR",    "label": "Carrier handling error",       "subsystem": "Mechanics", "severity": "HIGH"},
]

# Which codes apply to which modality. Derived from medical knowledge: no cryo
# compressor on an IVD analyzer, no aperture clog on an MRI.
FAILURE_CODES_BY_MODALITY: dict[str, list[str]] = {
    "MRI":         ["CRYO_COMPRESSOR_DEGRADED", "GRADIENT_COIL_OVERTEMP", "RF_AMPLIFIER_FAULT", "HELIUM_LEVEL_LOW"],
    "CT":          ["TUBE_ARC", "GANTRY_ENCODER_ERR", "DETECTOR_CALIB_DRIFT", "HVL_OVERTEMP", "SLIP_RING_NOISE"],
    "NM":          ["DETECTOR_PMT_DRIFT", "COLLIMATOR_ALIGN_ERR", "RADIOPHARM_DISPENSE_ERR"],
    "RAD":         ["TUBE_ARC", "GENERATOR_FAULT", "BUCKY_MOTOR_FAULT", "COLLIMATOR_LAMP_ERR", "DETECTOR_CALIB_DRIFT"],
    "IVD_BIOCHEM": ["PUMP_OCCLUSION", "REAGENT_PROBE_ERR", "PHOTOMETER_DRIFT", "CUVETTE_WASH_FAULT", "TEMP_REGULATION_ERR", "FLUIDIC_LEAK"],
    "IVD_HEMA":    ["APERTURE_CLOG", "LYSE_REAGENT_ERR", "HGB_PHOTOMETER_ERR", "PUMP_OCCLUSION", "TEMP_REGULATION_ERR"],
    "IVD_IMMUNO":  ["LUMINOMETER_DRIFT", "WASH_STATION_FAULT", "CARRIER_HANDLING_ERR", "PUMP_OCCLUSION", "REAGENT_PROBE_ERR", "TEMP_REGULATION_ERR"],
}