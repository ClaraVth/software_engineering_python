from vicsek.vicsek_bad import VicsekModel
from matplotlib.animation import FuncAnimation
import os
import numpy as np

def test_main():
  assert(True)

def test_figure():
  vicsek_model = VicsekModel()
  vicsek_model.init_model(200)
  ani = FuncAnimation(vicsek_model.fig, vicsek_model.animate, frames=20, interval=50, blit=True)
  outputfile = "animation.gif"
  #output_path.parent.mkdir(parents=True, exist_ok=True)
  ani.save(outputfile, writer="pillow")

  assert(os.path.exists(outputfile))
  #assert(outputfile.stat().st_size > 10)

def test_distance():
  r1 = np.array([1,1])
  r2 = np.array([2,2])
  assert(np.isclose(VicsekModel.distance(r1, r2), np.sqrt(2)))

