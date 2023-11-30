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
  
				# causes Error with colcon build --symlink-install --parallel-workers 1
				# fatal error: camera_calibration_parsers/parse.hpp: No such file or directory
				# unter /opt/ros/humble/include/camera_calibration_parsers/camera_calibration_parsers
				# liegt die Datei
				# => Pfade setzen, wie ?
				# ? PATH=PATH:"/opt/ros/humble/include/camera_calibration_parsers/camera_calibration_parsers"

				CMAKE_PREFIX_PATH=/home/ubuntu/turtlebot3_ws/install/turtlebot3_bringup:/home/ubuntu/turtlebot3_ws/install/turtlebot3_node:/home/ubuntu/turtlebot3_ws/install/turtlebot3_description:/home/ubuntu/turtlebot3_ws/install/tracetools_image_pipeline:/home/ubuntu/turtlebot3_ws/install/ros2_shared:/home/ubuntu/turtlebot3_ws/install/my_tb3_launcher:/home/ubuntu/turtlebot3_ws/install/ld08_driver:/home/ubuntu/turtlebot3_ws/install/image_transport:/home/ubuntu/turtlebot3_ws/install/camera_info_manager:/home/ubuntu/turtlebot3_ws/install/camera_calibration_parsers:/opt/ros/humble/include/camera_calibration_parsers/camera_calibration_parsers

  git clone https://github.com/clydemcqueen/opencv_cam.git

  cd turtlebot3_ws
  colcon build    # ohne symlink und parralel funktioniert es
  . install/setup.bash
 
 # welche Videos sinv vorhanden?  => index:=0 ?
  ls /dev/video*

  => keine camera dran


  ros2 run opencv_cam opencv_cam_main --ros-args --param index:=0
  => [opencv_cam]: cannot open device 0



=== Remote PC ===
 $ ros2 topic list
 $ ros2 run image_view image_view --ros-args --remap /image:=/image_raw