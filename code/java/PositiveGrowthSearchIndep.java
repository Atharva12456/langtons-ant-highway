import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Locale;

/**
 * Exact sharded search for positive-growth finite-support periodic Langton
 * traces, using NO consequence of the signed mod-four wake-residue theorem.
 *
 * <p>This is the theorem-independent reference engine.  It exists to certify
 * the small-period exclusion without assuming the residue theorem.  Compared
 * with {@code PositiveGrowthSearch}, every use of the strand-density bound
 * P16, g >= 2 max(|dx|,|dy|) --- a corollary of the residue theorem --- has
 * been removed:
 * <ul>
 *   <li>the leaf-level P16 rejection is gone: the exact criterion is now
 *       applied to EVERY positive-growth nonzero-drift leaf;</li>
 *   <li>endpoint reachability no longer contracts to the P16 square; it uses
 *       only the L1 reachability diamond;</li>
 *   <li>the deficit test enumerates every reachable nonzero drift, not only
 *       drifts inside the P16 square, and does not filter (growth, drift)
 *       pairs by P16.</li>
 * </ul>
 *
 * <p>The remaining pruning rules are independent of the residue theorem:
 * <ol>
 *   <li>cyclic-minimum normalization: every prefix has #R-#L >= 0
 *       (elementary cycle lemma);</li>
 *   <li>the final growth is a positive multiple of four (Cor. "growth is a
 *       positive multiple of four", a consequence of the even-winding
 *       theorem, NOT of the residue theorem);</li>
 *   <li>same physical-cell turns alternate (elementary alternating-visit
 *       proposition);</li>
 *   <li>L1 endpoint reachability with a nonzero endpoint;</li>
 *   <li>at selected depths, the odd-ending alternating-superword deficit
 *       is feasible for at least one reachable (growth, drift) pair.</li>
 * </ol>
 * Every surviving leaf is checked directly with the exact P3 stabilized
 * translation-class criterion.
 */
public final class PositiveGrowthSearchIndep {
    private static final int[] DX = {0, 1, 0, -1};
    private static final int[] DY = {1, 0, -1, 0};
    private static final int GRID_OFFSET = 64;
    private static final int GRID_SIDE = 128;

    private record Config(
            int period,
            int prefixLength,
            long rankStart,
            long rankStop,
            int[] deficitDepths,
            Path output) {}

    private static final class RankResult {
        long rank;
        String prefix;
        boolean prefixValid;
        long nodes;
        long growthPrunes;
        long endpointPrunes;
        long deficitPrunes;
        long deficitChecks;
        long deficitEndpoints;
        long leaves;
        long p3Checks;
        List<String> hits = new ArrayList<>();
        double seconds;
    }

    private static final class Search {
        final int n;
        final boolean[] deficitAt;
        final int[] posX;
        final int[] posY;
        final int[] turns; // R=0, L=1
        final byte[] lastTurn;
        final long[] scratchRepresentative;
        final int[] scratchLevel;
        final int[] scratchOrder;
        final RankResult result;

        int x = 0;
        int y = 0;
        int direction = 0;
        int depth = 0;
        int balance = 0;

        Search(int period, int[] deficitDepths, RankResult result) {
            this.n = period;
            this.result = result;
            this.deficitAt = new boolean[period + 1];
            for (int d : deficitDepths) {
                if (d > 0 && d < period) {
                    deficitAt[d] = true;
                }
            }
            this.posX = new int[period];
            this.posY = new int[period];
            this.turns = new int[period];
            this.lastTurn = new byte[GRID_SIDE * GRID_SIDE];
            this.scratchRepresentative = new long[period];
            this.scratchLevel = new int[period];
            this.scratchOrder = new int[period];
            Arrays.fill(lastTurn, (byte) -1);
        }

        int gridIndex(int px, int py) {
            int gx = px + GRID_OFFSET;
            int gy = py + GRID_OFFSET;
            if (gx < 0 || gx >= GRID_SIDE || gy < 0 || gy >= GRID_SIDE) {
                throw new AssertionError("period-sized walk escaped fixed grid");
            }
            return gx * GRID_SIDE + gy;
        }

        boolean applyPrefix(String prefix) {
            for (int i = 0; i < prefix.length(); ++i) {
                int turn = prefix.charAt(i) == 'R' ? 0 : 1;
                int cell = gridIndex(x, y);
                int previous = lastTurn[cell];
                if (previous >= 0 && turn != 1 - previous) {
                    return false;
                }
                if (balance + (turn == 0 ? 1 : -1) < 0) {
                    return false;
                }
                posX[depth] = x;
                posY[depth] = y;
                turns[depth] = turn;
                lastTurn[cell] = (byte) turn;
                balance += turn == 0 ? 1 : -1;
                direction = turn == 0 ? (direction + 1) & 3 : (direction + 3) & 3;
                x += DX[direction];
                y += DY[direction];
                ++depth;
            }
            return true;
        }

