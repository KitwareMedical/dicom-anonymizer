# Tags anonymized in DICOM standard
# Documentation for groups meaning can be found in default associated actions.
# http://dicom.nema.org/dicom/2013/output/chtml/part15/chapter_E.html#table_E.1-1

# Replaced tags
D_TAGS = [
    (0x0070, 0x0001),  # Graphic Annotation Sequence
    (0x0040, 0x1101),  # Person Identification Code Sequence
    (0x0040, 0xA123),  # Person Name
    (0x0040, 0xA075),  # Verifying Observer Name
    (0x0040, 0xA073),  # Verifying Observer Sequence
]

# Replaced with empty values (0, '', ...)
Z_TAGS = [
    (0x0008, 0x0050),  # Accession Number
    (0x0070, 0x0084),  # Content Creator's Name
    (0x0040, 0x2017),  # Filler Order Number / Imaging Service Request
    (0x0010, 0x0020),  # Patient ID
    (0x0010, 0x0030),  # Patient's Birth Date
    (0x0010, 0x0010),  # Patient's Name
    (0x0010, 0x0040),  # Patient's Sex
    (0x0040, 0x2016),  # Placer Order Number / Imaging Service Request
    (0x0008, 0x0090),  # Referring Physician's Name
    (0x0008, 0x0020),  # Study Date
    (0x0020, 0x0010),  # Study ID
    (0x0008, 0x0030),  # Study Time
    (0x0040, 0xA088),  # Verifying Observer Identification Code Sequence
]

