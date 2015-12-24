using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace BoggleFinder
{
    class Program
    {
        static int Main(string[] args)
        {
            if (args.Length != 2)
            {
                Console.WriteLine("Usage: BOGGLEFINDER <Word List> <Grid>");
                return 1;
            }

            // Read the grid from a space-delimited file
            var grid = new Grid();
            grid.ReadGrid(args[1]);

            // Read through word list, and look for each word in the grid.
            var f = new StreamReader(args[0]);
            string word;
            while ((word = f.ReadLine()) != null){

                if (grid.Contains(word))
                    Console.WriteLine(word);
            }

            return 0;
        }
    }
}
