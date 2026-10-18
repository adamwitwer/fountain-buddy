from fountain_buddy.nabirds import base_species


def test_variants_fold_into_base_species():
    assert base_species("Northern Cardinal (Adult Male)") == "Northern Cardinal"
    assert base_species("Dark-eyed Junco (Slate-colored)") == "Dark-eyed Junco"
    assert base_species("American Goldfinch") == "American Goldfinch"


def test_other_species_and_groups_are_ignored():
    assert base_species("Carolina Chickadee") is None
    assert base_species("Chickadees and Titmice") is None
