import psutil
import os
import json
import time


class ResourcesMonitor:
    def __init__(self, port=3030, pid=-1):
        self.port = port
        self.pid = pid
        self.process = None

    def get_pid(self):
        processes = os.popen('netstat -aon | find "{0}"'.format(self.port)).read()
        self.pid = int(processes[155:-1])
        return self.pid

    def create_process(self):
        if psutil.pid_exists(self.pid):
            self.process = psutil.Process(self.pid)
        else:
            print('No such process with PID: {0)'.format(self.pid))

    def monitor(self):
        cpu_times = self.process.cpu_times()
        cpu_per = self.process.cpu_percent()
        memory_data = self.process.memory_info()
        print(memory_data)
        data = {
            "user_time": cpu_times.user,
            "system_time": cpu_times.system,
            "cpu_percent": cpu_per,
            "resident_set_size": memory_data.rss,
            "virtual_set_size": memory_data.vms,
            "shared_memory": memory_data.num_page_faults
        }
        return data


if __name__ == "__main__":
    rm = ResourcesMonitor(port=3030)
    rm.get_pid()
    rm.create_process()

    history = []

    try:
            while True:
                data = rm.monitor()
                history.append(data)
                time.sleep(0.2)
    except KeyboardInterrupt:
        with open('cpu_memory_stats.json', 'w') as file:
            json.dump(history, file)
        exit(0)