# Deleted tags
X_TAGS = [
    (0x0018, 0x4000),  # Acquisition Comments
    (0x0040, 0x0555),  # Acquisition Context Sequence
    (0x0018, 0x9424),  # Acquisition Protocol Description
    (0x0040, 0x4035),  # Actual Human Performers Sequence
    (0x0010, 0x21B0),  # Additional Patient's History
    (0x0038, 0x0010),  # Admission ID
    (0x0038, 0x0020),  # Admitting Date
    (0x0008, 0x1084),  # Admitting Diagnoses Code Sequence
    (0x0008, 0x1080),  # Admitting Diagnoses Description
    (0x0038, 0x0021),  # Admitting Time
    (0x0000, 0x1000),  # Affected SOP Instance UID
    (0x0010, 0x2110),  # Allergies
    (0x4000, 0x0010),  # Arbitrary
    (0x0040, 0xA078),  # Author Observer Sequence
    (0x0010, 0x1081),  # Branch of Service
    (0x0018, 0x1007),  # Cassette ID
    (0x0040, 0x0280),  # Comments on the Performed Procedure Step
    (0x0040, 0x3001),  # Confidentiality Constraint on Patient Data Description
    (0x0070, 0x0086),  # Content Creator's Identification Code Sequence
    (0x0040, 0xA730),  # Content Sequence
    (0x0018, 0xA003),  # Contribution Description
    (0x0010, 0x2150),  # Country of Residence
    (0x0038, 0x0300),  # Current Patient Location
    (0x5000, 0x0000, 0xFF00, 0x0000),  # Curve Data
    (0x0008, 0x0025),  # Curve Date
    (0x0008, 0x0035),  # Curve Time
    (0x0040, 0xA07C),  # Custodial Organization Sequence
    (0xFFFC, 0xFFFC),  # Data Set Trailing Padding
    (0x0008, 0x2111),  # Derivation Description
    (0x0400, 0x0100),  # Digital Signature UID
    (0xFFFA, 0xFFFA),  # Digital Signatures Sequence
    (0x0038, 0x0040),  # Discharge Diagnosis Description
    (0x4008, 0x011A),  # Distribution Address
    (0x4008, 0x0119),  # Distribution Name
    (0x0010, 0x2160),  # Ethnic Group
    (0x0020, 0x9158),  # Frame Comments
    (0x0018, 0x1008),  # Gantry ID
    (0x0018, 0x1005),  # Generator ID
    (0x0040, 0x4037),  # Human Performers Name
    (0x0040, 0x4036),  # Human Performers Organization
    (0x0088, 0x0200),  # Icon Image Sequence(see Note 12)
    (0x0008, 0x4000),  # Identifying Comments
    (0x0020, 0x4000),  # Image Comments
    (0x0028, 0x4000),  # Image Presentation Comments
    (0x0040, 0x2400),  # Imaging Service Request Comments
    (0x4008, 0x0300),  # Impressions
    (0x0008, 0x0081),  # Institution Address
    (0x0008, 0x1040),  # Institutional Department Name
    (0x0010, 0x1050),  # Insurance Plan Identification
    (0x0040, 0x1011),  # Intended Recipients of Results Identification Sequence
    (0x4008, 0x0111),  # Interpretation Approver Sequence
    (0x4008, 0x010C),  # Interpretation Author
    (0x4008, 0x0115),  # Interpretation Diagnosis Description
    (0x4008, 0x0202),  # Interpretation ID Issuer
    (0x4008, 0x0102),  # Interpretation Recorder
    (0x4008, 0x010B),  # Interpretation Text
    (0x4008, 0x010A),  # Interpretation Transcriber
    (0x0038, 0x0011),  # Issuer of Admission ID
    (0x0010, 0x0021),  # Issuer of Patient ID
    (0x0038, 0x0061),  # Issuer of Service Episode ID
    (0x0010, 0x21D0),  # Last Menstrual Date
    (0x0400, 0x0404),  # MAC
    (0x0010, 0x2000),  # Medical Alerts
    (0x0010, 0x1090),  # Medical Record Locator
    (0x0010, 0x1080),  # Military Rank
    (0x0400, 0x0550),  # Modified Attributes Sequence
    (0x0020, 0x3406),  # Modified Image Description
    (0x0020, 0x3401),  # Modifying Device ID
    (0x0020, 0x3404),  # Modifying Device Manufacturer
    (0x0008, 0x1060),  # Name of Physician(s) Reading Study
    (0x0040, 0x1010),  # Names of Intended Recipient of Results
    (0x0010, 0x2180),  # Occupation
    (0x0400, 0x0561),  # Original Attributes Sequence
    (0x0040, 0x2010),  # Order Callback Phone Number
    (0x0040, 0x2008),  # Order Entered By
    (0x0040, 0x2009),  # Order Enterer Location
    (0x0010, 0x1000),  # Other Patient IDs
    (0x0010, 0x1002),  # Other Patient IDs Sequence
    (0x0010, 0x1001),  # Other Patient Names
    (0x6000, 0x4000, 0xFF00, 0xFFFF),  # Overlay Comments
    (0x6000, 0x3000, 0xFF00, 0xFFFF),  # Overlay Data
    (0x0008, 0x0024),  # Overlay Date
    (0x0008, 0x0034),  # Overlay Time
    (0x0040, 0xA07A),  # Participant Sequence
    (0x0010, 0x1040),  # Patient Address
    (0x0010, 0x4000),  # Patient Comments
    (0x0038, 0x0500),  # Patient State
    (0x0040, 0x1004),  # Patient Transport Arrangements
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
    (0x0010, 0x2154),  # Patient's Telephone Numbers
    (0x0010, 0x1030),  # Patient's Weight
    (0x0040, 0x0243),  # Performed Location
    (0x0040, 0x0254),  # Performed Procedure Step Description
    (0x0040, 0x0250),  # Performed Procedure Step End Date
    (0x0040, 0x0251),  # Performed Procedure Step End Time
    (0x0040, 0x0253),  # Performed Procedure Step ID
    (0x0040, 0x0244),  # Performed Procedure Step Start Date
    (0x0040, 0x0245),  # Performed Procedure Step Start Time
    (0x0040, 0x0241),  # Performed Station AE Title
    (0x0040, 0x4030),  # Performed Station Geographic Location Code Sequence
    (0x0040, 0x0242),  # Performed Station Name
    (0x0040, 0x4028),  # Performed Station Name Code Sequence
    (0x0008, 0x1052),  # Performing Physician Identification Sequence
    (0x0008, 0x1050),  # Performing Physicians' Name
    (0x0040, 0x1102),  # Person Address
    (0x0040, 0x1103),  # Person Telephone Numbers
    (0x4008, 0x0114),  # Physician Approving Interpretation
    (0x0008, 0x1062),  # Physician(s) Reading Study Identification Sequence
    (0x0008, 0x1048),  # Physician(s) of Record
    (0x0008, 0x1049),  # Physician(s) of Record Identification Sequence
    (0x0018, 0x1004),  # Plate ID
    (0x0040, 0x0012),  # Pre-Medication
    (0x0010, 0x21C0),  # Pregnancy Status
    (0x0040, 0x2001),  # Reason for the Imaging Service Request
    (0x0032, 0x1030),  # Reason for Study
    (0x0400, 0x0402),  # Referenced Digital Signature Sequence
    (0x0038, 0x0004),  # Referenced Patient Alias Sequence
    (0x0008, 0x1120),  # Referenced Patient Sequence
    (0x0400, 0x0403),  # Referenced SOP Instance MAC Sequence
    (0x0008, 0x0092),  # Referring Physician's Address
    (0x0008, 0x0096),  # Referring Physician's Identification Sequence
    (0x0008, 0x0094),  # Referring Physician's Telephone Numbers
    (0x0010, 0x2152),  # Region of Residence
    (0x0040, 0x0275),  # Request Attributes Sequence
    (0x0032, 0x1070),  # Requested Contrast Agent
    (0x0040, 0x1400),  # Requested Procedure Comments
    (0x0040, 0x1001),  # Requested Procedure ID
    (0x0040, 0x1005),  # Requested Procedure Location
    (0x0032, 0x1032),  # Requesting Physician
    (0x0032, 0x1033),  # Requesting Service
    (0x0010, 0x2299),  # Responsible Organization
    (0x0010, 0x2297),  # Responsible Person
    (0x4008, 0x4000),  # Results Comments
    (0x4008, 0x0118),  # Results Distribution List Sequence
    (0x4008, 0x0042),  # Results ID Issuer
    (0x0040, 0x4034),  # Scheduled Human Performers Sequence
    (0x0038, 0x001E),  # Scheduled Patient Institution Residence
    (0x0040, 0x000B),  # Scheduled Performing Physician Identification Sequence
    (0x0040, 0x0006),  # Scheduled Performing Physician Name
    (0x0040, 0x0004),  # Scheduled Procedure Step End Date
    (0x0040, 0x0005),  # Scheduled Procedure Step End Time
    (0x0040, 0x0007),  # Scheduled Procedure Step Description
    (0x0040, 0x0011),  # Scheduled Procedure Step Location
    (0x0040, 0x0002),  # Scheduled Procedure Step Start Date
    (0x0040, 0x0003),  # Scheduled Procedure Step Start Time
    (0x0040, 0x0001),  # Scheduled Station AE Title
    (0x0040, 0x4027),  # Scheduled Station Geographic Location Code Sequence
    (0x0040, 0x0010),  # Scheduled Station Name
    (0x0040, 0x4025),  # Scheduled Station Name Code Sequence
    (0x0032, 0x1020),  # Scheduled Study Location
    (0x0032, 0x1021),  # Scheduled Study Location AE Title
    (0x0008, 0x103E),  # Series Description
    (0x0038, 0x0062),  # Service Episode Description
    (0x0038, 0x0060),  # Service Episode ID
    (0x0010, 0x21A0),  # Smoking Status
    (0x0038, 0x0050),  # Special Needs
    (0x0032, 0x4000),  # Study Comments
    (0x0008, 0x1030),  # Study Description
    (0x0032, 0x0012),  # Study ID Issuer
    (0x4000, 0x4000),  # Text Comments
    (0x2030, 0x0020),  # Text String
    (0x0008, 0x0201),  # Timezone Offset From UTC
    (0x0088, 0x0910),  # Topic Author
    (0x0088, 0x0912),  # Topic Keywords
    (0x0088, 0x0906),  # Topic Subject
    (0x0088, 0x0904),  # Topic Title
    (0x0040, 0xA027),  # Verifying Organization
    (0x0038, 0x4000),  # Visit Comments
]

