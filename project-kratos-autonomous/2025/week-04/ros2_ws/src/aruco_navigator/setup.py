from glob import glob
import os
from setuptools import find_packages, setup

package_name = 'aruco_navigator'
worlds_dir = os.path.join('..', '..', '..', 'worlds')

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch',
            glob('launch/*.launch.py')),
        ('share/' + package_name + '/worlds',
            glob(os.path.join(worlds_dir, '*.wbt'))),
        ('share/' + package_name + '/worlds/textures',
            glob(os.path.join(worlds_dir, 'textures', '*'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='chaitanya',
    maintainer_email='chaitanyabelekar59@gmail.com',
    description='ArUco marker detection and autonomous navigation.',
    license='Apache-2.0',
    extras_require={
        'test': ['pytest'],
    },
    entry_points={
        'console_scripts': [
            'aruco_detector = aruco_navigator.aruco_detector:main',
            'navigation_controller = aruco_navigator.navigation_controller:main',
        ],
    },
)
