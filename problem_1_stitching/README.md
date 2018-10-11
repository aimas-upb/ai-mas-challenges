# Image stitching challenge

We are developing software for autonomous vehicles that rely on vision systems to navigate 
through their environment. We have multiple cameras and test different setup positions. Labeled 
data plays a critical role in training current machine learning systems, thus we are faced with 
very time-consuming task that we would want to make as efficient as possible.

Can you develop an efficient 'image stitching' tool that can be configured for multiple camera 
streams to merge the image streams in one single (bigger) image stream. Having the single image 
view and the coordinate transforms from the fused_image <-> individual_camera_stream can help us 
discard labeling duplicate image zones.

Example of a fused image result from multiple camera feeds can be seen in 
`image_stitching_example.jpeg`. (source http://daeyunshin.com).

Good luck using your computer vision skills!


## Submission Format
An easy to use & configure tool for video stitching. 

Script should get as input multiple video files +/ a configuration file (If setup previously 
configured).

The script should be able to output a video with a panoramic view of all the streams stitched 
together and the conversion methods for coordinate transforms (from panoramic view coord -> video_x 
coordinate).

**Send us instructions on how to test your tool on the provided tests & 4 different stitched 
image examples.**

## Running the tests

You can test your tool on the the data provided in folder data_1 and data_2.

Think about the problems that you may encounter, such as:
* Different video FPS format
* Different video resolutions
