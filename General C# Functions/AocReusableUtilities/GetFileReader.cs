using System;
using System.IO;

namespace AocReusableUtilities
{
    public static class GetFileReader
    {
        public static StreamReader OpenFileReader(string filePath)
        {
            if (string.IsNullOrEmpty(filePath))
            {
                throw new ArgumentException("No file path provided.");
            }

            FileInfo file = new FileInfo(filePath);

            if (!file.Exists || file.Attributes.HasFlag(FileAttributes.Directory))
            {
                throw new FileNotFoundException("File not found or path is a directory", filePath);
            }

            if (file.IsReadOnly)
            {
                throw new FileLoadException("File cannot be read", filePath);
            }

            return new StreamReader(file.OpenRead());
        }
    }
}
