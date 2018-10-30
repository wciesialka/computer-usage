import matplotlib.pyplot as plt
import numpy as np
import psutil
import time

DELAY = 5

plt.ion()

class ComputerUsagePlot():
	
	min_y = 0
	max_y = 100
	t = 0

	CPU_USAGE = []
	RAM_USAGE = []
	TIMES = []
	FORMATTED_TIMES = []

	def right_now(self):
		now = time.localtime()
		return str(now.tm_hour) + ":" + str(now.tm_min) + ":" + str(now.tm_sec)

	def init(self):
		self.fig, self.axs = plt.subplots()
		self.axs.set_xlabel("Time")
		self.axs.set_ylabel("Usage (percent)")
		self.axs.set_title("Usage Over Time")
		self.cpu_usage, = self.axs.plot([],[],color="blue",label="CPU")
		self.ram_usage, = self.axs.plot([],[],color="red",label="RAM")
		self.axs.set_autoscaley_on(True)
		self.axs.set_ylim(self.min_y,self.max_y)

	def update_lines(self):
		self.cpu_usage.set_xdata(self.TIMES)
		self.cpu_usage.set_ydata(self.CPU_USAGE)
		self.ram_usage.set_xdata(self.TIMES)
		self.ram_usage.set_ydata(self.RAM_USAGE)

		plt.xticks(self.TIMES,self.FORMATTED_TIMES,rotation=45)

		self.axs.relim()
		self.axs.autoscale_view()

		self.fig.canvas.draw()
		self.fig.canvas.flush_events()

	def update_usage(self):
		self.CPU_USAGE.append(psutil.cpu_percent(interval=None))
		self.RAM_USAGE.append(psutil.virtual_memory().percent)
		self.TIMES.append(self.t)
		self.FORMATTED_TIMES.append(self.right_now())
		self.t += 1

	def __call__(self):
		self.init()
		while True:
			self.update_usage()
			self.update_lines()
			time.sleep(DELAY)

if __name__=="__main__":
	psutil.cpu_percent(interval=None) #throw away
	time.sleep(1)
	compuseplot = ComputerUsagePlot()
	while time.localtime().tm_sec % DELAY != 0:
		pass
	compuseplot()
