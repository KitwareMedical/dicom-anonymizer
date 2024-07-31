# Tags anonymized in DICOM standard
# Documentation for groups meaning can be found in default associated actions.
# http://dicom.nema.org/dicom/2023/output/chtml/part15/chapter_E.html#table_E.1-1

# Replaced tags
D_TAGS = [
    (0x0018, 0x11BB),  # Acquisition Field Of View Label
    (0x006A, 0x0005),  # Annotation Group Label
    (0x006A, 0x0003),  # Annotation Group UID
    (0x0044, 0x0104),  # Assertion DateTime
    (0x0400, 0x0562),  # Attribute Modification DateTime
    (0x300C, 0x0127),  # Beam Hold Transition DateTime
    (0x0400, 0x0115),  # Certificate of Signer
    (0x0012, 0x0081),  # Clinical Trial Protocol Ethics Committee Name
    (0x0012, 0x0020),  # Clinical Trial Protocol ID
    (0x0012, 0x0010),  # Clinical Trial Sponsor Name
    (0x0012, 0x0040),  # Clinical Trial Subject ID
    (0x0012, 0x0042),  # Clinical Trial Subject Reading ID
    (0x0040, 0x0512),  # Container Identifier
    (0x0040, 0xA730),  # Content Sequence
    (0x0008, 0x0107),  # Context Group Local Version
    (0x0008, 0x0106),  # Context Group Version
    (0x0040, 0xA121),  # Date
    (0x0040, 0xA120),  # DateTime
    (0x0018, 0x9701),  # Decay Correction DateTime
    (0x2100, 0x0140),  # Destination AE
    (0x3010, 0x002D),  # Device Label
    (0x0400, 0x0105),  # Digital Signature DateTime
    (0x0068, 0x6226),  # Effective DateTime
    (0x0042, 0x0011),  # Encapsulated Document
    (0x3010, 0x0035),  # Entity Label
    (0x3010, 0x0038),  # Entity Long Label
    (0x0018, 0x9804),  # Exclusion Start DateTime
    (0x0034, 0x0002),  # Flow Identifier
    (0x0034, 0x0001),  # Flow Identifier Sequence
    (0x0018, 0x9074),  # Frame Acquisition DateTime
    (0x0034, 0x0007),  # Frame Origin Timestamp
    (0x0018, 0x9151),  # Frame Reference DateTime
    (0x0018, 0x9623),  # Functional Sync Pulse
    (0x0070, 0x0001),  # Graphic Annotation Sequence
    (0x0072, 0x000A),  # Hanging Protocol Creation DateTime
    (0x003A, 0x0314),  # Impedance Measurement DateTime
    (0x0068, 0x6270),  # Information Issue DateTime
    (0x300A, 0x0741),  # Interlock DateTime
    (0x300A, 0x0742),  # Interlock Description
    (0x300A, 0x0783),  # Interlock Origin Description
    (0x0400, 0x0563),  # Modifying System
    (0x300A, 0x0760),  # Override DateTime
    (0x0040, 0x1101),  # Person Identification Code Sequence
    (0x0040, 0xA123),  # Person Name
    (0x300A, 0x0002),  # RT Plan Label
    (0x3010, 0x0054),  # RT Prescription Label
    (0x300A, 0x062A),  # RT Tolerance Set Label
    (0x300A, 0x0619),  # Radiation Dose Identification Label
    (0x300A, 0x0623),  # Radiation Dose In-Vivo Measurement Label
    (0x300A, 0x067C),  # Radiation Generation Mode Label
    (0x0400, 0x0565),  # Reason for the Attribute Modification
    (0x300A, 0x073A),  # Recorded RT Control Point DateTime
    (0x0040, 0xA13A),  # Referenced DateTime
    (0x3008, 0x0162),  # Safe Position Exit Date
    (0x3008, 0x0164),  # Safe Position Exit Time
    (0x3008, 0x0166),  # Safe Position Return Date
    (0x3008, 0x0168),  # Safe Position Return Time
    (0x0072, 0x005E),  # Selector AE Value
    (0x0072, 0x005F),  # Selector AS Value
    (0x0072, 0x0061),  # Selector DA Value
    (0x0072, 0x0063),  # Selector DT Value
    (0x0072, 0x0066),  # Selector LO Value
    (0x0072, 0x0068),  # Selector LT Value
    (0x0072, 0x0065),  # Selector OB Value
    (0x0072, 0x006A),  # Selector PN Value
    (0x0072, 0x006C),  # Selector SH Value
    (0x0072, 0x006E),  # Selector ST Value
    (0x0072, 0x006B),  # Selector TM Value
    (0x0072, 0x006D),  # Selector UN Value
    (0x0072, 0x0071),  # Selector UR Value
    (0x0072, 0x0070),  # Selector UT Value
    (0x0018, 0x936A),  # Source End DateTime
    (0x0034, 0x0005),  # Source Identifier
    (0x0018, 0x9369),  # Source Start DateTime
    (0x300A, 0x022C),  # Source Strength Reference Date
    (0x300A, 0x022E),  # Source Strength Reference Time
    (0x0040, 0x0551),  # Specimen Identifier
    (0x3006, 0x0002),  # Structure Set Label
    (0x0040, 0xA122),  # Time
    (0x3008, 0x0024),  # Treatment Control Point Date
    (0x3008, 0x0025),  # Treatment Control Point Time
    (0x300A, 0x0608),  # Treatment Position Group Label
    (0x300A, 0x0736),  # Treatment Tolerance Violation DateTime
    (0x300A, 0x0734),  # Treatment Tolerance Violation Description
    (0x3010, 0x0033),  # User Content Label
    (0x3010, 0x0034),  # User Content Long Label
    (0x0040, 0xA030),  # Verification DateTime
    (0x0040, 0xA075),  # Verifying Observer Name
    (0x0040, 0xA073),  # Verifying Observer Sequence
    (0x0040, 0xA027),  # Verifying Organization
    (0x0018, 0x9371),  # X-Ray Detector ID
    (0x0018, 0x9367),  # X-Ray Source ID
]

