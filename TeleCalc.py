# This program will calculate telescope and eyepiece combinations. Lists
# of different eyepieces can be compared on different telescopes. The
# results can be printed to show magnification and actual field of view
# for each combination
#
# Written by Olivia Maynard and Jason Maynard 2015
#
# Input: There are 2 separate input files required. "tele_input.txt" for
# telescope input. Multiple telescopes are are allowed. Each telescope has a
# name, aperture (in), and length (mm). "eye_input.txt" allows for multiple
# eyepieces each with a name, apparent field of view, and focal length (mm).
#
# Sample output (written to "output.txt"):  xxx

# DATA STRUCTURES ------------------------------------------------------------------------------------------------------


def convert_length(n, unit):
    """

    :param n:
    :param unit:
    :return:
    """
    if unit == "in":
        return int(n) / 0.039370
    elif unit == "mm":
        return int(n) / 25.4
    else:
        print "Error: Please enter units in the following format \"in\" or \"mm\". "
        return -1


class Telescope:
    """
    This is the telescope class
    Attributes:
        name
        aperture
        focalLength

    Methods:
        getName
        getAperture
        getFocalLength
        getFocalRatio
        getResolution
        getMaxMag
        getMinMag
        getLongestUsefulEyepiece
        getShortestUsefulEyepiece
    """

    def __init__(self, my_name, telescope_aperture, l):
        self.name = my_name
        self.aperture = float(convert_length(telescope_aperture, "in"))
        self.l = float(l)

    def get_name(self):
        return self.name

    def get_aperture(self):
        return self.aperture

    def get_length(self):
        return self.l

    def get_focal_ratio(self):
        return self.l / self.aperture

    def get_resolution(self):
        """
        This function will return the resolution of the telescope, which is the smallest angle in arc seconds the
        telescope can see.
        :return:
        """
        return 120 / self.aperture

    def get_longest_useful_eyepiece(self):
        """
        This function returns the biggest eyepiece you can use on this telescope.
        :return:
        """
        return 7 * self.get_focal_ratio()

    def get_shortest_useful_eyepiece(self):
        """
        This function will return the shortest useful eyepiece you can use in this telescope.
        :return:
        """
        # print "\nDEBUGGING"
        # print '\nget focal ratio', self.get_focal_ratio()
        # print '\nget max mag', self.get_max_mag()
        return self.get_length() / self.get_max_mag()

    def get_max_mag(self):
        """
        This function returns the maximum useful magnification. The theoretical limit for useful magnification is 50 to
        60 x the aperture in inches or 2 x the aperture in mm.
        :return:
        """
        return 2.0 * self.aperture

    def get_min_mag(self):
        """
        This function returns the minimum useful magnification.
        :return:
        """
        return self.aperture / 7


# eyepiece class
class Eyepiece:
    """
    This is the eyepiece class
    Attributes:
        name
        apparent_fov
        length


    Methods:
        getName
        get_apparent_fov
        getLength
        getMag
        getFOV
        getFocalLength

    """

    def __init__(self, eyepiece_name, apparent_fov, eyepiece_length):
        self.name = eyepiece_name
        self.apparent_fov = float(apparent_fov)
        self.length = float(eyepiece_length)

    def get_name(self):
        return self.name

    def get_apparent_fov(self):
        return self.apparent_fov

    def get_length(self):
        return self.length


# GET DATA -------------------------------------------------------------------------------------------------------------

# This gets the  telescope data.........................................................................................
telescope_data = []
with open('tele_input.txt') as in_f:
    for line in in_f:
        clean_line = line.strip()
        if clean_line and not clean_line.startswith("#"):  # is not empty
            telescope_data.append(clean_line)

# Now that we have the telescope data, make a list of telescopes
telescope_list = []
num_telescopes = int(telescope_data[0])  # reads the first number from file

index = 1
for t in range(num_telescopes):  # for each telescope

    name = telescope_data[index]
    index += 1
    aperture = telescope_data[index]
    index += 1
    length = telescope_data[index]
    index += 1

    the_telescope = Telescope(name, aperture, length)
    telescope_list.append(the_telescope)

# We now have a list of telescope objects

# This gets the eyepiece data...........................................................................................
eyepiece_data = []
with open('eye_input.txt') as in_f:
    for line in in_f:
        clean_line = line.strip()
        if clean_line and not clean_line.startswith("#"):  # is not empty
            eyepiece_data.append(clean_line)

# Now that we have the eyepiece data, make a list of eyepieces
eyepiece_list = []
num_eyepieces = int(eyepiece_data[0])  # reads the first number from file

index = 1
for e in range(num_eyepieces):  # for each eyepiece

    name = eyepiece_data[index]
    index += 1
    aperture = eyepiece_data[index]
    index += 1
    length = eyepiece_data[index]
    index += 1

    the_eyepiece = Eyepiece(name, aperture, length)
    eyepiece_list.append(the_eyepiece)

# We know have a list of eyepiece objects


# CALCULATE AND PRINT THE RESULTS  ---------------------------------------------

f = open('output.txt', 'w')

# First the telescope stuff
for t in telescope_list:
    f.write('TELESCOPE {} ====================================================='
            .format(1 + telescope_list.index(t)))
    f.write('\nName: {}\n'.format(t.get_name()))
    f.write('Aperture: {:.0f} in \n'.format(t.get_aperture(),
            convert_length(t.get_aperture(), 'mm')))
    f.write('Length: {:.0f} mm\n'.format(t.get_length()))
    f.write('Focal ratio: {:.1f}\n'.format(t.get_focal_ratio()))
    f.write('The magnification range is {:.0f}x to {:.0f}x\n'
            .format(t.get_min_mag(), t.get_max_mag()))
    f.write('Shortest eyepiece: {:.1f} mm\n'
            .format(t.get_shortest_useful_eyepiece()))
    f.write('Longest eyepiece: {:.0f} mm\n\n'
            .format(t.get_longest_useful_eyepiece()))

    # Then the string eyepiece stuff
    # String formatting links
    # https://docs.pytjon.org/2/library/string.html#format-specification-mini-language
    f.write('EYEPIECES......................................................\n')
    f.write('{:<25}{:<15}{:<15}\n'.format("NAME", "MAG", "TFOV"))
    for e in eyepiece_list:
        name = e.name
        mag = t.get_length() / e.get_length()
        tfov = e.get_apparent_fov() / (t.get_length() / e.get_length())
        f.write('{:<25}{:<15.0f}{:<15.2f}'.format(name, mag, tfov))
        f.write('\n')
    f.write('\n\n')
