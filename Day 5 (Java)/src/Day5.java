import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.util.ArrayList;
import java.util.Collections;

public class Day5 {
    public static void main(String[] args) {
        if (args.length < 2) {
            throw new IllegalArgumentException("Missing task number or file path. Correct input: [filepath] [taskNum].");
        }
        String filePath = args[0];

        File file = ValidateFile.createAndValidateFile(filePath);

        if (args[1].equals("1")) {
            taskOne(file);
        }


    }

    public static void taskOne(File file) {
        try (BufferedReader reader = new BufferedReader(new FileReader(file))) {
            ArrayList<Long> source = getSeeds(reader);
            ArrayList<ArrayList<Long>> destination;
            for (int i = 0; i < 7; i++) {
                //the input always has 7 steps, so I feel comfortable hardcoding this
                destination = getNextLayer(reader);
                source = processLayers(source, destination);
            }

            Long result = Collections.min(source);
            System.out.println(result);
        }
        catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static ArrayList<ArrayList<Long>> getNextLayer(BufferedReader reader) {
        try {
            String line = reader.readLine();
            ArrayList<ArrayList<Long>> layer = new ArrayList<>();
            while (line.length() > 0) {
                ArrayList<Long> subLayer = new ArrayList<>();
                String[] splitLine = line.split(" ");
                for (int i = 0; i < splitLine.length; i++) {
                    subLayer.add(Long.parseLong(splitLine[i]));
                }
                layer.add(subLayer);
                line = reader.readLine();
                if (line == null) {
                    break;
                }
            }
            //skip a line - we're already one line past relevant info, so we skip one more to reach the next layer
            reader.readLine();
            return layer;
        } catch (Exception e) {
            e.printStackTrace();
        }
        return null;
    }

    public static ArrayList<Long> getSeeds(BufferedReader reader) {
        try {
            String[] line = reader.readLine().split(" ");
            ArrayList<Long> seeds = new ArrayList<>();
            for (int i = 1; i < line.length; i++) {
                seeds.add(Long.parseLong(line[i]));
            }
            //skip two lines to reach next layer, handling EoF with a null check
            if (reader.readLine() != null) {
                reader.readLine();
            }
            return seeds;
        } catch (Exception e) {
            e.printStackTrace();
        }
        return null;
    }

    public static ArrayList<Long> processLayers(ArrayList<Long> source,
                                                  ArrayList<ArrayList<Long>> destination) {
        ArrayList<Long> newLayer = new ArrayList<>();

        for (Long sourceVal : source) {
            boolean assigned = false;
            for (ArrayList<Long> destLayer : destination) {
                long sourceStart = destLayer.get(1); //index 1 is the start of the source
                long length = destLayer.get(2);
                long sourceEnd = sourceStart + length;
                long destStart = destLayer.get(0);
                if (sourceStart <= sourceVal && sourceVal < sourceEnd) {
                    long rangePos = sourceVal - sourceStart; //the relative position of our value in the range
                    long destPos = destStart + rangePos; //where our value lands
                    newLayer.add(destPos);
                    assigned = true;
                    break;
                }
            }
            if (!assigned) {
                //if a match isn't found, the source value corresponds 1:1 to the destination value
                newLayer.add(sourceVal);
            }
        }
        System.out.println();
        return newLayer;
    }
}
