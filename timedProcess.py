import time

class TimedProcess:
    def __init__(self, _object, f, params):
        self.object = _object
        self.function = getattr(_object, f)
        self.params = params
        self.timeToComplete = 0

    def run(self):
        start = time.time()
        self.function(**self.params)
        end = time.time()
        self.timeToComplete = end - start

    def getTime(self):
        return self.timeToComplete

class TimedProcessSeries():
    def __init__(self, _object, f, params: []):
        self.object = _object
        self.function = getattr(_object, f)
        self.params = params  # params is now a list of params, to run the function repeatedly
        self.completionTimes: [int] = []

    def run(self):
        for _params in self.params:
            start = time.time()
            self.function(**_params)
            end = time.time()
            self.completionTimes.append(end - start)

    def getMinTime(self):
        return min(*self.completionTimes)

    def getMaxTime(self):
        return max(*self.completionTimes)

    def getAverageTime(self):
        s = 0
        for t in self.completionTimes:
            s += t
        return s / len(self.completionTimes)

    def getTimes(self):
        return self.completionTimes
