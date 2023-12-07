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



