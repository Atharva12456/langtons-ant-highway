import Langton
import Langton.ResidueCharge
import Langton.ChargeTelescoping
import Langton.CollisionParity
import Langton.TraceGeometry
import Langton.DirectedPoseDiscrepancy
import Langton.P3Endpoint
import Langton.WidthFour
import Langton.WidthFourCrossing

open Langton

def main : IO Unit := do
  IO.println "Langton ant kernel and parity certificates compiled."
