# Main method
from vgosDBpy.argparser import CommandLineInterface

import matplotlib.pyplot as plt
import matplotlib


if __name__ == '__main__':
    plt.switch_backend('Qt5Agg')
    plt.ion()
    interface = CommandLineInterface()
