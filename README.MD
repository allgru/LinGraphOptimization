LinGraph Optimization
------------------------
LinGraph is a graph-based automated planner for concurrent task planning based on linear logic by Sıtar Kortik and Uluc̣ Saranli. This repository provides an implementation of different optimization methods and a testing interface implemented with Django.

Software was tested with
------------------------
Browser: Chrome Version 126.0.6478.127 \
Python: 3.10.9  

URL: http://127.0.0.1:8000 

Start Server on command line
----------------------------
pip install -r requirements.txt \
cd restserver \
python manage.py runserver

Build and run docker container
------------------------------
docker build -t lingraphsim . \
docker run -dp 8000:8000 lingraphsim

Stop docker container
---------------------
docker ps \
docker stop #container-id#

Main software packages used
---------------------------
Django \
D3js  \
Bootstrap \
JQuery \
OR-Tools \
SciPy 

File Structure of most important files and directories
------------------------------------------------------
css                                                             - Directory for css files \
js                                                              - Directory for javascript files \
restserver                                                      - Directory of web interface for simulator \
restserver/url.py                                               - Definition of REST Endpoints \
restserver/RestPlanServe                                        - Directory for Modules and Views \
restserver/RestPlanServe/views.py                               - Definition and configuration for views \
restserver/RestPlanServe/model.py                               - Definition of Modules \
restserver/RestPlanServe/graph                                  - Direcory for LinGraph files \
restserver/RestPlanServe/graph/clustering.py                    - Source code for grouping and merging action formulae \
restserver/RestPlanServe/graph/examples.py                      - Different predefined examples \
restserver/RestPlanServe/graph/graph.py                         - Main LinGraph Algorithm, is callable from path restserver/ \
restserver/RestPlanServe/graph/fSearch_multiple_or-tools.py     - Path to the source code obtainable at https://github.com/sitar42/LinGraph/blob/87ec3cc5191670cf1f90d87fec7e43528fd22eeb/fSearch_multiple_or-tools.py \
restserver/RestPlanServe/graph/measure.py                       - Source code for similarity and distance functions \
restserver/RestPlanServe/graph/optimize.py                      - Source code for weighting and pruning \
restserver/RestPlanServe/graph/plangenerator.py                 - Generates random plans \
restserver/RestPlanServe/graph/test.py                          - Testing different modules of the source code  \
restserver/RestPlanServe/templates                              - Direcory for Interface of simulator \
restserver/RestPlanServe/templates/graphInterface.html          - Template for running graph with different options \
restserver/RestPlanServe/templates/output.html                  - Template for analysing and modifying graph \
output                                                          - Directory for generated files LinGraph Algorithm with optimisation 

Reference
------------------------------------------------------
Kortik, S. and Saranli, U., 2017. LinGraph: a graph-based automated planner for concurrent task planning based on linear logic. Applied Intelligence, 47, pp.914-934. \
https://github.com/sitar42/LinGraph/blob/87ec3cc5191670cf1f90d87fec7e43528fd22eeb/fSearch_multiple_or-tools.py