# Replaced with empty values (0, '', ...)
Z_TAGS = [
    (0x0008, 0x0050),  # Accession Number
    (0x0018, 0x1203),  # Calibration DateTime
    (0x0012, 0x0060),  # Clinical Trial Coordinating Center Name
    (0x0012, 0x0021),  # Clinical Trial Protocol Name
    (0x0012, 0x0030),  # Clinical Trial Site ID
    (0x0012, 0x0031),  # Clinical Trial Site Name
    (0x0012, 0x0050),  # Clinical Trial Time Point ID
    (0x3010, 0x000F),  # Conceptual Volume Combination Description
    (0x3010, 0x0017),  # Conceptual Volume Description
    (0x0008, 0x009C),  # Consulting Physician's Name
    (0x3010, 0x001B),  # Device Alternate Identifier
    (0x0040, 0x2017),  # Filler Order Number / Imaging Service Request
    (0x3010, 0x007F),  # Fractionation Notes
    (0x0040, 0x0513),  # Issuer of the Container Identifier Sequence
    (0x0040, 0x0562),  # Issuer of the Specimen Identifier Sequence
    (0x3010, 0x0043),  # Manufacturer's Device Identifier
    (0x0040, 0xA082),  # Participation DateTime
    (0x0010, 0x0020),  # Patient ID
    (0x0010, 0x0030),  # Patient's Birth Date
    (0x0010, 0x0010),  # Patient's Name
    (0x0010, 0x0040),  # Patient's Sex
    (0x0040, 0x2016),  # Placer Order Number / Imaging Service Request
    (0x3010, 0x007B),  # Prescription Notes
    (0x3010, 0x0081),  # Prescription Notes Sequence
    (0x3006, 0x00A6),  # ROI Interpreter
    (0x3006, 0x0026),  # ROI Name
    (0x300A, 0x0615),  # RT Accessory Device Slot ID
    (0x300A, 0x0611),  # RT Accessory Holder Slot ID
    (0x3010, 0x005A),  # RT Physician Intent Narrative
    (0x300A, 0x067D),  # Radiation Generation Mode Description
    (0x3010, 0x005C),  # Reason for Superseding
    (0x0008, 0x0090),  # Referring Physician's Name
    (0x300E, 0x0004),  # Review Date
    (0x300E, 0x0005),  # Review Time
    (0x0400, 0x0564),  # Source of Previous Values
    (0x0040, 0x0610),  # Specimen Preparation Sequence
    (0x3006, 0x0008),  # Structure Set Date
    (0x3006, 0x0009),  # Structure Set Time
    (0x0008, 0x0020),  # Study Date
    (0x0020, 0x0010),  # Study ID
    (0x0008, 0x0030),  # Study Time
    (0x3010, 0x007A),  # Treatment Technique Notes
    (0x0040, 0xA088),  # Verifying Observer Identification Code Sequence
]

