import axelrod as axl

players = (axl.RiskyQLearner(), axl.RiskyQLearner())


tournament = axl.Tournament(players)
results=tournament.play()
plot= axl.Plot(results)
p = plot.boxplot()
p.show