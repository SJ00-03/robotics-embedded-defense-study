from __future__ import annotations
import argparse, logging, random, struct, time
from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path
from queue import Queue, Empty
from typing import Dict

class Fault(Enum):
    NONE = auto(); TIMEOUT = auto(); BAD_CSUM = auto(); ABNORMAL = auto()

@dataclass
class Config:
    node_count:int=3; steps:int=120; timeout_sec:float=1.0; abnormal_limit:float=85.0; out:Path=Path("report.txt")

class Packet:
    FMT="<BBIfH"  # node,seq,ts,value,csum
    @staticmethod
    def checksum(data:bytes)->int:
        s=0
        for b in data: s=(s+b)&0xFFFF
        return s
    @classmethod
    def build(cls,node:int,seq:int,val:float,ts:int|None=None)->bytes:
        t=int(time.time()) if ts is None else ts
        body=struct.pack("<BBIf",node,seq,t,val)
        c=cls.checksum(body)
        return body+struct.pack("<H",c)
    @classmethod
    def parse(cls,raw:bytes)->tuple[int,int,int,float]:
        if len(raw)!=struct.calcsize(cls.FMT): raise ValueError("size")
        n,s,t,v,c=struct.unpack(cls.FMT,raw)
        if cls.checksum(raw[:-2])!=c: raise ValueError("checksum")
        return n,s,t,v

class SensorNode:
    def __init__(self,node_id:int)->None:
        self.node_id=node_id; self.seq=0; self.rng=random.Random(100+node_id)
    def emit(self)->bytes:
        self.seq=(self.seq+1)&0xFF
        value=50.0+self.rng.uniform(-10,10)
        if self.seq%37==0: value=120.0
        pkt=Packet.build(self.node_id,self.seq,value)
        if self.seq%41==0:
            bad=bytearray(pkt); bad[-1]^=0xFF; return bytes(bad)
        return pkt

class SensorManager:
    def __init__(self,cfg:Config)->None:
        self.cfg=cfg; self.q:Queue[bytes]=Queue(); self.nodes=[SensorNode(i+1) for i in range(cfg.node_count)]
        self.last_ts:Dict[int,int]={}; self.faults:Dict[int,list[Fault]]={i+1:[] for i in range(cfg.node_count)}
    def collect(self)->None:
        for n in self.nodes: self.q.put(n.emit())
    def process(self)->None:
        while True:
            try: raw=self.q.get_nowait()
            except Empty: break
            try:
                nid,seq,ts,val=Packet.parse(raw)
                self.last_ts[nid]=ts
                if val>self.cfg.abnormal_limit:
                    self.faults[nid].append(Fault.ABNORMAL); logging.warning("abnormal node=%d val=%.1f",nid,val)
            except ValueError as e:
                if str(e)=="checksum": logging.error("invalid checksum"); self.faults[1].append(Fault.BAD_CSUM)
    def timeout_check(self,now:int)->None:
        for nid in self.faults:
            if nid in self.last_ts and now-self.last_ts[nid]>self.cfg.timeout_sec:
                self.faults[nid].append(Fault.TIMEOUT)
    def report(self)->str:
        lines=["Safety Surveillance Report"]
        for nid,fs in self.faults.items(): lines.append(f"node {nid}: {[f.name for f in fs]}")
        return "\n".join(lines)

def main()->int:
    p=argparse.ArgumentParser(); p.add_argument("--steps",type=int,default=120); args=p.parse_args()
    cfg=Config(steps=args.steps)
    logging.basicConfig(level=logging.INFO,format="%(levelname)s %(message)s")
    mgr=SensorManager(cfg)
    for _ in range(cfg.steps):
        mgr.collect(); mgr.process(); mgr.timeout_check(int(time.time()))
    cfg.out.write_text(mgr.report(),encoding="utf-8")
    print(mgr.report())
    return 0

if __name__=="__main__":
    raise SystemExit(main())