# Deleted tags
X_TAGS = [
    (0x0018, 0x4000),  # Acquisition Comments
    (0x0018, 0x9424),  # Acquisition Protocol Description
    (0x0040, 0x4035),  # Actual Human Performers Sequence
    (0x0010, 0x21B0),  # Additional Patient History
    (0x0040, 0xA353),  # Address (Trial)
    (0x0038, 0x0010),  # Admission ID
    (0x0038, 0x0020),  # Admitting Date
    (0x0008, 0x1084),  # Admitting Diagnoses Code Sequence
    (0x0008, 0x1080),  # Admitting Diagnoses Description
    (0x0038, 0x0021),  # Admitting Time
    (0x0000, 0x1000),  # Affected SOP Instance UID
    (0x0010, 0x2110),  # Allergies
    (0x006A, 0x0006),  # Annotation Group Description
    (0x0044, 0x0004),  # Approval Status DateTime
    (0x4000, 0x0010),  # Arbitrary
    (0x0044, 0x0105),  # Assertion Expiration DateTime
    (0x0040, 0xA078),  # Author Observer Sequence
    (0x300A, 0x00C3),  # Beam Description
    (0x300A, 0x00DD),  # Bolus Description
    (0x0010, 0x1081),  # Branch of Service
    (0x0014, 0x407E),  # Calibration Date
    (0x0014, 0x407C),  # Calibration Time
    (0x0016, 0x004D),  # Camera Owner Name
    (0x0018, 0x1007),  # Cassette ID
    (0x0400, 0x0310),  # Certified Timestamp
    (0x0012, 0x0082),  # Clinical Trial Protocol Ethics Committee Approval Number
    (0x0012, 0x0072),  # Clinical Trial Series Description
    (0x0012, 0x0071),  # Clinical Trial Series ID
    (0x0012, 0x0051),  # Clinical Trial Time Point Description
    (0x0040, 0x0310),  # Comments on Radiation Dose
    (0x0040, 0x0280),  # Comments on the Performed Procedure Step
    (0x300A, 0x02EB),  # Compensator Description
    (0x0040, 0x3001),  # Confidentiality Constraint on Patient Data Description
    (0x0008, 0x009D),  # Consulting Physician Identification Sequence
    (0x0050, 0x001B),  # Container Component ID
    (0x0040, 0x051A),  # Container Description
    (0x0070, 0x0086),  # Content Creator's Identification Code Sequence
    (0x0018, 0x1042),  # Contrast/Bolus Start Time
    (0x0018, 0x1043),  # Contrast/Bolus Stop Time
    (0x0018, 0xA002),  # Contribution DateTime
    (0x0018, 0xA003),  # Contribution Description
    (0x0010, 0x2150),  # Country of Residence
    (0x2100, 0x0040),  # Creation Date
    (0x2100, 0x0050),  # Creation Time
    (0x0040, 0xA307),  # Current Observer (Trial)
    (0x0038, 0x0300),  # Current Patient Location
    (0x5000, 0x0000, 0xFF00, 0x0000),  # Curve Data
    (0x0008, 0x0025),  # Curve Date
    (0x0008, 0x0035),  # Curve Time
    (0x0040, 0xA07C),  # Custodial Organization Sequence
    (0xFFFC, 0xFFFC),  # Data Set Trailing Padding
    (0x0040, 0xA110),  # Date of Document or Verbal Transaction (Trial)
    (0x0018, 0x1205),  # Date of Installation
    (0x0018, 0x1200),  # Date of Last Calibration
    (0x0018, 0x1204),  # Date of Manufacture
    (0x0018, 0x1012),  # Date of Secondary Capture
    (0x0018, 0x1202),  # DateTime of Last Calibration
    (0x0018, 0x937F),  # Decomposition Description
    (0x0008, 0x2111),  # Derivation Description
    (0x0050, 0x0020),  # Device Description
    (0x0016, 0x004B),  # Device Setting Description
    (0xFFFA, 0xFFFA),  # Digital Signatures Sequence
    (0x0038, 0x0030),  # Discharge Date
    (0x0038, 0x0040),  # Discharge Diagnosis Description
    (0x0038, 0x0032),  # Discharge Time
    (0x300A, 0x079A),  # Displacement Reference Label
    (0x4008, 0x011A),  # Distribution Address
    (0x4008, 0x0119),  # Distribution Name
    (0x300A, 0x0016),  # Dose Reference Description
    (0x3010, 0x0037),  # Entity Description
    (0x3010, 0x0036),  # Entity Name
    (0x300A, 0x0676),  # Equipment Frame of Reference Description
    (0x0012, 0x0087),  # Ethics Committee Approval Effectiveness End Date
    (0x0012, 0x0086),  # Ethics Committee Approval Effectiveness Start Date
    (0x0010, 0x2160),  # Ethnic Group
    (0x0040, 0x4011),  # Expected Completion DateTime
    (0x003A, 0x032B),  # Filter Lookup Table Description
    (0x0040, 0xA023),  # Findings Group Recording Date (Trial)
    (0x0040, 0xA024),  # Findings Group Recording Time (Trial)
    (0x300A, 0x0196),  # Fixation Device Description
    (0x300A, 0x0072),  # Fraction Group Description
    (0x0020, 0x9158),  # Frame Comments
    (0x0016, 0x0076),  # GPS Altitude
    (0x0016, 0x0075),  # GPS Altitude Ref
    (0x0016, 0x008C),  # GPS Area Information
    (0x0016, 0x007B),  # GPS DOP
    (0x0016, 0x008D),  # GPS Date Stamp
    (0x0016, 0x0088),  # GPS Dest Bearing
    (0x0016, 0x008A),  # GPS Dest Distance
    (0x0016, 0x0089),  # GPS Dest Distance Ref
    (0x0016, 0x0086),  # GPS Dest Longitude
    (0x0016, 0x0085),  # GPS Dest Longitude Ref
    (0x0016, 0x0087),  # GPS Dest Bearing Ref
    (0x0016, 0x0084),  # GPS Dest Latitude
    (0x0016, 0x0083),  # GPS Dest Latitude Ref
    (0x0016, 0x008E),  # GPS Differential
    (0x0016, 0x0081),  # GPS Img Direction
    (0x0016, 0x0080),  # GPS Img Direction Ref
    (0x0016, 0x0072),  # GPS Latitude
    (0x0016, 0x0071),  # GPS Latitude Ref
    (0x0016, 0x0074),  # GPS Longitude
    (0x0016, 0x0073),  # GPS Longitude Ref
    (0x0016, 0x0082),  # GPS Map Datum
    (0x0016, 0x007A),  # GPS Measure Mode
    (0x0016, 0x008B),  # GPS Processing Method
    (0x0016, 0x0078),  # GPS Satellites
    (0x0016, 0x007D),  # GPS Speed
    (0x0016, 0x007C),  # GPS Speed Ref
    (0x0016, 0x0079),  # GPS Status
    (0x0016, 0x0077),  # GPS Time Stamp
    (0x0016, 0x007F),  # GPS Track
    (0x0016, 0x007E),  # GPS Track Ref
    (0x0016, 0x0070),  # GPS Version ID
    (0x0018, 0x1008),  # Gantry ID
    (0x0018, 0x1005),  # Generator ID
    (0x0040, 0xE004),  # HL7 Document Effective Time
    (0x0040, 0x4037),  # Human Performer's Name
    (0x0040, 0x4036),  # Human Performer's Organization
    (0x0088, 0x0200),  # Icon Image Sequence
    (0x0008, 0x4000),  # Identifying Comments
    (0x0020, 0x4000),  # Image Comments
    (0x0028, 0x4000),  # Image Presentation Comments
    (0x0040, 0x2400),  # Imaging Service Request Comments
    (0x4008, 0x0300),  # Impressions
    (0x0008, 0x0015),  # Instance Coercion DateTime
    (0x0400, 0x0600),  # Instance Origin Status
    (0x0008, 0x0081),  # Institution Address
    (0x0008, 0x1040),  # Institutional Department Name
    (0x0008, 0x1041),  # Institutional Department Type Code Sequence
    (0x0010, 0x1050),  # Insurance Plan Identification
    (0x3010, 0x0085),  # Intended Fraction Start Time
    (0x0040, 0x1011),  # Intended Recipients of Results Identification Sequence
    (0x4008, 0x0112),  # Interpretation Approval Date
    (0x4008, 0x0113),  # Interpretation Approval Time
    (0x4008, 0x0111),  # Interpretation Approver Sequence
    (0x4008, 0x010C),  # Interpretation Author
    (0x4008, 0x0115),  # Interpretation Diagnosis Description
    (0x4008, 0x0200),  # Interpretation ID
    (0x4008, 0x0202),  # Interpretation ID Issuer
    (0x4008, 0x0100),  # Interpretation Recorded Date
    (0x4008, 0x0101),  # Interpretation Recorded Time
    (0x4008, 0x0102),  # Interpretation Recorder
    (0x4008, 0x010B),  # Interpretation Text
    (0x4008, 0x010A),  # Interpretation Transcriber
    (0x4008, 0x0108),  # Interpretation Transcription Date
    (0x4008, 0x0109),  # Interpretation Transcription Time
    (0x0018, 0x0035),  # Intervention Drug Start Time
    (0x0018, 0x0027),  # Intervention Drug Stop Time
    (0x0040, 0x2004),  # Issue Date of Imaging Service Request
    (0x0040, 0x2005),  # Issue Time of Imaging Service Request
    (0x0038, 0x0011),  # Issuer of Admission ID
    (0x0038, 0x0014),  # Issuer of Admission ID Sequence
    (0x0010, 0x0021),  # Issuer of Patient ID
    (0x0038, 0x0061),  # Issuer of Service Episode ID
    (0x0038, 0x0064),  # Issuer of Service Episode ID Sequence
    (0x0010, 0x21D0),  # Last Menstrual Date
    (0x0016, 0x004F),  # Lens Make
    (0x0016, 0x0050),  # Lens Model
    (0x0016, 0x0051),  # Lens Serial Number
    (0x0016, 0x004E),  # Lens Specification
    (0x0050, 0x0021),  # Long Device Description
    (0x0400, 0x0404),  # MAC
    (0x0016, 0x002B),  # Maker Note
    (0x0010, 0x2000),  # Medical Alerts
    (0x0010, 0x1090),  # Medical Record Locator
    (0x0010, 0x1080),  # Military Rank
    (0x0400, 0x0550),  # Modified Attributes Sequence
    (0x0020, 0x3403),  # Modified Image Date
    (0x0020, 0x3406),  # Modified Image Description
    (0x0020, 0x3405),  # Modified Image Time
    (0x0020, 0x3401),  # Modifying Device ID
    (0x0018, 0x937B),  # Multi-energy Acquisition Description
    (0x0008, 0x1060),  # Name of Physician(s) Reading Study
    (0x0040, 0x1010),  # Names of Intended Recipients of Results
    (0x0008, 0x1000),  # Network ID
    (0x0400, 0x0552),  # Nonconforming Data Element Value
    (0x0400, 0x0551),  # Nonconforming Modified Attributes Sequence
    (0x0040, 0xA192),  # Observation Date (Trial)
    (0x0040, 0xA033),  # Observation Start DateTime
    (0x0040, 0xA193),  # Observation Time (Trial)
    (0x0010, 0x2180),  # Occupation
    (0x0040, 0x2010),  # Order Callback Phone Number
    (0x0040, 0x2011),  # Order Callback Telecom Information
    (0x0040, 0x2008),  # Order Entered By
    (0x0040, 0x2009),  # Order Enterer's Location
    (0x0400, 0x0561),  # Original Attributes Sequence
    (0x2100, 0x0070),  # Originator
    (0x0010, 0x1000),  # Other Patient IDs
    (0x0010, 0x1002),  # Other Patient IDs Sequence
    (0x0010, 0x1001),  # Other Patient Names
    (0x6000, 0x4000, 0xFF00, 0xFFFF),  # Overlay Comments
    (0x6000, 0x3000, 0xFF00, 0xFFFF),  # Overlay Data
    (0x0008, 0x0024),  # Overlay Date
    (0x0008, 0x0034),  # Overlay Time
    (0x0040, 0xA07A),  # Participant Sequence
    (0x0010, 0x4000),  # Patient Comments
    (0x300A, 0x0794),  # Patient Setup Photo Description
    (0x0038, 0x0500),  # Patient State
    (0x0040, 0x1004),  # Patient Transport Arrangements
    (0x300A, 0x0792),  # Patient Treatment Preparation Method Description
    (0x300A, 0x078E),  # Patient Treatment Preparation Procedure Parameter Description
    (0x0010, 0x1040),  # Patient's Address
    (0x0010, 0x1010),  # Patient's Age
    (0x0010, 0x1005),  # Patient's Birth Name
    (0x0010, 0x0032),  # Patient's Birth Time
    (0x0038, 0x0400),  # Patient's Institution Residence
    (0x0010, 0x0050),  # Patient's Insurance Plan Code Sequence
    (0x0010, 0x1060),  # Patient's Mother's Birth Name
    (0x0010, 0x0101),  # Patient's Primary Language Code Sequence
    (0x0010, 0x0102),  # Patient's Primary Language Modifier Code Sequence
    (0x0010, 0x21F0),  # Patient's Religious Preference
    (0x0010, 0x1020),  # Patient's Size
    (0x0010, 0x2155),  # Patient's Telecom Information
    (0x0010, 0x2154),  # Patient's Telephone Numbers
    (0x0010, 0x1030),  # Patient's Weight
    (0x0040, 0x0243),  # Performed Location
    (0x0040, 0x0254),  # Performed Procedure Step Description
    (0x0040, 0x0250),  # Performed Procedure Step End Date
    (0x0040, 0x4051),  # Performed Procedure Step End DateTime
    (0x0040, 0x0251),  # Performed Procedure Step End Time
    (0x0040, 0x0253),  # Performed Procedure Step ID
    (0x0040, 0x0244),  # Performed Procedure Step Start Date
    (0x0040, 0x4050),  # Performed Procedure Step Start DateTime
    (0x0040, 0x0245),  # Performed Procedure Step Start Time
    (0x0040, 0x0241),  # Performed Station AE Title
    (0x0040, 0x4030),  # Performed Station Geographic Location Code Sequence
    (0x0040, 0x0242),  # Performed Station Name
    (0x0040, 0x4028),  # Performed Station Name Code Sequence
    (0x0008, 0x1052),  # Performing Physician Identification Sequence
    (0x0008, 0x1050),  # Performing Physician's Name
    (0x0040, 0x1102),  # Person's Address
    (0x0040, 0x1104),  # Person's Telecom Information
    (0x0040, 0x1103),  # Person's Telephone Numbers
    (0x4008, 0x0114),  # Physician Approving Interpretation
    (0x0008, 0x1062),  # Physician(s) Reading Study Identification Sequence
    (0x0008, 0x1048),  # Physician(s) of Record
    (0x0008, 0x1049),  # Physician(s) of Record Identification Sequence
    (0x0018, 0x1004),  # Plate ID
    (0x3002, 0x0123),  # Position Acquisition Template Description
    (0x3002, 0x0121),  # Position Acquisition Template Name
    (0x0040, 0x0012),  # Pre-Medication
    (0x0010, 0x21C0),  # Pregnancy Status
    (0x300A, 0x000E),  # Prescription Description
    (0x0070, 0x0082),  # Presentation Creation Date
    (0x0070, 0x0083),  # Presentation Creation Time
    (0x3010, 0x0061),  # Prior Treatment Dose Description
    (0x0040, 0x4052),  # Procedure Step Cancellation DateTime
    (0x0044, 0x000B),  # Product Expiration DateTime
    (0x0008, 0x1088),  # Pyramid Description
    (0x0020, 0x0027),  # Pyramid Label
    (0x3006, 0x0028),  # ROI Description
    (0x3006, 0x0038),  # ROI Generation Description
    (0x3006, 0x0088),  # ROI Observation Description
    (0x3006, 0x0085),  # ROI Observation Label
    (0x300A, 0x0004),  # RT Plan Description
    (0x300A, 0x0003),  # RT Plan Name
    (0x0018, 0x1078),  # Radiopharmaceutical Start DateTime
    (0x0018, 0x1072),  # Radiopharmaceutical Start Time
    (0x0018, 0x1079),  # Radiopharmaceutical Stop DateTime
    (0x0018, 0x1073),  # Radiopharmaceutical Stop Time
    (0x300C, 0x0113),  # Reason for Omission Description
    (0x0040, 0x100A),  # Reason for Requested Procedure Code Sequence
    (0x0032, 0x1030),  # Reason for Study
    (0x0032, 0x1066),  # Reason for Visit
    (0x0032, 0x1067),  # Reason for Visit Code Sequence
    (0x0040, 0x2001),  # Reason for the Imaging Service Request
    (0x0040, 0x1002),  # Reason for the Requested Procedure
    (0x0074, 0x1234),  # Receiving AE
    (0x0400, 0x0402),  # Referenced Digital Signature Sequence
    (0x0038, 0x0004),  # Referenced Patient Alias Sequence
    (0x0010, 0x1100),  # Referenced Patient Photo Sequence
    (0x0008, 0x1120),  # Referenced Patient Sequence
    (0x0400, 0x0403),  # Referenced SOP Instance MAC Sequence
    (0x0008, 0x0096),  # Referring Physician Identification Sequence
    (0x0008, 0x0092),  # Referring Physician's Address
    (0x0008, 0x0094),  # Referring Physician's Telephone Numbers
    (0x0010, 0x2152),  # Region of Residence
    (0x0040, 0x0275),  # Request Attributes Sequence
    (0x0032, 0x1070),  # Requested Contrast Agent
    (0x0040, 0x1400),  # Requested Procedure Comments
    (0x0040, 0x1001),  # Requested Procedure ID
    (0x0040, 0x1005),  # Requested Procedure Location
    (0x0018, 0x9937),  # Requested Series Description
    (0x0074, 0x1236),  # Requesting AE
    (0x0032, 0x1032),  # Requesting Physician
    (0x0032, 0x1033),  # Requesting Service
    (0x0018, 0x9185),  # Respiratory Motion Compensation Technique Description
    (0x0010, 0x2299),  # Responsible Organization
    (0x0010, 0x2297),  # Responsible Person
    (0x4008, 0x4000),  # Results Comments
    (0x4008, 0x0118),  # Results Distribution List Sequence
    (0x4008, 0x0040),  # Results ID
    (0x4008, 0x0042),  # Results ID Issuer
    (0x0008, 0x0054),  # Retrieve AE Title
    (0x0100, 0x0420),  # SOP Authorization DateTime
    (0x0038, 0x001A),  # Scheduled Admission Date
    (0x0038, 0x001B),  # Scheduled Admission Time
    (0x0038, 0x001C),  # Scheduled Discharge Date
    (0x0038, 0x001D),  # Scheduled Discharge Time
    (0x0040, 0x4034),  # Scheduled Human Performers Sequence
    (0x0038, 0x001E),  # Scheduled Patient Institution Residence
    (0x0040, 0x000B),  # Scheduled Performing Physician Identification Sequence
    (0x0040, 0x0006),  # Scheduled Performing Physician's Name
    (0x0040, 0x0007),  # Scheduled Procedure Step Description
    (0x0040, 0x0004),  # Scheduled Procedure Step End Date
    (0x0040, 0x0005),  # Scheduled Procedure Step End Time
    (0x0040, 0x4008),  # Scheduled Procedure Step Expiration DateTime
    (0x0040, 0x0009),  # Scheduled Procedure Step ID
    (0x0040, 0x0011),  # Scheduled Procedure Step Location
    (0x0040, 0x4010),  # Scheduled Procedure Step Modification DateTime
    (0x0040, 0x0002),  # Scheduled Procedure Step Start Date
    (0x0040, 0x4005),  # Scheduled Procedure Step Start DateTime
    (0x0040, 0x0003),  # Scheduled Procedure Step Start Time
    (0x0040, 0x0001),  # Scheduled Station AE Title
    (0x0040, 0x4027),  # Scheduled Station Geographic Location Code Sequence
    (0x0040, 0x0010),  # Scheduled Station Name
    (0x0040, 0x4025),  # Scheduled Station Name Code Sequence
    (0x0032, 0x1020),  # Scheduled Study Location
    (0x0032, 0x1021),  # Scheduled Study Location AE Title
    (0x0032, 0x1000),  # Scheduled Study Start Date
    (0x0032, 0x1001),  # Scheduled Study Start Time
    (0x0032, 0x1010),  # Scheduled Study Stop Date
    (0x0032, 0x1011),  # Scheduled Study Stop Time
    (0x0008, 0x103E),  # Series Description
    (0x0038, 0x0062),  # Service Episode Description
    (0x0038, 0x0060),  # Service Episode ID
    (0x300A, 0x01B2),  # Setup Technique Description
    (0x300A, 0x01A6),  # Shielding Device Description
    (0x0040, 0x06FA),  # Slide Identifier
    (0x0010, 0x21A0),  # Smoking Status
    (0x300A, 0x0216),  # Source Manufacturer
    (0x0038, 0x0050),  # Special Needs
    (0x0040, 0x050A),  # Specimen Accession Number
    (0x0040, 0x0602),  # Specimen Detailed Description
    (0x0040, 0x0600),  # Specimen Short Description
    (0x0008, 0x0055),  # Station AE Title
    (0x3006, 0x0006),  # Structure Set Description
    (0x3006, 0x0004),  # Structure Set Name
    (0x0032, 0x1040),  # Study Arrival Date
    (0x0032, 0x1041),  # Study Arrival Time
    (0x0032, 0x4000),  # Study Comments
    (0x0032, 0x1050),  # Study Completion Date
    (0x0032, 0x1051),  # Study Completion Time
    (0x0008, 0x1030),  # Study Description
    (0x0032, 0x0012),  # Study ID Issuer
    (0x0032, 0x0034),  # Study Read Date
    (0x0032, 0x0035),  # Study Read Time
    (0x0032, 0x0032),  # Study Verified Date
    (0x0032, 0x0033),  # Study Verified Time
    (0x0044, 0x0010),  # Substance Administration DateTime
    (0x0040, 0xA354),  # Telephone Number (Trial)
    (0x0040, 0xDB07),  # Template Local Version
    (0x0040, 0xDB06),  # Template Version
    (0x4000, 0x4000),  # Text Comments
    (0x2030, 0x0020),  # Text String
    (0x0040, 0xA112),  # Time of Document Creation or Verbal Transaction (Trial)
    (0x0018, 0x1201),  # Time of Last Calibration
    (0x0018, 0x1014),  # Time of Secondary Capture
    (0x0008, 0x0201),  # Timezone Offset From UTC
    (0x0088, 0x0910),  # Topic Author
    (0x0088, 0x0912),  # Topic Keywords
    (0x0088, 0x0906),  # Topic Subject
    (0x0088, 0x0904),  # Topic Title
    (0x0018, 0x5011),  # Transducer Identification Sequence
    (0x300A, 0x000B),  # Treatment Sites
    (0x0018, 0x100A),  # UDI Sequence
    (0x0018, 0x1009),  # Unique Device Identifier
    (0x0040, 0xA352),  # Verbal Source (Trial)
    (0x0040, 0xA358),  # Verbal Source Identifier Code Sequence (Trial)
    (0x0038, 0x4000),  # Visit Comments
    (0x0018, 0x9373),  # X-Ray Detector Label
    (0x003A, 0x0329),  # Waveform Filter Description
]

