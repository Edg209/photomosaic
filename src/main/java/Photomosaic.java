import java.awt.*;
import java.io.File;
import java.io.IOException;
import java.util.HashSet;
import java.util.Objects;
import java.util.Set;

/**
 * Photomosaic is a class which represents a photomosaic and how it is generated.
 * A photomosaic is the combination of multiple sub-images to imitate a single target image.
 * The concepts involved in a photomosaic are:
 * <ul>
 *     <li>The target image is the image that we are trying to replicate</li>
 *     <li>The sub-images are the individual images that we compose to make the main image</li>
 *     <li>A candidate image is a single one of the possible images that can be used as a sub-image</li>
 *     <li>A chosen sub-image is a sub-image where one of the candidate images has been calculated as best choice</li>
 *     <li>The sub-image grid is a two dimensional array of all the sub-images</li>
 *     <li>The background color is the default color of the image to be used in case of transparency</li>
 *     <li>The output image is the image the composes all the sub-images together</li>
 *     <li>A target pixel is a pixel in the target image, which corresponds to multiple pixels in the output image</li>
 * </ul>
 * <p>
 * The algorithm used for generating a photomosaic is:
 * <ul>
 *     <li>Load all candidate images and resize them to consistent dimensions</li>
 *     <li>Apply the background color to any transparent pixels</li>
 *     <li>Determine the size and shape of the sub-image array</li>
 *     <li>Iterate over the sub-images going first left to right then bottom to top:</li>
 *     <ul>
 *         <li>Determine the target pixels corresponding to each pixel in the sub-image</li>
 *         <li>Determine the pixels from the adjacent chosen sub-images that align to these target pixels</li>
 *         <li>For each candidate image, calculate average distance:</li>
 *         <ul>
 *             <li>For each target pixel that is used for this candidate image:</li>
 *             <ul>
 *                 <li>Determine the relevant pixels in the candidate image and the adjacent chosen sub-images</li>
 *                 <li>Determine the average color of all the corresponding to this target pixel</li>
 *                 <li>Calculate the distance between the target pixel and the average color</li>
 *             </ul>
 *             <li>Average each of the distance values of the target pixels for this candidate image</li>
 *         </ul>
 *         <li>Pick the candidate image with the best average distance as the chosen sub-image</li>
 *     </ul>
 *     <li>Combine all of the chosen sub-images to generate the output image</li>
 * </ul>
 * <p>
 * TODO: Add details of the public fields of the object
 */
public class Photomosaic {
    public TargetImage targetImage;
    Set<CandidateImage> candidateImageSet;
    public Integer subImageX;
    public Integer subImageY;
    public Integer outputImageX;
    public Integer outputImageY;
    public Integer subImageArrayX;
    public Integer subImageArrayY;
    public CandidateImage[][] subImageArray;

    /**
     * Create a new Photomosaic object with none of the processing done yet.
     *
     * @param targetImage     A String giving the target image to create a photomosaic of
     * @param candidateImages A String giving the path to the directory that contains the candidate images
     * @param subImageX       An Integer giving the width that each subImage will be converted to
     * @param subImageY       An Integer giving the height that each subImage will be converted to
     * @param outputImageX    An Integer giving the width of the photomosaic to be produced
     * @param outputImageY    An Integer giving the height of the photomosaic to be produced
     * @param backgroundColor The background color to use in the case of transparent pixels
     *
     * @throws  IOException When reading candidate and image files
     */
    public Photomosaic(String targetImage, String candidateImages, Integer subImageX, Integer subImageY, Integer outputImageX, Integer outputImageY, Color backgroundColor) throws IOException {
        //We load the target and candidate images
        this.targetImage = new TargetImage(targetImage, backgroundColor);
        this.candidateImageSet = new HashSet<>();
        for (File candidateImageFile : Objects.requireNonNull(new File(candidateImages).listFiles())) {
            if (candidateImageFile.isFile()) {
                this.candidateImageSet.add(new CandidateImage(candidateImageFile.getPath(), subImageX, subImageY, backgroundColor));
            }
        }
        this.subImageX = subImageX;
        this.subImageY = subImageY;
        this.outputImageX = outputImageX;
        this.outputImageY = outputImageY;
        //We want to generate an array large enough to create the full output image
        //The output image dimensions may not be a nice multiple of the sub image dimensions
        //Therefore, there may be a bit that "sticks out" over the output image dimensions
        this.subImageArrayX = (int) Math.ceil(((double) outputImageX)/subImageX);
        this.subImageArrayY = (int) Math.ceil(((double) outputImageY)/subImageY);
        this.subImageArray = new CandidateImage[subImageArrayX][subImageArrayY];
    }
}
