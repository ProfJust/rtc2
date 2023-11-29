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
sudo apt-get install ros-${ROS_DISTRO}-v4l2-camera
sudo nano /boot/firmware/config.txt
   => Set   camera_autodetect=0
sudo apt install v4l-utils
v4l2-ctl -D


sudo apt install v4l2loopback-dkms
sudo modprobe v4l2loopback

#usage
ubuntu@ubuntu:~$ ros2 run v4l2_camera v4l2_camera_node

=> Wrong Pixel Format use Param.file


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
               timeout_image_io 0x0098f903 (bool)   : default=0 value=0
