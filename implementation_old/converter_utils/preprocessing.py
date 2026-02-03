from pm4py import PetriNet
from pm4py.algo.analysis.workflow_net import algorithm as wf_eval


def validate_workflow_net(net: PetriNet):
    places_no_incoming = [p for p in net.places if not p.in_arcs]
    if len(places_no_incoming) == 1:
        start_place = places_no_incoming[0]
    else:
        raise Exception(f"Not a WF-net!")

    places_no_outgoing = [p for p in net.places if not p.out_arcs]
    if len(places_no_outgoing) == 1:
        end_place = places_no_outgoing[0]
    else:
        raise Exception(f"Not a WF-net!")

    if not wf_eval.apply(net):
        raise Exception(f"Not a WF-net!")

    return start_place, end_place