# License:  This  program  is  free  software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the  Free Software Foundation; either version 3 of the License, or (at your
# option)  any later version. This program is distributed in the hope that it
# will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
# Public License for more details.


# Set global constants
BLOCK = 16
IMG_BLOCK = 512 # This is standard for JPEGS on camera memory cards
img_count = 0

def main():

	# Get the name of the image file and the name for files to write
	filename = raw_input('What is the name of the disc image file? ')
	newfilename = raw_input('What Prefix would you like to use as names of recovered images? ')

	# Try opening the file
	try:
		file = open(filename, 'rb')
	except IOError:
		'The image file ' + filename + ' does not exist or is too corrupt to open'
	else:
		'The file ' + filename + ' loaded successfully!'

	# Use the global variables in main()
	global IMG_BLOCK
	global img_count
	global BLOCK

	print '===================='
	print ' Scanning for files '
	print '===================='

	# Read the first BLOCK bytes, then start the loop
	data = file.read(BLOCK)
	while(data != ''):
		location = findHeaders(data)
		relative_location = location - BLOCK + file.tell() # Because BLOCK bytes have been read and the file is file.read() bytes into the file, we need to adjust
		if location >= 0:
			print 'Header located at byte ' + str(relative_location) 
			writeImage(file, relative_location, newfilename)
			img_count = img_count + 1
		data = file.read(BLOCK)
		if img_count > 10:
			break
	print ' '
	print '===================='
	print ' Recovered ' + str(img_count) + ' images.'
	print '===================='		
	file.close()

def findHeaders(data):
	length = len(data)

	# Loop through each byte of the data and see if any JPEG headers are found
	for i in range(0, length - 3):
		if data[i] == '\xff':
			if data[i+1:i+4] == '\xd8\xff\xe0' or data[i+1:i+4] == '\xd8\xff\xe1':
				return i
	return -1

def findTermination(data):
	length = len(data)

	# Loop through each byte to see if there is a termination header
	for i in range(0, length - 1):
		if data[i] == '\xff' and data[i+1] == '\xd9':
			print 'Termination byte pattern found!'
			return i + 1
	return -1				

def writeImage(file, location, newfilename):
	
	# First, adjust the file reader to the correct location
	file.seek(location)

	global IMG_BLOCK # Use the global constant for writing image blocks
	global img_count
	name = newfilename + 'image%03d.jpg' % img_count

	# Try to open the file for writing
	try:
		writefile = open(name, 'wb')
	except IOError:
		'There was an error opening the image file ' + name + ' for writing!'

	# Loop through IMG_BLOCKS and write them until a) end of the overall disk image file is reached, b) a new JPEG header is found, c) a termination header is found
	data = file.read(IMG_BLOCK)
	while(True):
		writefile.write(data)
		data = file.read(IMG_BLOCK)
		location = findHeaders(data)
		termination = findTermination(data)

		if location >= 0:
			break
		elif termination >= 0:
			break
		elif data == '':
			break

	file.seek(file.tell() - IMG_BLOCK) # Reset the file header minus one block
	writefile.close() # Always make sure to close a file when done with it!
	print 'Successfully wrote ' + name
	#file.seek(file.tell() - IMG_BLOCK) # Set the file reader to a location minus a full IMG_BLOCK from where it last finished reading, so we can scan for new headers					


if __name__ == '__main__':
		main()