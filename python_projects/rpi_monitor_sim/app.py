from __future__ import annotations
import argparse, logging, random, threading, time
from contextlib import AbstractContextManager
from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path
from queue import Queue, Empty

class Fault(Enum): NONE=auto(); HIGH_TEMP=auto(); CLOSE_RANGE=auto()
@dataclass
class Cfg: interval:float=0.05; cycles:int=100; temp_limit:float=70; dist_limit:float=20; log:Path=Path("rpi_monitor.log")

class MockGPIO:
    def read_pin(self,p:int)->int: return random.randint(0,1)
class MockI2C:
    def read_temp(self)->float: return 55+random.uniform(-8,20)
class MockSPI:
    def read_distance(self)->float: return 40+random.uniform(-30,30)

class HAL(AbstractContextManager):
    def __init__(self)->None: self.gpio=MockGPIO(); self.i2c=MockI2C(); self.spi=MockSPI()
    def __exit__(self,exc_type,exc,tb): return False

class Monitor:
    def __init__(self,cfg:Cfg)->None:
        self.cfg=cfg; self.q:Queue[tuple[float,float]]=Queue(); self.faults:list[Fault]=[]; self.stop=False
        self.temp_hist:list[float]=[]; self.dist_hist:list[float]=[]
    def producer(self)->None:
        with HAL() as h:
            for _ in range(self.cfg.cycles):
                if self.stop: break
                self.q.put((h.i2c.read_temp(),h.spi.read_distance()))
                time.sleep(self.cfg.interval)
    def consumer(self)->None:
        for _ in range(self.cfg.cycles):
            try:t,d=self.q.get(timeout=1)
            except Empty: break
            self.temp_hist.append(t); self.dist_hist.append(d)
            ma_t=sum(self.temp_hist[-5:])/min(len(self.temp_hist),5)
            ma_d=sum(self.dist_hist[-5:])/min(len(self.dist_hist),5)
            if ma_t>self.cfg.temp_limit: self.faults.append(Fault.HIGH_TEMP)
            if ma_d<self.cfg.dist_limit: self.faults.append(Fault.CLOSE_RANGE)
            logging.info("temp=%.2f dist=%.2f ma_t=%.2f ma_d=%.2f",t,d,ma_t,ma_d)

def main()->int:
    p=argparse.ArgumentParser(); p.add_argument("--cycles",type=int,default=100); a=p.parse_args(); cfg=Cfg(cycles=a.cycles)
    logging.basicConfig(level=logging.INFO,handlers=[logging.FileHandler(cfg.log,mode="w"),logging.StreamHandler()])
    m=Monitor(cfg); th=threading.Thread(target=m.producer); th.start(); m.consumer(); m.stop=True; th.join()
    print("faults",[f.name for f in m.faults]); return 0

if __name__=="__main__": raise SystemExit(main())
