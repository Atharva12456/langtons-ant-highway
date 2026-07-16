#!/usr/bin/env bash
# Work-queue run of the Theorem-7.1-independent reference engine.
# Many small shards + xargs -P so slow rank blocks cannot dominate wall time.
# Usage: run_indep_q.sh PERIOD PREFIXLEN NSHARDS NPROC OUTDIR
set -u
P=$1; PL=$2; NS=$3; NP=$4; OUT=$5
mkdir -p "$OUT"
TOTAL=$((1 << (PL - 1)))
STEP=$(( (TOTAL + NS - 1) / NS ))
echo "period=$P prefix=$PL total_ranks=$TOTAL shards=$NS step=$STEP nproc=$NP -> $OUT"
seq 0 $((NS - 1)) | xargs -P "$NP" -I{} bash -c '
  s={}; P='"$P"'; PL='"$PL"'; STEP='"$STEP"'; TOTAL='"$TOTAL"'; OUT="'"$OUT"'"
  A=$((s * STEP)); B=$((A + STEP))
  if [ $A -ge $TOTAL ]; then exit 0; fi
  if [ $B -gt $TOTAL ]; then B=$TOTAL; fi
  F="$OUT/shard_$(printf "%04d" $s).json"
  if [ -f "$F" ]; then exit 0; fi
  java -cp indep_classes PositiveGrowthSearchIndep \
    --period "$P" --prefix-length "$PL" --rank-start "$A" --rank-stop "$B" \
    --deficit-depths 0 --output "$F" > "$OUT/shard_$(printf "%04d" $s).log" 2>&1
'
echo "queue drained for period $P"
