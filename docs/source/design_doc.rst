Design Doc
==========

**The Semicolon Coders: Elevation Aware Navigation**

Date: 12/16/2022

Written By: Logan Mimaroglu, Jiachang Situ

Introduction
------------
This project enables a user to determine the shortest path between two points or optimize by other heuristics such as elevation or distance or a combination of both.

System Overview
---------------
The program is broken into a front end and a back end. The backend is responsible for taking in a series of arguments in the form of a JSON object and returning a patch that best matches these arguments in the form of a JSON object. The front end makes a call to this API and visualizes the route returned by the backend.

Design Considerations
---------------------

Assumptions and Dependencies
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- For performance reasons, the routable space is limited to Piedmont, California, USA or an otherwise similary sized graph (in terms of nodes and edges).
- Open Street Maps is needed to get map data, Google Elevation API is used to elevation data, and NetworkX is used for performing basic graph functions (i.e., shortest path with weight of length).

General Constraints
^^^^^^^^^^^^^^^^^^^
Backend must store elevation data from Google Maps API to reduce monetary costs. Backend must also store the map data to reduce load on Open Street Map servers as per their request.

Goals
^^^^^

The program must adhere to the functional and non-functional requirements defined in requirements.rst.

Development Methods
^^^^^^^^^^^^^^^^^^^
The MVC architecture design pattern will be used to structure the code. The waterfall method will be used for the development process.

System Design
-------------

For detailed system design documentation please refer to backend.rst.

Routing Algorithm
^^^^^^^^^^^^^^^^^

The high-level overview of our routing algorithm is that we will compute all of the paths between two nodes. Then, we will compute the average absolute grade across all of these paths (grade is like the steepness of the route, absolute grade would mean that we don't care about the direction of the steepness). Order the paths by there grade. Then pick the route that is x% longer than the shortest distance.

This algorithm design has a number of hurdles that needed to be overcome.

First off, even in "small" graphs (<500 nodes) a computational explosion occurs when trying to find the all paths. To resolve this issue we needed to find some logic for determining a cutoff. Our solution was that we actually know the theoretical maximum length of the optimal path. Since we know how many nodes are in the shortest path, we know the length of the shortest edge in the entire graph, and we know the desired distance, we can compute the number of nodes that will be in the optimal path:

{desired distance}/{shortest edge} = maximum number of nodes

Secondly, the OSMNX does not automatically store elevation data. Without elevation data for every node we cannot compute and edges grade. By using the Google Elevation API we are able to attach elevation data to every node. Then using an OSMNX built in function we are able to compute the grade and absolute grade and add them it as a key-value pair to every edge in the graph.

Endpoints
^^^^^^^^^

There is only a single endpoint:

/route | POST | JSON object

This endpoint takes in a JSON object as documented in backend.rst and returns a JSON object which represents an array where every element is an array of size 2 where the first element is the longitude and the second element is the latitude.

