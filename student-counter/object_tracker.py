# USAGE
# python object_tracker.py --prototxt deploy.prototxt --model res10_300x300_ssd_iter_140000.caffemodel

# import the necessary packages
from pyimagesearch.centroidtracker import CentroidTracker
from imutils.video import VideoStream
import numpy as np
import argparse
import imutils
import time
import cv2
import mysql.connector

class TrackableObject:
	def __init__(self, objectID, centroid):
		
		self.objectID = objectID
		self.centroids = [centroid]
		self.countedI=False
		self.countedO=False

	

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--prototxt", required=True,
	help="path to Caffe 'deploy' prototxt file")
ap.add_argument("-m", "--model", required=True,
	help="path to Caffe pre-trained model")
ap.add_argument("-c", "--confidence", type=float, default=0.5,
	help="minimum probability to filter weak detections")
args = vars(ap.parse_args())

# initialize our centroid tracker and frame dimensions
ct = CentroidTracker()
(H, W) = (None, None)

# model warming up
print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])

totalUp=0
totalDown=0
trackableObjects = {}
n=30


#camera warming up
print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
time.sleep(2.0)
ip=input("Enter database server IP:")
mydb=mysql.connector.connect(host=ip,user="raspi",password="root",database="project")
mycursor=mydb.cursor()
mycursor.execute("CREATE TABLE IF NOT EXISTS temp_body (inside VARCHAR(5), outside VARCHAR(5), bodycount Varchar(10))")
mycursor.execute("Truncate table temp_body")
mydb.commit()
# loop warna ek frame pe band ho jayega
while True:
		#Live video with resize 
	frame = vs.read()
	frame = imutils.resize(frame, width=400)

		# if the frame dimensions are None, grab them
	if W is None or H is None:
		(H, W) = frame.shape[:2]

		# construct a blob from the frame, pass it through the network,
		# obtain our output predictions, and initialize the list of
		# bounding box rectangles
	blob = cv2.dnn.blobFromImage(frame, 1.0, (W, H),
		(104.0, 177.0, 123.0))
	net.setInput(blob)
	detections = net.forward()
	rects = []

		# loop over the detections
	for i in range(0, detections.shape[2]):
		# idhar low confidence pe ignore karnega
		# probability is greater than a minimum threshold
		if detections[0, 0, i, 2] > args["confidence"]:
				# compute the (x, y)-coordinates of the bounding box for
				# the object, then update the bounding box rectangles list
			box = detections[0, 0, i, 3:7] * np.array([W, H, W, H])
			rects.append(box.astype("int"))

				#IDHAR BOX BANEGA
			(startX, startY, endX, endY) = box.astype("int")
			cv2.rectangle(frame, (startX, startY), (endX, endY),
				(0, 255, 0), 2)

		# update our centroid tracker using the computed set of bounding
		# box rectangles
	objects = ct.update(rects)
	cv2.line(frame, (W//2,0), (W//2, H), (0, 255, 255), 2)
		# loop over the tracked objects
	for (objectID, centroid) in objects.items():
			# draw both the ID of the object and the centroid of the
			# object on the output frame
		
		to = trackableObjects.get(objectID, None)

			
		if to is None:
			to = TrackableObject(objectID, centroid)

		else:
			x = [c[0] for c in to.centroids]
			direction = centroid[0] - np.mean(x)
			to.centroids.append(centroid)
			if not to.countedI:
				if direction < 0 and centroid[0] < W // 2:
					totalUp += 1
					to.countedI=True
					to.countedO=False
							
			if not to.countedO:
				if direction > 0 and centroid[0] > W // 2:
					totalDown += 1
					to.countedO=True
					to.countedI=False

			
		trackableObjects[objectID] = to
		text = "ID {}".format(objectID)
		cv2.putText(frame, text, (centroid[0] - 10, centroid[1] - 10),
			cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
		cv2.circle(frame, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)



	info = [
		("Inside Class", totalUp),
		("Outside Class", totalDown),
	]

	for (i, (k, v)) in enumerate(info):
		text = "{}: {}".format(k, v)
		cv2.putText(frame, text, (10, H - ((i * 20) + 20)),
			cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)


		
		# show the output frame
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
	if key == ord("q"):
		break

body=totalUp-totalDown-1
mycursor.execute("Insert into temp_body (inside,outside,bodycount) Values('%s','%s','%s')"%(totalUp,totalDown,body))
mydb.commit()
mycursor.execute("Update attendance set Missed=Conducted-Attended")
mydb.commit()
mycursor.execute("Update attendance set Percentage=(Attended/Conducted)*100")
mydb.commit()
mydb.close()
# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
