from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.http import JsonResponse

from RestPlanServe.models import  GraphInterfaceForm, ShowGraphForm
from RestPlanServe.graph import graph

# from RestPlanServe.graph.graph import prove
class GraphInterfaceView( CreateView ):
    """
    View for GraphInterface 
    """
    template = "graph/graphInterface.html"
    form_class = GraphInterfaceForm

    def get( self, request, *args, **kwargs ):
        """ Get Request
            Set Default values for form variables
            Load Template
        """
        context = { 'form'                : GraphInterfaceForm(), 
                   'graph_input'          : "[('C1', 32), ('C2', 32), ('M', 48)]\n[('P', 16), ('FP', 4), ('M', 48)]\n[('Make S1',[('C1', 1),('M', 1)],[('S1', 1),('M', 1)]),('Make S2',[('C2', 1),('M', 1)],[('S2', 1),('M', 1)]),('Make P',[('S1', 1),('S2', 1),('M', 1)],[('P', 1),('M', 1)]),('Make FP',[('P', 4),('M', 1)],[('FP', 1),('M', 1)])]\n", 
                   "similarity_threshold" : 0.7, 
                   "merge_technique"      : "standard",  
                   "pruning"              : 0,
                   "value_boundry"        : 0,
                   "pruning_percentage"   : 33
                 }
        return render(request, 'graph/graphInterface.html', context)

    def post( self, request, *args, **kwargs ):
        """ POST request 
            Collect all form variables
            Run Model
            Load Template
        """

        self.form_class.runGraph( self.form_class, 
                                 request.POST.get( "graph_input", "" ), 
                                 request.POST.get( "algorithm", "new" ), 
                                 request.POST.get( "reverse","False" ), 
                                 request.POST.get( "action_combine", "" ), 
                                 request.POST.get( "distance_functions", "" ), 
                                 request.POST.get( "similarity_threshold", None ), 
                                 request.POST.get( "merge_technique", "standard" ), 
                                 request.POST.get( "weighting_method", None ), 
                                 request.POST.get( "pruning", 0 ), 
                                 request.POST.get( "pruning_type", None ), 
                                 request.POST.get( "pruning_percentage", None ), 
                                 request.POST.get( "value_boundary", False ) )
        
        context = { 'form'                  : GraphInterfaceForm(), 
                    "graph_input"           : request.POST.get( "graph_input", "" ), 
                    "graph_input"           : request.POST.get( "graph_input", "" ), 
                    "algorithm"             : request.POST.get( "algorithm", "" ), 
                    "action_combine"        : request.POST.get( "action_combine", "" ), 
                    "reverse"               : request.POST.get( "reverse", "" ), 
                    "value_boundary"        : request.POST.get( "value_boundary", "" ),
                    "distance_functions"    : request.POST.get( "distance_functions", "" ), 
                    "similarity_threshold"  : request.POST.get( "similarity_threshold", 0.7 ), 
                    "merge_technique"       : request.POST.get( "merge_technique", "standard" ), 
                    "value_boundary"        : request.POST.get( "value_boundary", False), 
                    "pruning"               : request.POST.get( "pruning", 0), 
                    "weighting_method"      : request.POST.get( "weighting_method", "" ), 
                    "pruning_type"          : request.POST.get( "pruning_type", "" ), 
                    "pruning_percentage"    : request.POST.get( "pruning_percentage", None ) 
                }
        return render( request, self.template, context )
    


class ShowGraphView( CreateView ):
    """
    View for editor (output)
    """
    template = "graph/output.html"
    form_class = ShowGraphForm

    def get( self, request, *args, **kwargs ):
        self.form_class.url = request.GET.get( "url", "" )
        context = { 'form': ShowGraphForm() }
        return render( request, self.template, context )
    
    def post( self, request, *args, **kwargs ):
        """
        Run step or run all
        """

        mode = request.GET.get( "mode", "" )

        # 1. get json
        jsonStr = request.body.decode( "utf-8" )

        # 2. integrate json
        graphInstance = graph.LinGraph()

        graphInstance.fromJson( jsonStr )

        if mode == "all":
            # 3. render all steps
            graphInstance.process()
        else:
            # 3. render next step
            graphInstance.step()
        
        result = dict()
        result[  'data'  ] = graphInstance.toJson()
        result[ 'output' ] = "\n".join( graph.output_contents )

        # 4. give json back
        return JsonResponse( result )

