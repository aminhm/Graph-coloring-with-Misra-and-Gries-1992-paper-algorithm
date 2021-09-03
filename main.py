from copy import deepcopy


class Edge:

    def __init__(self,startVertex,endVertex,color):

        self.startVertex = startVertex
        self.endVertex = endVertex
        self.color = color



class Graph:

    def __init__(self,edges,vertices):

        self.edges = edges

        self.vertices = vertices



class Vertex:

    def __init__(self,name,d,colors):

        self.name=name
        self.d=d
        self.colors=colors


def find_cd_path(c,d,vertex,f_vertex,graph):

    i=0

    startVertex=deepcopy(vertex)

    findedEdges = []

    findedVertices = []

    findedVertices.append(startVertex)

    findedVertices[0].colors.remove(d)

    findedVertices[0].colors.append(c)

    cORd = deepcopy(d)

    while i != len(graph.edges):

        if(graph.edges[i].startVertex==startVertex.name and graph.edges[i].color==cORd):

            findedEdges.append(graph.edges[i])

            for j in range(len(graph.vertices)):

                if(graph.vertices[j].name==graph.edges[i].endVertex):

                    startVertex = deepcopy(graph.vertices[j])

                    findedVertices.append(startVertex)

                    break
            
            if(cORd == "d"):

                cORd=deepcopy(c)

                findedEdges[len(findedEdges)-1].color = c

                if(d not in findedVertices[len(findedVertices)-1].colors):

                    break

                findedVertices[len(findedVertices)-1].colors.remove(d)

                findedVertices[len(findedVertices)-1].colors.append(c)

            else:

                cORd=deepcopy(d)

                findedEdges[len(findedEdges)-1].color = d

                if(c not in findedVertices[len(findedVertices)-1].colors):

                    break
                

                findedVertices[len(findedVertices)-1].colors.remove(c)

                findedVertices[len(findedVertices)-1].colors.append(d)

            i=0

        else:

            i+=1

    isEndedWith_F=False
    
    if(startVertex.name==f_vertex.name):

        isEndedWith_F=True

        for k in range(len(findedEdges)):

            for l in range(len(graph.edges)):

                if(graph.edges[l].startVertex == findedEdges[k].startVertex and
                    graph.edges[l].endVertex == findedEdges[k].endVertex):

                    graph.edges[l] = deepcopy(findedEdges[k])

                    break

        for k in range(len(findedVertices)):

            for l in range(len(graph.vertices)):

                if(graph.vertices[l].name == findedVertices[k].name):

                    graph.vertices[l] = deepcopy(findedVertices[k])

                    break


    return [graph,isEndedWith_F]








def invertingPath(vertex,fan_edges,fan_vertices,colors,graph):

    whichCase = -1

    c = -1

    d = -1

    for i in range(len(colors)):

        if(colors[i] not in fan_vertices[len(fan_vertices)-1].colors):

            d = colors[i]

            break

    for i in range(len(colors)):

        if(colors[i] not in vertex.colors and colors[i] != d):

            c = colors[i]

            break

    for i in range(len(fan_edges)):

        if(fan_edges[i].color == d):

            whichCase=1

            break

        else:

            whichCase=0
    
    if(whichCase==0):

        res = rotatingFan(vertex,fan_edges,fan_vertices,d)

        vertex = res[0]

        fan_edges = res[1]

        fan_vertices = res[2]

    if(whichCase==1):

        res = find_cd_path(c,d,vertex,fan_vertices[0],graph)

        graph = res[0]

        isEndedWith_F = res[1]

        if(isEndedWith_F==False):

            isEdgeColored=False

            for i in range(len(colors)):

                if(colors[i] not in vertex.colors and colors[i] not in fan_vertices[0].colors):

                    isEdgeColored=True

                    fan_vertices[0].colors.append(colors[i])

                    vertex.colors.append(colors[i])

                    fan_edges[0].color = colors[i]

                    break
            if(isEdgeColored==False):

                res = rotatingFan(vertex,fan_edges,fan_vertices,d)

                vertex = res[0]

                fan_edges = res[1]

                fan_vertices = res[2]

        else:

            breakFlag=0

            for i in range(len(graph.edges)):

                for j in range(len(fan_edges)):

                    if(graph.edges[i].startVertex==fan_edges[j].startVertex
                        and graph.edges[i].endVertex == fan_edges[j].endVertex):

                        fan_edges[j] = graph.edges[i]

                        breakFlag=1

                        break

                if(breakFlag==1):

                    break

            for j in range(len(fan_vertices)):

                for i in range(len(graph.vertices)):

                    if(graph.vertices[i].name == fan_vertices[j].name):

                        fan_vertices[j] = graph.vertices[i]

                        break

            for i in range(graph.vertices):

                if(graph.vertices[i].name == vertex.name):

                    vertex = graph.vertices[i]

            res = rotatingFan(vertex,fan_edges,fan_vertices,d)

            vertex = res[0]

            fan_edges = res[1]

            fan_vertices = res[2]            
    
    return [graph,vertex,fan_edges,fan_vertices]
            