        void dfs() {
            ++result.nodes;
            int remaining = n - depth;

            int[] possibleGrowth = possibleGrowths(remaining);
            if (possibleGrowth.length == 0) {
                ++result.growthPrunes;
                return;
            }
            if (!coarseEndpointPossible(possibleGrowth, remaining)) {
                ++result.endpointPrunes;
                return;
            }
            if (deficitAt[depth]) {
                ++result.deficitChecks;
                if (!deficitFeasible(possibleGrowth, remaining)) {
                    ++result.deficitPrunes;
                    return;
                }
            }

            if (depth == n) {
                ++result.leaves;
                if (x == 0 && y == 0) {
                    return;
                }
                if (balance <= 0 || (balance & 3) != 0) {
                    return;
                }
                // NO P16 REJECTION HERE.  The exact criterion is applied to
                // every positive-growth nonzero-drift leaf.
                ++result.p3Checks;
                if (p3Valid(x, y)) {
                    result.hits.add(hitJson(x, y));
                }
                return;
            }

            int cell = gridIndex(x, y);
            int previous = lastTurn[cell];
            if (previous >= 0) {
                pushAndRecurse(1 - previous, cell, (byte) previous);
            } else {
                pushAndRecurse(0, cell, (byte) -1);
                pushAndRecurse(1, cell, (byte) -1);
            }
        }

        int[] possibleGrowths(int remaining) {
            int[] values = new int[n / 4 + 1];
            int count = 0;
            for (int g = 4; g <= n; g += 4) {
                int delta = g - balance;
                if (Math.abs(delta) <= remaining && ((remaining - delta) & 1) == 0) {
                    values[count++] = g;
                }
            }
            return Arrays.copyOf(values, count);
        }

        /**
         * Necessary endpoint test, free of P16.  Without the strand-density
         * bound the only residue-theorem-free constraint on the endpoint is
         * that it be nonzero and L1-reachable in the steps that remain.  A
         * nonzero lattice point within L1 distance {@code remaining} of (x,y)
         * exists whenever any step remains; with no steps left the current
         * point must itself be nonzero.  Endpoint parity is ignored, which
         * can only retain extra nodes.
         */
        boolean coarseEndpointPossible(int[] growths, int remaining) {
            if (growths.length == 0) {
                return false;
            }
            return remaining != 0 || x != 0 || y != 0;
        }

        void pushAndRecurse(int turn, int cell, byte previous) {
            int nextBalance = balance + (turn == 0 ? 1 : -1);
            if (nextBalance < 0) {
                ++result.growthPrunes;
                return;
            }
            int oldX = x;
            int oldY = y;
            int oldDirection = direction;
            posX[depth] = x;
            posY[depth] = y;
            turns[depth] = turn;
            lastTurn[cell] = (byte) turn;
            balance = nextBalance;
            direction = turn == 0 ? (direction + 1) & 3 : (direction + 3) & 3;
            x += DX[direction];
            y += DY[direction];
            ++depth;
            dfs();
            --depth;
            x = oldX;
            y = oldY;
            direction = oldDirection;
            balance -= turn == 0 ? 1 : -1;
            lastTurn[cell] = previous;
        }

        /**
         * P16-free deficit test.  The candidate drifts are the whole L1
         * reachability diamond of radius {@code remaining} about (x,y) minus
         * the origin, rather than the P16 square of the largest growth, and
         * no (growth, drift) pair is filtered by the strand-density bound.
         */
        boolean deficitFeasible(int[] growths, int remaining) {
            for (int driftX = x - remaining; driftX <= x + remaining; ++driftX) {
                int slack = remaining - Math.abs(driftX - x);
                for (int driftY = y - slack; driftY <= y + slack; ++driftY) {
                    if (driftX == 0 && driftY == 0) {
                        continue;
                    }
                    int distance = Math.abs(driftX - x) + Math.abs(driftY - y);
                    if (distance > remaining || ((remaining - distance) & 1) != 0) {
                        continue;
                    }
                    ++result.deficitEndpoints;
                    int[] need = oddEndingNeeds(driftX, driftY);
                    for (int g : growths) {
                        int delta = g - balance;
                        int futureR = (remaining + delta) / 2;
                        int futureL = (remaining - delta) / 2;
                        if (need[0] <= futureR && need[1] <= futureL) {
                            return true;
                        }
                    }
                }
            }
            return false;
        }

