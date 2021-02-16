#!/usr/bin/env python3

from os.path import exists
from Core import Core


class PowerManager():
    def __init__(self):
        self.utilization_target = 0.25
        self.cores = self._get_cores()
        self.total_cpus = len(self.cores)

    def _get_cores(self):
        cores = []
        i = 0
        while True:
            if exists(f'/sys/devices/system/cpu/cpu{i}'):
                cores.append(Core(i))
                i += 1
            else:
                break
        return cores

    def get_utilization_target(self, filepath='/tmp/powermanager_target'):
        if exists('/tmp/powermanager_target'):
            try:
                with open('/tmp/powermanager_target', 'r') as f:
                    self.utilization_target = float(f.readline())
            except ValueError:
                with open('/tmp/powermanager_target', 'w') as f:
                    f.write(str(self.utilization_target))
        else:
            with open('/tmp/powermanager_target', 'w') as f:
                f.write(str(self.utilization_target))
        return self.utilization_target

    def set_utilization_target(self, value, filepath='/tmp/powermanager_target'):
        with open('/tmp/powermanager_target', 'w') as f:
            f.write(str(self.utilization_target))

    def set_core_status(self, cores, online):
        if online in (0, 1):
            for core in cores:
                core.set_status(online)


if __name__ == '__main__':
    manager = PowerManager()
    for i in range(len(manager.cores)):
        # manager.cores[i].disable()
        print(manager.cores[i])
