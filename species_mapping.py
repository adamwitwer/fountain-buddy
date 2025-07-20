#!/usr/bin/env python3
"""
Species mapping for unified 19-class bird classifier.
Maps both fountain and peanut feeder species to a single model.
"""

# Unified species list for 19-class model
UNIFIED_SPECIES_LIST = [
    "American Robin",           # 0 - Fountain
    "Black-capped Chickadee",   # 1 - Peanut (NEW)
    "Blue Jay",                 # 2 - Fountain
    "Carolina Wren",            # 3 - Peanut (NEW)
    "Common Grackle",           # 4 - Fountain
    "Downy Woodpecker",         # 5 - Peanut (NEW)
    "European Starling",        # 6 - Both locations
    "Gray Catbird",             # 7 - Fountain
    "Hairy Woodpecker",         # 8 - Peanut (NEW)
    "House Finch",              # 9 - Fountain
    "House Sparrow",            # 10 - Fountain
    "Mourning Dove",            # 11 - Fountain
    "Northern Cardinal",        # 12 - Fountain
    "Northern Flicker",         # 13 - Peanut (NEW)
    "Red-bellied Woodpecker",   # 14 - Peanut (NEW)
    "Song Sparrow",             # 15 - Fountain
    "Squirrel",                 # 16 - Both locations (non-bird)
    "Tufted Titmouse",          # 17 - Peanut (NEW)
    "White-breasted Nuthatch",  # 18 - Peanut (NEW)
]

# Location mapping for species
SPECIES_LOCATIONS = {
    "American Robin": ["fountain"],
    "Black-capped Chickadee": ["peanut"],
    "Blue Jay": ["fountain"],
    "Carolina Wren": ["peanut"],
    "Common Grackle": ["fountain"],
    "Downy Woodpecker": ["peanut"],
    "European Starling": ["fountain", "peanut"],  # Cross-location species
    "Gray Catbird": ["fountain"],
    "Hairy Woodpecker": ["peanut"],
    "House Finch": ["fountain"],
    "House Sparrow": ["fountain"],
    "Mourning Dove": ["fountain"],
    "Northern Cardinal": ["fountain"],
    "Northern Flicker": ["peanut"],
    "Red-bellied Woodpecker": ["peanut"],
    "Song Sparrow": ["fountain"],
    "Squirrel": ["fountain", "peanut"],  # Non-bird, appears at both
    "Tufted Titmouse": ["peanut"],
    "White-breasted Nuthatch": ["peanut"],
}

# Migration mapping from old 13-class to new 19-class
OLD_TO_NEW_MAPPING = {
    # Old class name -> New class name (if changed)
    "American Robin": "American Robin",      # 0 -> 0
    "Blue Jay": "Blue Jay",                  # 1 -> 2
    "Catbird": "Gray Catbird",              # 2 -> 7 (consolidated naming)
    "Common Grackle": "Common Grackle",      # 3 -> 4
    "European Starling": "European Starling", # 4 -> 6
    "Gray Catbird": "Gray Catbird",          # 5 -> 7
    "House Finch": "House Finch",            # 6 -> 9
    "House Sparrow": "House Sparrow",        # 7 -> 10
    "Mourning Dove": "Mourning Dove",        # 8 -> 11
    "Northern Cardinal": "Northern Cardinal", # 9 -> 12
    "Red-winged Blackbird": None,           # 10 -> REMOVE (being replaced)
    "Song Sparrow": "Song Sparrow",          # 11 -> 15
    "Squirrel": "Squirrel",                 # 12 -> 16
}

# New species to add (peanut feeder birds)
NEW_SPECIES = [
    "Black-capped Chickadee",
    "Carolina Wren", 
    "Downy Woodpecker",
    "Hairy Woodpecker",
    "Northern Flicker",
    "Red-bellied Woodpecker",
    "Tufted Titmouse",
    "White-breasted Nuthatch",
]

