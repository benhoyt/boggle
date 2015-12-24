using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.IO;

namespace BoggleFinder
{
    class Grid
    {
        const int minWordLength = 3;

        /// <summary>
        /// The grid of letters.
        /// </summary>
        private char[] letterGrid;

        /// <summary>
        /// Keeps track of which letters in the grid we have visited while searching for a word.
        /// </summary>
        private bool[] visitedGrid;

        /// <summary>
        /// Number of letters in the grid.
        /// </summary>
        private int lettersInGrid;

        /// <summary>
        /// Number of letters in a row
        /// </summary>
        private int lettersInRow;

        void ReinitialiseVisited()
        {
            visitedGrid = new bool[lettersInGrid];
        }
        

        /// <summary>
        /// Read grid of letters from a file.
        /// </summary>
        /// <param name="fileName"></param>
        public void ReadGrid(string fileName)
        {
            var letterList = new List<char>();

            var f = new StreamReader(fileName);
            string line;
            while ((line = f.ReadLine()) != null){
                var parts = line.Split(new[]{' '}, StringSplitOptions.RemoveEmptyEntries);
                foreach (string st in parts)
                {
                    char c = st.ToLower()[0];
                    letterList.Add(c);
                }
            }

            letterGrid = letterList.ToArray();
            lettersInGrid = letterGrid.Length;
            lettersInRow = (int)Math.Round(Math.Sqrt(lettersInGrid)); // TODO: cope with non-square grid.  And nicer to check individual line lengths.
        }

        /// <summary>
        /// Get the (up to) 8 cell indexes for a cell's neighbours.
        /// </summary>
        /// <param name="cell"></param>
        /// <returns></returns>
        private IEnumerable<int> GetNeighbouringCells(int cell)
        {
            // TODO: store all these in an array rather than recalculating each call.

            // Left
            if (cell % lettersInRow > 0)
            {
                // Left
                yield return cell - 1;

                // Top left
                if (cell >= lettersInRow)
                    yield return cell - lettersInRow - 1;

                // Bottom left
                if (cell < lettersInGrid - lettersInRow)
                    yield return cell + lettersInRow - 1;
            }

            // Up
            if (cell >= lettersInRow)
                yield return cell - lettersInRow;

            // Right 
            if (cell % lettersInRow < (lettersInRow - 1))
            {
                // Right
                yield return cell + 1;

                // Top Right
                if (cell >= lettersInRow)
                    yield return cell - lettersInRow + 1;

                // Bottom right
                if (cell < lettersInGrid - lettersInRow - 1)
                    yield return cell + lettersInRow + 1;
            }

            // Down
            if (cell < lettersInGrid - lettersInRow)
                yield return cell + lettersInRow;
        }

        /// <summary>
        /// See if a word is contained in the grid.
        /// </summary>
        /// <param name="word">Word to seek.</param>
        /// <returns></returns>
        internal bool Contains(string word)
        {
            if (word.Length < minWordLength || word.Length > lettersInGrid)
                return false;

            ReinitialiseVisited();

            char firstLetter = word[0];

            // Loop through grid looking for a match on first letter
            // TODO: cast to char array rather than burning up lots of strings.
            int startpos = 0;
            while (startpos < lettersInGrid)
            {
                if (letterGrid[startpos] == firstLetter)
                {
                    visitedGrid[startpos] = true;

                    // See if remaining letters can be found in neighbouring cells
                    if (Matches(word.Substring(1), startpos))
                        return true;

                    visitedGrid[startpos] = false;
                }
                startpos++;
            }
            
            //If we get to here, we couldn't find a match
            return false;
        }

        /// <summary>
        /// Recursively see if we can get a match for the word provided, starting from the specified position.
        /// </summary>
        /// <param name="p"></param>
        /// <param name="startpos"></param>
        /// <returns></returns>
        private bool Matches(string word, int startpos)
        {
            if (word.Length <= 0)
                return true; // Got to the end of the word

            char firstLetter = word[0];
            foreach (char pos in GetNeighbouringCells(startpos))
            {
                if (!visitedGrid[pos] && letterGrid[pos] == firstLetter)
                {
                    visitedGrid[pos] = true;
                    if (Matches(word.Substring(1), pos)) // Check the rest of the word
                        return true;

                    visitedGrid[pos] = false;
                }
            }

            return false;
        }
    }
}
