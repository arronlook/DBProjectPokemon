import csv
import requests

API = "https://pokeapi.co/api/v2/pokemon/"
OUTPUT = "temp.csv"

# For pokemon.csv, japanese name starts at 29th index

if __name__ == "__main__":

  # Read in all the relevant pokemon names
  with open("../pokemon.csv", "r") as file:
    csvReader = csv.DictReader(file)
    AllNames = [row["name"] for row in csvReader]

  # with open(OUTPUT, "w") as file: # Start over with empty file
  #   file.write("name\n")

  # Ask PokemonAPI for all the moves for each pokemon in AllNames
  # for name in AllNames:
  #   try:
  #     r = requests.get(url = (API + name.lower()))
  #     data = r.json()
  #     AllMoves = set([data["moves"][i]["move"]["name"] for i in range(len(data["moves"]))])
  #     print(name)
  #     with open(OUTPUT, "a") as file:
  #       file.write(name.lower())
  #       for move in AllMoves:
  #         file.write("," + move)
  #       file.write("\n")
  #   except Exception as e:
  #     print("--------\n", name, e, end="\n\n", flush=True)

  # Find the names of the missing pokemon
  with open("name-moves.csv") as file:
    csvReader = csv.DictReader(file)
    recordNames = [row["name"] for row in csvReader]
  AllNames = set(map(lambda x : x.lower(), AllNames))
  MissingPokemon = list(set(AllNames) - set(recordNames)) # Can't do anything about this

  # Find out the required length of the bitstring (# moves for the pokemon)
  AllMoves = set()
  TotalNumMoves = 0 # The number of tuples if we did it the non-bitstring way
  with open("name-moves.csv") as file:
    file.readline()
    for row in file:
      for move in row[row.find(",")+1:].split(","):
        AllMoves.add(move)
        TotalNumMoves += 1

  print(TotalNumMoves)

