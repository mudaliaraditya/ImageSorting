#!/usr/bin/python3
from __future__ import print_function
import exifread
import os
import shutil
import logging
from datetime import datetime


class Picture:
	FileName = ""
	Date = ""
	Path = ""



now = datetime.now()
NameOfFile='applog_' + now.strftime("%d%m%Y")+'_log.txt'
logging.basicConfig(filename=NameOfFile, filemode='a', format='%(message)s')

current_time = now.strftime("%H:%M:%S")
stringtobewritteninlog = "=============================================================="
logging.warning(stringtobewritteninlog)
stringtobewritteninlog = "starting a sorting of images at time : " + str(current_time)
logging.warning(stringtobewritteninlog)

stringtobewritteninlog = "=============================================================="
logging.warning(stringtobewritteninlog)
stringtobewritteninlog = "\n"
logging.warning(stringtobewritteninlog)



RequestDialog = "Enter Image Dir : "
try:
	path = raw_input(RequestDialog)
except:
	try:
		path = input(RequestDialog)
	except Exception as err:
		exit(1)

path = os.path.join(path, '')
print(path)
files = []
UnableToSortError = []



for root_dir, ListOfDirectories, ListOfFileNames in os.walk(path):
	for file in ListOfFileNames:
		files.append(os.path.join(root_dir, file))



FinalListOfImagesToBeSorted = []

Path_Confirmation = "you have entered \'" + path + " \',Ensure its not a system path theres no way to reverse, enter y to proceed \n"
try:
	ychar = raw_input(Path_Confirmation)
except:
	try:
		ychar = input(Path_Confirmation)
	except:
		exit(1)

ychar = ychar.lower()

if not ychar == 'y':
	exit(0)

stringtobewritteninlog = "starting sorting of images in path : " + path
logging.warning(stringtobewritteninlog)
stringtobewritteninlog = "\n"
logging.warning(stringtobewritteninlog)

FileCount = 0
DirCount = 0
ImageCount = 0
ErrorCount = 0
buffer_size = 1024


for entry in  files:
	if os.path.isdir(entry):
		print("\nIt is a directory")
		DirCount = DirCount + 1
	elif os.path.isfile(entry):
		print("\nIt is a normal file")
		FileCount = FileCount + 1
		ListOfFileNames = open(str(entry), 'rb')
		try:
			print(entry)
			tags = exifread.process_file(ListOfFileNames)
			i = 0

			File = Picture()
			stringtobewritteninlog = "processed file : " + entry
			logging.warning(stringtobewritteninlog)
			for tag in tags.keys():
				if tag in ('Image DateTime'):
					File.FileName = os.path.basename(entry)
					File.Date = str(tags[tag])
					head, tail = os.path.split(entry)
					File.Path = head
					ImageCount = ImageCount + 1
					FinalListOfImagesToBeSorted.append(File)
		finally:
			ListOfFileNames.close()
	else:
		print("It is a special file (socket, FIFO, device file)")

stringtobewritteninlog = "**************************************************************"
logging.warning(stringtobewritteninlog)

for Filelist in FinalListOfImagesToBeSorted:
	datetime_object = datetime.strptime(Filelist.Date, '%Y:%m:%d %H:%M:%S')
	print(Filelist.FileName, " ", datetime_object.second, " ", datetime_object.hour, " ", datetime_object.minute)
	day = str(datetime_object.day)
	month = str(datetime_object.month)
	year = str(datetime_object.year)
	if len(day) == 1:
		day = '0' + day
	if len(month) == 1:
		month = '0' + month

	FinalStringName = path + day + month + year

	if not os.path.isdir(FinalStringName):
		os.mkdir(FinalStringName)
	FinalFile = os.path.join(FinalStringName, Filelist.FileName)
	SourceFile = os.path.join(Filelist.Path, Filelist.FileName)
	print("source file is ", SourceFile)
	print("final file is ", FinalFile)
	try:
		if not os.path.exists(FinalFile):
			stringtobewritteninlog = "copying file from " + SourceFile + " |to| "+ FinalFile
			buffer_size = max(buffer_size, os.path.getsize(SourceFile))
			if (buffer_size == 0):
				buffer_size = 1024
			logging.warning(stringtobewritteninlog)
			#shutil.copyfile(SourceFile, FinalFile)
			with open(SourceFile, 'rb') as fsrc:
				with open(FinalFile, 'wb') as fdst:
					shutil.copyfileobj(fsrc, fdst, buffer_size)
			#if (perserveFileDate):
			#shutil.copystat(SourceFile, FinalFile)
			fsrc.close()
			fdst.close()
			os.remove(SourceFile)
		else :
			raise Exception("file already present")
	except:
		print("error occured but still continuing")
		UnableToSortError.append(SourceFile)
		continue

stringtobewritteninlog = "**************************************************************"
logging.warning(stringtobewritteninlog)

if not len(UnableToSortError) == 0:
	print("The following files were not sorted because of errors")
	stringtobewritteninlog = "There were errors for sorting images in path : " + path
	logging.warning(stringtobewritteninlog)
	stringtobewritteninlog = "\n"
	logging.warning(stringtobewritteninlog)
	for i in UnableToSortError:
		stringtobewritteninlog = i
		logging.warning(stringtobewritteninlog)
		print(i)

endtime = datetime.now()
endtimestring = endtime.strftime("%H:%M:%S")

stringtobewritteninlog = "\n"
logging.warning(stringtobewritteninlog)

stringtobewritteninlog = "=============================================================="
logging.warning(stringtobewritteninlog)

stringtobewritteninlog = "Completed sorting : " + str(endtimestring)
logging.warning(stringtobewritteninlog)
stringtobewritteninlog = "=============================================================="
logging.warning(stringtobewritteninlog)
stringtobewritteninlog = "\n"
logging.warning(stringtobewritteninlog)
stringtobewritteninlog = "File Count : "+ str(FileCount)
logging.warning(stringtobewritteninlog)
stringtobewritteninlog = "Dir Count : " + str(DirCount)
logging.warning(stringtobewritteninlog)
stringtobewritteninlog = "Image with exiff Count : " + str(ImageCount)
logging.warning(stringtobewritteninlog)
stringtobewritteninlog = "Error Count : " + str(ErrorCount)
logging.warning(stringtobewritteninlog)
stringtobewritteninlog = "\n"
logging.warning(stringtobewritteninlog)
stringtobewritteninlog = "=============================================================="
logging.warning(stringtobewritteninlog)
stringtobewritteninlog = "\n"
logging.warning(stringtobewritteninlog)
try:
	path = raw_input("Press Enter to quit")
except:
	try:
		path = input("Press Enter to quit")
	except:
		exit(1)
