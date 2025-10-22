import subprocess


class Deployment:
    def __init__(self, core_dir: str):
        self.core_dir = core_dir

    def restart(self):
        subprocess.run(["make", "restart"], cwd=self.core_dir, check=True)
