import tempfile
import subprocess
import shlex
import os
import scipy.io

script_dirname = os.path.abspath(os.path.dirname(__file__))


def get_windows(image_fnames):
    """
    Run MATLAB Selective Search code on the given image filenames to
    generate window proposals.

    Parameters
    ----------
    image_filenames: strings
        Paths to images to run on.
    """
    # Form the MATLAB script command that processes images and write to
    # temporary results file.
    f, output_filename = tempfile.mkstemp(suffix='.mat')
    fnames_cell = '{' + ','.join("'{}'".format(x) for x in image_fnames) + '}'
    command = "selective_search({}, '{}')".format(fnames_cell, output_filename)
    print(command)

    # Execute command in MATLAB.
    mc = "matlab -nojvm -r \"try; {}; catch; exit; end; exit\"".format(command)
    pid = subprocess.Popen(
        shlex.split(mc), stdout=open('/dev/null', 'w'), cwd=script_dirname)
    retcode = pid.wait()
    if retcode != 0:
        raise Exception("Matlab script did not exit successfully!")

    # Read the results, remove temporary file, and return.
    boxes = list(scipy.io.loadmat(output_filename)['all_boxes'][0])
    os.remove(output_filename)
    if len(boxes) != len(image_fnames):
        raise Exception("Something went wrong computing the windows!")
    return boxes

if __name__ == '__main__':
    """
    Run a demo.
    """
    import time

    image_filenames = [
        script_dirname + '/000015.jpg',
        script_dirname + '/cat.jpg'
    ] * 4
    t = time.time()
    boxes = get_windows(image_filenames)
    print("Processed {} images in {:.3f} s".format(
        len(image_filenames), time.time() - t))
