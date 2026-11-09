from setuptools import find_packages, setup

package_name = 'week3_assignment'

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
    install_requires=['setuptools', 'numpy'],
    zip_safe=True,
    maintainer='Chaitanya Belekar',
    maintainer_email='chaitanyabelekar59@gmail.com',
    description='QSTP 2024 Week 3 path planning and PID controller exercises.',
    license='Unspecified',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'pid_controller = week3_assignment.pid_controller:main',
        ],
    },
)
