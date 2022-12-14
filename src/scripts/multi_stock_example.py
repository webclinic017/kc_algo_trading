def example():
    # for every stock in my data
    for d in self.datas:

        # if no position is open on this stock
        if not self.broker.getposition(d):
            if self.inds[d]['crossover'] > 0:
                self.buy(d)

        elif self.inds[d]['crossover'] < 0:
            self.close(d)
        
        elif self.broker.getposition(d):
            timeNow = d.datetime.datetime()
            holdingTime = (timeNow - self.bar_executed.get(d._name, timeNow)).days
            if holdingTime > 100:
                self.close(d)

# ---- 

def example():
    def __init__(self):
        self.order = {}
        for i, d in enumerate(d for d in self.datas if len(d)):
        self.order[d._name] = None

    def notify(self, order):
    # standard code for notification 
        self.order[order.data._name] = None

    def next(self):
    for i, d in enumerate(d for d in self.datas if len(d)):
        if not self.order[d._name]:
            continue