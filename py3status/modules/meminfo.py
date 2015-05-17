# -*- coding: utf-8 -*-
"""
Display system RAM utilization.

@author Shahin Azad <ishahinism at Gmail>

modified by Brian Bove <bmbove at Gmail>
"""

import subprocess
from time import time


class GetData:

    def memory(self):
        """ Read and parse /proc/meminfo for total and used memory
        then return; Memory size total_mem, used_mem, and percentage
        of used memory.
        """

        mem_dict = {}
        with open("/proc/meminfo", "r") as fh:
            lines = [line.strip() for line in fh]

        for line in lines:
            data = [info for info in line.split(" ") if info]
            mem_dict[data[0].replace(":", "")] = int(data[1])

        total_mem = mem_dict["MemTotal"]/1024.0**2
        used_mem = mem_dict["Active"]/1024.0**2

        # Caculate percentage
        used_mem_percent = int(used_mem / (total_mem / 100))

        # Results are in kilobyte.
        return total_mem, used_mem, used_mem_percent


class Py3status:
    """
    """
    # available configuration parameters
    cache_timeout = 10
    med_threshold = 40
    high_threshold = 75

    def __init__(self):
        self.data = GetData()

    def ramInfo(self, i3s_output_list, i3s_config):
        """Calculate the memory (RAM) status and return it.
        """
        response = {'full_text': ''}
        total_mem, used_mem, used_mem_percent = self.data.memory()

        if used_mem_percent <= self.med_threshold:
            response['color'] = i3s_config['color_good']
        elif used_mem_percent <= self.high_threshold:
            response['color'] = i3s_config['color_degraded']
        else:
            response['color'] = i3s_config['color_bad']

        response['full_text'] = "RAM: %.2f/%.2f GB (%d%%)" % (
            float(used_mem),
            float(total_mem),
            used_mem_percent
        )
        response['cached_until'] = time() + self.cache_timeout

        return response

if __name__ == "__main__":
    """
    Test this module by calling it directly.
    """
    from time import sleep
    x = Py3status()
    config = {
        'color_good': '#00FF00',
        'color_bad': '#FF0000',
    }
    while True:
        print(x.ramInfo([], config))
        sleep(1)
