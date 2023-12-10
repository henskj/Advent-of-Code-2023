import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;

public class Day5 {
    public static void main(String[] args) {
        if (args.length < 2) {
            throw new IllegalArgumentException("Missing task number or file path. Correct input: [filepath] [taskNum].");
        }
        String filePath = args[0];

        File file = ValidateFile.createAndValidateFile(filePath);

        if (args[1].equals("1")) {
            taskOne(file);
        } else {
            taskTwo(file);
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

    public static void taskTwo(File file) {
        try (BufferedReader reader = new BufferedReader(new FileReader(file))) {
            ArrayList<Long> sourceBase = getSeeds(reader);
            ArrayList<ArrayList<Long>> source = new ArrayList<>();
            for (int i = 0; i < sourceBase.size(); i += 2) {
                ArrayList<Long> sourceRange = new ArrayList<>();
                sourceRange.add(sourceBase.get(i));
                sourceRange.add(sourceBase.get(i+1));
                source.add(sourceRange);
            }

             //sort seeds in ascending order of start values
            Collections.sort(source, Comparator.comparing(o -> o.get(0)));

            //ArrayList<ArrayList<Long>> destination = getNextLayer(reader);
            //sort the destinations the same way
            //Collections.sort(destination, Comparator.comparing(o -> o.get(1)));

            for (int i = 0; i < 7; i++) {
                //the input always has 7 steps, so I feel comfortable hardcoding this
                ArrayList<ArrayList<Long>> destination = getNextLayer(reader);
                //sort the destinations the same way
                long rangeSum  = 0;
                for (int p = 0; p < source.size(); p++) {
                    rangeSum += source.get(p).get(1);
                }
                Collections.sort(destination, Comparator.comparing(o -> o.get(1)));
                source = processLayerRanges(source, destination);
                Collections.sort(source, Comparator.comparing(o -> o.get(0)));
                Collections.sort(destination, Comparator.comparing(o -> o.get(1)));
            }

            Long result = Long.MAX_VALUE;
            for (ArrayList<Long> range : source) {
                Long rangeMin = range.get(0);
                if (rangeMin < result) {
                    result = rangeMin;
                }
            }
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

    public static ArrayList<ArrayList<Long>> processLayerRanges(ArrayList<ArrayList<Long>> origin,
                                                    ArrayList<ArrayList<Long>> destination) {
        ArrayList<ArrayList<Long>> retRanges = new ArrayList<>();
        for (ArrayList<Long> originRange : origin) {
            boolean added = false;
            Long sourceStart = originRange.get(0);
            Long sourceEnd = sourceStart + originRange.get(1);
            for (ArrayList<Long> destLayer : destination) {
                //initialise values
                ArrayList<Long> layerRange;
                Long destSourceRangeStart = destLayer.get(1);
                Long destLength = destLayer.get(2);
                Long destSourceRangeEnd = destSourceRangeStart + destLength;
                if (sourceEnd == sourceStart) {
                    break; //we get here if in a previous run of the loop, the entire length of the range was used
                }
                if (sourceEnd < destSourceRangeStart || sourceStart > destSourceRangeEnd) {
                    continue;
                } else if (sourceStart >= destSourceRangeStart) {
                    layerRange = getRange(originRange, destLayer, sourceStart);
                    //we get here if the source range's start begins at or after the current layer's compatible values
                    sourceStart = layerRange.get(2); //last item in list is updated sourceStart value
                    layerRange.remove(2);
                    retRanges.add(layerRange);
                    added = true;
                } else {
                    //otherwise, we get here, where we strip off the beginning of the range
                    ArrayList<Long> strippedRange = new ArrayList<>();
                    strippedRange.add(sourceStart);
                    strippedRange.add(destSourceRangeStart - sourceStart + 1);
                    retRanges.add(strippedRange);
                    added = true;

                    sourceStart = destSourceRangeStart;

                    if (sourceStart + 1 == sourceEnd) {
                        //check for an off-by-1. surely there is a better way to do this
                        sourceStart++;
                        continue;
                    }

                    layerRange = getRange(originRange, destLayer, sourceStart);
                    sourceStart = layerRange.get(2);
                    layerRange.remove(2);

                    retRanges.add(layerRange);
                    added = true;
                }
            }
            if (!added) {
                //we get here if there were no compatible values
                retRanges.add(originRange);
            } else if (sourceStart < sourceEnd) {
                ArrayList<Long> layerRange = new ArrayList<>();
                layerRange.add(sourceStart);
                layerRange.add(sourceEnd - sourceStart);
                retRanges.add(layerRange);
            }
        }
        return retRanges;
    }

    public static ArrayList<Long> getRange(ArrayList<Long> originRange, ArrayList<Long> destLayer, long sourceStart) {
        //reinitialise layers - will fix later

        Long sourceEnd = originRange.get(0) + originRange.get(1);
        Long destSourceRangeStart = destLayer.get(1);
        Long destStart = destLayer.get(0);
        Long destLength = destLayer.get(2);
        Long destSourceRangeEnd = destSourceRangeStart + destLength;
        Long destPosEnd;
        ArrayList<Long> layerRange = new ArrayList<>();
        Long rangePosStart = Math.abs(sourceStart - destSourceRangeStart);
        Long destPosStart = destStart + rangePosStart;

        //actual logic here
        if (sourceEnd <= destSourceRangeEnd) {
            Long rangePosEnd = sourceEnd - sourceStart;
            destPosEnd = destPosStart + rangePosEnd;
            sourceStart = sourceEnd;
        } else {
            destPosEnd = destStart + destLength;
            sourceStart = destSourceRangeEnd;
        }
        layerRange.add(destPosStart);
        layerRange.add(destPosEnd - destPosStart);
        layerRange.add(sourceStart);
        return layerRange;
    }
}
