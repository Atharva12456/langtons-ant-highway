import java.util.Arrays;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/** Compiled exact violation checker, cross-validated against langton_research.py. */
public final class HammingStandard {
    private static final int[] DX = {0, 1, 0, -1};
    private static final int[] DY = {1, 0, -1, 0};

    private static int score(int[] word) {
        int n = word.length;
        int[] xs = new int[n];
        int[] ys = new int[n];
        int x = 0, y = 0, direction = 0;
        for (int phase = 0; phase < n; phase++) {
            xs[phase] = x;
            ys[phase] = y;
            direction = (direction + (word[phase] == 0 ? 1 : 3)) & 3;
            x += DX[direction];
            y += DY[direction];
        }
        if (direction != 0) return n;
        int driftX = x, driftY = y;
        if (driftX == 0 && driftY == 0) return n;

        long[] ordered = new long[n];
        for (int phase = 0; phase < n; phase++) {
            int level, repX, repY;
            if (driftX != 0) {
                int reducedX = Math.floorMod(xs[phase], Math.abs(driftX));
                level = (xs[phase] - reducedX) / driftX;
                repX = reducedX;
                repY = ys[phase] - level * driftY;
            } else {
                int reducedY = Math.floorMod(ys[phase], Math.abs(driftY));
                level = (ys[phase] - reducedY) / driftY;
                repX = xs[phase];
                repY = reducedY;
            }
            if (repX < -32768 || repX > 32767 || repY < -32768 || repY > 32767
                    || level < -511 || level > 512 || phase > 127) {
                throw new AssertionError("packing bound exceeded");
            }
            long groupX = repX + 32768L;
            long groupY = repY + 32768L;
            long descendingLevel = 512L - level;
            ordered[phase] = (groupX << 34) | (groupY << 18)
                    | (descendingLevel << 8) | ((long) phase << 1) | word[phase];
        }
        Arrays.sort(ordered);
        int violations = 0;
        long previousGroup = -1;
        int previousTurn = -1;
        for (long item : ordered) {
            long group = item >>> 18;
            int turn = (int) (item & 1L);
            if (group != previousGroup) {
                if (turn != 0) violations++;
                previousGroup = group;
            } else if (turn == previousTurn) {
                violations++;
            }
            previousTurn = turn;
        }
        return violations;
    }

    private static void record(int[] word, int[] edits, long[] evaluated,
                               int[] best, long[] bestCount, long[] hits,
                               Map<Integer, Long> histogram, List<String> bestEdits,
                               List<String> nearEdits) {
        int value = score(word);
        evaluated[0]++;
        histogram.merge(value, 1L, Long::sum);
        if (value <= 5) nearEdits.add(Arrays.toString(edits));
        if (value < best[0]) {
            best[0] = value;
            bestCount[0] = 1;
            bestEdits.clear();
            bestEdits.add(Arrays.toString(edits));
        } else if (value == best[0]) {
            bestCount[0]++;
            if (bestEdits.size() < 50) bestEdits.add(Arrays.toString(edits));
        }
        if (value == 0) {
            hits[0]++;
            System.err.println("zero at edits " + Arrays.toString(edits));
        }
    }

    public static void main(String[] args) {
        if (args.length != 2) {
            throw new IllegalArgumentException("usage: HammingStandard WORD DISTANCE");
        }
        String text = args[0];
        int distance = Integer.parseInt(args[1]);
        int[] word = new int[text.length()];
        for (int i = 0; i < word.length; i++) word[i] = text.charAt(i) == 'L' ? 1 : 0;
        if (score(word) != 0) throw new AssertionError("standard word did not score zero");

        long started = System.nanoTime();
        long[] evaluated = {0}, bestCount = {0}, hits = {0};
        int[] best = {Integer.MAX_VALUE};
        Map<Integer, Long> histogram = new HashMap<>();
        List<String> bestEdits = new ArrayList<>();
        List<String> nearEdits = new ArrayList<>();
        int n = word.length;
        if (distance == 2) {
            for (int i = 0; i < n; i++) for (int j = i + 1; j < n; j++) {
                word[i] ^= 1; word[j] ^= 1;
                record(word, new int[]{i, j}, evaluated, best, bestCount, hits, histogram, bestEdits, nearEdits);
                word[i] ^= 1; word[j] ^= 1;
            }
        } else if (distance == 4) {
            for (int i = 0; i < n; i++) for (int j = i + 1; j < n; j++)
                for (int k = j + 1; k < n; k++) for (int l = k + 1; l < n; l++) {
                    word[i] ^= 1; word[j] ^= 1; word[k] ^= 1; word[l] ^= 1;
                    record(word, new int[]{i, j, k, l}, evaluated, best, bestCount, hits, histogram, bestEdits, nearEdits);
                    word[i] ^= 1; word[j] ^= 1; word[k] ^= 1; word[l] ^= 1;
                }
        } else {
            throw new IllegalArgumentException("distance must be 2 or 4");
        }
        double seconds = (System.nanoTime() - started) / 1_000_000_000.0;
        System.out.printf(
                "{\n  \"distance\": %d,\n  \"evaluated\": %d,\n  \"best_score\": %d,\n"
                + "  \"best_score_count\": %d,\n  \"exact_highways_found\": %d,\n"
                + "  \"seconds\": %.6f,\n  \"best_edits\": \"%s\",\n  \"near_edits_score_at_most_5\": \"%s\",\n  \"score_histogram\": \"%s\"\n}\n",
                distance, evaluated[0], best[0], bestCount[0], hits[0], seconds,
                bestEdits.toString().replace("\"", "\\\""),
                nearEdits.toString().replace("\"", "\\\""),
                histogram.toString().replace("\"", "\\\""));
    }
}
