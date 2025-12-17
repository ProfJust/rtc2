    printf "Install ROS2Jazyy auf Ubuntu Noble"
    timedatectl set-local-rtc 1 # Konfiguriert die Hardwareuhr auf lokale Zeit

    cd ~
    mkdir turtlebot3_ws
    cd turtlebot3_ws/
    mkdir src
    cd src
    sudo apt install git
    git clone https://github.com/ProfJust/rtc2.git   # -b jazzy_branch
    locale  # check for UTF-8
    sudo apt update && sudo apt install locales
    sudo apt install software-properties-common -y
    sudo add-apt-repository universe -y
    sudo apt update && sudo apt install curl -y
    export ROS_APT_SOURCE_VERSION=$(curl -s https://api.github.com/repos/ros-infrastructure/ros-apt-source/releases/latest | grep -F "tag_name" | awk -F\" '{print $4}')
    curl -L -o /tmp/ros2-apt-source.deb "https://github.com/ros-infrastructure/ros-apt-source/releases/download/${ROS_APT_SOURCE_VERSION}/ros2-apt-source_${ROS_APT_SOURCE_VERSION}.$(. /etc/os-release && echo $VERSION_CODENAME)_all.deb" # If using Ubuntu derivates use $UBUNTU_CODENAME
    sudo dpkg -i /tmp/ros2-apt-source.deb
    sudo apt update && sudo apt install ros-dev-tools
    sudo apt update
    sudo apt upgrade
    sudo apt install ros-jazzy-desktop -y
    sudo apt install ros-jazzy-ros-gz-sim -y
    sudo apt install gedit -y
    source /opt/ros/jazzy/setup.bash
    ###### VS - Code ####
    # wget -P ~/Downloads https://code.visualstudio.com/assets/icons/download.svg
    wget -O ~/Downloads/code.deb https://code.visualstudio.com/sha/download?build=stable&os=linux-deb-x64
    #cd ~/Download
    #sudo apt install ./code_1.107.0-1765353552_amd64.deb #ggf. ändert sich der Name des Files
    sudo apt install ~/Downloads/code.deb
    code  # startet Visual Studio Code

   