'''Install Blender dependencies.

Meant to be run ONCE via blender as follows
`blender --background --python scripts/install_btb.py`
'''

import bpy
import sys
import subprocess
import os
from pathlib import Path

THISDIR = Path(__file__).parent


def run(cmd):
    try:
        output = subprocess.check_output(cmd)
        print(output)
    except subprocess.CalledProcessError as e:
        print(e.output)
        sys.exit(1)


def install(name, upgrade=False, user=False, editable=False):
    cmd = [sys.executable, '-m', 'pip', 'install']
    if upgrade:
        cmd.append('--upgrade')
    if user:
        cmd.append('--user')
    if editable:
        cmd.append('-e')
    cmd.append(name)
    run(cmd)


def bootstrap(user=False):
    cmd = [sys.executable, '-m', 'ensurepip', '--upgrade']
    if user:
        cmd.append('--user')
    run(cmd)
    cmd = [sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip']
    if user:
        cmd.append('--user')
    run(cmd)


def main():
    print('Installing Blender dependencies. This might take a while...')
    bootstrap()
    install("ipdb")
    install("trimesh")
    install("pyyaml")
    install("supershape")
    install(os.path.join(THISDIR, "..", "pkg_blender"), editable=True)

main()