        int[] oddEndingNeeds(int driftX, int driftY) {
            for (int phase = 0; phase < depth; ++phase) {
                int px = posX[phase];
                int py = posY[phase];
                int level;
                if (driftX != 0) {
                    int reducedX = Math.floorMod(px, Math.abs(driftX));
                    level = (px - reducedX) / driftX;
                } else {
                    int reducedY = Math.floorMod(py, Math.abs(driftY));
                    level = (py - reducedY) / driftY;
                }
                int representativeX = px - level * driftX;
                int representativeY = py - level * driftY;
                long key = (((long) representativeX) << 32)
                        ^ (representativeY & 0xffffffffL);
                scratchRepresentative[phase] = key;
                scratchLevel[phase] = level;
                scratchOrder[phase] = phase;
            }
            sortStableEntries(depth);
            int needR = 0;
            int needL = 0;
            int previousPhase = -1;
            long previousRepresentative = 0;
            for (int slot = 0; slot < depth; ++slot) {
                int phase = scratchOrder[slot];
                long representative = scratchRepresentative[phase];
                if (previousPhase < 0 || representative != previousRepresentative) {
                    if (turns[phase] == 1) {
                        ++needR;
                    }
                } else {
                    int left = turns[previousPhase];
                    int right = turns[phase];
                    if (left == 1 && right == 1) {
                        ++needR;
                    } else if (left == 0 && right == 0) {
                        ++needL;
                    }
                }
                previousPhase = phase;
                previousRepresentative = representative;
            }
            return new int[] {needR, needL};
        }

        void sortStableEntries(int length) {
            // Primitive insertion sort is faster here than allocating maps and
            // Entry objects: the period is at most a few dozen in this search.
            for (int i = 1; i < length; ++i) {
                int phase = scratchOrder[i];
                int j = i - 1;
                while (j >= 0 && compareStable(phase, scratchOrder[j]) < 0) {
                    scratchOrder[j + 1] = scratchOrder[j];
                    --j;
                }
                scratchOrder[j + 1] = phase;
            }
        }

        int compareStable(int phaseA, int phaseB) {
            long representativeA = scratchRepresentative[phaseA];
            long representativeB = scratchRepresentative[phaseB];
            if (representativeA != representativeB) {
                return Long.compare(representativeA, representativeB);
            }
            int levelA = scratchLevel[phaseA];
            int levelB = scratchLevel[phaseB];
            if (levelA != levelB) {
                return Integer.compare(levelB, levelA); // decreasing level
            }
            return Integer.compare(phaseA, phaseB);
        }

        boolean p3Valid(int driftX, int driftY) {
            for (int phase = 0; phase < n; ++phase) {
                int px = posX[phase];
                int py = posY[phase];
                int level;
                if (driftX != 0) {
                    int reducedX = Math.floorMod(px, Math.abs(driftX));
                    level = (px - reducedX) / driftX;
                } else {
                    int reducedY = Math.floorMod(py, Math.abs(driftY));
                    level = (py - reducedY) / driftY;
                }
                int representativeX = px - level * driftX;
                int representativeY = py - level * driftY;
                scratchRepresentative[phase] = (((long) representativeX) << 32)
                        ^ (representativeY & 0xffffffffL);
                scratchLevel[phase] = level;
                scratchOrder[phase] = phase;
            }
            sortStableEntries(n);
            int previousPhase = -1;
            long previousRepresentative = 0;
            for (int slot = 0; slot < n; ++slot) {
                int phase = scratchOrder[slot];
                long representative = scratchRepresentative[phase];
                if (previousPhase < 0 || representative != previousRepresentative) {
                    if (turns[phase] != 0) {
                        return false;
                    }
                } else if (turns[previousPhase] == turns[phase]) {
                    return false;
                }
                previousPhase = phase;
                previousRepresentative = representative;
            }
            return true;
        }

        String hitJson(int driftX, int driftY) {
            StringBuilder word = new StringBuilder(n);
            for (int i = 0; i < n; ++i) {
                word.append(turns[i] == 0 ? 'R' : 'L');
            }
            return String.format(Locale.ROOT,
                    "{\"trace\":\"%s\",\"growth\":%d,\"drift\":[%d,%d]}",
                    word, balance, driftX, driftY);
        }
    }

