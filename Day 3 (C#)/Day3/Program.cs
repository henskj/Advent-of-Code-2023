using System;
using System.Collections;
using System.Data;
using System.IO;
using System.Numerics;
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
        bool skip = false; //set to true when a number is found to not check it more than onec
        for (int row = 0; row < arr.Length; row++) 
        {
            for (int col = 0; col < arr[row].Length; col++)
            {
                bool indexIsDigit = Char.IsDigit(arr[row][col]);
                if (indexIsDigit && !skip)
                {
                    if (NumberHasSpecials(arr, row, col))
                    {
                        numberStartIndices.Add((row, col));
                        skip = true;
                    }
                } else if (!indexIsDigit)
                {
                    skip = false;
                }
            }
        }
        int ret = 0;
        List<char> chars;
        foreach ((int,int) tup in numberStartIndices) {
            //Console.WriteLine(tup);
            chars = [];
            int row = tup.Item1;
            int col = tup.Item2;
            while (Char.IsDigit(arr[row][col]))
            {
                chars.Add(arr[row][col]);
                if (col < arr[row].Length - 1)
                {
                    col++;
                } else
                {
                    break;
                }
            }
            char[] numberAsCharArray = chars.ToArray();
            string numberAsString = new string(numberAsCharArray);
            int add = int.Parse(numberAsString);
            ret += add;
            //Console.WriteLine(add);
        }
        Console.WriteLine($"Final result: {ret}");
    }
                    
        /*

        Earlier algorithm. Realised after writing that it is stupid. This version checked around all special characters; better to check around all numbers
        to avoid redoing work.

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
    */
    public static char[][] InputToArray(string filePath) 
    {
        //Converts the text file input to an array of chars. Returns null if an error is raised.
        char[][] retArray;
        try
        {
            // Open a reader - errors are handled in the function for better readability here, see GetFileReader in the general C# utilities folder.
            using (StreamReader reader = AocReusableUtilities.AocReusableUtilities.OpenFileReader(filePath))
            {
                (int rows, int columns) = GetDimensions(reader);
                //Console.WriteLine($"Dimensions determined to be ({rows},{columns})");
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

    public static bool NumberHasSpecials (char[][] arr, int row, int col)
    {
        //Check a number in the array to see if it has an adjacent special character; return true if so, otherwise false
        //when we find a digit, we want to determine the size of the number it belongs to
        //then we want to search indices around said number's area until we find a special character
        //when we do, we can break, which is much faster and simpler than the commented-out algo

        int startCol = col; //first column index of our number, inclusive
        int endCol = col; //last column index of our number, exclusive
        int[] subRows = [row-1, row+1]; //lets us iterate over the row above and below the current one. We check later whether these rows are out of bounds
        //Console.WriteLine($"Beginning at ({row},{startCol})");
        while (Char.IsDigit(arr[row][endCol]))
        {
            //increment endCol until its index is no longer a number or we hit the final index
            if (endCol < arr[row].Length-1)
            {
                endCol++;
            } else
            {
                break;
            }
        }
        int[] adjacentCols = [startCol-1, endCol];
        //Console.WriteLine($"Adjacent columns are {adjacentCols[0]} and {adjacentCols[1]}");
        foreach (int subCol in adjacentCols) {
            int clampedCol = AocReusableUtilities.AocReusableUtilities.Clamp(subCol, 0, arr[row].Length-1); //clamp the column number to be in bounds
            //Console.WriteLine($"Checking at ({row},{clampedCol})");
            char character = arr[row][clampedCol];
            if (IsSpecial(character)) //check if the char is a special character other than .
            {
                return true;
            }
            
        }
        foreach (int subRow in subRows)
        {
            int clampedRow = AocReusableUtilities.AocReusableUtilities.Clamp(subRow, 0, arr.Length-1); //clamp the row number to be in bounds
            
            for (int i = AocReusableUtilities.AocReusableUtilities.Clamp(startCol-1, 0, arr[row].Length-1); i < endCol + 1; i++)
            {
                //Console.WriteLine($"Checking at ({clampedRow},{i}); last is {endCol + 1}");
                char character = arr[clampedRow][i];
                if (IsSpecial(character)) //check if the char is a special character other than .
                {
                    return true;
                }
            }
        }
        return false;
    }

    public static bool IsSpecial(char character)
    {
        int asciiVal = (int) character; //cast char to int to get ASCII value
        if (!Char.IsDigit(character) && !Char.IsLetter(character) && asciiVal != 46)
        {
            return true;
        }
        return false;
    }
}
