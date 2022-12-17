Requirements
============

Non-functional
--------------

Accessability
^^^^^^^^^^^^^
The user interface should be accessible to the color-blind. There are a variety of different types of colorblind. Inorder to cover them all we will use industry best practices for designing with color blind users in mind. This includes:

- Use patterns and textures to show contrast in the Map
- Use colors and symbols to convey meaning
- Add text labels when necessary
- Avoiding green-red and blue-purple color combinations

Testability
^^^^^^^^^^^
The code should have comprehensive test cases for both friend and and back end where possible. User testing should be used when normal unit testing does not fit (i.e., accessible design).

Readability
^^^^^^^^^^^
The code should prioritize clearly communicating its intent.

Documentation
^^^^^^^^^^^^^
The code should use some tool for documenting the front-end and back-end code with inline function comments when necessary (i.e., pydoc, jsdoc).

Function
--------

- Find the shortest path between two addresses.
- Find the path between two addresses that satisfies x% longer than the shortest route and whether to minimize or maximize elevation.
- Cache elevation and map data locally to decrease runtimes and avoid the cost of touching the Google Elevation API frequntly.
- Front-end and back-end must use the MVC architecture pattern

