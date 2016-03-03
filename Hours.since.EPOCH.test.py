__author__ = 'Bat Cave'
from datetime import datetime


X = 1419811199038
type(X)
print(X)  # Fri, 02 Jan 2015 20:33:53 + milliseconds
EPOCH = (X / (15 * 60 * 1000)) * (15 * 60) + (15*60)
print(EPOCH)            # Fri, 02 Jan 2015 20:00:00

print("\nNext\n")

X = 1419811199038
type(X)
print(X)  # Fri, 02 Jan 2015 20:33:53 + milliseconds
EPOCH = (X / (30 * 60 * 1000)) * (30 * 60) + (30*60)
print(EPOCH)            # Fri, 02 Jan 2015 20:00:00

print("\nNext\n")

X = 1419811199038
type(X)
print(X)  # Fri, 02 Jan 2015 20:33:53 + milliseconds
EPOCH = (X / (60 * 60 * 1000)) * (60 * 60) + (60*60)
print(EPOCH)            # Fri, 02 Jan 2015 20:00:00

diff = 1420412400 - 1419807600
print(diff / (60 * 60))