from vicsek.vicsek_bad import VicsekModel
import numpy as np

def test_distance():
  r1 = np.array([1,1])
  r2 = np.array([2,2])
  assert(VicsekModel.distance(r1, r2) == np.sqrt(2))
  
def test_main():
  assert(True)