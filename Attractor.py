import igraph, cairocffi

g=igraph.Graph.Read_Ncol("net.txt")
igraph.plot(g)
g.write_svg("attractor.svg", vertex_size=10)

