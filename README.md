# 2020electionmodel

Methodology:
1.	Cluster states be demographics to get correlation matrix (may cutoff)
a.	Census data (provisional?)
b.	Demographic:
i.	Race
ii.	Ethnicity
iii.	Age
iv.	College
v.	Urban v rural v suburban
vi.	Income per capita
vii.	Population density
c.	Method:
i.	Impute the number of clusters?
ii.	Primarily want correlation matrix
iii.	Options:
1.	GMM?
2.	K-means
2.	Polling averages
a.	Weight polls by (national vs state etc), time, quality, number of people, population type
b.	Mean-shift between states
i.	Look at window of previous data to create this average?
ii.	Take into account when the polls are within the window
iii.	Look at delta from time series value vs poll
1.	To insert data from other states, calculate its deltas from time series average at that point, adjust state data by these deltas
c.	Treat national as another state
d.	Undecided voters
i.	Data source (curated?) 
ii.	For now, scale every poll to 100%
3.	Running discrete simulations 
