import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Locale;

/**
 * Exploratory exact search for diagonal Langton highways of transverse width four.
 *
 * <p>The five-line geometry is collapsed into the four odd-line states LN, LS, UN,
 * US described in {@code code/python/search_width4.py}.  Each transition expands to
 * exactly two ant turns.  The search is complete for each requested period: it is
 * based immediately after a bottom-extremal visit, assumes positive longitudinal
 * drift by a half-turn of the plane, and does not use cyclic-minimum normalisation.
 *
 * <p>This is a bounded research search, not an all-period proof.  Every leaf is
 * grouped by the exact translation-class key {@code (t, x mod m)}.  The aggregate
 * odd-class identity is used as a necessary prefilter, after which the full
 * chronological start-R and alternation criterion is applied.
 */
public final class WidthFourSearch {
    private static final int LN = 0;
    private static final int LS = 1;
    private static final int UN = 2;
    private static final int US = 3;

    private static final int[] ODD_LINE = {1, 1, 3, 3};

    // Per state: next state, delta ell, encoded pair, even line, even offset.
    // Pair bits: high bit is odd-cell turn, low bit is even-cell turn; R=0, L=1.
    private static final int[][][] TRANSITIONS = {
        {{LS, +1, 0b00, 2, +1}, {UN, +1, 0b01, 2, +1}, {LN, -1, 0b10, 0, -1}},
        {{LN, -1, 0b00, 0, -1}, {LS, +1, 0b10, 2, +1}, {UN, +1, 0b11, 2, +1}},
        {{US, +1, 0b00, 4, +1}, {UN, -1, 0b10, 2, -1}, {LS, -1, 0b11, 2, -1}},
        {{UN, -1, 0b00, 2, -1}, {LS, -1, 0b01, 2, -1}, {US, +1, 0b10, 4, +1}}
    };

    private final int macros;
    private final int requiredDrift;
    private final int period;
    private final int span;
    private final int offset;
    private final byte[] lastTurn;
    private final byte[] turns;
    private final int[] phaseLine;
    private final int[] phaseEll;
    private final boolean[][] boundaryResidueSeen;

    private long nodes;
    private long structuralLeaves;
    private long oddIdentityPass;
    private long startsRPass;
    private long extremalSingletonPass;
    private long startsRExtremalPass;
    private long criterionChecks;
    private long hits;
    private int minGrowthMinusOdd = Integer.MAX_VALUE;
    private int maxGrowthMinusOdd = Integer.MIN_VALUE;
    private int closestGrowthOddGap = Integer.MAX_VALUE;
    private String closestGapWord;
    private int maxLeftOvershoot;
    private int maxRightOvershoot;
    private final List<String> hitWords = new ArrayList<>();
    private final List<String> startsRWords = new ArrayList<>();

    private WidthFourSearch(int macros, int requiredDrift) {
        this.macros = macros;
        this.requiredDrift = requiredDrift;
        this.period = 2 * macros;
        this.span = 4 * macros + 9;
        this.offset = 2 * macros + 4;
        this.lastTurn = new byte[5 * span];
        Arrays.fill(lastTurn, (byte)-1);
        this.turns = new byte[period];
        this.phaseLine = new int[period];
        this.phaseEll = new int[period];
        this.boundaryResidueSeen = requiredDrift > 0
                ? new boolean[2][requiredDrift] : null;
    }

    private int cellIndex(int line, int ell) {
        int e = ell + offset;
        if (line < 0 || line > 4 || e < 0 || e >= span) {
            throw new AssertionError("cell outside fixed search array: line=" + line + " ell=" + ell);
        }
        return line * span + e;
    }

