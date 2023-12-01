# rtc2
Ruhr Turtlebot Competition mit ROS2

# installation
erstelle den Ordner  ~/turtlebot3_ws/src
  $ cd ~
  $ mkdir turtlebot3_ws
  $ cd turtlebot3_ws
  $ mkdir src
  $ cd src

clone rtc2 dorthin
  $ git clone https://github.com/ProfJust/rtc2
  

mache step1....sh und step2....sh ausführbar
und führe sie aus

$ cd ~/turtlebot3_ws/src
$ ./step1...
$ ./step2...

# usage
to be done



# nano ~/.bashrc

In der .bashrc muss folgendes stehen (realBot)
 => Gazebo mit mehreren Tln in einem Netz:  export ROS_LOCALHOST_ONLY=1  

export ROS_DOMAIN_ID=30 #TURTLEBOT3
export TURTLEBOT3_MODEL=burger
export ROS_LOCALHOST_ONLY=0  # 0 = Communication allowed
# this environment variable allows you to limit ROS 2 communication to localhost only.
source /opt/ros/humble/setup.bash
source ~/turtlebot3_ws/install/setup.bash


# ======= RASPICAM on TB3 ==================
# -- install Raspicam Driver for ROS2 on TB3
tB3 $ sudo apt-get install ros-${ROS_DISTRO}-v4l2-camera

tB3 $ sudo nano /boot/firmware/config.txt
	=> Set   camera_autodetect=0	
	   Add   start_x=1

tB3 $ reboot

$ sudo apt install v4l-utils
# --Check correct driver
	tB3 $ v4l2-ctl -D
	Driver Info:
		Driver name      : bm2835 mmal
		...

# -- welche Videos sind vorhanden?  => index:=0 ?
  ls /dev/video*

# -- Start für video0 (default)
 $ ros2 run v4l2_camera v4l2_camera_node

# -- ggf. Start mit Parametern
  https://docs.ros.org/en/foxy/How-To-Guides/Node-arguments.html
 $ ros2 run v4l2_camera v4l2_camera_node --ros-args -p video_device:=/dev/video14

===>>> Kamera läuft !!!
ubuntu@ubuntu:~$ ros2 run v4l2_camera v4l2_camera_node
[INFO] [1701420711.342873481] [v4l2_camera]: Driver: bm2835 mmal
[INFO] [1701420711.343465837] [v4l2_camera]: Version: 331646
[INFO] [1701420711.343552205] [v4l2_camera]: Device: mmal service 16.1
[INFO] [1701420711.343649925] [v4l2_camera]: Location: platform:bcm2835-v4l2-0
[INFO] [1701420711.343702683] [v4l2_camera]: Capabilities:
[INFO] [1701420711.343785348] [v4l2_camera]:   Read/write: YES
[INFO] [1701420711.343863531] [v4l2_camera]:   Streaming: YES
[INFO] [1701420711.343933159] [v4l2_camera]: Current pixel format: JPEG @ 1024x768
[INFO] [1701420711.345048356] [v4l2_camera]: Available pixel formats: 
[INFO] [1701420711.345108669] [v4l2_camera]:   YU12 - Planar YUV 4:2:0
[INFO] [1701420711.345161075] [v4l2_camera]:   YUYV - YUYV 4:2:2
[INFO] [1701420711.345209852] [v4l2_camera]:   RGB3 - 24-bit RGB 8-8-8
[INFO] [1701420711.345255499] [v4l2_camera]:   JPEG - JFIF JPEG
[INFO] [1701420711.345302461] [v4l2_camera]:   H264 - H.264
[INFO] [1701420711.345348367] [v4l2_camera]:   MJPG - Motion-JPEG
[INFO] [1701420711.345394107] [v4l2_camera]:   YVYU - YVYU 4:2:2
[INFO] [1701420711.345440550] [v4l2_camera]:   VYUY - VYUY 4:2:2
[INFO] [1701420711.345485919] [v4l2_camera]:   UYVY - UYVY 4:2:2
[INFO] [1701420711.345534789] [v4l2_camera]:   NV12 - Y/CbCr 4:2:0
[INFO] [1701420711.345583436] [v4l2_camera]:   BGR3 - 24-bit BGR 8-8-8
[INFO] [1701420711.345629768] [v4l2_camera]:   YV12 - Planar YVU 4:2:0
[INFO] [1701420711.345674711] [v4l2_camera]:   NV21 - Y/CrCb 4:2:0
[INFO] [1701420711.345749117] [v4l2_camera]:   RX24 - 32-bit XBGR 8-8-8-8

