"""
This script grabs the minimum - or maximum - value for each row and returns the associated frame's index (this behaviour can be modified to adapt the script, it's inside the for loop).
It then copies the dataframe and adds another column with the index there; the original dataframe is preserved.
"""


import pandas, numpy, argparse

parser = argparse.ArgumentParser(description="Grab the min value from each row in a .csv file and add its corresponding header as an extra column.")
parser.add_argument('-i', '--input_path', type = str, required = True, help = "Path to the input .csv file.")
parser.add_argument('-o', '--output_path', type = str, required = False, help = "Path to the output .csv file.")
parser.add_argument('-m', '--minmax', type = str, required = False, help = 'Searching for the "min" or "max" value. Default is minimum.')

arg = parser.parse_args()
if arg.minmax == None:
    selector = "min"
else:
    selector = arg.minmax

# Load the dataframe, check if the first column has data (a.k.a has "ref" in the header) or is just the row index, and proceed accordingly
df = pandas.read_csv(arg.input_path)
if "ref" not in df.columns[0]:
    df = pandas.read_csv(arg.input_path, index_col=0)

valuesArray = numpy.empty(len(df.values), dtype = int)

if selector == "min":
    for i in range(len(df)):
        # Strip and splits are only to grab the refFrame's index. The numpy.where method gets the index of the minimum RMSD value for the i-th row.
        # df.columns just gets the index mentioned, but in the headers' array, and the [0] indexing is to get the shape (1,) array's data - the corresponding header.
        valuesArray[i] = df.columns[numpy.where(df.loc[i] == min(df.loc[i].values))][0].strip().split('.pdb')[0].split('Frame')[-1]

elif selector == "max":
    for i in range(len(df)):
        # Strip and splits are only to grab the refFrame's index. The numpy.where method gets the index of the minimum RMSD value for the i-th row.
        # df.columns just gets the index mentioned, but in the headers' array, and the [0] indexing is to get the shape (1,) array's data - the corresponding header.
        valuesArray[i] = df.columns[numpy.where(df.loc[i] == max(df.loc[i].values))][0].strip().split('.pdb')[0].split('Frame')[-1]

df2 = df.copy()
df2["minValues"] = valuesArray
if arg.output_path != None:
    df2.to_csv(arg.output_path)
else:
    df2.to_csv('./output.csv')