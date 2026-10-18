"""The species vocabulary: what the tray expects, and every label a human can give.

Names are the canonical form stored in the database (title case, spaces). The Discord
dropdown holds at most 25 options, so keep LABELS within that.
"""

# Expected on safflower at the Tray Feeder (Adam, 2026-10-18).
TRAY_SPECIES = [
    "Northern Cardinal",
    "Tufted Titmouse",
    "House Finch",
    "American Goldfinch",
    "Mourning Dove",
    "Black-capped Chickadee",
    "Dark-eyed Junco",
    "White-breasted Nuthatch",
]

# Seen at the old cameras, or plausible visitors. Dropdown only, never buttons by default.
OCCASIONAL_SPECIES = [
    "Red-breasted Nuthatch",
    "White-throated Sparrow",
    "House Sparrow",
    "European Starling",
    "Common Grackle",
    "Blue Jay",
    "Downy Woodpecker",
    "Hairy Woodpecker",
    "Red-bellied Woodpecker",
    "Carolina Wren",
    "Song Sparrow",
    "American Robin",
    "Gray Catbird",
    "Red-winged Blackbird",
]

SPECIES = TRAY_SPECIES + OCCASIONAL_SPECIES

# For zero-shot text prompts: BioCLIP 2 was trained on taxonomic names.
SCIENTIFIC = {
    "Northern Cardinal": "Cardinalis cardinalis",
    "Tufted Titmouse": "Baeolophus bicolor",
    "House Finch": "Haemorhous mexicanus",
    "American Goldfinch": "Spinus tristis",
    "Mourning Dove": "Zenaida macroura",
    "Black-capped Chickadee": "Poecile atricapillus",
    "Dark-eyed Junco": "Junco hyemalis",
    "White-breasted Nuthatch": "Sitta carolinensis",
    "Red-breasted Nuthatch": "Sitta canadensis",
    "White-throated Sparrow": "Zonotrichia albicollis",
    "House Sparrow": "Passer domesticus",
    "European Starling": "Sturnus vulgaris",
    "Common Grackle": "Quiscalus quiscula",
    "Blue Jay": "Cyanocitta cristata",
    "Downy Woodpecker": "Dryobates pubescens",
    "Hairy Woodpecker": "Dryobates villosus",
    "Red-bellied Woodpecker": "Melanerpes carolinus",
    "Carolina Wren": "Thryothorus ludovicianus",
    "Song Sparrow": "Melospiza melodia",
    "American Robin": "Turdus migratorius",
    "Gray Catbird": "Dumetella carolinensis",
    "Red-winged Blackbird": "Agelaius phoeniceus",
}

# Labels that are not a bird species. SKIP means "unusable photo": it trains the
# classifier's not-usable class but never counts as a sighting.
SQUIRREL = "Squirrel"
NOT_A_BIRD = "Not a bird"
SKIP = "Skip"
NON_SPECIES = [SQUIRREL, NOT_A_BIRD, SKIP]

LABELS = SPECIES + NON_SPECIES

_ALIASES = {
    "skiip": SKIP,
    "poor quality": SKIP,
    "unknown; not a bird": NOT_A_BIRD,
}
_BY_LOWER = {name.lower(): name for name in LABELS}


def canonical(name: str) -> str | None:
    """Map a stored or typed label to its canonical form, or None if unknown."""
    key = " ".join(name.replace("_", " ").split()).lower()
    return _BY_LOWER.get(key) or _ALIASES.get(key)