=== Remote PC ===
 $ ros2 topic list
 $ rqt
   Bild anzeigen mit Plugin Image_View   Topic /image_raw   


 Kamaera Calibration (auf dem Remote PC)
 ros2 run camera_calibration cameracalibrator \
  --size=8x6 \
  --square=0.063 \
  --approximate=0.3 \
  --no-service-check \
  --ros-args --remap /image:=/image_raw








####################### ALTER KRAM #####################

					# Error Faile Stream start =>
					sudo apt install v4l2loopback-dkms
					sudo modprobe v4l2loopback



					#usage
					ubuntu@ubuntu:~$ ros2 run v4l2_camera v4l2_camera_node

					=>ERROR Wrong Pixel Format use Param.file


					$ v4l2-ctl -d /dev/video0 --all
					ubuntu@ubuntu:~$ v4l2-ctl -d /dev/video0 --all
					Driver Info:
						Driver name      : v4l2 loopback
						Card type        : Dummy video device (0x0000)
						Bus info         : platform:v4l2loopback-000
						Driver version   : 5.15.116
						Capabilities     : 0x85200003
							Video Capture
							Video Output
							Read/Write
							Streaming
							Extended Pix Format
							Device Capabilities
						Device Caps      : 0x05200003
							Video Capture
						# install Raspicam Driver for ROS2 on TB3
					$ sudo apt-get install ros-${ROS_DISTRO}-v4l2-camera

					$ sudo nano /boot/firmware/config.txt
					=> Set   camera_autodetect=0

					$ sudo apt install v4l-utils
					$ v4l2-ctl -D

					# Error Faile Stream start =>
					sudo apt install v4l2loopback-dkms
					sudo modprobe v4l2loopback



					#usage
					ubuntu@ubuntu:~$ ros2 run v4l2_camera v4l2_camera_node

					=>ERROR Wrong Pixel Format use Param.file


					$ v4l2-ctl -d /dev/video0 --all
					ubuntu@ubuntu:~$ v4l2-ctl -d /dev/video0 --all
					Driver Info:
							Video Output
							Read/Write
							Streaming
							Extended Pix Format
					Priority: 2
					Video input : 0 (loopback: ok)
					Video output: 0 (loopback in)
					Format Video Output:
						Width/Height      : 0/0
						Pixel Format      : 'BGR4' (32-bit BGRA/X 8-8-8-8)
						Field             : None
						Bytes per Line    : 0
						Size Image        : 0
						Colorspace        : sRGB
						Transfer Function : Default (maps to sRGB)
						YCbCr/HSV Encoding: Default (maps to ITU-R 601)
						Quantization      : Default (maps to Full Range)
						Flags             : 
					Streaming Parameters Video Capture:
						Frames per second: 30.000 (30/1)
						Read buffers     : 2
					Streaming Parameters Video Output:
						Frames per second: 30.000 (30/1)
						Write buffers    : 2

					User Controls

										keep_format 0x0098f900 (bool)   : default=0 value=0
								sustain_framerate 0x0098f901 (bool)   : default=0 value=0
											timeout 0x0098f902 (int)    : min=0 max=100000 step=1 default=0 value=0
								timeout_image_io 0x0098f903 (bool)   : 
								
					$ ros2 run v4l2_camera v4l2_camera_node -ros-args --params-file /home/ubuntu/ros2ws/v4l2_camera_params.yaml


					ros2 run v4l2_camera v4l2_camera_node  -ros-args --params-file /home/ubuntu/v4l2_camera_params.yaml



