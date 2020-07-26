# Hittegods-matchmaker

This program will match one entry x with parameters x_1, x_2 ... x_n against a dataset with corresponding parameters 
y_1, y_2 .. y_n. Both the single entry 'x' and the dataset 'data' are separate pandas dataframes. It will then write 
the best scores to a database where they will be used for other things by other programs.

![Alt text](./PythonBackend.png?raw=true "Matching flowchart and process")

## Datastructure and what is compared

The program will only compare columns, referred to earlier as parameters x_i, with column labels exactly equal to
the column names in the ./Constants/columnLabels.txt csv file. It will ignore parameters from columns with names 
not in the csv file.

## Comparisons

The program is modelled with the idea of data as coordinates in n-dimensional Euclidian space in mind, however
it is hard to implement properly with datatypes such as color or transport line, as one can't simply subtract
a string with one color from another and expect the result to represent their distance in Euclidian space.

As a result, with the cosine-similarity as a reference where two entries are scored between -1 and +1 in similarity, 
the parameters of each entry are compared and returns a value between 0 and 1, depending on how similar they are. Here,
0 is representing no similarity, and 1 is representing completely similar. 

Each datatype has a separate comparison function in comparison.py, which will be deterministic or probabilistic
depending on the nature of the type. When each parameter of one entry x, and one entry from the dataset data have been 
compared, they are put in an array of similarity scores for each pair of the parameters like for example [1, 0, 0.5]. 

The comparisons are somewhat intelligent, for instance the text recognition is somewhat smart, capable of matching 'Apple phone'
with 'iPhone 7s' even though the strings are different. However, the comparisons aren't overly sophisticated to the 
point where it impacts performance.

##Weights

Then, weights are applied to each score in the similarity array. The weights are set dynamically for each entry 
comparison, and can be adjusted with the weights matrix.

####How to adjust  weights:

The weight matrix is found in ./Constants/weightMatrix.txt, and can be adjusted by editing the file. Each cell in
the matrix will in turn be part of a weighted sum, so for a 10x10 matrix, increasing one cell from 1 to 2 will only
increase the overall score by a factor 2/(10*10). 

####Conditional weights
Let's say we have columns x_1 and x_2, and we want to differ how it is weighted depending on whether x_1 is a match, 
x_2 is match, neither is a match or both are a match. Then we have 4 sets of cases:

[++, +-, -+, --]

Where + represents it being a match, and - represents it not being a match. To cover all possible cases with its own
weight, one can construct a following set of matrices:

M(++):[1,1;1,1],M(+-):[1,1;1,1],M(-+):[1,1;1,1],M(--):[1,1;1,1],

Where the columns [x_1,x_2] and the wors are [x_1,x_2].

Now, let's say we want to adjust the weight of x_1 where x_1 and x_2 is a match, then we can adjust the matrix M(++) 
such that:

M(++):[1,2;2,1] = M(++):[1,4;1,1]

for a total of 4 times the original neutral weight. 

Note that each wight will inevitably be represented two places as both [x_1,x_2] and [x_2,x_1].

Chains of conditions can be constructed to fit specific cases where for instance [x_1,x_2] and [x_2,x_3] is adjusted, 
causing x_1 and x_3 to have a correlation through x_2.

## Weighted sum
After all the weights have been applied, the score values with weights are summed and divided by the maximum possible 
sum of scores and weights for the set of weights and scores given. As such, the final score will be a number between 
0 and 1, and will be analogous to a percentage of similarity, making it easy to compare matches with different 
weights and parameters. 

## Writing to database
The n number of matches with a higher score than some threshold (0.55 currently) will be written to the relation
database for further use. 

