import multiprocessing as mp


class Communication(mp.Process):
    def __init__(self):
        mp.Process.__init__(self)
        self.in_soc = mp.Queue()
        self.out = mp.Queue()
        self.ready = mp.Queue()

    def get_queue(self):
        """ returns frontend, backend, ready """
        return self.in_soc, self.out, self.ready

    def set_agents(self, agents_backend):
        self.agents_backend = agents_backend


    def run(self):
        agents_finished, total_number = 0, 0
        total_number_known = False
        self.ready.put('working')
        try:
            while True:
                msg = self.in_soc.get()
                #cprint (msg, '%i/%i' % (agents_finished, total_number))
                if msg == '.':
                    agents_finished += 1
                    if agents_finished == total_number:
                        agents_finished, total_number = 0, 0
                        total_number_known = False
                        self.ready.put('.')
                elif msg[0] == '+':
                    try:
                        total_number += int(msg[1])  # for speed, if a string
                    except ValueError:               # is send Communication
                        return                       # is ended
                elif msg[1] == 'all':
                        for agent in self.agents_backend['all'][msg[0]]:
                            agent.put(msg[2:])
                else:
                    self.agents_backend[msg[0]][msg[1]].put(msg[2])
        except KeyboardInterrupt:
                print('KeyboardInterrupt: _Communication: Waiting for messages %i/%i' % (agents_finished, total_number))
