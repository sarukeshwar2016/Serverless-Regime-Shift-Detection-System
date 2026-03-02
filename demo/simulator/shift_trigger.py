"""
Shift trigger — generates artificial regime shifts for testing.
Useful for verifying that the detection engine correctly identifies changes.
"""

import numpy as np
from typing import List


def generate_shift_signal(
    n: int = 1000,
    n_shifts: int = 3,
    base_value: float = 100.0,
    noise_std: float = 1.0,
) -> List[float]:
    """
    Generate a synthetic signal with abrupt mean shifts.
    Returns a list of float values.
    """
    segment_len = n // (n_shifts + 1)
    signal = []
    current_mean = base_value

    for i in range(n_shifts + 1):
        seg = np.random.normal(current_mean, noise_std, segment_len).tolist()
        signal.extend(seg)
        current_mean += np.random.choice([-1, 1]) * np.random.uniform(5, 20)

    return signal[:n]


if __name__ == "__main__":
    sig = generate_shift_signal()
    print(f"Generated signal with {len(sig)} points")
    print(f"First 10: {sig[:10]}")
    print(f"Last 10:  {sig[-10:]}")
