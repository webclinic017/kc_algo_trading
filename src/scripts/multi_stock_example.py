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