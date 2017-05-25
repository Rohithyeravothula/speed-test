import speedtest
import time
import ConfigParser

def ConfigSectionMap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1


Config = ConfigParser.ConfigParser()
Config.read("config.ini")
configs = ConfigSectionMap('speed')
interval_time = int(configs['interval'])
iterations = int(configs['iterations'])

# interval_time = 30 #seconds
# iterations = 2


def get_speed():
	s = speedtest.Speedtest()
	s.get_best_server()
	down_speed = s.download()
	up_speed = s.upload()
	return down_speed/10**6, up_speed/10**6

def write(s):
	f = open("results.csv", 'a')
	f.write(s)
	f.close()

def sample(c):
	count = c 
	while count:
		prev = 0
		current = time.time()
		if current - prev > interval_time:
			t1 = time.time()
			down_speed, up_speed = get_speed()
			t2 = time.time()
			curTime = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(current))
			write(curTime + ", " + str(down_speed) + ", " + str(up_speed) + "\n")
			count -= 1
			prev = current
			print "done for iteration: " + str(c-count)
			print "completed in " + str(t2 - t1) + " seconds"


if __name__=='__main__':
	write("time, download, upload\n")
	sample(iterations)