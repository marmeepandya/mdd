"""Rebuild every study guide PDF:  python build_all.py"""
import runpy, os
here = os.path.dirname(os.path.abspath(__file__))
os.chdir(here)
for n in range(1, 10):
    runpy.run_path(os.path.join(here, f"build_l{n}.py"), run_name="__main__")