# Replace UID
U_TAGS = [
    (0x0008, 0x0017),  # Acquisition UID
    (0x0020, 0x9161),  # Concatenation UID
    (0x3010, 0x0006),  # Conceptual Volume UID
    (0x3010, 0x0013),  # Constituent Conceptual Volume UID
    (0x0018, 0x1002),  # Device UID
    (0x0400, 0x0100),  # Digital Signature UID
    (0x0020, 0x9164),  # Dimension Organization UID
    (0x300A, 0x0013),  # Dose Reference UID
    (0x3010, 0x006E),  # Dosimetric Objective UID
    (0x0008, 0x0058),  # Failed SOP Instance UID List
    (0x0070, 0x031A),  # Fiducial UID
    (0x0020, 0x0052),  # Frame of Reference UID
    (0x0008, 0x0014),  # Instance Creator UID
    (0x0008, 0x3010),  # Irradiation Event UID
    (0x0028, 0x1214),  # Large Palette Color Lookup Table UID
    (0x0018, 0x100B),  # Manufacturer's Device Class UID
    (0x0002, 0x0003),  # Media Storage SOP Instance UID
    (0x003A, 0x0310),  # Multiplex Group UID
    (0x0040, 0xA402),  # Observation Subject UID (Trial)
    (0x0040, 0xA171),  # Observation UID
    (0x0028, 0x1199),  # Palette Color Lookup Table UID
    (0x300A, 0x0650),  # Patient Setup UID
    (0x0070, 0x1101),  # Presentation Display Collection UID
    (0x0070, 0x1102),  # Presentation Sequence Collection UID
    (0x0008, 0x0019),  # Pyramid UID
    (0x3010, 0x003B),  # RT Treatment Phase UID
    (0x3010, 0x000B),  # Referenced Conceptual Volume UID
    (0x300A, 0x0083),  # Referenced Dose Reference UID
    (0x3010, 0x006F),  # Referenced Dosimetric Objective UID
    (0x3010, 0x0031),  # Referenced Fiducials UID
    (0x3006, 0x0024),  # Referenced Frame of Reference UID
    (
        0x0040,
        0x4023,
    ),  # Referenced General Purpose Scheduled Procedure Step Transaction UID
    (0x0040, 0xA172),  # Referenced Observation UID (Trial)
    (0x0008, 0x1155),  # Referenced SOP Instance UID
    (0x0004, 0x1511),  # Referenced SOP Instance UID in File
    (0x300A, 0x0785),  # Referenced Treatment Position Group UID
    (0x3006, 0x00C2),  # Related Frame of Reference UID
    (0x0000, 0x1001),  # Requested SOP Instance UID
    (0x0008, 0x0018),  # SOP Instance UID
    (0x0020, 0x000E),  # Series Instance UID
    (0x3010, 0x0015),  # Source Conceptual Volume UID
    (0x0064, 0x0003),  # Source Frame of Reference UID
    (0x0040, 0x0554),  # Specimen UID
    (0x0088, 0x0140),  # Storage Media File-set UID
    (0x0020, 0x000D),  # Study Instance UID
    (0x0020, 0x0200),  # Synchronization Frame of Reference UID
    (0x0018, 0x2042),  # Target UID
    (0x0040, 0xDB0D),  # Template Extension Creator UID
    (0x0040, 0xDB0C),  # Template Extension Organization UID
    (0x0062, 0x0021),  # Tracking UID
    (0x0008, 0x1195),  # Transaction UID
    (0x300A, 0x0609),  # Treatment Position Group UID
    (0x300A, 0x0700),  # Treatment Session UID
    (0x0040, 0xA124),  # UID
]

