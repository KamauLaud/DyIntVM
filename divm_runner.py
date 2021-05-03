#
#Author: Cory Ilo
#
#
# This runner will
# 


import cv2

class DIVM_runner:

	def __init__(self, video_filename):
		self.filename = video_filename
		self.vid = cv2.VideoCapture(video_filename)
		self.isPlaying = False 

	def __del__(self):
		self.vid.release()
		cv2.destroyAllWindows()


	# Code inspired by: https://stackoverflow.com/questions/38064777/use-waitkey-in-order-pause-and-play-video
	def runPlayer(self):
		isPlaying = True
		while self.vid.isOpened():
			ret, img =  self.vid.read()

			cv2.imshow("curFrame", img)
			key = cv2.waitKey(1)

			if key == ord('q'):
				#close player
				break
			elif key == ord('p'):
				
				if (isPlaying):
					isPlaying = False
					cv2.waitKey(-1)
				elif (not isPlaying):
					isPlaying = True
					continue 

			elif key == ord('n'):
				# spawn notification
				continue

	def notify( screenshot ):
		## screenshot is an image from the video
		## TODO, Adheesh - add code to return a placement classification
		## Expected return: a string "xxxx" representing the placement
		return


def main():

	f_names = ["test_vidz/apexLegends_fail.mp4"]

	#test 1
	player = DIVM_runner(f_names[0])
	player.runPlayer()

	#test 1
	#player = DIVM_runner(f_names[0])





if __name__ == '__main__':
	main()


