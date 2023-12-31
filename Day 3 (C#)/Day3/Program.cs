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
                TaskTwo(filePath);
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
        foreach ((int r, int c) in numberStartIndices) {
            chars = [];
            int row = r;
            int col = c;
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
            int add = CharListToInt(chars);
            ret += add;
            //Console.WriteLine(add);
        }
        Console.WriteLine($"Final result for task 1 of day 3: {ret}");
    }

    static void TaskTwo(string filePath) 
    {
        //convert the input file to a char[][] array
        char[][] arr = InputToArray(filePath);

        if (arr == null)
        {
            Console.WriteLine("Retrieving input failed. Exiting");
            return;
        }
        int result = 0; //we add to this as we find gears
        for (int row = 0; row < arr.Length; row++) 
        {
            for (int col = 0; col < arr[row].Length; col++)
            {
                bool indexIsAsterisk = arr[row][col] == '*';
                if (indexIsAsterisk)
                {
                    result += GearValue(arr, row, col);
                }
            }
        }
        Console.WriteLine($"Final result for task 2 of day 3: {result}");
    }

    static void Test()
    {

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
        int[] subRows = [row-1, row+1]; //lets us iterate over the row above and below the current one.
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
            int clampedCol = Math.Clamp(subCol, 0, arr[row].Length-1); //clamp the column number to be in bounds
            //Console.WriteLine($"Checking at ({row},{clampedCol})");
            char character = arr[row][clampedCol];
            if (IsSpecial(character)) //check if the char is a special character other than .
            {
                return true;
            }
            
        }
        foreach (int subRow in subRows)
        {
            int clampedRow = Math.Clamp(subRow, 0, arr.Length-1); //clamp the row number to be in bounds
            
            for (int i = Math.Clamp(startCol-1, 0, arr[row].Length-1); i < endCol + 1; i++)
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
        if (!Char.IsDigit(character) && !Char.IsLetter(character) && character != '.')
        {
            return true;
        }
        return false;
    }

    public static int GearValue(char[][] arr, int row, int col)
    {
        //Check an asterisk in the array to see if it has exactly two adjacent numbers; if so, return those multiplied; otherwise, return 0
        int[] adjacentColumns = [col-1, col+1];
        int[] subRows = [row-1, row+1]; //lets us iterate over the row above and below the current one.
        List<(int,int)> numCoords = [];
        int numbersFound = 0; //we exit early if this exceeds 2
        foreach (int adj in adjacentColumns)
        {
            if (Char.IsDigit(arr[row][adj]))
            {
                numCoords.Add((row,adj));
                numbersFound++;
            }
        }

        foreach (int subRow in subRows)
        {
            bool lastColumnWasDigit = false;
            for (int subCol = col-1; subCol < col+2; subCol++)
            {
                if (char.IsDigit(arr[subRow][subCol]))
                {
                    if (!lastColumnWasDigit)
                    {
                        numCoords.Add((subRow,subCol));
                        numbersFound++;
                        lastColumnWasDigit = true;
                    } 
                    else
                    {
                        lastColumnWasDigit = true;
                    }
                }
                else
                {
                    lastColumnWasDigit = false;
                }
                if (numbersFound > 2)
                {
                    return 0;
                }
            }
        }
        if (numbersFound == 2)
        {
            int num1 = GetNumber(arr, numCoords[0].Item1, numCoords[0].Item2);
            int num2 = GetNumber(arr, numCoords[1].Item1, numCoords[1].Item2);
            return num1 * num2;
        }
        return 0;
    }

    public static int GetNumber(char[][] arr, int row, int col)
    {
        //Given the (row,col) indices of a digit, return that digit's number


        //first we need to find the entire number in the array

        int startCol = GetFirstIndexOfNumber(arr, row, col);

        int endCol = GetLastIndexOfNumber(arr, row, startCol);

        List<char> chars = [];
        for (int i = startCol; i < endCol + 1; i++)
        //retrieve the whole number
        {
            chars.Add(arr[row][i]);
        }
        return CharListToInt(chars);
    }

    public static int GetFirstIndexOfNumber(char[][] arr, int row, int col)
    {
        int startCol = col;

        while (startCol > -1) {
            if (Char.IsDigit(arr[row][startCol]))
            {
                //decrement current column if it's a digit
                startCol--;
            } else 
            {
                //otherwise bring it back to a digit and break
                startCol++;
                break;
            }
        }
        startCol = Math.Clamp(startCol, 0, arr[row].Length); //clamp to bounds in case startCol is -1

        return startCol;
    }

    public static int GetLastIndexOfNumber(char[][] arr, int row, int col)
    {
        int endCol = col;
        while (endCol < arr[row].Length) 
        {
            if (Char.IsDigit(arr[row][endCol]))
            {
                //increment column if it's a digit
                endCol++;
            } else
            {
                //otherwise bring it back to a digit and break
                endCol--;
                break;
            }
        }

        endCol = Math.Clamp(endCol, 0, arr[row].Length - 1); //clamp to bounds in case endCol == length

        return endCol;
    }

    public static int CharListToInt(List<char> chars) {
        //convert a List<char> to an int. Assumes all contents are numbers, you've fucked up otherwise
        char[] numberAsCharArray = chars.ToArray();
        string numberAsString = new string(numberAsCharArray);
        int ret = int.Parse(numberAsString);
        return ret;
    }
}
