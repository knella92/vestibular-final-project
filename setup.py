
##############################################################################################################################
###  BEGIN SAMPLED CODE taken from https://docs.ros.org/en/api/catkin/html/howto/format2/installing_python.html 10/21/2021 ###
##############################################################################################################################

from setuptools import setup
from catkin_pkg.python_setup import generate_distutils_setup
setup_args = generate_distutils_setup(
    packages=['plotter', 'board_pid','planner', 'maze_solve'],
    package_dir={'':'src'}
)

setup(**setup_args)

##############################################################################################################################
###  END SAMPLED CODE                                                                                                      ###
##############################################################################################################################