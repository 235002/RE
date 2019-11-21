import psutil
import os
import json
import time
import pandas as pd
import matplotlib.pyplot as plt


class ResourcesMonitor:
    def __init__(self, port=3030, pid=-1):
        self.port = port
        self.pid = pid
        self.process = None

    def get_pid(self):
        processes = os.popen('netstat -aon | find "{0}"'.format(self.port)).read()
        self.pid = int(processes[155:-1])
        return self.pid

    def set_pid(self, pid):
        self.pid = pid

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

    @staticmethod
    def prepare_data(file_name):
        with open(file_name, 'r') as file:
            data = json.load(file)
            df = pd.DataFrame.from_dict(data, orient='columns')

            time_list = []
            for index, item in df.iterrows():
                time_list.append(index/5)
            df['time'] = time_list
        return df

    @staticmethod
    def memory_plot(df):
        plt.figure()
        ax = plt.gca()
        df.plot(kind='line', x='time', y='resident_set_size', color='blue', ax=ax)
        df.plot(kind='line', x='time', y='virtual_set_size', color='red', ax=ax)
        ax.set_title('Memory usage')
        ax.set_xlabel('Time [s]')
        ax.set_ylabel('Memory [B]')
        plt.show()

    @staticmethod
    def cpu_plot(df):
        plt.figure()
        ax = plt.gca()
        df.plot(kind='line', x='time', y='user_time', color='red', ax=ax)
        df.plot(kind='line', x='time', y='system_time', color='green', ax=ax)
        ax.set_title('Time of CPU usage')
        ax.set_xlabel('Time [s]')
        ax.set_ylabel('CPU')
        plt.show()

    @staticmethod
    def cpu_plot2(df):
        plt.figure()
        ax = plt.gca()
        df.plot(kind='line', x='time', y='cpu_percent', color='blue', ax=ax)
        ax.set_title('Percentage of CPU usage')
        ax.set_xlabel('Time [s]')
        ax.set_ylabel('CPU')
        plt.show()


if __name__ == "__main__":
    rm = ResourcesMonitor(port=3030)
    df = rm.prepare_data("all_reqs.json")
    rm.memory_plot(df)
    rm.cpu_plot(df)
    rm.cpu_plot2(df)
    # rm.set_pid(12984)
    # rm.create_process()
    #
    # history = []
    #
    # try:
    #         while True:
    #             data = rm.monitor()
    #             history.append(data)
    #             time.sleep(0.2)
    # except KeyboardInterrupt:
    #     with open('all_reqs.json', 'w') as file:
    #         json.dump(history, file)
    #     exit(0)
