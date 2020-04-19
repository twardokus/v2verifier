import os


TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
TEST_RESULTS_DIR = os.path.join(os.path.dirname(__file__), 'results')

IMG_NAME = 'floor plan.png'
IMG_PATH = os.path.join(TEST_DATA_DIR, IMG_NAME)

IMG_NAME_JPEG = 'elevation.jpg'
IMG_PATH_JPEG = os.path.join(TEST_DATA_DIR, IMG_NAME_JPEG)

WTR_NAME = 'watermark.png'
WTR_PATH = os.path.join(TEST_DATA_DIR, WTR_NAME)


def init_result_dir(sub_folder):
    """
    Initialize test result file destination directory.

    If the directory exists, delete the files it contains.
    Else, create the directory.
    """
    # Confirm 'results' folder exists
    if not os.path.isdir(TEST_RESULTS_DIR):
        os.mkdir(TEST_RESULTS_DIR)

    # Confirm the sub-folder exists and remove its contents, otherwise make the folder
    folder = os.path.join(TEST_RESULTS_DIR, sub_folder)
    if os.path.isdir(folder):
        for f in os.listdir(folder):
            os.remove(os.path.join(folder, f))
    else:
        os.mkdir(folder)
    return folder


__all__ = ['IMG_PATH', 'WTR_PATH', 'TEST_DATA_DIR', 'TEST_RESULTS_DIR', 'IMG_NAME_JPEG', 'IMG_PATH_JPEG',
           'init_result_dir']
