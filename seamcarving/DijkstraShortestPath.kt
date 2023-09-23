package seamcarving


class DijkstraShortestPath {
    fun shortestPath(graph: Graph, sourceVertex: Vertex): Map<Vertex, Vertex?> {

        //heap + map data structure
        val minHeap = BinaryMinHeap()

        //stores shortest distance from root to every vertex
        val distance: MutableMap<Vertex, Double> = HashMap()

        //stores parent of every vertex in shortest distance
        val parent: MutableMap<Vertex, Vertex?> = HashMap()

        //initialize all vertex with infinite distance from source vertex
        for (vertex in graph.getAllVertices()) {
            minHeap.add(Double.MAX_VALUE, vertex)
        }

        //set distance of source vertex to 0
        minHeap.decrease(sourceVertex, 0.0)

        //put it in map
        distance[sourceVertex] = 0.0

        //source vertex parent is null
        parent[sourceVertex] = null

        //iterate till heap is not empty
        while (!minHeap.empty()) {
            //get the min value from heap node which has vertex and distance of that vertex from source vertex.
            val heapNode: BinaryMinHeap.Node = minHeap.extractMinNode()
            val current = heapNode.key

            //update shortest distance of current vertex from source vertex
            distance[current] = heapNode.weight

            //iterate through all edges of current vertex
            for (edge in current.getEdges()) {

                //get the adjacent vertex
                val adjacent: Vertex = getVertexForEdge(current, edge)

                //if heap does not contain adjacent vertex means adjacent vertex already has shortest distance from source vertex
                if (!minHeap.containsData(adjacent)) {
                    continue
                }

                //add distance of current vertex to edge weight to get distance of adjacent vertex from source vertex
                //when it goes through current vertex
                val newDistance = distance[current]!! + edge.weight

                //see if this above calculated distance is less than current distance stored for adjacent vertex from source vertex
                if (minHeap.getWeight(adjacent)!! > newDistance) {
                    minHeap.decrease(adjacent, newDistance)
                    parent[adjacent] = current
                }
            }
        }
        return  /*distance*/parent
    }

    private fun getVertexForEdge(v: Vertex, e: Edge): Vertex {
        return if (e.vertex1.equals(v)) e.vertex2 else e.vertex1
    }


}