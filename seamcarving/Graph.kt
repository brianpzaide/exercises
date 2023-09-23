package seamcarving

import java.util.*
import kotlin.collections.HashMap
import kotlin.collections.set

class Coordinates(var x: Int, var y: Int) {

    override fun toString(): String {
        return "Coordinates(x=$x, y=$y)"
    }
}


class Graph {
    private val edges: MutableList<Edge>
    private val vertices: MutableMap<Int, Vertex>

    fun getVertex(id: Int): Vertex {
        return vertices[id]!!
    }

    fun addEdge(id1: Int, id2: Int, weight: Double) {
        val v1: Vertex
        if (vertices.containsKey(id1)) v1 = vertices[id1]!! else {
            v1 = Vertex(id1)
            vertices[id1] = v1
        }
        val v2: Vertex
        if (vertices.containsKey(id2)) v2 = vertices[id2]!! else {
            v2 = Vertex(id2)
            vertices[id2] = v2
        }
        val edge = Edge(v1, v2, weight)
        edges.add(edge)
        v1.addAdjacentVertex(edge, v2)
    }

    private fun getAllEdges(): List<Edge> {
        return edges
    }

    fun getAllVertices(): Collection<Vertex>{
        return vertices.values
    }


    fun setDataForVertex(id: Int, data: Coordinates) {
        if (vertices.containsKey(id)) {
            val v = vertices[id]!!
            v.setData(data)
        }
    }

    override fun toString(): String {
        val buffer = StringBuffer()
        for (edge in getAllEdges()) {
            buffer.append(edge.vertex1.toString() + " " + edge.vertex2 + " " + edge.weight)
            buffer.append("\n")
        }
        return buffer.toString()
    }

    init {
        edges = ArrayList()
        vertices = HashMap()
    }
}

class Edge(v1: Vertex, v2: Vertex, var weight: Double) {

    var vertex1: Vertex = v1
    var vertex2: Vertex = v2

    override fun equals(other: Any?): Boolean {
        if (this === other) return true
        if (other == null) return false
        if (this.javaClass != other.javaClass) return false
        val otherObj = other as Edge
        if (vertex1 != otherObj.vertex1) return false
        if (vertex2 != otherObj.vertex2) return false
            return true
    }

    override fun toString(): String {
        return ("Edge [Vertex1 = " + vertex1 + " , Vertex2 = " + vertex2
                + " , weight = " + weight + " ]")
    }
}

class Vertex(var id: Int) {
    private lateinit var vertexData: Coordinates

    private val edges: MutableList<Edge> = ArrayList()
    private val adjacentVertex: MutableList<Vertex> = ArrayList()

    fun getData():Coordinates {
        return this.vertexData
    }
    fun setData(vertexData: Coordinates) {
        this.vertexData = vertexData
    }

    fun addAdjacentVertex(e: Edge, v: Vertex) {
        edges.add(e)
        adjacentVertex.add(v)
    }

    override fun toString(): String {
        return vertexData.toString()
    }

    fun getEdges(): List<Edge> {
        return edges
    }

    override fun equals(other: Any?): Boolean {
        if (this === other) return true
        if (other == null) return false
        if (this.javaClass != other.javaClass) return false
        val otherObj = other as Vertex
        return id == otherObj.id
    }
}
