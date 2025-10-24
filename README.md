This is a simple script that searches for matching elements and merges the information from two CSV files.

Instructions
  1.	Place both CSV files in the same directory as the script
  2.	When you run the script, you will be asked to select the two files
  3.	File 1 will be used as the template. Information from File 2 will be added to it
  4.	You will then be asked to select the column that contains the unique identifier for both files, and the script will try to find matches
  5.	If it finds a match, it appends the row from file 2 to the end of the corresponding row in file 1
  6.	Once complete, the script will generate two output files:
     
        o	One with the combined information.
    	
        o	One with the rows from file 2 that couldn’t be matched, allowing for manual review in case of false negative during the matching process.
