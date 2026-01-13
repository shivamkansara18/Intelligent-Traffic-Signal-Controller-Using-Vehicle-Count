"""Traffic signal timing helper functions.

This module provides a weighted-load calculation and green-time computation
based on detected vehicle classes per direction.

API:
- compute_load(detections) -> float
- compute_green_time(load, max_load, T_min=10, T_max=45) -> float
- determine_signal_timing(direction_detections, T_min=10, T_max=45) -> dict

`direction_detections` should be a dict mapping direction name to an
iterable of class names (strings) produced by the detector.
"""
from typing import Dict, Iterable

WEIGHTS = {
    "truck": 4.0,
    "bus": 3.5,
    "car": 2.0,
    "auto": 1.5,
    "autorickshaw": 1.5,
    "rickshaw": 1.5,
    "motorcycle": 1.0,
    "motorbike": 1.0,
    "bike": 1.0,
    "motorbike": 1.0,
    # add common synonyms
}


def compute_load(detections: Iterable[str]) -> float:
    """Compute weighted load from an iterable of class name strings.

    Unknown class names are ignored.
    """
    load = 0.0
    for cls in detections:
        if not isinstance(cls, str):
            cls = str(cls)
        key = cls.strip().lower()
        if key in WEIGHTS:
            load += WEIGHTS[key]
    return load


def compute_green_time(load: float, max_load: float, T_min: float = 10, T_max: float = 45) -> float:
    """Linearly interpolate green time between T_min and T_max given relative load.

    If max_load == 0, returns T_min.
    """
    if max_load <= 0:
        return float(T_min)
    ratio = load / max_load
    return float(T_min + ratio * (T_max - T_min))


def determine_signal_timing(direction_detections: Dict[str, Iterable[str]], T_min: float = 10, T_max: float = 45) -> Dict:
    """Given detections per direction produce loads, green times, and order.

    Returns a dict with keys: 'loads', 'green_times', 'priority_order', 'max_load'.
    """
    loads = {}
    for direction, dets in direction_detections.items():
        loads[direction] = compute_load(dets)

    max_load = max(loads.values()) if loads else 0.0

    green_times = {d: compute_green_time(L, max_load, T_min, T_max) for d, L in loads.items()}

    # Priority order by descending load
    order = sorted(loads.keys(), key=lambda x: loads[x], reverse=True)

    return {
        "loads": loads,
        "green_times": green_times,
        "priority_order": order,
        "max_load": max_load,
    }
