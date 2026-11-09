from setuptools import find_packages, setup

package_name = 'week2_assignments'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=('test', 'test.*')),
    data_files=[
        (
            'share/ament_index/resource_index/packages',
            ['resource/' + package_name],
        ),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Chaitanya Belekar',
    maintainer_email='chaitanyabelekar59@gmail.com',
    description='ROS 2 TurtleBot keyboard control and obstacle-stop exercises.',
    license='Unspecified',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'keyboard_control = week2_assignments.keyboard_control:main',
            'turtlebot_controller = week2_assignments.turtlebot_controller:main',
        ],
    },
)
