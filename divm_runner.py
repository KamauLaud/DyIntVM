#
#Author: Cory Ilo
#
#

import sys
import cv2
import random
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

		self.notif_imgs = []
		self.notif_imgs.append( cv2.resize( cv2.imread('discord_noti1.png'), (500,300), interpolation = cv2.INTER_AREA))
		self.notif_imgs.append( cv2.resize( cv2.imread('discord_noti2.png'), (500,300), interpolation = cv2.INTER_AREA))
		self.notif_imgs.append( cv2.resize( cv2.imread('discord_noti3.png'), (500,300), interpolation = cv2.INTER_AREA))
		#self.noDisplay = cv2.imread("noDisplay.jpg")

		self.isPlaying = False 
		# self.model = AlexNet(n_classes=4, device=device)
		# self.model.load_state_dict(torch.load('saved_model/alexnet.pth'))
		map_location = "cuda" if torch.cuda.is_available() else "cpu"
		self.model = torch.load('saved_model/alexnet.pth',map_location=map_location)
		self.model.device = "cuda" if torch.cuda.is_available() else "cpu"

	def __del__(self):
		self.vid.release()
		cv2.destroyAllWindows()

	# More code inspo - https://stackoverflow.com/questions/56002672/display-an-image-over-another-image-at-a-particular-co-ordinates-in-opencv
	# Grid in opencv - https://towardsdatascience.com/image-geometric-transformation-in-numpy-and-opencv-936f5cd1d315
	def displayNoti(self, screenshot):

		#pause screen
		cv2.waitKey(-1)
		noti_img = random.choice(self.notif_imgs)
		tmp_img = screenshot.copy()

		width = screenshot.shape[0]
		height = screenshot.shape[1]
		print("image size w,h: " + str(width) + ", " + str(height))
		print("tmp w,h: " + str(tmp_img.shape[0]) + ", " + str(tmp_img.shape[1]))
		position = self.notify(screenshot)
		# position = "1111"
		if position == "1111":
			#place randomly
			position = random.choice(["1000","0100","0010","0001"])

		if position == "0000":
			pass
			#Do not place
		elif position == "1000":
			#top left corner
			tmp_img[0:300, 0:500,:] = noti_img

		elif position == "0100":
			#top right corner
			tmp_img[0:300, height-500:height,:] = noti_img

		elif position == "0010":
			#bottom left corner
			tmp_img[width-300:width, 0:500:,:] = noti_img

		elif position == "0001":
			#bottom right corner
			tmp_img[width-300:width, height-500:height,:] = noti_img
            
		else:
			print("You done goofed.")

		cv2.imshow("DIVM Demo", tmp_img)
		#relase screen and wait for key press
		cv2.waitKey(0)

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

	# Code inspired by -  https://stackoverflow.com/questions/38064777/use-waitkey-in-order-pause-and-play-video
	def runPlayer(self):
		isPlaying = True
		while self.vid.isOpened():
			ret, img =  self.vid.read()

			cv2.imshow("DIVM Demo", img)
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
				##notify(img)
				self.displayNoti(img)

def main():

	file_name = sys.argv[1]
	f_names = ["test_vidz/"+file_name+".mp4"]
	print(f_names)

	#test 1
	player = DIVM_runner(f_names[0])
	player.runPlayer()

	#for i in range(len(player.notif_imgs)):
	#	cv2.imshow("DIVM Demo", player.notif_imgs[i])
	#	print(player.notif_imgs[i].shape)
	#	cv2.waitKey(-1)
	#test 1
	#player = DIVM_runner(f_names[0])

if __name__ == '__main__':
	main()