    private void dfs(int depth, int state, int ell, int balance, boolean usedTop) {
        ++nodes;
        int remaining = macros - depth;
        if (requiredDrift > 0
                && (ell + remaining < requiredDrift || ell - remaining > requiredDrift)) {
            return;
        }
        if (ell + remaining <= 0 || balance + 2 * remaining <= 0) {
            return;
        }
        if (depth == macros) {
            if (state == LN && ell > 0 && balance > 0 && usedTop
                    && (requiredDrift <= 0 || ell == requiredDrift)) {
                evaluateLeaf(ell, balance);
            }
            return;
        }

        int oddLine = ODD_LINE[state];
        int oddCell = cellIndex(oddLine, ell);
        byte oldOdd = lastTurn[oddCell];
        for (int[] tr : TRANSITIONS[state]) {
            int pair = tr[2];
            byte oddTurn = (byte)((pair >>> 1) & 1);
            byte evenTurn = (byte)(pair & 1);
            if (oldOdd >= 0 && oldOdd == oddTurn) {
                continue;
            }
            int evenLine = tr[3];
            int evenEll = ell + tr[4];
            int evenCell = cellIndex(evenLine, evenEll);
            byte oldEven = lastTurn[evenCell];
            if (oldEven >= 0 && oldEven == evenTurn) {
                continue;
            }
            int boundarySide = evenLine == 0 ? 0 : (evenLine == 4 ? 1 : -1);
            int boundaryResidue = -1;
            if (boundarySide >= 0 && requiredDrift > 0) {
                boundaryResidue = Math.floorMod(evenEll, requiredDrift);
                if (boundaryResidueSeen[boundarySide][boundaryResidue]) {
                    continue;
                }
                boundaryResidueSeen[boundarySide][boundaryResidue] = true;
            }

            int i = 2 * depth;
            turns[i] = oddTurn;
            turns[i + 1] = evenTurn;
            phaseLine[i] = oddLine;
            phaseEll[i] = ell;
            phaseLine[i + 1] = evenLine;
            phaseEll[i + 1] = evenEll;
            lastTurn[oddCell] = oddTurn;
            lastTurn[evenCell] = evenTurn;
            int pairGrowth = (oddTurn == 0 ? 1 : -1) + (evenTurn == 0 ? 1 : -1);
            int nextBalance = balance + pairGrowth;
            dfs(depth + 1, tr[0], ell + tr[1], nextBalance,
                    usedTop || evenLine == 4);
            if (boundarySide >= 0 && requiredDrift > 0) {
                boundaryResidueSeen[boundarySide][boundaryResidue] = false;
            }
            lastTurn[evenCell] = oldEven;
            lastTurn[oddCell] = oldOdd;
        }
    }

    private void evaluateLeaf(int drift, int growth) {
        ++structuralLeaves;
        int classCount = 5 * drift;
        int[] counts = new int[classCount];
        int[] minKey = new int[classCount];
        byte[] minTurn = new byte[classCount];
        Arrays.fill(minKey, Integer.MAX_VALUE);

        int minEll = Integer.MAX_VALUE;
        int maxEll = Integer.MIN_VALUE;

        for (int i = 0; i < period; ++i) {
            int r = Math.floorMod(phaseEll[i], drift);
            minEll = Math.min(minEll, phaseEll[i]);
            maxEll = Math.max(maxEll, phaseEll[i]);
            int cls = phaseLine[i] * drift + r;
            int a = Math.floorDiv(phaseEll[i] - r, drift);
            int key = i - period * a;
            ++counts[cls];
            if (key < minKey[cls]) {
                minKey[cls] = key;
                minTurn[cls] = turns[i];
            }
        }
        maxLeftOvershoot = Math.max(maxLeftOvershoot, -minEll);
        maxRightOvershoot = Math.max(maxRightOvershoot, maxEll - drift);

        int odd = 0;
        boolean startsR = true;
        boolean extremes = true;
        for (int cls = 0; cls < classCount; ++cls) {
            int count = counts[cls];
            if ((count & 1) != 0) {
                ++odd;
            }
            if (count > 0 && minTurn[cls] != 0) {
                startsR = false;
            }
            int line = cls / drift;
            if ((line == 0 || line == 4) && count > 1) {
                extremes = false;
            }
        }
        int growthOddGap = growth - odd;
        minGrowthMinusOdd = Math.min(minGrowthMinusOdd, growthOddGap);
        maxGrowthMinusOdd = Math.max(maxGrowthMinusOdd, growthOddGap);
        if (Math.abs(growthOddGap) < closestGrowthOddGap) {
            closestGrowthOddGap = Math.abs(growthOddGap);
            closestGapWord = word() + " drift=" + drift + " growth=" + growth
                    + " odd=" + odd;
        }
        if (startsR) {
            ++startsRPass;
            if (startsRWords.size() < 6) {
                startsRWords.add(word() + " drift=" + drift + " growth=" + growth
                        + " extremaSingleton=" + extremes);
            }
        }
        if (extremes) {
            ++extremalSingletonPass;
        }
        if (startsR && extremes) {
            ++startsRExtremalPass;
        }
        if (growth != odd) {
            return;
        }
        ++oddIdentityPass;
        ++criterionChecks;

        long[] order = new long[period];
        final long bias = 1_000_000L;
        for (int i = 0; i < period; ++i) {
            int r = Math.floorMod(phaseEll[i], drift);
            int cls = phaseLine[i] * drift + r;
            int a = Math.floorDiv(phaseEll[i] - r, drift);
            int key = i - period * a;
            order[i] = ((long)cls << 48) | ((key + bias) << 1) | turns[i];
        }
        Arrays.sort(order);
        int previousClass = -1;
        int previousTurn = -1;
        for (long packed : order) {
            int cls = (int)(packed >>> 48);
            int turn = (int)(packed & 1L);
            if (cls != previousClass) {
                if (turn != 0) {
                    return;
                }
            } else if (turn == previousTurn) {
                return;
            }
            previousClass = cls;
            previousTurn = turn;
        }
        ++hits;
        if (hitWords.size() < 20) {
            hitWords.add(word());
        }
    }

