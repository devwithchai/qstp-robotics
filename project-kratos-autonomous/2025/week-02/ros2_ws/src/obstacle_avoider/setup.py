from setuptools import find_packages, setup

package_name = 'obstacle_avoider'

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
    maintainer='chaitanya',
    maintainer_email='chaitanyabelekar59@gmail.com',
    description='Basic LiDAR-based obstacle avoidance for a ROS 2 robot.',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'obstacle_avoider = obstacle_avoider.obstacle_avoider:main',
        ],
    },
)
