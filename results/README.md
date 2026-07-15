# Results

Small, human-readable summaries of the exact computations. The **full per-rank shard
records are large (~150 MB) and are intentionally not committed**; they are exactly
regenerable with the commands in the top-level `README.md` and `../code/README.md`.

## Files

### `period_exclusion_summary.json`
Aggregated totals of the exhaustive periodic-highway searches. For every period up to
48 the number of highways found is **0**. Highlights:

- **Period ≤ 32:** complete legal-trace enumeration, 46,185,421 feasible nodes.
- **Periods 34–40:** exact positive-growth searches, up to ~2.0×10⁸ nodes each.
- **Periods 42, 44, 46, 48:** two independent engines, rank-by-rank cross-audited.
  At period 48 both engines visited the identical **8,677,026,370 nodes** and
  **451,962,870 leaves** over all 2¹⁶ prefix ranks, with **0 highways**; the
  residue-pruned engine rejected 439,705,662 leaves via the residue identity and
  applied the exact criterion to the remaining 12,257,208 — with all per-rank
  counters in agreement.

**Conclusion:** no finite-support periodic highway of nonzero drift and period ≤ 48
exists (other than, at period 104, the standard highway itself).

### `standard_highway.json`
The standard highway in exact form: its normalized 104-symbol turn word, drift
`(2,-2)`, net growth `12`, blank-orbit onset step `9977`, and the explicit 13-cell
black seed that produces it immediately from a north-facing ant at the origin.

## Regenerating the full records
See the top-level `README.md` (§ *Reproducing the search results*). Each shard is an
independent job; a complete exclusion is the union of shards covering every prefix
rank exactly once, with matching counters across the two engines.
