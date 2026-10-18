from fountain_buddy import species


def test_labels_fit_a_discord_dropdown():
    assert len(species.LABELS) <= 25
    assert len(set(species.LABELS)) == len(species.LABELS)


def test_canonical_handles_legacy_spellings():
    assert species.canonical("Blue_Jay") == "Blue Jay"
    assert species.canonical("  northern   cardinal ") == "Northern Cardinal"
    assert species.canonical("Skiip") == species.SKIP
    assert species.canonical("Unknown; Not A Bird") == species.NOT_A_BIRD
    assert species.canonical("Squirrel") == species.SQUIRREL
    assert species.canonical("Ostrich") is None
