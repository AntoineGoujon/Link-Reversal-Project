# -*- generated by 1.0.13 -*-
import da
PatternExpr_192 = da.pat.ConstantPattern('REV')
PatternExpr_196 = da.pat.FreePattern('sender')
PatternExpr_224 = da.pat.ConstantPattern('NOP')
PatternExpr_228 = da.pat.FreePattern('sender')
PatternExpr_244 = da.pat.ConstantPattern('ACK')
PatternExpr_248 = da.pat.FreePattern('sender')
_config_object = {}

class Agent(da.DistProcess):

    def __init__(self, procimpl, props):
        super().__init__(procimpl, props)
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_AgentReceivedEvent_0', PatternExpr_192, sources=[PatternExpr_196], destinations=None, timestamps=None, record_history=None, handlers=[self._Agent_handler_191]), da.pat.EventPattern(da.pat.ReceivedEvent, '_AgentReceivedEvent_1', PatternExpr_224, sources=[PatternExpr_228], destinations=None, timestamps=None, record_history=None, handlers=[self._Agent_handler_223]), da.pat.EventPattern(da.pat.ReceivedEvent, '_AgentReceivedEvent_2', PatternExpr_244, sources=[PatternExpr_248], destinations=None, timestamps=None, record_history=None, handlers=[self._Agent_handler_243])])

    def setup(self, in_neighbours, out_neighbours, isDest, **rest_554):
        super().setup(in_neighbours=in_neighbours, out_neighbours=out_neighbours, isDest=isDest, **rest_554)
        self._state.in_neighbours = in_neighbours
        self._state.out_neighbours = out_neighbours
        self._state.isDest = isDest
        self._state.msg_count = 0
        self._state.ack_count = 0
        self._state.neighbours = (self._state.in_neighbours + self._state.out_neighbours)
        self._state.links_to_reverse = []

    def run(self):
        while True:
            if ((len(self._state.out_neighbours) == 0) and (not self._state.isDest)):
                for v in self._state.neighbours:
                    self.send('REV', to=v)
                self._state.links_to_reverse = self._state.neighbours
            else:
                for v in self._state.neighbours:
                    self.send('NOP', to=v)
            super()._label('_st_label_306', block=False)
            _st_label_306 = 0
            while (_st_label_306 == 0):
                _st_label_306 += 1
                if (self._state.msg_count == len(self._state.neighbours)):
                    _st_label_306 += 1
                else:
                    super()._label('_st_label_306', block=True)
                    _st_label_306 -= 1
            else:
                if (_st_label_306 != 2):
                    continue
            if (_st_label_306 != 2):
                break
            self._state.msg_count = 0
            if (not (len(self._state.links_to_reverse) == 0)):
                self.output(f'Reversing {len(self._state.links_to_reverse)}/{len(self._state.neighbours)} links')
            for v in self._state.links_to_reverse:
                if (v in self._state.in_neighbours):
                    self._state.in_neighbours.remove(v)
                    self._state.out_neighbours.append(v)
                else:
                    self._state.out_neighbours.remove(v)
                    self._state.in_neighbours.append(v)
            self._state.links_to_reverse = []
            for v in self._state.neighbours:
                self.send('ACK', to=v)
            super()._label('_st_label_399', block=False)
            _st_label_399 = 0
            while (_st_label_399 == 0):
                _st_label_399 += 1
                if (self._state.ack_count == len(self._state.neighbours)):
                    _st_label_399 += 1
                else:
                    super()._label('_st_label_399', block=True)
                    _st_label_399 -= 1
            else:
                if (_st_label_399 != 2):
                    continue
            if (_st_label_399 != 2):
                break
            self._state.ack_count = 0

    def _Agent_handler_191(self, sender):
        assert (sender in self._state.out_neighbours)
        self._state.msg_count += 1
        self.output(f"Received 'reversed' message from {sender}")
        self._state.links_to_reverse.append(sender)
    _Agent_handler_191._labels = None
    _Agent_handler_191._notlabels = None

    def _Agent_handler_223(self, sender):
        assert (sender in self._state.neighbours)
        self._state.msg_count += 1
    _Agent_handler_223._labels = None
    _Agent_handler_223._notlabels = None

    def _Agent_handler_243(self, sender):
        assert (sender in self._state.neighbours)
        self._state.ack_count += 1
    _Agent_handler_243._labels = None
    _Agent_handler_243._notlabels = None

class Node_(da.NodeProcess):

    def __init__(self, procimpl, props):
        super().__init__(procimpl, props)
        self._events.extend([])

    def run(self):
        graph = [[0, 0, 0, 0, 0, 1, 0], [1, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0], [0, 0, 1, 0, 1, 0, 0], [0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0]]
        N = len(graph[0])
        agents = list(self.new(Agent, num=N))
        for k in range(N):
            neighbors_in = [agents[i] for i in range(N) if (graph[k][i] == 1)]
            neighbors_out = [agents[i] for i in range(N) if (graph[i][k] == 1)]
            self._setup(agents[k], (neighbors_out, neighbors_in, (k == 6)))
        self._start(agents)