def get_species_index(species_name):
    """Get the index of a species in the unified list."""
    try:
        return UNIFIED_SPECIES_LIST.index(species_name)
    except ValueError:
        return None

def get_species_by_location(location):
    """Get all species that can appear at a given location."""
    species_for_location = []
    for species, locations in SPECIES_LOCATIONS.items():
        if location in locations:
            species_for_location.append(species)
    return sorted(species_for_location)

def get_location_for_species(species_name):
    """Get all locations where a species can appear."""
    return SPECIES_LOCATIONS.get(species_name, [])

def validate_species_mapping():
    """Validate the species mapping for consistency."""
    
    print("🔍 Validating species mapping...")
    
    # Check total count
    expected_count = 19
    actual_count = len(UNIFIED_SPECIES_LIST)
    
    if actual_count != expected_count:
        print(f"❌ Species count mismatch: expected {expected_count}, got {actual_count}")
        return False
    
    # Check for duplicates
    if len(set(UNIFIED_SPECIES_LIST)) != len(UNIFIED_SPECIES_LIST):
        print("❌ Duplicate species found in unified list")
        return False
    
    # Check location mapping consistency
    for species in UNIFIED_SPECIES_LIST:
        if species not in SPECIES_LOCATIONS:
            print(f"❌ Species '{species}' missing from location mapping")
            return False
    
    # Check location counts
    fountain_species = get_species_by_location("fountain")
    peanut_species = get_species_by_location("peanut")
    
    print(f"✅ Total species: {actual_count}")
    print(f"✅ Fountain species: {len(fountain_species)}")
    print(f"✅ Peanut species: {len(peanut_species)}")
    print(f"✅ Cross-location species: {len([s for s in UNIFIED_SPECIES_LIST if len(SPECIES_LOCATIONS[s]) > 1])}")
    
    return True

def generate_metadata():
    """Generate metadata for the new 19-class model."""
    
    metadata = {
        "class_names": UNIFIED_SPECIES_LIST,
        "num_classes": len(UNIFIED_SPECIES_LIST),
        "species_locations": SPECIES_LOCATIONS,
        "model_version": "v2.0-unified",
        "description": "Unified 19-class bird classifier for fountain and peanut feeder locations",
        "fountain_species_count": len(get_species_by_location("fountain")),
        "peanut_species_count": len(get_species_by_location("peanut")),
        "cross_location_species": [s for s in UNIFIED_SPECIES_LIST if len(SPECIES_LOCATIONS[s]) > 1],
        "new_species_added": NEW_SPECIES,
        "removed_species": ["Red-winged Blackbird"],
    }
    
    return metadata

if __name__ == "__main__":
    print("🐦 Fountain Buddy Species Mapping")
    print("=" * 50)
    
    # Validate mapping
    if validate_species_mapping():
        print("\n✅ Species mapping validation passed!")
        
        # Show breakdown
        print(f"\n📋 Unified Species List ({len(UNIFIED_SPECIES_LIST)} classes):")
        for i, species in enumerate(UNIFIED_SPECIES_LIST):
            locations = ", ".join(SPECIES_LOCATIONS[species])
            print(f"  {i:2d}: {species} ({locations})")
        
        # Show location breakdown
        print(f"\n🏛️ Fountain Species ({len(get_species_by_location('fountain'))}):")
        for species in get_species_by_location("fountain"):
            print(f"     {species}")
        
        print(f"\n🥜 Peanut Species ({len(get_species_by_location('peanut'))}):")
        for species in get_species_by_location("peanut"):
            print(f"     {species}")
        
        # Generate metadata
        metadata = generate_metadata()
        print(f"\n📊 Model Metadata Generated:")
        print(f"   Version: {metadata['model_version']}")
        print(f"   Total Classes: {metadata['num_classes']}")
        print(f"   New Species Added: {len(metadata['new_species_added'])}")
        
    else:
        print("\n❌ Species mapping validation failed!")
        exit(1)