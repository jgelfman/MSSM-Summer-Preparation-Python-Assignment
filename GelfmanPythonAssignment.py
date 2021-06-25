# Python Assignment for MSSM Preparation - Jonathan Gelfman

import pandas as pd
import csv


#####################################
# TASK 1 - Separate Movie IDs and Movie names
#####################################

# Read CSV
tempRatingsInput = pd.read_csv('./InputFiles/RatingsInput.csv')

# Split into the two columns
tempRatingsInput[['MovieID', 'MovieName']] = tempRatingsInput.MovieName.str.split(',', expand=True)

# Create new format CSV
tempRatingsInput.to_csv('./OutputFiles/Task1.csv', index=False)


#####################################
# TASK 2 - String Capitalization 
# Capitalizing the first letter of every word in the movie names
#####################################

# Titlize every entry in MovieName column
tempRatingsInput[['MovieName']] = tempRatingsInput.MovieName.str.title()

# Create new format CSV
tempRatingsInput.to_csv('./OutputFiles/Task2.csv', index=False)


#####################################
# TASK 3 - Read in from your new CSV file from Task 2 and parse data into lists and dictionaries
#####################################

dictInput = pd.read_csv('./OutputFiles/Task2.csv')
dictInput.drop(columns=dictInput.columns[0])

# Create list of all entries
all = []
with open('./OutputFiles/Task2.csv', "r") as task2:
    reader = csv.reader(task2)
    for r in reader:
        all.append(r)

# Remove headers
all.pop(0)

# Prepare outer ages dictionary
ages = []
for a in range(len(all)):
    ages.append(all[a][2])

# Prepare inner rankings dictionaries and append to ages
agesDict = {}
for row in range(len(all)):
    thisrow = all[row]

    # What age is this person
    age = int(thisrow[2])
    ageRatings = {}

    # Work on films for this rating
    rating = int(thisrow[5])
    film = str(thisrow[4])
    thisratingFilms = {}
    
    try:
        if rating not in agesDict[age].keys():
            # Initialize new rating and its first film
            thisratingFilms = {rating : [film]}

            # Append rating to age
            ageRatings.update(thisratingFilms)

        else:
            # Append film to existing rating
            agesDict[age][rating].append(film)


    except KeyError:
        # Debugging first rating added for age
        firstFilmForAge = {rating : [film]}
        ageRatings.update(firstFilmForAge)

    # Append to age
    if age not in agesDict:
        agesDict[age] = ageRatings
    else:
        agesDict[age].update(ageRatings)


#####################################
# TASK 4 - Find the recommended movies for a given age from best to worst ratings
#####################################

# Approximation function in case input age does not exist
def approx(d, inpt):
    # Make sorted temp list of ages
    templ = list()
    for k in d.keys(): templ.append(k)
    templ.sort()

    # Retrieve existing upper and lower available ages
    lentempl = len(templ)
    upbnd = lentempl - 1
    for k in range(lentempl):
        if inpt == templ[k]:
            rtNum = inpt
            break
        else:
            if int(inpt) > int(templ[k]) and k < upbnd: 
                pass
            else:
                # In case input is higher than any available age
                if k <= upbnd:
                    rtNum = templ[k]
                    break
                else:
                    rtNum = templ[k - 1]
                    break
    
    return rtNum


# Main function for reocmmending films
def ageRecommendations(inputAge, maxNfilms):
    # Figure out closest age in case of age mismatch:
    inputAge = int(inputAge)

    agesPresent = agesDict.keys()
    if inputAge not in agesPresent:
        age = approx(agesDict, inputAge)
# Commented for Task 5, but uncomment for better UI
#        print("(No data for ratings by users aged " + str(inputAge) + ", displaying ratings by users of closest age " + str(age) + " instead.) \n\n")

    else:
        age = inputAge

# Commented for Task 5, but uncomment for better UI
#    # Print clarification
#    print("Movies with a rating of 4 and above, \n" + "as rated by other users of age " + str(age) + ": \n")
    
    # Work on films
    whichFilms = []
    for r in agesDict[age]:
        # Recommend movies only with ratings 4 and above
        if r >= 4:
            for f in agesDict[age].get(r):
                whichFilms.append(f)

    # Display only specific amount of films as specified
    lengthReturntMovies = len(whichFilms)

    maxNfilms = int(maxNfilms)
    NFilms = lengthReturntMovies - maxNfilms

    returnMovies = []
    # If user specifies to display more than there are films with a good rating, simply return all films rated 4 and above
    if NFilms < 0:
        for i in whichFilms[0 : lengthReturntMovies]:
            returnMovies.append(i)
    else:
        for i in whichFilms[NFilms : lengthReturntMovies]:
            returnMovies.append(i)


    # Figure out right order to display
    returnMovies.reverse()
# Commented for Task 5, but uncomment for better UI
#    for i in returnMovies: 
#        print(str(i) + "\n")
    return returnMovies



#####################################
# TASK 5 - Recommend movies to users in the second input file
#####################################

# Read CSV
NewUsersData = []
with open('./InputFiles/NewUsers.csv', "r") as task5:
    reader = csv.reader(task5)
    for r in reader:
        NewUsersData.append(r)

# Remove headers
NewUsersData.pop(0)

ProcessedNewUsers = NewUsersData
for NewUser in range(len(ProcessedNewUsers)):
    
    # Copy name, age, and films amount
    NewUserName = ProcessedNewUsers[NewUser][0]
    NewUserAge = ProcessedNewUsers[NewUser][1]
    NewUserNFilms = ProcessedNewUsers[NewUser][2]

    # Replace question marks with films
    films = ageRecommendations(NewUserAge, NewUserNFilms)

    for f in films:
        if ProcessedNewUsers[NewUser][3] != '?':
            ProcessedNewUsers[NewUser][3] += ", " + str(f)
        else:
            ProcessedNewUsers[NewUser][3] = str(f)

# Write the new processed CSV
with open('./OutputFiles/Task5.csv', 'w') as f:
    writer = csv.writer(f)
    for r in ProcessedNewUsers:
        writer.writerow(r)
    f.close()

