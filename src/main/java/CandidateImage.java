import javax.imageio.ImageIO;
import java.awt.*;
import java.io.File;

import java.awt.image.BufferedImage;
import java.io.IOException;

/**
 * CandidateImage is an object that represents a single candidate image for a photomosaic.
 *
 * TODO: Add details of fields
 */
public class CandidateImage {
    public BufferedImage image;
    public CandidateImage(String path, Integer targetX, Integer targetY, Color background) throws IOException {
        //We read the image from the path
        File imageFile = new File(path);
        BufferedImage bufferedImage = ImageIO.read(imageFile);
        //We create another bufferedImage for the processed image
        BufferedImage processedImage = new BufferedImage(targetX, targetY,bufferedImage.getType());
        //We scale the image to the desired dimensions using Graphics2D
        //We also set the background color using Graphics2d
        Graphics2D g2d = processedImage.createGraphics();
        g2d.setBackground(background);
        g2d.drawImage(bufferedImage, 0, 0, targetX, targetY, null);
        g2d.dispose();
        this.image = processedImage;
    }
}
