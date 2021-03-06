import matplotlib.pyplot as plt
import psutil
import time
import sys
import math

DELAY = 5
MAX_TICKS = 3

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

	def linspace(self,lower,upper,length):
		ret = []
		for x in range(length):
			ret.append(round(lower + x*(upper-lower)/(length-1)))
		return ret

	def update_lines(self):
		self.cpu_usage.set_xdata(self.TIMES)
		self.cpu_usage.set_ydata(self.CPU_USAGE)
		self.ram_usage.set_xdata(self.TIMES)
		self.ram_usage.set_ydata(self.RAM_USAGE)
		
		tick_array = self.linspace(self.TIMES[0],self.TIMES[len(self.TIMES)-1],MAX_TICKS) #[self.TIMES[0],self.TIMES[len(self.TIMES)-1]]
		tick_labels = []
		for i in tick_array:
			tick_labels.append(self.FORMATTED_TIMES[i])

		plt.xticks(tick_array,tick_labels,rotation=45)

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
	try:
		DELAY = int(sys.argv[1]) or 5
	except:
		DELAY = 5
	try:
		MAX_TICKS = int(sys.argv[2]) or 3
	except:
		MAX_TICKS = 3
	psutil.cpu_percent(interval=None) #throw away
	time.sleep(1)
	compuseplot = ComputerUsagePlot()
	while time.localtime().tm_sec % DELAY != 0:
		pass
	compuseplot()
