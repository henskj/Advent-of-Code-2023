import java.io.File;

public class ValidateFile {
    public static File createAndValidateFile(String filePath) {

        File file = new File(filePath);
        if (!file.exists()) {
            throw new IllegalArgumentException("File does not exist: " + filePath);
        }
        if (!file.isFile()) {
            throw new IllegalArgumentException("Path does not denote a file: " + filePath);
        }
        if (!file.canRead()) {
            throw new IllegalArgumentException("File cannot be read: " + filePath);
        }
        return file;
    }
}
