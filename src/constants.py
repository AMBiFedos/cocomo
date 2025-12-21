# Contains constants and enumerations used in the COCOMO II.2000 model
# All default values are taken from the COCOMO documentation.

from enum import Enum

# Default model calibrated values
# The variable names are taken from the COCOMO II.2000 model they are coefficients in the effort estimation equations
# The values can be found on page 14
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
    EXTRA_HIGH  = "Extra High"

class ScaleFactor(Enum):
    PREC = "Precedentedness"
    FLEX = "Development Flexibility"
    RESL = "Risk Resolution"
    TEAM = "Team Cohesion"
    PMAT = "Process Maturity"
    
SCALE_FACTOR_VALUES = {
    ScaleFactor.PREC: {RatingLevel.VERY_LOW: 6.20, RatingLevel.LOW: 4.96, RatingLevel.NOMINAL: 3.72, RatingLevel.HIGH: 2.48, RatingLevel.HIGH: 1.24, RatingLevel.EXTRA_HIGH: 0.00},
    ScaleFactor.FLEX: {RatingLevel.VERY_LOW: 5.07, RatingLevel.LOW: 4.05, RatingLevel.NOMINAL: 3.04, RatingLevel.HIGH: 2.03, RatingLevel.HIGH: 1.01, RatingLevel.EXTRA_HIGH: 0.00},
    ScaleFactor.RESL: {RatingLevel.VERY_LOW: 7.07, RatingLevel.LOW: 5.65, RatingLevel.NOMINAL: 4.24, RatingLevel.HIGH: 2.83, RatingLevel.HIGH: 1.41, RatingLevel.EXTRA_HIGH: 0.00},
    ScaleFactor.TEAM: {RatingLevel.VERY_LOW: 5.48, RatingLevel.LOW: 4.38, RatingLevel.NOMINAL: 3.29, RatingLevel.HIGH: 2.19, RatingLevel.HIGH: 1.10, RatingLevel.EXTRA_HIGH: 0.00},
    ScaleFactor.PMAT: {RatingLevel.VERY_LOW: 7.80, RatingLevel.LOW: 6.24, RatingLevel.NOMINAL: 4.68, RatingLevel.HIGH: 3.12, RatingLevel.HIGH: 1.56, RatingLevel.EXTRA_HIGH: 0.00},
    
}

class EffortModifier(Enum):
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

