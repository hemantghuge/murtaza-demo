import os
import json
import socket
import sys

def saveStats(filename, fps):

	stats_file = "stats.json"

	if not os.path.exists(stats_file):
		dict = {
			0: {'filename': 'dummy.py', 'device_name':'dummy', 'fps': 30}
		}
	else:
		with open(stats_file, 'r') as openfile:
			dict = json.load(openfile)

	device_name = socket.gethostname()

	write_flag = True

	for key in dict:
		#print(dict[key])
		if dict[key]['filename'] == filename and dict[key]['device_name'] == device_name and dict[key]['fps'] == fps:
			write_flag = False
			break

	if write_flag:
		dict[len(dict)] = {'filename': filename, 'device_name': device_name, 'fps': fps}

		json_object = json.dumps(dict, indent = 4)

		# Writing to sample.json
		with open(stats_file, "w") as outfile:
			outfile.write(json_object)

def main():
	filename = __file__
	fps = 24
	saveStats(filename, fps)


if __name__ == "__main__":
	main()
