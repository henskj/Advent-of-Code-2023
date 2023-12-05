import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;

public class aoc2_2 {
    public static void main(String[] args) {
        if (args.length == 0) {
            throw new IllegalArgumentException("No file path provided.");
        }
        String filePath = args[0];
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

        ArrayList<Integer[]> rgbMins = new ArrayList<>();
        try (BufferedReader reader = new BufferedReader(new FileReader(file))) {
            String line;
            int lineCount = 0;
            while ((line = reader.readLine()) != null) {
                lineCount++; //we use this to keep track of game ID, instead of actually reading the string
                line = line.replaceAll("Game \\d+: ", ""); //so we drop that info from the string
                line = line.replaceAll(",", ""); //and remove commas
                String[] subGames = line.split("; ");
                Integer[] greatestMins = {0, 0, 0};
                for (String sub : subGames) {
                    //evaluate each subgame, delineated by semicolons; we don't assume each colour can only appear once
                    //(although that seems to be the case)
                    int[] subMins = evaluateSubGame(sub);
                    for (int i = 0; i < 3; i++) {
                        if (subMins[0] > greatestMins[0]) {
                            greatestMins[0] = subMins[0];
                        }
                        if (subMins[1] > greatestMins[1]) {
                            greatestMins[1] = subMins[1];
                        }
                        if (subMins[2] > greatestMins[2]) {
                            greatestMins[2] = subMins[2];
                        }
                    }
                }
                rgbMins.add(greatestMins);

            }
            int tot = 0;
            for (int i = 0; i < rgbMins.size(); i++) {
                int redMin = rgbMins.get(i)[0];
                int greenMin = rgbMins.get(i)[1];
                int blueMin = rgbMins.get(i)[2];
                int power = redMin * greenMin * blueMin;
                tot += power;
                System.out.printf("Lowest for game %d: %d red, %d green, %d blue; power %d\n", i+1, redMin, greenMin, blueMin, power);
            }
            System.out.println(tot);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
    public static int[] evaluateSubGame(String game) {
        /*
        Evaluate a streamlined subgame string, on the form of e.g. "7 red 5 blue 2 green".
        Find the lowest amount of each colour that could be used for each game.
         */
        int redCount = 0;
        int blueCount = 0;
        int greenCount = 0;
        String[] infos = game.split(" ");
        for (int i = 0; i < infos.length; i += 2) {
            int count = Integer.parseInt(infos[i]);
            String colour = infos[i + 1];
            switch (colour) {
                case "red" -> redCount += count;
                case "green" -> greenCount += count;
                case "blue" -> blueCount += count;
            }
        }
        int[] ret = {redCount, greenCount, blueCount};
        return ret;
    }
}
