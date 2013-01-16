#Globals and Constants
BLOCK = 16
IMG_BLOCK = 512
img_count = 0


def main():

	#Get the filename and try to open it
	filename = raw_input('What is the name of the file/directory? ')
	newfilename = raw_input('Where would you like to put the recovered photos?')

	try:
		file = open(filename, 'rb')
	except IOError:
		print 'File does not exist or is corrupt.'
	else:
		print 'The file [' + filename + '] loaded successfully.'
	
	global BLOCK
	global img_count
	location = checkHeader(file, BLOCK)
	if location >= 0:
		print 'A header has been located at byte [' + str(file.tell()) + ']'
		getImages(file, location, newfilename)
		file.close()
		print '==============='
		print str(img_count) + ' images were recovered.'
		print '==============='
	else:
		print '==============='
		print 'No JPEG image headers were found.'
		print '==============='	



# Loop through blocks of the file to find the first image header. Return False if nothing is found.
def checkHeader(file, SIZE):
	data = file.read(SIZE)
	while (data != ''):
		if hasHeader(data):
			tell = file.tell()
			return locateHeader(data, tell)
		data = file.read(SIZE)
	return -1	

# Simple boolean function for finding the header
def hasHeader(data):
	for i in range(len(data)-3):
		if data[i] == '\xff':
				if data[i+1:i+4] == '\xd8\xff\xe0' or data[i+1:i+4] == '\xd8\xff\xe1':
					return True
	return False							

# Calculates the location of the header in respect to the whole file buffer (in bytes). Returns -1 or -2 in there is no header.
def locateHeader(data, tell):
	header1 = data.find('\xff\xd8\xff\xe0')
	header2 = data.find('\xff\xd8\xff\xe1')
	global BLOCK

	if header1 < 0 and header2 < 0:
		return -1
	elif header1 < 0:
		return tell - BLOCK + header2
	elif header2 < 0:
		return tell - BLOCK + header1
	else:
		return -2


def getImages(file, location, newfilename):
	global IMG_BLOCK
	file.seek(location)

	while(True):
		if writeImage(file, newfilename):
			break



def writeImage(file, newfilename):
	global img_count
	global IMG_BLOCK
	name = newfilename + 'image%03d.jpg' % img_count
	

	try:
		newfile = open(name, 'wb')
	except IOError:
		'There was an error while attempting to write [' + name + ']'
	
	# Loop through the IMG_BLOCKs and write to new file
	data = file.read(IMG_BLOCK)
	while(True):
		newfile.write(data)
		data = file.read(IMG_BLOCK)
		if data == '':
			break
		elif hasHeader(data[:10]):
			break	
	
	newfile.close()
	print name + ' was successfully created.'
	img_count = img_count + 1		

	#If EOF not reached, set the head to the next image header location		
	if data != '':
		position = file.tell() - IMG_BLOCK
		file.seek(position)
		return False
	else:
		return True						
					


if __name__ == '__main__':
	main()