from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app import Cfg,Monitor

def test_monitor_construct()->None:
    m=Monitor(Cfg(cycles=2))
    assert m.cfg.cycles==2
