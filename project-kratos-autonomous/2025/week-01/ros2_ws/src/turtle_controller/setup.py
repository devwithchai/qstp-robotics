from setuptools import setup

package_name = 'turtle_controller'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Chaitanya Belekar',
    maintainer_email='157277524+devwithchai@users.noreply.github.com',
    description='Beginner-friendly TurtleBot velocity controller',
    license='MIT',
    entry_points={
        'console_scripts': [
            'move_in_circle = turtle_controller.move_in_circle:main',
        ],
    },
)