    private String word() {
        StringBuilder out = new StringBuilder(period);
        for (byte turn : turns) {
            out.append(turn == 0 ? 'R' : 'L');
        }
        return out.toString();
    }

    private void run() {
        long start = System.nanoTime();
        dfs(0, LN, 0, 0, false);
        double seconds = (System.nanoTime() - start) / 1.0e9;
        System.out.printf(Locale.ROOT,
                "P=%d N=%d nodes=%,d leaves=%,d odd-id=%,d starts-R=%,d " +
                "ext=%,d R+ext=%,d p3=%,d hits=%,d gap=[%s,%s] near=%s " +
                "overshoot=%d/%d sec=%.3f%n",
                macros, period, nodes, structuralLeaves, oddIdentityPass, startsRPass,
                extremalSingletonPass, startsRExtremalPass, criterionChecks, hits,
                minGrowthMinusOdd == Integer.MAX_VALUE ? "-" : Integer.toString(minGrowthMinusOdd),
                maxGrowthMinusOdd == Integer.MIN_VALUE ? "-" : Integer.toString(maxGrowthMinusOdd),
                closestGrowthOddGap == Integer.MAX_VALUE ? "-" : Integer.toString(closestGrowthOddGap),
                maxLeftOvershoot, maxRightOvershoot,
                seconds);
        for (String hit : hitWords) {
            System.out.println("  HIT " + hit);
        }
        for (String candidate : startsRWords) {
            System.out.println("  STARTS-R " + candidate);
        }
        if (closestGapWord != null && (macros <= 20 || structuralLeaves <= 10)) {
            System.out.println("  CLOSEST " + closestGapWord);
        }
    }

    public static void main(String[] args) {
        int min = args.length >= 1 ? Integer.parseInt(args[0]) : 2;
        int max = args.length >= 2 ? Integer.parseInt(args[1]) : min;
        int drift = args.length >= 3 ? Integer.parseInt(args[2]) : 0;
        if (min < 1 || max < min) {
            throw new IllegalArgumentException(
                    "usage: WidthFourSearch [minMacros [maxMacros [requiredDrift]]]");
        }
        for (int p = min; p <= max; ++p) {
            if (drift > 0 && ((p - drift) & 1) != 0) {
                System.out.printf("P=%d N=%d skipped: displacement parity%n", p, 2*p);
                continue;
            }
            new WidthFourSearch(p, drift).run();
        }
    }
}
