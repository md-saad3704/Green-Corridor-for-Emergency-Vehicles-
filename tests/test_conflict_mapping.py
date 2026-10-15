
from backend.inspect_conflicts import (
    decode_foes,
    load_junction_requests,
)


def test_ambulance_foes_decode_to_expected_signal_indices():
    requests = load_junction_requests()

    assert 17 in requests

    foes = decode_foes(requests[17])

    assert foes == {1, 2, 3, 8, 9, 10, 11, 12, 13}


def test_all_foe_indices_exist_in_junction_requests():
    requests = load_junction_requests()

    for foes_string in requests.values():
        foes = decode_foes(foes_string)

        assert foes.issubset(requests.keys())


def test_foe_relationships_are_symmetric():
    requests = load_junction_requests()

    decoded = {
        index: decode_foes(foes_string)
        for index, foes_string in requests.items()
    }

    for index, foes in decoded.items():
        for foe_index in foes:
            assert index in decoded[foe_index], (
                f"Foe relationship is asymmetric: "
                f"{index} conflicts with {foe_index}, "
                f"but not vice versa."
            )
