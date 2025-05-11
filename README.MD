Software was tested with
------------------------
Browser: Chrome Version 126.0.6478.127
Python 3.10.9

URL: http://127.0.0.1:8000

Start Server on command line
----------------------------
pip install -r requirements.txt
cd restserver
python manage.py runserver

Build and run docker container
------------------------------
docker build -t lingraphsim .
docker run -dp 8000:8000 lingraphsim

Stop docker container
---------------------
docker ps 
docker stop <container-id>

Main software packages used
---------------------------
Django
D3js
Bootstrap
JQuery
OR-Tools
SciPy

File Structure of most important files and directories
------------------------------------------------------
css                                                             - Directory for css files__
js                                                              - Directory for javascript files__
restserver                                                      - Directory of web interface for simulator__
restserver/url.py                                               - Definition of REST Endpoints__
restserver/RestPlanServe                                        - Directory for Modules and Views__
restserver/RestPlanServe/views.py                               - Definition and configuration for views__
restserver/RestPlanServe/model.py                               - Definition of Modules__
restserver/RestPlanServe/graph                                  - Direcory for LinGraph files__
restserver/RestPlanServe/graph/clustering.py                    - Source Code for grouping and merging action formulae__
restserver/RestPlanServe/graph/examples.py                      - Different predefined examples__
restserver/RestPlanServe/graph/graph.py                         - Main LinGraph Algorithm, is callable from path restserver/__
restserver/RestPlanServe/graph/fSearch_multiple_or-tools.py     - Path for the Source obtainable at https://github.com/sitar42/LinGraph/blob/87ec3cc5191670cf1f90d87fec7e43528fd22eeb/fSearch_multiple_or-tools.py__
restserver/RestPlanServe/graph/measure.py                       - Source code for similarity and distance functions__
restserver/RestPlanServe/graph/optimize.py                      - Source Code for weighting and pruning__
restserver/RestPlanServe/graph/plangenerator.py                 - Generates random plans__
restserver/RestPlanServe/graph/test.py                          - Testing different modules of the source code __
restserver/RestPlanServe/templates                              - Direcory for Interface of simulator__
restserver/RestPlanServe/templates/graphInterface.html          - Template for running graph with different options__
restserver/RestPlanServe/templates/output.html                  - Template for analysing and modifying graph__
output                                                          - Directory for generated files LinGraph Algorithm with optimisation__