    static String prefixForRank(long rank, int prefixLength) {
        if (prefixLength < 1 || prefixLength > 62) {
            throw new IllegalArgumentException("prefix length must be in [1,62]");
        }
        StringBuilder prefix = new StringBuilder(prefixLength);
        prefix.append('R');
        for (int bit = prefixLength - 2; bit >= 0; --bit) {
            prefix.append(((rank >>> bit) & 1L) == 0 ? 'R' : 'L');
        }
        return prefix.toString();
    }

    static Config parseArgs(String[] args) {
        int period = 34;
        int prefixLength = 10;
        long rankStart = 0;
        long rankStop = -1;
        int[] deficitDepths = new int[0];
        Path output = null;
        for (int i = 0; i < args.length; ++i) {
            switch (args[i]) {
                case "--period" -> period = Integer.parseInt(args[++i]);
                case "--prefix-length" -> prefixLength = Integer.parseInt(args[++i]);
                case "--rank-start" -> rankStart = Long.parseLong(args[++i]);
                case "--rank-stop" -> rankStop = Long.parseLong(args[++i]);
                case "--deficit-depths" -> {
                    String value = args[++i];
                    if (value.isBlank() || value.equals("0")) {
                        deficitDepths = new int[0];
                    } else {
                        deficitDepths = Arrays.stream(value.split(","))
                                .mapToInt(Integer::parseInt).toArray();
                    }
                }
                case "--output" -> output = Path.of(args[++i]);
                default -> throw new IllegalArgumentException("unknown argument: " + args[i]);
            }
        }
        if (rankStop < 0) {
            rankStop = 1L << (prefixLength - 1);
        }
        long totalRanks = 1L << (prefixLength - 1);
        if (period < prefixLength || rankStart < 0 || rankStop < rankStart
                || rankStop > totalRanks) {
            throw new IllegalArgumentException("invalid period/prefix/rank interval");
        }
        return new Config(period, prefixLength, rankStart, rankStop,
                deficitDepths, output);
    }

    static String jsonEscape(String text) {
        return text.replace("\\", "\\\\").replace("\"", "\\\"");
    }

    static void checkOneTrace(String text) {
        String trace = text.toUpperCase(Locale.ROOT);
        if (trace.isEmpty() || trace.chars().anyMatch(c -> c != 'R' && c != 'L')) {
            throw new IllegalArgumentException("--check-trace requires a nonempty R/L word");
        }
        RankResult result = new RankResult();
        Search search = new Search(trace.length(), new int[0], result);
        boolean prefixRulesValid = search.applyPrefix(trace);
        boolean structural = prefixRulesValid
                && search.balance > 0
                && (search.balance & 3) == 0
                && (search.x != 0 || search.y != 0);
        // P16 is reported for information only and does NOT gate the exact
        // criterion: the criterion is evaluated on every structural leaf.
        boolean p16 = structural
                && 2 * Math.max(Math.abs(search.x), Math.abs(search.y)) <= search.balance;
        boolean p3 = structural && search.p3Valid(search.x, search.y);
        System.out.printf(Locale.ROOT,
                "{\"period\":%d,\"prefix_rules_valid\":%s,\"growth\":%d,"
                        + "\"drift\":[%d,%d],\"p16_informational\":%s,\"p3_valid\":%s}%n",
                trace.length(), prefixRulesValid, search.balance, search.x, search.y,
                p16, p3);
    }

