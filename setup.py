from setuptools import find_packages, setup

package_name = 'rtc2'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='oj',
    maintainer_email='olaf.just@w-hs.de',
    description='Ruhr TurtleBot Competition using ROS2 and turtlebot3',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        # hier alle Pythons Scripte eintragen, die übersetzt werden sollen 
        #  Bezeichner zum starten mit ros2 run  =  
        #              Name des Files (ohne py) : Funktion die starten soll 
        'say_temp= rtc2.pub_temp:main',
        # 'min_pub= rtc2.publisher_member_function:main',
        'talk= rtc2.talker:main',
        'listen= rtc2.listener:main',
        'move_turtlesim= rtc2.move_turtle:main'
        ],
    },
)
