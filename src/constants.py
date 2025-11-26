from enum import Enum

# Default model calibrated values
A: float = 2.94
B: float = 0.91
C: float = 3.67
D: float = 0.28

class RatingLevel(Enum):
    VERY_LOW    = "Very Low"
    LOW         = "Low"
    NOMINAL     = "Nominal"
    HIGH        = "High"
    VERY_HIGH   = "Very High"

class ScaleFactors(Enum):
    PREC = "Precedentedness"
    FLEX = "Development Flexibility"
    RESL = "Risk Resolution"
    TEAM = "Team Cohesion"
    PMAT = "Process Maturity"

class EffortModifiers(Enum):
    RELY = "Required Reliability"
    DATA = "Database Size"
    CPLX = "Product Complexity"
    RUSE = "Developed for Reuse"
    DOCU = "Documentation  Match to Lifecycle"
    TIME = "Execution Time Constraint"
    STOR = "Main Storage Constraint"
    PVOL = "Platform Volatility"
    ACAP = "Analyst Capability"
    PCAP = "Programmer Capability"
    PCON = "Personnel Continuity"
    APEX = "Applications Experience"
    PLEX = "Platform Experience"
    LTEX = "Language and Tool Experience"
    TOOL = "Use of Software Tools"
    SITE = "Multisite Development"
    SCED = "Required Development Schedule"

FUNCTION_POINT_WEIGHTS: dict[str, tuple[int, int, int]] = {
    "EI":  (3, 4, 6),      # External Inputs
    "EO":  (4, 5, 7),      # External Outputs
    "ILF": (7, 10, 15),    # Internal Logical Files
    "EIF": (5, 7, 10),     # External Interfaces Files
    "EQ":  (3, 4, 6),      # External Inquiries
}

FUNCTION_POINT_LANGUAGE_RATIOS: dict[str, int] = {
    "Access": 38,
    "Jovial": 107,
    "Ada 83": 71,
    "Lisp": 64,
    "Ada 95": 49,
    "Machine Code": 640,
    "AI Shell": 49,
    "Modula 2": 80,
    "APL": 32,
    "Pascal": 91,
    "Assembly - Basic": 320,
    "PERL": 27,
    "Assembly - Macro": 213,
    "PowerBuilder": 16,
    "Basic - ANSI": 64, 
    "Prolog": 64,
    "Basic - Compiled": 91,
    "Query - Default": 13,
    "Basic - Visual": 32,
    "Report Generator": 80,
    "C": 128,
    "Second Generation Language": 107,
    "C++": 55,
    "Simulation - Default": 46,
    "Cobol (ANSI 85)": 91,
    "Spreadsheet": 6,
    "Database - Default": 40,
    "Third Generation Language": 80,
    "Fifth Generation Language": 4,
    "Unix Shell Scripts": 107,
    "First Generation Language": 320,
    "Forth": 64,
    "Fortran 77": 10,
    "Fortran 95": 71,
    "Fourth Generation Language": 20,
    "High Level Language": 64,
    "Visual Basic 5.0": 29,
    "HTML 3.0": 15,
    "Visual C++": 34,
    "Java": 53
}