
class IOwait():
	def __init__(self):
		self.jobs=[]

	#our function to add a job
	def addJob(self, job):
		#need to define this in the PROCESS class
		job.wait_on_IO()
		self.jobs.append(job)


	#this waits for 1 unit of time for each job in this q. any jobs that are finished waiting
	#are returned in the list ready_processes. Any processes that reenter the ready q are given
	# a birthday
	def wait_one(self, time):
		ready_processes=[]
		for i in xrange(len(self.jobs)-1, -1, -1):
			#if the process is done waiting add it ready_processes
			if self.jobs[i].run():
				self.jobs[i].set_burst_time(time)
				ready_processes.append(self.jobs.pop(i))
		return ready_processes