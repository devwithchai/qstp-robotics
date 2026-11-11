from setuptools import find_packages, setup

package_name = 'coordinate_follower'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/config',
            ['config/coordinates.txt']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='chaitanya',
    maintainer_email='chaitanyabelekar59@gmail.com',
    description='ROS 2 action-based coordinate follower.',
    license='Apache-2.0',
    extras_require={
        'test': ['pytest'],
    },
    entry_points={
        'console_scripts': [
            'coordinate_action_server = coordinate_follower.coordinate_action_server:main',
            'coordinate_sequence_client = coordinate_follower.coordinate_sequence_client:main',
        ],
    },
)
