"""Cross-check the independent criterion verifier against the Java engines.

Three tests:
  A. the standard period-104 highway word must PASS both;
  B. exhaustive agreement of criterion_literal vs criterion_onesort over all
     heading-reset nonzero-drift words up to length L (this also tests the
     Remark 3.2 reduction, which the Java engines rely on);
  C. agreement with the ACTUAL Java binary on a sample, via --check-trace.
"""
import itertools
import json
import subprocess
import sys

from verify_criterion_indep import criterion_literal, criterion_onesort, path

STD = ("RRRRLLRLLRRRRLLRRRRLLRLRRRRLRLLLLRRRRLRRLRRRRLLLLRLRRRRLRRRR"
       "LLLLRLRRRRLRLLRRLLLLRRLLRRRRLLRRLRLLRLLRLRLL")


def test_A():
    lit, one = criterion_literal(STD), criterion_onesort(STD)
    pts, h, d = path(STD)
    print(f"A. standard word: literal={lit} onesort={one} heading={h} drift={d}")
    assert lit and one, "standard highway must satisfy the criterion"
    return lit and one


def test_B(maxlen):
    print(f"B. exhaustive literal-vs-onesort agreement, lengths 1..{maxlen}")
    total = reset = nonzero = passed = disagree = 0
    for L in range(1, maxlen + 1):
        for bits in itertools.product("RL", repeat=L):
            w = "".join(bits)
            total += 1
            _, h, d = path(w)
            if h != 0:
                continue
            reset += 1
            if d == (0, 0):
                continue
            nonzero += 1
            a, b = criterion_literal(w), criterion_onesort(w)
            if a != b:
                disagree += 1
                if disagree <= 5:
                    print(f"   DISAGREE w={w} literal={a} onesort={b}")
            if a:
                passed += 1
                if passed <= 5:
                    print(f"   PASSES CRITERION: {w}")
    print(f"   words={total:,} heading-reset={reset:,} nonzero-drift={nonzero:,}")
    print(f"   literal-vs-onesort disagreements: {disagree}")
    print(f"   nonzero-drift words passing the criterion: {passed}")
    return disagree == 0, reset, nonzero, passed


def test_C(sample):
    print(f"C. agreement with the actual Java binary on {len(sample)} words")
    bad = 0
    for w in sample:
        out = subprocess.run(
            ["java", "-cp", "indep_classes", "PositiveGrowthSearchIndep",
             "--check-trace", w],
            capture_output=True, text=True, timeout=120)
        j = json.loads(out.stdout.strip())
        mine = criterion_literal(w)
        # Java reports p3_valid only for structural (heading-reset handled by caller)
        theirs = j["p3_valid"]
        if mine != theirs:
            bad += 1
            print(f"   MISMATCH w={w} python={mine} java={theirs} raw={j}")
    print(f"   mismatches: {bad}")
    return bad == 0


if __name__ == "__main__":
    maxlen = int(sys.argv[1]) if len(sys.argv) > 1 else 14
    ok_a = test_A()
    ok_b, reset, nonzero, passed = test_B(maxlen)
    # sample: the standard word plus short heading-reset nonzero-drift words
    sample = [STD]
    for L in range(4, 13):
        for bits in itertools.product("RL", repeat=L):
            w = "".join(bits)
            _, h, d = path(w)
            if h == 0 and d != (0, 0):
                sample.append(w)
                break
    ok_c = test_C(sample)
    print()
    print(f"RESULT: A={ok_a} B={ok_b} C={ok_c}")
