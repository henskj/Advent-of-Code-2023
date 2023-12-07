import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;

public class aoc2_1 {
    public static void run(File file) {

        ArrayList<Integer> possibleGames = new ArrayList<>();
        try (BufferedReader reader = new BufferedReader(new FileReader(file))) {
            String line;
            int lineCount = 0;
            while ((line = reader.readLine()) != null) {
                lineCount++; //we use this to keep track of game ID, instead of actually reading the string
                line = line.replaceAll("Game \\d+: ", ""); //so we drop that info from the string
                line = line.replaceAll(",", ""); //and remove commas
                String[] subGames = line.split("; ");
                boolean possible = true;
                for (String sub : subGames) {
                    //evaluate each subgame, delineated by semicolons; we don't assume each colour can only appear once
                    //(although that seems to be the case)
                    possible = evaluateSubGame(sub);
                    if (!possible) {
                        break;
                    }
                }
                if (possible) {
                    possibleGames.add(lineCount); //add the game's ID to the list of IDs of possible games
                }
            }
            int tot = 0;
            for (Integer id : possibleGames) {
                tot += id;
            }
            System.out.println(tot);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
    public static boolean evaluateSubGame(String game) {
        /*
        Evaluate a streamlined subgame string, on the form of e.g. "7 red 5 blue 2 green".
        The subgame is possible if there are at most 12 red, 13 green, and 14 blue cubes.
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
        return redCount <= 12 && greenCount <= 13 && blueCount <= 14;
    }
}