    public static void main(String[] args) throws IOException {
        if (args.length == 2 && args[0].equals("--check-trace")) {
            checkOneTrace(args[1]);
            return;
        }
        Config config = parseArgs(args);
        List<RankResult> results = new ArrayList<>();
        long allNodes = 0;
        long allGrowthPrunes = 0;
        long allEndpointPrunes = 0;
        long allDeficitPrunes = 0;
        long allDeficitChecks = 0;
        long allDeficitEndpoints = 0;
        long allLeaves = 0;
        long allP3Checks = 0;
        List<String> allHits = new ArrayList<>();
        long globalStart = System.nanoTime();

        for (long rank = config.rankStart; rank < config.rankStop; ++rank) {
            RankResult result = new RankResult();
            result.rank = rank;
            result.prefix = prefixForRank(rank, config.prefixLength);
            long start = System.nanoTime();
            Search search = new Search(config.period, config.deficitDepths, result);
            result.prefixValid = search.applyPrefix(result.prefix);
            if (result.prefixValid) {
                search.dfs();
            }
            result.seconds = (System.nanoTime() - start) / 1_000_000_000.0;
            results.add(result);
            allNodes += result.nodes;
            allGrowthPrunes += result.growthPrunes;
            allEndpointPrunes += result.endpointPrunes;
            allDeficitPrunes += result.deficitPrunes;
            allDeficitChecks += result.deficitChecks;
            allDeficitEndpoints += result.deficitEndpoints;
            allLeaves += result.leaves;
            allP3Checks += result.p3Checks;
            allHits.addAll(result.hits);
        }
        double totalSeconds = (System.nanoTime() - globalStart) / 1_000_000_000.0;

        StringBuilder json = new StringBuilder();
        json.append("{\n");
        json.append("  \"schema\": \"positive-growth-periodic-search-indep-v1\",\n");
        json.append("  \"claim\": \"exact finite search over the stated rank interval; no node cap\",\n");
        json.append("  \"residue_theorem_used\": false,\n");
        json.append("  \"exact_criterion_applied_to\": \"every positive-growth nonzero-drift leaf\",\n");
        json.append("  \"period\": ").append(config.period).append(",\n");
        json.append("  \"prefix_length\": ").append(config.prefixLength).append(",\n");
        json.append("  \"rank_start\": ").append(config.rankStart).append(",\n");
        json.append("  \"rank_stop\": ").append(config.rankStop).append(",\n");
        json.append("  \"total_rank_count\": ")
                .append(1L << (config.prefixLength - 1)).append(",\n");
        json.append("  \"deficit_depths\": ").append(Arrays.toString(config.deficitDepths)).append(",\n");
        json.append("  \"normalization\": \"cyclic shift after a global minimum: first symbol R and every prefix #R-#L nonnegative\",\n");
        json.append("  \"pruning\": [\"same-cell alternation\", \"positive growth multiple of 4 reachability\", \"nonzero L1-reachable endpoint\", \"odd-ending completion deficit\"],\n");
        json.append("  \"search_complete\": true,\n");
        json.append("  \"node_cap\": null,\n");
        json.append("  \"nodes\": ").append(allNodes).append(",\n");
        json.append("  \"growth_prunes\": ").append(allGrowthPrunes).append(",\n");
        json.append("  \"endpoint_prunes\": ").append(allEndpointPrunes).append(",\n");
        json.append("  \"deficit_checks\": ").append(allDeficitChecks).append(",\n");
        json.append("  \"deficit_prunes\": ").append(allDeficitPrunes).append(",\n");
        json.append("  \"deficit_endpoints_tested\": ").append(allDeficitEndpoints).append(",\n");
        json.append("  \"leaves\": ").append(allLeaves).append(",\n");
        json.append("  \"p3_checks\": ").append(allP3Checks).append(",\n");
        json.append("  \"hits\": [");
        for (int i = 0; i < allHits.size(); ++i) {
            if (i > 0) json.append(',');
            json.append(allHits.get(i));
        }
        json.append("],\n");
        json.append(String.format(Locale.ROOT, "  \"seconds\": %.9f,\n", totalSeconds));
        json.append("  \"results\": [\n");
        for (int i = 0; i < results.size(); ++i) {
            RankResult result = results.get(i);
            json.append("    {\"rank\":").append(result.rank)
                    .append(",\"prefix\":\"").append(jsonEscape(result.prefix))
                    .append("\",\"prefix_valid\":").append(result.prefixValid)
                    .append(",\"nodes\":").append(result.nodes)
                    .append(",\"growth_prunes\":").append(result.growthPrunes)
                    .append(",\"endpoint_prunes\":").append(result.endpointPrunes)
                    .append(",\"deficit_checks\":").append(result.deficitChecks)
                    .append(",\"deficit_prunes\":").append(result.deficitPrunes)
                    .append(",\"deficit_endpoints_tested\":").append(result.deficitEndpoints)
                    .append(",\"leaves\":").append(result.leaves)
                    .append(",\"p3_checks\":").append(result.p3Checks)
                    .append(",\"hits\":[");
            for (int j = 0; j < result.hits.size(); ++j) {
                if (j > 0) json.append(',');
                json.append(result.hits.get(j));
            }
            json.append(']');
            json.append(String.format(Locale.ROOT, ",\"seconds\":%.9f}", result.seconds));
            if (i + 1 < results.size()) json.append(',');
            json.append('\n');
        }
        json.append("  ]\n}\n");
        String rendered = json.toString();
        if (config.output != null) {
            Path parent = config.output.toAbsolutePath().getParent();
            if (parent != null) Files.createDirectories(parent);
            Files.writeString(config.output, rendered, StandardCharsets.UTF_8);
        }
        System.out.print(rendered);
    }
}