##################### Install opencv_cam Driver #####################
see https://jeffzzq.medium.com/ros2-image-pipeline-tutorial-3b18903e7329

=== TB3 ===
 # Install openCV
  $ sudo apt update
  $ sudo apt dist-upgrade    # dauert 20 Minuten
  $ sudo apt install libopencv-dev python3-opencv
  $ export OpenCV_DIR=/usr/share/OpenCV

 # Humble Version, sonst kompiliert es nicht
  cd turtlebot3_ws/src
  # git clone -b humble https://github.com/ros-perception/image_pipeline.git
  # git clone -b humble https://github.com/ros-perception/image_common.git

  # ==>> since colcon build has errors use apt packages
  sudo apt install ros-humble-image-pipeline
  sudo apt install ros-humble-image-common
  
  # no apt packages available
  git clone https://github.com/ptrmu/ros2_shared.git
  git clone https://github.com/clydemcqueen/opencv_cam.git

  cd turtlebot3_ws
  colcon build --parallel-workers 1      # ohne symlink  funktioniert es
  . install/setup.bash

	# causes Error with colcon build --symlink-install --parallel-workers 1
	# fatal error: camera_c
#---
 
 # welche Videos sind vorhanden?  => index:=0 ?
  ls /dev/video*

  => viedeo10, 11,...18,20,...23,32


  ros2 run opencv_cam opencv_cam_main --ros-args --param index:=0
  => [opencv_cam]: cannot open device 0

  ros2 run opencv_cam opencv_cam_main --ros-args --param index:=14
  => 
	ubuntu@ubuntu:~$ ros2 run opencv_cam opencv_cam_main --ros-args --param index:=14
[INFO] [1701418458.583778888] [opencv_cam]: use_intra_process_comms=1
[INFO] [1701418458.584824433] [opencv_cam]: opencv_cam Parameters
camera_frame_id = camera_frame
camera_info_path = info.ini
file = false
filename = 
fps = 0
height = 0
index = 14
width = 0
[INFO] [1701418458.585187263] [opencv_cam]: OpenCV version 4
[ WARN:0] global ./modules/videoio/src/cap_gstreamer.cpp (616) isPipelinePlaying OpenCV | GStreamer warning: GStreamer: pipeline have not been created
[ WARN:0] global ./modules/videoio/src/cap_v4l.cpp (1911) getProperty VIDEOIO(V4L2:/dev/video14): Unable to get camera FPS
[INFO] [1701418458.597158868] [opencv_cam]: device 14 open, width 640, height 480, device fps -1


Hier fehlt die Kamera-Calibration
[ERROR] [1701418458.597437680] [camera_calibration_parsers]: Failed to detect content in .ini file
[ERROR] [1701418458.597491642] [opencv_cam]: cannot get camera info, will not publish
[INFO] [1701418458.611173434] [opencv_cam]: start publishing
[ WARN:1] global ./modules/videoio/src/cap_v4l.cpp (1001) tryIoctl VIDEOIO(V4L2:/dev/video14): select() timeout.
[INFO] [1701418468.624567662] [opencv_cam]: EOF, stop publishing




=== Remote PC ===
 $ ros2 topic list
 $ ros2 run image_view image_view --ros-args --remap /image:=/image_raw



 Kamaera Calibration (auf dem Remote PC)
 ros2 run camera_calibration cameracalibrator \
  --size=8x6 \
  --square=0.063 \
  --approximate=0.3 \
  --no-service-check \
  --ros-args --remap /image:=/image_raw


  VERSION2
  ==================================================================
  https://gitlab.com/boldhearts/ros2_v4l2_camera
  sudo apt-get install ros-${ROS_DISTRO}-v4l2-camera

  ros2 run v4l2_camera v4l2_camera_node
  => Failed opening device /dev/video0: No such file or directory (2)

  ros2 run v4l2_camera v4l2_camera_node --ros-args -video_device:="/dev/video14"
  found unknown ROS arguments: '-video_device:=/dev/video14'

