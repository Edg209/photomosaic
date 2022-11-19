# The photomosaic process

This document will detail the process used in generating a photomosaic, and the concepts that will be used during the generation process.

Note that every image is expected to be in PNG format. Candidate images that do not have the extension `.png` will be ignored, and the target image is assumed to be in PNG format.

## Concepts

| Concept          | Meaning                                                                                                                                                                              |
|------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Target image     | The image that we want the photomosaic to generate                                                                                                                                   |
| Output image     | An image that has been generated to resemble the target image                                                                                                                        |
| Candidate image  | One of the images that will be arranged to generate the photomosaic                                                                                                                  |
| The grid         | The layout of candidate images to generate an output image                                                                                                                           |
| Comparison image | One of the candidate images or a sub-image of the target image that has been scaled to a consistent smaller size for the purpose of comparison                                       |
| Pixel distance   | A measure of how similar a pixel in one comparison image is to another pixel at the same location in another comparison image. A lower number indicates the pixels are more similar. |
| Image distance   | The sum of all pixel distances for a pair of comparison images                                                                                                                       |

## Process

Each of the steps involved in the process will be detailed below.

### Parsing of input and folder setup

This process is called with a JSON file that contains the full set of parameters for running the process.

| Parameter                | Parameter details                                                                                                                    | Parameter format             |
|--------------------------|--------------------------------------------------------------------------------------------------------------------------------------|------------------------------|
| `photomosaic_folder`     | The path of the folder that all the generated photomosaic files will be placed in. This folder will be created as part of this step. | String up to 1000 characters |
| `target_image`           | The path of the target image to be used in the photomosaic                                                                           | String up to 1000 characters |
| `candidate_image_folder` | The path of the folder that contains the candidate images. Each file in the folder must be a candidate image.                        | String up to 1000 characters |
| `grid_x`                 | The width of the grid of candidate images                                                                                            | Positive integer             |
| `grid_y`                 | The height of the grid of candidate images                                                                                           | Positive integer             |
| `output_x`               | The width of each candidate image in the output in pixels                                                                            | Positive integer             |
| `output_y`               | The height of each candidate image in the output in pixels                                                                           | Positive integer             |
| `comparison_x`           | The width of each image to be used during comparison                                                                                 | Positive Integer             |
| `comparison_y`           | The height of each image to be used during comparison                                                                                | Positive Integer             |

The cost of computing the photomosaic is proportional to the product of `comparison_x`, `comparison_y`, `grid_x`, `grid_y` and the number of images in `candidate_image_folder`. It is recommended to keep these parameters low.

If the json is formatted correctly, then the folder `photomosaic_folder` will be created, and within it five subfolders will be created:

* `comparison_candidate_images`
* `comparison_target_images`
* `output_candidate_images`
* `output_layouts`
* `output_images`

Each of these subfolders will initially be empty, and they will be populated during the later steps.

### Rescaling of candidate images

Each image in `candidate_image_folder` will have two copies made, at different resolutions.

Within the folder `comparison_candidate_images` we will resize to the dimensions given by `comparison_x` and `comparison_y`.

Within the folder `output_candidate_images` we will resize to the dimensions given by `output_x` and `output_y`.

### Generation of comparison target images

The image `target_image` will be resized to a width of `grid_x` * `comparison_x` and a height of `grid_y` * `comparison_y`, then partitioned into `grid_x` * `grid_y` sub-images. Each of these sub-images will be saved to the `comparison_target_images` folder. 

### Comparing images

We will iterate over every one of the candidate images in `candidate_image_folder` and do the following:

#### Generating image distances

For each target sub-image in `comparison_target_images`, we generate the image distance of that target sub-image and the chosen candidate image. The image distance is the mean of all the pixel distances.

#### Generating an output layout

Once we have calculated an updated set of images distances, we generate an output layout. An output layout is a grid of the names of each of the candidate images that have the lowest image distance for each of the corresponding target sub-images. The names of these files will be saved as a CSV file in the folder `output_layouts`.

#### Generating an output image

The output layout describes what the layout of an output image should be, and we construct an image that consists of the appropriate candidate images (from the `output_candidate_images` folder) in the appropriate locations.