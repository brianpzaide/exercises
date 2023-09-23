package seamcarving

import java.util.*
import kotlin.collections.HashMap
import kotlin.collections.MutableList
import kotlin.collections.MutableMap
import kotlin.collections.set


class BinaryMinHeap {
    private val allNodes: MutableList<Node> = ArrayList<Node>()
    private val nodePosition: MutableMap<Vertex, Int> = HashMap()

    inner class Node {
        var weight = 0.0
        lateinit var key: Vertex
    }

    fun containsData(key: Vertex): Boolean {
        return nodePosition.containsKey(key)
    }

    fun add(weight: Double, key: Vertex) {
        val node = Node()
        node.weight = weight
        node.key = key
        allNodes.add(node)
        val size = allNodes.size
        var current = size - 1
        var parentIndex = (current - 1) / 2
        nodePosition[node.key] = current
        while (parentIndex >= 0) {
            val parentNode: Node = allNodes[parentIndex]
            val currentNode: Node = allNodes[current]
            if (parentNode.weight > currentNode.weight) {
                swap(parentNode, currentNode)
                updatePositionMap(parentNode.key, currentNode.key, parentIndex, current)
                current = parentIndex
                parentIndex = (parentIndex - 1) / 2
            } else {
                break
            }
        }
    }


    fun min(): Vertex {
        return allNodes[0].key
    }


    fun empty(): Boolean {
        return allNodes.size == 0
    }


    fun decrease(vertex: Vertex, newWeight: Double) {
        var position = nodePosition[vertex]!!
        allNodes[position].weight = newWeight
        var parent = (position - 1) / 2
        while (parent >= 0) {
            if (allNodes[parent].weight > allNodes[position].weight) {
                swap(allNodes[parent], allNodes[position])
                updatePositionMap(allNodes[parent].key, allNodes[position].key, parent, position)
                position = parent
                parent = (parent - 1) / 2
            } else {
                break
            }
        }
    }

    fun getWeight(key: Vertex): Double? {
        val position = nodePosition[key]
        return if (position == null) null else allNodes[position].weight
    }


    fun extractMinNode(): Node {
        var size = allNodes.size - 1
        val minNode = Node()
        minNode.key = allNodes[0].key
        minNode.weight = allNodes[0].weight
        val lastNodeWeight = allNodes[size].weight
        allNodes[0].weight = lastNodeWeight
        allNodes[0].key = allNodes[size].key
        nodePosition.remove(minNode.key)
        nodePosition.remove(allNodes[0].key)
        nodePosition[allNodes[0].key] = 0
        allNodes.removeAt(size)
        var currentIndex = 0
        size--
        while (true) {
            val left = 2 * currentIndex + 1
            var right = 2 * currentIndex + 2
            if (left > size) {
                break
            }
            if (right > size) {
                right = left
            }
            val smallerIndex = if (allNodes[left].weight <= allNodes[right].weight) left else right
            currentIndex = if (allNodes[currentIndex].weight > allNodes[smallerIndex].weight) {
                swap(allNodes[currentIndex], allNodes[smallerIndex])
                updatePositionMap(allNodes[currentIndex].key, allNodes[smallerIndex].key, currentIndex, smallerIndex)
                smallerIndex
            } else {
                break
            }
        }
        return minNode
    }


    fun extractMin(): Vertex {
        val node: Node = extractMinNode()
        return node.key
    }

    private fun printPositionMap() {
        println(nodePosition)
    }

    private fun swap(node1: Node, node2: Node) {
        val weight = node1.weight
        val data = node1.key
        node1.key = node2.key
        node1.weight = node2.weight
        node2.key = data
        node2.weight = weight
    }

    private fun updatePositionMap(vertex1: Vertex, vertex2: Vertex, pos1: Int, pos2: Int) {
        nodePosition.remove(vertex1)
        nodePosition.remove(vertex2)
        nodePosition[vertex1] = pos1
        nodePosition[vertex2] = pos2
    }

    fun printHeap() {
        for (n in allNodes) {
            println(n.weight.toString() + " " + n.key)
        }
    }

}