so geht es mit Parametern
https://docs.ros.org/en/foxy/How-To-Guides/Node-arguments.html
  ros2 run v4l2_camera v4l2_camera_node --ros-args -p video_device:=/dev/video14

  ros2 run v4l2_camera v4l2_camera_node --ros-args -p video_device:=/dev/video14
[INFO] [1701419937.399904184] [v4l2_camera]: Driver: bcm2835-isp
[INFO] [1701419937.400450660] [v4l2_camera]: Version: 331646
[INFO] [1701419937.400523567] [v4l2_camera]: Device: bcm2835-isp
[INFO] [1701419937.400577270] [v4l2_camera]: Location: platform:bcm2835-isp
[INFO] [1701419937.400621232] [v4l2_camera]: Capabilities:
[INFO] [1701419937.400663325] [v4l2_camera]:   Read/write: NO
[INFO] [1701419937.400704158] [v4l2_camera]:   Streaming: YES
[INFO] [1701419937.400761453] [v4l2_camera]: Current pixel format: BGR3 @ 2560x1440
[INFO] [1701419937.400978173] [v4l2_camera]: Available pixel formats: 
[INFO] [1701419937.401023858] [v4l2_camera]:   YUYV - YUYV 4:2:2
[INFO] [1701419937.401062543] [v4l2_camera]:   YVYU - YVYU 4:2:2
[INFO] [1701419937.401100005] [v4l2_camera]:   VYUY - VYUY 4:2:2
[INFO] [1701419937.401137671] [v4l2_camera]:   UYVY - UYVY 4:2:2
[INFO] [1701419937.401174541] [v4l2_camera]:   YU12 - Planar YUV 4:2:0
[INFO] [1701419937.401211782] [v4l2_camera]:   YV12 - Planar YVU 4:2:0
[INFO] [1701419937.401263855] [v4l2_camera]:   RGB3 - 24-bit RGB 8-8-8
[INFO] [1701419937.401305207] [v4l2_camera]:   BGR3 - 24-bit BGR 8-8-8
[INFO] [1701419937.401344892] [v4l2_camera]:   XB24 - 32-bit RGBX 8-8-8-8
[INFO] [1701419937.401381724] [v4l2_camera]:   XR24 - 32-bit BGRX 8-8-8-8
[INFO] [1701419937.401417094] [v4l2_camera]:   RGBP - 16-bit RGB 5-6-5
[INFO] [1701419937.401451576] [v4l2_camera]:   NV12 - Y/CbCr 4:2:0
[INFO] [1701419937.401488094] [v4l2_camera]:   NV21 - Y/CrCb 4:2:0
[INFO] [1701419937.401523390] [v4l2_camera]: Available controls: 
[INFO] [1701419937.402953245] [v4l2_camera]: Requesting format: 2560x1440 YUYV
[INFO] [1701419937.403281871] [v4l2_camera]: Success
[INFO] [1701419937.403348704] [v4l2_camera]: Requesting format: 640x480 YUYV
[INFO] [1701419937.403546350] [v4l2_camera]: Success
[INFO] [1701419937.404598468] [v4l2_camera]: Starting camera

https://www.raspberrypi.com/documentation/computers/config_txt.html
TB3 $ sudo nano /boot/firmware/config.txt

	camera_auto_detect=0
	start_x=1

$ reboot

ubuntu@ubuntu:~$ v4l2-ctl -D
Driver Info:
	Driver name      : bm2835 mmal
	Card type        : mmal service 16.1
	Bus info         : platform:bcm2835-v4l2-0
	Driver version   : 5.15.126
	Capabilities     : 0x85200005
		Video Capture
		Video Overlay
		Read/Write
		Streaming
		Extended Pix Format
		Device Capabilities
	Device Caps      : 0x05200005
		Video Capture
		Video Overlay
		Read/Write
		Streaming
		Extended Pix Format


$ ls /dev/video*
/dev/video0   /dev/video11  /dev/...

$ ros2 run v4l2_camera v4l2_camera_node

=> läuft!!!

oj@RosePC:~$ ros2 topic list
/camera_info
/image_raw
/parameter_events
/rosout

$ rqt   Plugin Image View  /image_raw
