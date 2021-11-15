import javax.imageio.ImageIO;
import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;

/**
 * TargetImage is an object that represents the target image of a photomosaic.
 * The data on the individual pixels is in CIE-Lab format.
 *
 * TODO: Add details of fields
 */
public class TargetImage {

    public BufferedImage image;

    /**
     * Create a new TargetImage
     *
     * @param path A String giving the path to the image to be used
     * @param background A Color that will be used as background to the image
     * @throws IOException When attempting to read the file containing the image
     */

    public TargetImage(String path, Color background) throws IOException {
        //We read the image from the path
        File imageFile = new File(path);
        BufferedImage bufferedImage = ImageIO.read(imageFile);
        //We create another bufferedImage for the processed image
        BufferedImage processedImage = new BufferedImage(bufferedImage.getWidth(), bufferedImage.getHeight(),bufferedImage.getType());
        //We set the background color using Graphics2d
        Graphics2D g2d = processedImage.createGraphics();
        g2d.setBackground(background);
        g2d.drawImage(bufferedImage, 0, 0, bufferedImage.getWidth(), bufferedImage.getHeight(), null);
        g2d.dispose();
        this.image = processedImage;
    }
}
