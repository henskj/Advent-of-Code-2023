using System;
using System.Collections;
using System.IO;
using System.Runtime.Versioning;
using System.Text;
using AocReusableUtilities;

class Day3
{
    static void Main(string[] args)
    {
        try
        {
            // Ensure that a file path is provided in the arguments
            if (args.Length < 2)
            {
                Console.WriteLine("Please provide a task number (1 or 2) and a file path.");
                return;
            }

            int task = int.Parse(args[0]);
            string filePath = args[1];

            if (task == 1) {
                TaskOne(filePath);
            } else {
                Console.WriteLine("Task two not implemented yet.");
                return;
            }


            
        }
        catch (Exception ex)
        {
            // Handle any exceptions that might occur
            Console.WriteLine("An error occurred: " + ex.Message);
        }
    }

    static void TaskOne(string filePath) 
    {
        //convert the input file to a char[][] array
        char[][] arr = InputToArray(filePath);

        if (arr == null)
        {
            Console.WriteLine("Retrieving input failed. Exiting");
            return;
        }
        List<(int,int)> numberStartIndices = []; //a list of (row,col) tuples storing the starting coordinate of numbers we'll read and sum later
        for (int row = 0; row < arr.Length; row++) 
        {
            for (int col = 0; col < arr[row].Length; col++)
            {
                int asciiVal = (int) arr[row][col]; //cast char to int to get ASCII value
                if (32 < asciiVal && asciiVal < 48 && asciiVal != 46) 
                {
                    //this checks if the character is a special character but not a full stop
                    for (int subRow = int.Max(row - 1, 0); subRow < int.Min(row + 2, arr.Length); subRow++) 
                    {
                        for (int subCol = int.Max(col - 1, 0); subCol < int.Min(col + 2, arr[subRow].Length); subCol++) 
                        {
                            //check if there are any numbers adjacent to our special character. we also check the special character itself, but that's fine;
                            //our special character is not a number.
                            //This implementation also will check many numbers more than once; will optimise later
                            if (Char.IsDigit(arr[subRow][subCol]))
                            {
                                int currentCol = subCol;
                                int leftest = subCol;
                                while (currentCol > 0 && Char.IsDigit(arr[subRow][currentCol-1]))
                                {
                                    leftest = currentCol-1;
                                    currentCol--;
                                }
                                var rowColTuple = (subRow, leftest);
                                if (!numberStartIndices.Contains(rowColTuple)) {
                                    numberStartIndices.Add(rowColTuple);
                                }
                            }
                        }
                    }
                }
            }
        }
        foreach ((int,int) tup in numberStartIndices) {
            Console.WriteLine(tup);
        }

    }
    static char[][] InputToArray(string filePath) 
    {
        //Converts the text file input to an array of chars. Returns null if an error is raised.
        char[][] retArray;
        try
        {
            // Open a reader - errors are handled in the function for better readability here, see GetFileReader in the general C# utilities folder.
            using (StreamReader reader = GetFileReader.OpenFileReader(filePath))
            {
                (int rows, int columns) = GetDimensions(reader);
                reader.BaseStream.Position = 0; //reset the reader instead of making a new one
                reader.DiscardBufferedData();
                string line;
                retArray = new char[rows][];
                int lineCount = 0;
                while ((line = reader.ReadLine())!= null)
                {
                    retArray[lineCount] = line.ToCharArray();
                    lineCount += 1;
                }
            }
            return retArray;
        }
        catch (Exception ex)
        {
            // Handle any exceptions that might occur
            Console.WriteLine("An error occurred: " + ex.Message);
            return null;
        }
    }

    public static (int rows, int columns) GetDimensions (StreamReader reader) 
    {
        int rows = 0;
        int columns = -1;
        string line;
        while ((line = reader.ReadLine()) != null)
        {
            rows++;
            if (columns == -1 && !string.IsNullOrWhiteSpace(line))
            {
                columns = line.Length;
            }
        }
        return (rows,columns);

    }
}