# Replace element according to the VR
Z_D_TAGS = [
    (0x0070, 0x0084),  # Content Creator's Name
    (0x0008, 0x0023),  # Content Date
    (0x0008, 0x0033),  # Content Time
    (0x0018, 0x0010),  # Contrast/Bolus Agent
    (0x0018, 0x9919),  # Instruction Performed DateTime
]

# Set the value to empty according to the VR
X_Z_TAGS = [
    (0x0040, 0x0555),  # Acquisition Context Sequence
    (0x0008, 0x0022),  # Acquisition Date
    (0x0008, 0x0032),  # Acquisition Time
    (0x2200, 0x0005),  # Barcode Value
    (0x2200, 0x0002),  # Label Text
    (0x0010, 0x2203),  # Patient's Sex Neutered
    (0x0008, 0x1110),  # Referenced Study Sequence
    (0x0032, 0x1060),  # Requested Procedure Description
    (0x300E, 0x0008),  # Reviewer Name
    (0x3008, 0x0105),  # Source Serial Number
    (0x300A, 0x00B2),  # Treatment Machine Name
]

# Replace element according to the VR
X_D_TAGS = [
    (0x0018, 0x1400),  # Acquisition Device Processing Description
    (0x0018, 0x700C),  # Date of Last Detector Calibration
    (0x0018, 0x700A),  # Detector ID
    (0x0018, 0x9517),  # End Acquisition DateTime
    (0x3008, 0x0054),  # First Treatment Date
    (0x0008, 0x0012),  # Instance Creation Date
    (0x3010, 0x004D),  # Intended Phase End Date
    (0x3010, 0x004C),  # Intended Phase Start Date
    (0x3008, 0x0056),  # Most Recent Treatment Date
    (0x0040, 0xA032),  # Observation DateTime
    (0x0008, 0x1072),  # Operator Identification Sequence
    (0x0018, 0x1030),  # Protocol Name
    (0x300A, 0x0006),  # RT Plan Date
    (0x300A, 0x0007),  # RT Plan Time
    (0x3010, 0x0056),  # RT Treatment Approach Label
    (0x0008, 0x0021),  # Series Date
    (0x0008, 0x0031),  # Series Time
    (0x0018, 0x9516),  # Start Acquisition DateTime
    (0x0018, 0x700E),  # Time of Last Detector Calibration
    (0x3008, 0x0250),  # Treatment Date
    (0x3010, 0x0077),  # Treatment Site
    (0x3008, 0x0251),  # Treatment Time
]


