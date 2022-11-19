class InputParser(object):
    """
    An object that represents the input to set up a photomosaic.

    Attributes:
        photomosaic_folder: The folder that will be generated to contain all files related to this photomosaic
        target_image: A numpy.ndarray of RGB values of the assembled image
        grid_shape: A tuple giving the x,y size of the grid of images
        output_shape: A tuple giving the x,y size of each of the candidate images
        comparison_shape: A tuple giving the x,y size of each of the comparison images

    Methods:
        parse: Generate the folder structure and populate the candidate and output image folders
    """

    def __init__(self, parameters_json: str):
        """
        Construct an InputParser to parse the inputs for a photomosaic and create the necessary files and folders.

        :param parameters_json: A string giving the path to a json file that contains the parameters for the photomosaic
        """
        raise NotImplementedError

    def parse(self):
        raise NotImplementedError
