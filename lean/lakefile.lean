import Lake
open Lake DSL

package «lean-langton» where
  version := v!"0.1.0"

lean_lib «Langton» where

@[default_target]
lean_exe «langton-check» where
  root := `Main