EFFORT_MODIFIER_COST_DRIVERS = {
    EffortModifier.RELY: {RatingLevel.VERY_LOW: 0.82, RatingLevel.LOW: 0.92, RatingLevel.NOMINAL: 1.00, RatingLevel.HIGH: 1.10, RatingLevel.HIGH: 1.26},
    EffortModifier.DATA: {                            RatingLevel.LOW: 0.90, RatingLevel.NOMINAL: 1.00, RatingLevel.HIGH: 1.14, RatingLevel.HIGH: 1.28},
    EffortModifier.CPLX: {RatingLevel.VERY_LOW: 0.73, RatingLevel.LOW: 0.87, RatingLevel.NOMINAL: 1.00, RatingLevel.HIGH: 1.17, RatingLevel.VERY_HIGH: 1.34, RatingLevel.EXTRA_HIGH: 1.74},
    EffortModifier.RUSE: {                            RatingLevel.LOW: 0.95, RatingLevel.NOMINAL: 1.00, RatingLevel.HIGH: 1.07, RatingLevel.VERY_HIGH: 1.15, RatingLevel.EXTRA_HIGH: 1.24},
    EffortModifier.DOCU: {RatingLevel.VERY_LOW: 0.81, RatingLevel.LOW: 0.91, RatingLevel.NOMINAL: 1.00, RatingLevel.HIGH: 1.11, RatingLevel.VERY_HIGH: 1.23},
    EffortModifier.TIME: {                                                   RatingLevel.NOMINAL: 1.00, RatingLevel.HIGH: 1.11, RatingLevel.VERY_HIGH: 1.29, RatingLevel.EXTRA_HIGH: 1.63},
    EffortModifier.STOR: {                                                   RatingLevel.NOMINAL: 1.00, RatingLevel.HIGH: 1.05, RatingLevel.VERY_HIGH: 1.17, RatingLevel.EXTRA_HIGH: 1.46},
    EffortModifier.PVOL: {                            RatingLevel.LOW: 0.87, RatingLevel.NOMINAL: 1.00, RatingLevel.HIGH: 1.15, RatingLevel.VERY_HIGH: 1.30},
    EffortModifier.ACAP: {RatingLevel.VERY_LOW: 1.42, RatingLevel.LOW: 1.19, RatingLevel.NOMINAL: 1.00, RatingLevel.HIGH: 0.85, RatingLevel.VERY_HIGH: 0.71},
    EffortModifier.PCAP: {RatingLevel.VERY_LOW: 1.34, RatingLevel.LOW: 1.15, RatingLevel.NOMINAL: 1.00, RatingLevel.HIGH: 0.88, RatingLevel.VERY_HIGH: 0.76},
    EffortModifier.PCON: {RatingLevel.VERY_LOW: 1.29, RatingLevel.LOW: 1.12, RatingLevel.NOMINAL: 1.00, RatingLevel.HIGH: 0.90, RatingLevel.VERY_HIGH: 0.81},
    EffortModifier.APEX: {RatingLevel.VERY_LOW: 1.22, RatingLevel.LOW: 1.10, RatingLevel.NOMINAL: 1.00, RatingLevel.HIGH: 0.88, RatingLevel.VERY_HIGH: 0.81},
    EffortModifier.PLEX: {RatingLevel.VERY_LOW: 1.19, RatingLevel.LOW: 1.09, RatingLevel.NOMINAL: 1.00, RatingLevel.HIGH: 0.91, RatingLevel.VERY_HIGH: 0.85},
    EffortModifier.LTEX: {RatingLevel.VERY_LOW: 1.20, RatingLevel.LOW: 1.09, RatingLevel.NOMINAL: 1.00, RatingLevel.HIGH: 0.91, RatingLevel.VERY_HIGH: 0.84},
    EffortModifier.TOOL: {RatingLevel.VERY_LOW: 1.17, RatingLevel.LOW: 1.09, RatingLevel.NOMINAL: 1.00, RatingLevel.HIGH: 0.90, RatingLevel.VERY_HIGH: 0.78},
    EffortModifier.SITE: {RatingLevel.VERY_LOW: 1.22, RatingLevel.LOW: 1.09, RatingLevel.NOMINAL: 1.00, RatingLevel.HIGH: 0.93, RatingLevel.VERY_HIGH: 0.86, RatingLevel.EXTRA_HIGH: 0.80},
}

SCHEDULE_COST_DRIVER = {RatingLevel.VERY_LOW: 1.43, RatingLevel.LOW: 0.92, RatingLevel.NOMINAL: 1.00, RatingLevel.HIGH: 1.26, RatingLevel.VERY_HIGH: 1.26, RatingLevel.EXTRA_HIGH: 1.24}

class Language(Enum):
    Access = "Access"
    Ada83 = "Ada 83"
    Ada95 = "Ada 95"
    AI_Shell = "AI Shell"
    APL = "APL"
    AssemblyBasic = "Assembly - Basic"
    AssemblyMacro = "Assembly - Macro"
    BasicANSI = "Basic - ANSI"
    BasicCompiled = "Basic - Compiled"
    BasicVisual = "Basic - Visual"
    VisualBasic5 = "Visual Basic 5.0"
    C = "C"
    Cpp = "C++"
    VisualCpp = "Visual C++"
    Cobol85 = "Cobol (ANSI 85)"
    Database = "Database"
    FirstGenerationLanguage = "First Generation Language"
    SecondGenerationLanguage = "Second Generation Language"
    ThirdGenerationLanguage = "Third Generation Language"
    FourthGenerationLanguage = "Fourth Generation Language"
    FifthGenerationLanguage = "Fifth Generation Language"
    Forth = "Forth"
    Fortran77 = "Fortran 77"
    Fortran95 = "Fortran 95"
    HighLevelLanguage = "High Level Language"
    HTML3 = "HTML 3.0"
    Java = "Java"
    Jovial = "Jovial"
    Lisp = "Lisp"
    MachineCode = "Machine Code"
    Modula2 = "Modula 2"
    Pascal = "Pascal"
    PERL = "PERL"
    PowerBuilder = "PowerBuilder"
    Prolog = "Prolog"
    Query = "Query"
    ReportGenerator = "Report Generator"
    Simulation = "Simulation"
    Spreadsheet = "Spreadsheet"
    UnixShellScript = "Unix Shell Script"


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