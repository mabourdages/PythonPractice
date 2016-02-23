import re
from Tkinter import Tk
from tkFileDialog import askopenfilename

Tk().withdraw()
file_path = askopenfilename()


# Function to find animation length
def find_animation_length():
    # Check for a valid .ma file//Checking later for maya or Mbbu file.
    if ".ma" not in file_path:
        raise TypeError("Make sure to use a valid file.")

    with open(file_path, "r") as ascii_file:
        # Regex to find frame content of -min (frame) -max (frame) of ascii maya file.
        for content_lines in ascii_file.readlines():
            regex_content = re.compile("(-min)(\s-{0,1}\d*\s)(-max)(\s-{0,1}\d*)").search(content_lines)

            if regex_content:
                frame_start, frame_end = regex_content.group(2), regex_content.group(4)

                # Printing the result
                anim_length = float(frame_end) - float(frame_start)
                print "Animation length is {0} frame or {1} seconds"\
                      .format(int(anim_length), round(float(anim_length/30), 2))
                break
        # Making sure we get a result otherwise raise error.
        else:
            raise ValueError("Could not find time frame or file is not from Maya.")

find_animation_length()
