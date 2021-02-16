#!/usr/bin/env python3

import re
from os.path import exists, join


class Core():
    def __init__(self, core_number):
        self.core_number = core_number
        self.system_directory = f'/sys/devices/system/cpu/cpu{self.core_number}'
        self.enabled = self._get_enabled()

        # Frequency bounds (MHz)
        with open(join(self.system_directory, 'cpufreq/cpuinfo_min_freq'), 'r') as f:
            self.min_frequency = int(float(f.readline()) / 1000)
        with open(join(self.system_directory, 'cpufreq/cpuinfo_max_freq'), 'r') as f:
            self.max_frequency = int(float(f.readline()) / 1000)

        # Sibling unavailable if core is disabled. enable() sets this as well
        try:
            self.sibling = self._get_sibling()  # ID of the other virtual core that shares the same physical core
        except FileNotFoundError:
            self.sibling = None

    def enable(self):
        if self.core_number != 0:
            with open(join(self.system_directory, 'online'), 'w') as f:
                f.write('1')
            self.enabled = True
            while True:
                if exists(join(self.system_directory, 'topology/thread_siblings_list')):
                    break
            self.sibling = self._get_sibling()

    def disable(self):
        if self.core_number != 0:
            with open(join(self.system_directory, 'online'), 'w') as f:
                f.write('0')
            self.enabled = False

    def _get_enabled(self):
        if self.core_number == 0:
            return True
        with open(join(self.system_directory, 'online'), 'r') as f:
            return '0' not in f.readline()

    def _get_sibling(self):
        with open(join(self.system_directory, 'topology/thread_siblings_list'), 'r') as f:
            contents = re.sub('[^\\d]', ',', f.readline().strip()).split(',')
            pair = tuple(int(i) for i in contents)
            for core in pair:
                if core != self.core_number:
                    return core

    def __str__(self):
        return f'Core: {self.core_number} [{"ENABLED" if self.enabled else "DISABLED"}]\n  Sibling: {self.sibling}\n  Min Freq: {self.min_frequency} MHz\n  Max Freq: {self.max_frequency} MHz'


if __name__ == '__main__':
    core = Core(1)
    print(core)
