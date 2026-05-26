from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from simulator import Packet

def test_packet_roundtrip()->None:
    raw=Packet.build(1,2,3.5,100)
    n,s,t,v=Packet.parse(raw)
    assert (n,s,t)==(1,2,100)
    assert abs(v-3.5)<1e-6
