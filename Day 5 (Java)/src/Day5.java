import java.io.File;

public class Day5 {
    public static void main(String[] args) {
        if (args.length < 2) {
            throw new IllegalArgumentException("Missing task number or file path. Correct input: [taskNum] [filepath].");
        }
        String filePath = args[0];

        File file = ValidateFile.createAndValidateFile(filePath);


    }
}
