"""Explore crossing sequences for the width-four macro machine.

The signature implemented here is deliberately *not* claimed sufficient for a
pumping theorem.  It records the chronological boundary-crossing events of a macro
word and is useful for discovering which additional tape/stack data a sound splice
signature must carry.
"""
from __future__ import annotations

import argparse
from collections import defaultdict

from search_width4 import LN, ODD_LINE, STATE_NAME, TRANSITIONS


TRANSITION_NAME = {
    (0, 0): "x", (0, 1): "a", (0, 2): "b",
    (1, 0): "c", (1, 1): "d", (1, 2): "e",
    (2, 1): "h", (2, 2): "q", (2, 3): "f",
    (3, 1): "j", (3, 2): "i", (3, 3): "y",
}

PAIR = {
    "a": "RR", "b": "RL", "x": "LR",
    "c": "RR", "d": "LR", "e": "LL",
    "f": "RR", "q": "LR", "h": "LL",
    "i": "RR", "j": "RL", "y": "LR",
}


def endpoint_family(m: int) -> list[str]:
    if m < 3:
        raise ValueError("the endpoint family is stated for m >= 3")
    initial = ["b", "q", "f", "j", "d", "d", "c"]
    middle = ["b", "h", "d", "d", "c"]
    final = ["b", "h", "d", "d", "e", "f", "i", "h", "c"]
    return initial + middle * (m - 2) + final


def transition_by_name(state: int, name: str):
    for nxt, delta, pair, even_line, even_offset in TRANSITIONS[state]:
        if TRANSITION_NAME[state, nxt] == name:
            if pair != PAIR[name]:
                raise AssertionError((state, name, pair))
            return nxt, delta, pair, even_line, even_offset
    raise ValueError(f"transition {name} is not available from {STATE_NAME[state]}")


def crossing_signatures(names: list[str], modulus: int | None = None):
    state = LN
    ell = 0
    signatures = defaultdict(list)
    trajectory = [(state, ell)]
    for phase, name in enumerate(names):
        nxt, delta, pair, even_line, even_offset = transition_by_name(state, name)
        new_ell = ell + delta
        absolute_cut = min(ell, new_ell)
        cut = absolute_cut if modulus is None else absolute_cut % modulus
        lift = 0 if modulus is None else (absolute_cut - cut) // modulus
        key = phase if modulus is None else phase - len(names) * lift
        direction = "+" if delta > 0 else "-"
        signatures[cut].append(
            (direction, STATE_NAME[state], STATE_NAME[nxt], name, pair, key,
             phase, absolute_cut, lift)
        )
        state, ell = nxt, new_ell
        trajectory.append((state, ell))
    for events in signatures.values():
        events.sort(key=lambda event: event[5])
    return dict(signatures), trajectory


def phase_free(signature):
    """Forget absolute phase/cut lift while retaining chronological event order."""
    return tuple(event[:5] for event in signature)


def control_signature(signature):
    """Return the one-tape crossing state: direction and destination even line."""
    out = []
    for event in signature:
        direction, source_name, _target, name, _pair = event[:5]
        source = STATE_NAME.index(source_name)
        _nxt, _delta, _pair2, even_line, _offset = transition_by_name(source, name)
        out.append((direction, even_line))
    return tuple(out)


def audit_control_projection():
    """Check the geometric projection on all twelve macro transitions."""
    controls = {+1: set(), -1: set()}
    for state, transitions in TRANSITIONS.items():
        arrives_north = state in (0, 2)  # LN or UN
        for nxt, delta, pair, even_line, even_offset in transitions:
            odd_turn = pair[0]
            expected_delta = (+1 if odd_turn == "R" else -1) if arrives_north \
                else (-1 if odd_turn == "R" else +1)
            assert delta == expected_delta, (state, nxt, delta, pair)
            assert even_offset == delta, (state, nxt, even_offset, delta)
            assert even_line == ODD_LINE[state] + delta, (
                state, nxt, even_line, ODD_LINE[state], delta)
            controls[delta].add(even_line)
    assert controls == {+1: {2, 4}, -1: {0, 2}}, controls


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--drift", type=int, default=10)
    args = parser.parse_args()
    audit_control_projection()
    names = endpoint_family(args.drift)
    signatures, trajectory = crossing_signatures(names, args.drift)
    state, ell = trajectory[-1]
    print(f"m={args.drift} P={len(names)} endpoint=({STATE_NAME[state]},{ell})")
    if sum(len(events) for events in signatures.values()) != len(names):
        raise AssertionError("modular cut signatures must partition all macro steps")

    decorated_choices = 6
    decorated_bound = sum(decorated_choices ** length for length in (1, 3, 5, 7))
    control_choices = 2
    control_bound = sum(control_choices ** length for length in (1, 3, 5, 7))
    deficit_below_seven = sum((7 - length) * control_choices ** length
                              for length in (1, 3, 5))
    long_capacity = deficit_below_seven // 2
    weighted_cutoff = control_bound + long_capacity
    extremal_caps = {length: ((length - 1) // 2 + 2) * ((length - 1) // 2 + 1)
                     for length in (1, 3, 5, 7)}
    extremal_deficit = sum((7 - length) * capacity
                           for length, capacity in extremal_caps.items())
    extremal_long_capacity = extremal_deficit // 2
    extremal_weighted_cutoff = sum(extremal_caps.values()) + extremal_long_capacity
    print(f"decorated low-signature upper bound={decorated_bound} "
          f"candidate cutoff={4 * decorated_bound}")
    print(f"control low-signature upper bound={control_bound} "
          f"candidate cutoff={4 * control_bound}")
    print(f"weighted distinct-signature cutoff={weighted_cutoff} "
          f"(short deficit={deficit_below_seven}, long capacity={long_capacity})")
    print(f"extremal-weighted cutoff={extremal_weighted_cutoff} "
          f"(capacities={extremal_caps}, deficit={extremal_deficit}, "
          f"long capacity={extremal_long_capacity})")

    groups = defaultdict(list)
    control_groups = defaultdict(list)
    for cut in range(args.drift):
        sig = phase_free(signatures.get(cut, ()))
        control = control_signature(signatures.get(cut, ()))
        assert sum(event == ("+", 4) for event in control) <= 1, (cut, control)
        assert sum(event == ("-", 0) for event in control) <= 1, (cut, control)
        directions = tuple(event[0] for event in sig)
        expected = tuple("+" if index % 2 == 0 else "-"
                         for index in range(len(sig)))
        if directions != expected:
            raise AssertionError((cut, directions, expected))
        groups[sig].append(cut)
        control_groups[control].append(cut)
        events = signatures.get(cut, ())
        lifts = [event[8] for event in events]
        keys = [event[5] for event in events]
        print(f"cut={cut:3d} crossings={len(sig)} lifts={lifts} keys={keys} "
              f"control={control} signature={sig}")
    print("repeated phase-free signatures:")
    for signature, cuts in sorted(groups.items(), key=lambda item: item[1]):
        if len(cuts) > 1:
            print(f"  cuts={cuts} length={len(signature)} signature={signature}")
    print("repeated splice-sufficient control signatures:")
    for signature, cuts in sorted(control_groups.items(), key=lambda item: item[1]):
        if len(cuts) > 1:
            print(f"  cuts={cuts} length={len(signature)} signature={signature}")


if __name__ == "__main__":
    main()