# Replace element according to the VR
X_Z_D_TAGS = [
    (0x0008, 0x002A),  # Acquisition DateTime
    (0x0018, 0x1000),  # Device Serial Number
    (0x0008, 0x0013),  # Instance Creation Time
    (0x0008, 0x0082),  # Institution Code Sequence
    (0x0008, 0x0080),  # Institution Name
    (0x0008, 0x1070),  # Operators' Name
    (0x0008, 0x1111),  # Referenced Performed Procedure Step Sequence
    (0x0008, 0x1010),  # Station Name
]

# Replace element with UI as VR, else replace according to VR with empty values
X_Z_U_STAR_TAGS = [
    (0x0008, 0x1140),  # Referenced Image Sequence
    (0x0008, 0x2112),  # Source Image Sequence
]

# Contains all previous tags into one array
ALL_TAGS = []
ALL_TAGS.extend(D_TAGS)
ALL_TAGS.extend(Z_TAGS)
ALL_TAGS.extend(X_TAGS)
ALL_TAGS.extend(U_TAGS)
ALL_TAGS.extend(Z_D_TAGS)
ALL_TAGS.extend(X_Z_TAGS)
ALL_TAGS.extend(X_D_TAGS)
ALL_TAGS.extend(X_Z_D_TAGS)
ALL_TAGS.extend(X_Z_U_STAR_TAGS)
