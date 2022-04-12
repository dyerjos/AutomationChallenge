# Notes

## The challenge details

- Cartesian 2d grid

- origin is upper left

- coordinates increase going down and right

- coordinates have one decimal place `(0.0, 0.0)`

- each instruction of the laser requires a target coordinate `G01 X2.00 Y1.00` followed immediately by a line to toggle the laser on/off `M01`

- in grid, `.` represent untouched grid square and `X` represents a cut

- **euclidean distance of <= 0.5 from the center of the respective square** which means that the laser can move diagonally and that needs to be taken into account

- program should always terminate by toggling laser off and returning to origin (0.0,0.0)

- laser moves at a rate of 1 unit per second

- setup test to confirm my program follows correct time tracking method
    - traveling straight from (0.0, 0.0) to (3.0, 0.0) takes 3.0 seconds
        - manhattan distance of 3
    - traveling straight from (0.0, 0.0) to (3.0, 4.0) takes 5.0 seconds
    - travel time is purely Euclidean distance

- 1.0 second for every `M01` command

- the program's input must be a string like the visualized "result" below:
    ```
    X....
    .XX..
    ..XX.
    ....X
    ```
    - our program therefore must parse this string and convert it into a 2d cartesian graph

## Euclidean distance in Python:

```python
import math

p = [0.0, 0.0]
q = [3.0, 4.0]
print (math.dist(p, q))
output: 5.0
```

```
math.dist(p, q):
    Return the Euclidean distance between two points p and q, each given as a sequence (or iterable) of coordinates. The two points must have the same dimension.

    Roughly equivalent to:
    sqrt(sum((px - qx) ** 2.0 for px, qx in zip(p, q)))

    New in version 3.8.
```

## Assumptions

- machine is smart enough to go from a source coordinate to a target coordinate
- in a real world project we would need to know more details on what the output of this program should look like and about memory constraints

## Rough Process

1. User inputs a string like so:
    ```
    X....
    .XX..
    ..XX.
    ....X
    ```

2. Program parses this string
    - We can now determine grid dimensions
    - We can determine cut mark coordinates
        - store these known cut mark coordinates

3. Using starting position of laser cutter (0.0, 0.0) we will essentially be setting up an indexed priority queue of nodes with Dijkstra's algorithm or A* for order of target coordinates and when to toggle laser on/off
    - if there are strict memory requirements, we can reduce the amount of memory by limiting number of nodes put on the priority queue
        - use collections.deque?
    - these instructions will be output including an instruction to make sure laser is toggled off at the end and returned to origin:
        ```
        M01
        G01 X4.0 Y3.0
        M01
        G01 X0.0 Y0.0
        ```
        - for simplicity sake, maybe commands are an tuple of strings so that another program can iterate through the commands one by one and we can insure immutability

## Extra Ideas
- [ ] Make a command to Generate a blank grid programmatically.

    This could then be used to test larger scale grids

    ```shell
    $ laser_program_generator new_grid --rows 5 --col 9

    output:
    .........
    .........
    .........
    .........
    .........
    ```

- [ ] Make a command to Generate a grid programmatically with a random output pattern.

    This could then be used to test larger scale grids without manually placing cut marks

    ```shell
    $ laser_program_generator new_grid --rows 5 --col 9 --cuts 6

    output:
    .........
    .........
    .........
    .........
    .........
    ```