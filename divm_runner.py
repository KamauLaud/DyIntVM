#
#Author: Cory Ilo
#
#

import cv2
import torch

from torchvision import transforms

from model import AlexNet
from utils import Normalize, RandomCrop, SquarifyImage, \
    ToTensor, PredictImageSet

# mention torch device for gpu
device = None

class DIVM_runner:

	def __init__(self, video_filename):
		self.filename = video_filename
		self.vid = cv2.VideoCapture(video_filename)
		cv2.namedWindow("DIVM Demo", cv2.WINDOW_NORMAL)
		self.isPlaying = False 
		self.model = AlexNet(n_classes=4, device=device)
		# TODO: load trained model

	def __del__(self):
		self.vid.release()
		cv2.destroyAllWindows()


	# Code inspired by -  https://stackoverflow.com/questions/38064777/use-waitkey-in-order-pause-and-play-video
	def runPlayer(self):
		isPlaying = True
		while self.vid.isOpened():
			ret, img =  self.vid.read()

			cv2.imshow("curFrame", img)
			key = cv2.waitKey(1)

			if key == ord('q'):
				#close player
				exit()
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
				self.notify(img)
				# display(img)

	#More code inspo - https://stackoverflow.com/questions/56002672/display-an-image-over-another-image-at-a-particular-co-ordinates-in-opencv
	def displayNoti(self, screenshot, position):

		if position == "0000":
			pass
			#Do not place
		elif position == "1111":
			pass
			#Randomly pick one of the 4
		elif position == "1000":
			pass
			#top left corner
		elif position == "0100":
			pass
			#top right corner

		elif position == "0010":
			pass
			#bottom left corner

		elif position == "0001":
			pass
			#bottom right corner

		else:
			print("You done goofed.")




	def notify(self, screenshot):

		dataset_temp = PredictImageSet(
			img=screenshot,
			transform=transforms.Compose(
				[SquarifyImage(),
				RandomCrop(224),
				Normalize(),
				ToTensor()]))
		batch_size = 16
		dataloader = torch.utils.data.DataLoader(dataset_temp, batch_size=batch_size,
											num_workers=4)

		predictions = self.model.predict(dataloader)
		predictions = torch.LongTensor(predictions[0]>0.5).tolist()
		
		print(''.join(map(str, predictions)))
		
		return ''.join(map(str, predictions))



def main():

	f_names = ["test_vidz/apexLegends_fail.mp4"]

	#test 1
	player = DIVM_runner(f_names[0])
	player.runPlayer()

	#test 1
	#player = DIVM_runner(f_names[0])





if __name__ == '__main__':
	main()