def getNeighbors(vertex,graph):

    neighbors_vertices = []

    neighbors_edges = []

    for i in range(len(graph.edges)):

        if(graph.edges[i].startVertex == vertex.name):

            for j in range(len(graph.vertices)):

                if(graph.vertices[j].name==graph.edges[i].endVertex):

                    neighbors_vertices.append(graph.vertices[j])

                    break

            neighbors_edges.append(graph.edges[i])

        elif(graph.edges[i].endVertex == vertex.name):

            for j in range(len(graph.vertices)):

                if(graph.vertices[j].name==graph.edges[i].startVertex):

                    neighbors_vertices.append(graph.vertices[j])

                    break

            neighbors_edges.append(graph.edges[i])

    return [neighbors_vertices,neighbors_edges]



def createFan(vertex,graph,colors):

    fan = getNeighbors(vertex,graph)

    fan_neighbor_vertices = fan[0]

    fan_neighbor_edges = fan[1]

    empty_fan_edge_added = False

    fan_edges = []

    fan_vertices = []

    i=0

    vertex_index=0

    while i != len(fan_neighbor_edges):

        if(empty_fan_edge_added==False):

            if(fan_neighbor_edges[i].color == 0):

                fan_edges.append(fan_neighbor_edges[i])

                fan_vertices.append(fan_neighbor_vertices[i])

                fan_neighbor_edges.remove(fan_neighbor_edges[i])

                fan_neighbor_vertices.remove(fan_neighbor_vertices[i])

                empty_fan_edge_added=True

                i=0
            
            else:

                i+=1

        else:

            if(fan_neighbor_edges[i].color != 0 and fan_neighbor_edges[i].color not in fan_vertices[vertex_index].colors):

                fan_edges.append(fan_neighbor_edges[i])

                fan_vertices.append(fan_neighbor_vertices[i])

                fan_neighbor_edges.remove(fan_neighbor_edges[i])

                fan_neighbor_vertices.remove(fan_neighbor_vertices[i])
                
                i=0

                vertex_index+=1

            else:
                i+=1


    if(len(fan_edges)==0):

        return graph


    if(len(fan_edges)==1):

        for i in range(len(colors)):

            if(colors[i] not in fan_vertices[0].colors):

                fan_edges[0].color = colors[i]

                fan_vertices[0].colors.append(colors[i])

                graph.vertices[graph.vertices.index(vertex)].colors.append(colors[i])

                break

    else:

        res = invertingPath(vertex,fan_edges,fan_vertices,colors,graph)

        graph = res[0]

        vertex = res[1]

        fan_edges = res[2]

        fan_vertices = res[3]

    for i in range(len(graph.vertices)):

        if(graph.vertices[i].name == vertex.name):

            graph.vertices[i] = vertex

            break


    for i in range(len(fan_edges)):

        for j in range(len(graph.edges)):

            if(graph.edges[j].startVertex == fan_edges[i].startVertex and graph.edges[j].endVertex == fan_edges[i].endVertex):

                graph.edges[j] = fan_edges[i]

                break

        for j in range(len(graph.vertices)):

            if(graph.vertices[j].name == fan_vertices[i].name):

                graph.vertices[j] = fan_vertices[i]

                break

    return graph




def rotatingFan(vertex,fan_edges,fan_vertices,d):

    for i in range(len(fan_edges)-1):

        fan_edges[i].color = fan_edges[i+1].color

        fan_vertices[i].colors.append(fan_edges[i+1].color)

        fan_vertices[i+1].colors.remove(fan_edges[i+1].color)

    fan_edges[len(fan_edges)-1].color = d

    fan_vertices[len(fan_vertices)-1].colors.append(d)

    vertex.colors.append(d)

    return [vertex,fan_edges,fan_vertices]


def main():
    numberOfVertexAndEdges = input()
    numberOfVertex = int(numberOfVertexAndEdges.split(" ")[0])
    numberOfEdges = int(numberOfVertexAndEdges.split(" ")[1])
    graph = Graph([],[])
    delta = -1
    vertices = []
    for i in range(numberOfEdges):
        edge_input = input()
        edge = Edge(edge_input.split(" ")[0],edge_input.split(" ")[1],0)
        graph.edges.append(edge)
        vertices.append(edge.startVertex)
        vertices.append(edge.endVertex)

    vertices.sort()

    for i in range(numberOfVertex):
        graph.vertices.append(Vertex(vertices[i],1,[]))
        while True:
            if(len(vertices)==numberOfVertex):
                break
            if(vertices[i+1]==vertices[i]):
                graph.vertices[i].d+=1
                if(graph.vertices[i].d > delta):
                    delta = graph.vertices[i].d
                vertices.remove(vertices[i+1])
            else:
                break

    colors = []

    for i in range(delta+1):

        colors.append(i+1)

    i = 0

    while True:

        if(i==len(graph.vertices)-2):

            break

        if(len(graph.vertices[i].colors) == graph.vertices[i].d):

            i+=1

        graph = createFan(graph.vertices[i],graph,colors)

    
    print(str(delta) + " " + str(len(colors)))

    a=0

    for i in range(len(colors)):

        for j in range(len(graph.vertices)):

            if(colors[i] in graph.vertices[j].colors):

                graph.vertices[j].colors.remove(colors[i])

                if(colors[i] in graph.vertices[j].colors):

                    print("ridi",j)

                    a=1

                    break
        if(a==1):
            break


    
    for i in range(len(graph.edges)):

        print(graph.edges[i].startVertex + " " + graph.edges[i].endVertex + " " + str(graph.edges[i].color))



if __name__ == "__main__":

    main()