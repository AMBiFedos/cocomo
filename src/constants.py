# Default model calibrated values
A: float = 2.94
B: float = 0.91
C: float = 3.67
D: float = 0.28

WEIGHTS: dict[str, tuple[int, int, int]] = {
    "EI":  (3, 4, 6),      # External Inputs
    "EO":  (4, 5, 7),      # External Outputs
    "ILF": (7, 10, 15),    # Internal Logical Files
    "EIF": (5, 7, 10),     # External Interfaces Files
    "EQ":  (3, 4, 6),      # External Inquiries
}