# Replace UID
U_TAGS = [
    (0x0020, 0x9161),  # Concatenation UID
    (0x0008, 0x010D),  # Context Group Extension Creator UID
    (0x0008, 0x9123),  # Creator Version UID
    (0x0018, 0x1002),  # Device UID
    (0x0020, 0x9164),  # Dimension Organization UID
    (0x300A, 0x0013),  # Dose Reference UID
    (0x0008, 0x0058),  # Failed SOP Instance UID List
    (0x0070, 0x031A),  # Fiducial UID
    (0x0020, 0x0052),  # Frame of Reference UID
    (0x0008, 0x0014),  # Instance Creator UID
    (0x0008, 0x3010),  # Irradiation Event UID
    (0x0028, 0x1214),  # Large Palette Color Lookup Table UID
    (0x0002, 0x0003),  # Media Storage SOP Instance UID
    (0x0028, 0x1199),  # Palette Color Lookup Table UID
    (0x3006, 0x0024),  # Referenced Frame of Reference UID
    (
        0x0040,
        0x4023,
    ),  # Referenced General Purpose Scheduled Procedure Step Transaction UID
    (0x0008, 0x1155),  # Referenced SOP Instance UID
    (0x0004, 0x1511),  # Referenced SOP Instance UID in File
    (0x3006, 0x00C2),  # Related Frame of Reference UID
    (0x0000, 0x1001),  # Requested SOP Instance UID
    (0x0020, 0x000E),  # Series Instance UID
    (0x0008, 0x0018),  # SOP Instance UID
    (0x0088, 0x0140),  # Storage Media File-set UID
    (0x0020, 0x000D),  # Study Instance UID
    (0x0020, 0x0200),  # Synchronization Frame of Reference UID
    (0x0040, 0xDB0D),  # Template Extension Creator UID
    (0x0040, 0xDB0C),  # Template Extension Organization UID
    (0x0008, 0x1195),  # Transaction UID
    (0x0040, 0xA124),  # UID
]

# Replace element according to the VR
Z_D_TAGS = [
    (0x0008, 0x0023),  # Content Date
    (0x0008, 0x0033),  # Content Time
    (0x0018, 0x0010),  # Contrast Bolus Agent
]

# Set the value to empty according to the VR
X_Z_TAGS = [
    (0x0008, 0x0022),  # Acquisition Date
    (0x0008, 0x0032),  # Acquisition Time
    (0x0010, 0x2203),  # Patient Sex Neutered
    (0x0008, 0x1110),  # Referenced Study Sequence
    (0x0032, 0x1060),  # Requested Procedure Description
    (0x300E, 0x0008),  # Reviewer Name
]

# Replace element according to the VR
X_D_TAGS = [
    (0x0008, 0x002A),  # Acquisition DateTime
    (0x0018, 0x1400),  # Acquisition Device Processing Description
    (0x0018, 0x700A),  # Detector ID
    (0x0008, 0x1072),  # Operators' Identification Sequence
    (0x0018, 0x1030),  # Protocol Name
    (0x0008, 0x0021),  # Series Date
    (0x0008, 0x0031),  # Series Time
]

# Replace element according to the VR
X_Z_D_TAGS = [
    (0x0018, 0x1000),  # Device Serial Number
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
