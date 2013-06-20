<h1>JPEG-Recover</h1>
<p>A small Python program for recovering JPEG images from an accidentally erased/damaged memory card</p>
<br/>
<h3>How It Works</h3>
<p>The program takes as its input a given disk image file. In order to recover photos from a memory card, you will first have to make a disk image of that memory card. Methods for doing this vary across systems. On Mac OSX, you can insert the memory card into the computer and then open the Disk Utility application. Create a new Disk Image from the memory card. Make sure that you are not using any kind of compression -- we need this to be a straight copy of the bytes.<p>
<br/>
<h3>How to Run</h3>
<p>Place the script and the disk image in a directory where you want the photos to go. Open a Terminal window (the Terminal application on Mac OSX) and navigate to that directory using <pre>cd</pre></p>
<p>type the following command:</p>
<pre>python jpegrecover2.py</pre>
<p>You will then be asked to provide the filename for the disk image file, followed by a "prefix" for recovered images. What does this mean? Let's say I choose "recovered" as my prefix. As the images are written, each file will have "recovered" followed by a number as its filename. That's all it means.</p>
<br/>
<h4>NOTE</h4>
<p><pre>jpegrecover2.py</pre> is recommended for use, as it's the latest and best refactored version of the program. The old file is there only temporarily.</p>
