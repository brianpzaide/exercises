package seamcarving

import java.awt.image.BufferedImage
import java.io.File
import javax.imageio.ImageIO
import kotlin.math.sqrt

const val End1 = -1
const val End2 = -2
const val Vertical = 1
/*
fun createRectWithDiagonalsAndSaveImg(w: Int, h: Int, filename: String) {
    val bufferedImage = BufferedImage(w, h, BufferedImage.TYPE_INT_RGB)
    val g = bufferedImage.graphics

    g.color = Color.black
    g.drawRect(0, 0, w - 1, h - 1)
    g.color = Color.red
    g.drawLine(0, 0, w - 1, h - 1)
    g.drawLine(0, h - 1, w - 1, 0)

    ImageIO.write(bufferedImage, "png", File(filename))
}

fun createNegativeImg(input: String, output: String) {
    val inputImage = ImageIO.read(File(input))
    val height = inputImage.height
    val width = inputImage.width
    var rgb: Int
    for (i in 0 until height) {
        for(j in 0 until width) {
            rgb = inputImage.getRGB(j, i)

            inputImage.setRGB(j, i, ((255 - ((rgb shr 16) and 0xFF)) shl 16) or (255 - (rgb and 0xFF)) or ((255 - (rgb shr 8 and 0xFF)) shl 8))
        }
    }
    ImageIO.write(inputImage, "png", File(output))


}

fun computeEnergyIntensityForImage(input: String, output: String) {
    val image = ImageIO.read(File(input))
    val height = image.height
    val width = image.width


    val colorDiffArrayForPixels = Array(height){Array(width) { DoubleArray(2) {0.0} } }

    // Computing energy for the inner pixels
    for (y in 1 until height-1) {
        for (x in 1 until width-1) {
            colorDiffArrayForPixels[y][x] = doubleArrayOf(computeDeltaXSquare(image, x, y), computeDeltaYSquare(image, x, y))//doubleArrayOf(computeDeltaXSquare(image, x, y), computeDeltaYSquare(image, x, y))
        }
    }

    // computing energy for top row excluding the corners
    for (x in 1 until width-1) {
        colorDiffArrayForPixels[0][x] = doubleArrayOf(computeDeltaXSquare(image, x, 0), colorDiffArrayForPixels[1][x][1])
    }

    // computing energy for bottom row excluding the corners
    for (x in 1 until width-1) {
        colorDiffArrayForPixels[height - 1][x] = doubleArrayOf(computeDeltaXSquare(image, x, height - 1), colorDiffArrayForPixels[height - 2][x][1])
    }

    // computing energy for left col excluding the corners
    for (y in 1 until height-1) {
        colorDiffArrayForPixels[y][0] = doubleArrayOf(colorDiffArrayForPixels[y][1][0], computeDeltaYSquare(image, 0, y))
    }

    // computing energy for right col excluding the corners
    for (y in 1 until height-1) {
        colorDiffArrayForPixels[y][width - 1] = doubleArrayOf(colorDiffArrayForPixels[y][width - 2][0], computeDeltaYSquare(image, width - 1, y))
    }

    // Top Left Corner
    colorDiffArrayForPixels[0][0] = doubleArrayOf(colorDiffArrayForPixels[0][1][0], colorDiffArrayForPixels[1][0][1])

    // Top Right Corner
    colorDiffArrayForPixels[0][width - 1] = doubleArrayOf(colorDiffArrayForPixels[0][width - 2][0], colorDiffArrayForPixels[1][width - 1][1])

    // Bottom Left Corner
    colorDiffArrayForPixels[height - 1][0] = doubleArrayOf(colorDiffArrayForPixels[height - 1][1][0], colorDiffArrayForPixels[height - 2][0][1])

    // Bottom Right Corner
    colorDiffArrayForPixels[height - 1][width - 1] = doubleArrayOf(colorDiffArrayForPixels[height - 1][width - 2][0], colorDiffArrayForPixels[height - 2][width - 1][1])


    val energyArrayPixels = Array(height)
    { i ->
        Array(width) { j ->
            sqrt((colorDiffArrayForPixels[i][j][0] + colorDiffArrayForPixels[i][j][1]))
        }
    }

    var maxEnergy = 0.0
    for (y in 0 until height) {
        for (x in 0 until width) {
            //maxEnergy = maxOf(maxEnergy, energyArrayPixels[y][x])
            if (maxEnergy < energyArrayPixels[y][x]) {
                maxEnergy = energyArrayPixels[y][x]
            }

        }
    }

    val intensityArrayPixels = Array(height)
    { i ->
        Array(width) { j ->
            (255.0 * energyArrayPixels[i][j] / maxEnergy).toInt()
        }
    }

    for (i in 0 until height) {
        for(j in 0 until width) {
            image.setRGB(j, i, (intensityArrayPixels[i][j] shl 16) or intensityArrayPixels[i][j] or (intensityArrayPixels[i][j] shl 8))
        }
    }
    ImageIO.write(image, "png", File(output))
}
*/
fun computeDeltaXSquare(image: BufferedImage, x: Int, y: Int): Double {
    val next: Int = if (x == image.width -1) {
        0
    } else{
        x + 1
    }
    val prev: Int = if (x == 0) {
        image.width-1
    } else {
        x-1
    }
    val rgbXPrev = image.getRGB(prev, y)
    val rgbXNext = image.getRGB(next, y)

    val redXPrev = ((rgbXPrev shr 16) and 0xFF)
    val redXNext = ((rgbXNext shr 16) and 0xFF)
    val greenXPrev = ((rgbXPrev shr 8) and 0xFF)
    val greenXNext = ((rgbXNext shr 8) and 0xFF)
    val blueXPrev = (rgbXPrev and 0xFF)
    val blueXNext = (rgbXNext and 0xFF)

    return ((redXNext-redXPrev)*(redXNext-redXPrev) + (greenXNext-greenXPrev)*(greenXNext-greenXPrev) + (blueXNext-blueXPrev)*(blueXNext-blueXPrev)).toDouble()
}

fun computeDeltaYSquare(image: BufferedImage, x: Int, y: Int): Double {
    val next: Int = if (y == image.height -1) {
        0
    } else{
        y + 1
    }
    val prev: Int = if (y == 0) {
        image.height-1
    } else {
        y-1
    }

    val rgbYPrev = image.getRGB(x, prev)
    val rgbYNext = image.getRGB(x, next)

    val redYPrev = ((rgbYPrev shr 16) and 0xFF)
    val redYNext = ((rgbYNext shr 16) and 0xFF)
    val greenYPrev = ((rgbYPrev shr 8) and 0xFF)
    val greenYNext = ((rgbYNext shr 8) and 0xFF)
    val blueYPrev = (rgbYPrev and 0xFF)
    val blueYNext = (rgbYNext and 0xFF)

    return ((redYNext-redYPrev)*(redYNext-redYPrev) + (greenYNext-greenYPrev)*(greenYNext-greenYPrev) + (blueYNext-blueYPrev)*(blueYNext-blueYPrev)).toDouble()

}

// part 4
fun computeEnergyForImage(image: BufferedImage): Array<Array<Double>> {

    val height = image.height
    val width = image.width


    val colorDiffArrayForPixels = Array(height){Array(width) { DoubleArray(2) {0.0} } }

    // Computing energy for the inner pixels
    for (y in 1 until height-1) {
        for (x in 1 until width-1) {
            colorDiffArrayForPixels[y][x] = doubleArrayOf(computeDeltaXSquare(image, x, y), computeDeltaYSquare(image, x, y))//doubleArrayOf(computeDeltaXSquare(image, x, y), computeDeltaYSquare(image, x, y))
        }
    }

    // computing energy for top row excluding the corners
    for (x in 1 until width-1) {
        colorDiffArrayForPixels[0][x] = doubleArrayOf(computeDeltaXSquare(image, x, 0), colorDiffArrayForPixels[1][x][1])
    }

    // computing energy for bottom row excluding the corners
    for (x in 1 until width-1) {
        colorDiffArrayForPixels[height - 1][x] = doubleArrayOf(computeDeltaXSquare(image, x, height - 1), colorDiffArrayForPixels[height - 2][x][1])
    }

    // computing energy for left col excluding the corners
    for (y in 1 until height-1) {
        colorDiffArrayForPixels[y][0] = doubleArrayOf(colorDiffArrayForPixels[y][1][0], computeDeltaYSquare(image, 0, y))
    }

    // computing energy for right col excluding the corners
    for (y in 1 until height-1) {
        colorDiffArrayForPixels[y][width - 1] = doubleArrayOf(colorDiffArrayForPixels[y][width - 2][0], computeDeltaYSquare(image, width - 1, y))
    }

    // Top Left Corner
    colorDiffArrayForPixels[0][0] = doubleArrayOf(colorDiffArrayForPixels[0][1][0], colorDiffArrayForPixels[1][0][1])

    // Top Right Corner
    colorDiffArrayForPixels[0][width - 1] = doubleArrayOf(colorDiffArrayForPixels[0][width - 2][0], colorDiffArrayForPixels[1][width - 1][1])

    // Bottom Left Corner
    colorDiffArrayForPixels[height - 1][0] = doubleArrayOf(colorDiffArrayForPixels[height - 1][1][0], colorDiffArrayForPixels[height - 2][0][1])

    // Bottom Right Corner
    colorDiffArrayForPixels[height - 1][width - 1] = doubleArrayOf(colorDiffArrayForPixels[height - 1][width - 2][0], colorDiffArrayForPixels[height - 2][width - 1][1])


    val energyArrayPixels = Array(height)
    { i ->
        Array(width) { j ->
            sqrt((colorDiffArrayForPixels[i][j][0] + colorDiffArrayForPixels[i][j][1]))
        }
    }
/*
    // Compute the maxEnergy in the above loop
    var maxEnergy = 0.0
    for (y in 0 until height) {
        for (x in 0 until width) {
            //maxEnergy = maxOf(maxEnergy, energyArrayPixels[y][x])
            if (maxEnergy < energyArrayPixels[y][x]) {
                maxEnergy = energyArrayPixels[y][x]
            }

        }
    }

    return Array(height)
    { i ->
        Array(width) { j ->
            (255.0 * energyArrayPixels[i][j] / 1)
        }
    }
    */
    return energyArrayPixels
}

fun buildVerticalGraph(pixelIntensityMatrix: Array<Array<Double>>, width: Int, height: Int) :Graph {
    //build the vertical graph from pixel intensity matrix
    val graph = Graph()

    for (x in 0 until width) {
        graph.addEdge(End1, x, pixelIntensityMatrix[0][x])
    }
    graph.setDataForVertex(End1, Coordinates(-1, -1))

    for (y in 0 until height-1) {
        for (x in 0 until width) {
            when(x) {
                0 -> {
                    graph.addEdge(width * y + x, width * (y + 1) + x, pixelIntensityMatrix[y + 1][x])
                    graph.addEdge(width * y + x, width * (y + 1) + x + 1, pixelIntensityMatrix[y + 1][x + 1])
                }
                width - 1 -> {
                    graph.addEdge(width * y + x, width * (y + 1) + x - 1, pixelIntensityMatrix[y + 1][x - 1])
                    graph.addEdge(width * y + x, width * (y + 1) + x, pixelIntensityMatrix[y + 1][x])
                }
                else -> {
                    graph.addEdge(width * y + x, width * (y + 1) + x - 1, pixelIntensityMatrix[y + 1][x - 1])
                    graph.addEdge(width * y + x, width * (y + 1) + x, pixelIntensityMatrix[y + 1][x])
                    graph.addEdge(width * y + x, width * (y + 1) + x + 1, pixelIntensityMatrix[y + 1][x + 1])
                }
            }
            graph.setDataForVertex(width * y + x, Coordinates(x, y))
            if (y == height - 2) {
                graph.setDataForVertex(width * (y + 1) + x, Coordinates(x, y+1))
            }
        }
    }

    for (x in 0 until width) {
        graph.addEdge(width * (height - 1) + x, End2, 0.0)
    }
    graph.setDataForVertex(End2, Coordinates(-2, -2))

    return graph
}

fun buildHorizontalGraph(pixelIntensityMatrix: Array<Array<Double>>, width: Int, height: Int) :Graph {
    //build the horizontal graph from pixel intensity matrix
    val graph = Graph()

    for (y in 0 until height) {
        graph.addEdge(End1, (width * y), pixelIntensityMatrix[y][0])
    }
    graph.setDataForVertex(End1, Coordinates(-1, -1))

    for (x in 0 until width-1) {
        for (y in 0 until height) {
            when(y) {
                0 -> {
                    graph.addEdge(width * y + x, (width * y) + (x + 1), pixelIntensityMatrix[y][x + 1])
                    graph.addEdge(width * y + x, (width * (y + 1)) + (x + 1), pixelIntensityMatrix[y + 1][x + 1])
                }
                height - 1 -> {
                    graph.addEdge(width * y + x, (width * (y - 1)) + (x + 1), pixelIntensityMatrix[y - 1][x + 1])
                    graph.addEdge(width * y + x, (width * y) + (x + 1), pixelIntensityMatrix[y][x + 1])
                }
                else -> {
                    graph.addEdge(width * y + x, (width * (y - 1)) + (x + 1), pixelIntensityMatrix[y - 1][x + 1])
                    graph.addEdge(width * y + x, (width * y) + (x + 1), pixelIntensityMatrix[y][x + 1])
                    graph.addEdge(width * y + x, (width * (y + 1)) + (x + 1), pixelIntensityMatrix[y + 1][x + 1])
                }
            }
            graph.setDataForVertex(width * y + x, Coordinates(x, y))
            if (x == width - 2) {
                graph.setDataForVertex((width * y) + (x+1), Coordinates(x+1, y))
            }
        }
    }

    for (y in 0 until height) {
        graph.addEdge((width * y) + (width-1), End2, 0.0)
    }
    graph.setDataForVertex(End2, Coordinates(-2, -2))

    return graph
}

fun findShortestPath(graph: Graph, width:Int): MutableMap<Int, Int> {

    val dsp = DijkstraShortestPath()
    val sourceVertex = graph.getVertex(End1)

    val parentMap = dsp.shortestPath(graph, sourceVertex)

    val path : MutableMap<Int, Int> = HashMap()
    var parent: Vertex?
    var currVertex = graph.getVertex(End2)
    while (true){
        parent= parentMap[currVertex]
        if (parent == null) {
            break
        }
        val data = parent.getData()
        path[width*(data.y) + data.x] = 1
        //println(""+ currVertex.getData() + " -> " + parent.getData())
        currVertex = parent
    }


    return path
}

fun computeSeam(image: BufferedImage, width: Int, height: Int, direction:Int):  MutableMap<Int, Int>{

    val pixelIntensityMatrix = computeEnergyForImage(image)
    val graph: Graph
    graph = if (direction == Vertical ){
        buildVerticalGraph(pixelIntensityMatrix, width, height)
    } else{
        buildHorizontalGraph(pixelIntensityMatrix, width, height)
    }
    return findShortestPath(graph, width)
}

fun resize(image:BufferedImage, width: Int, height: Int, direction:Int): BufferedImage {



    val newImage: BufferedImage
    val newHeight: Int
    val newWidth: Int

    val path = computeSeam(image, width, height, direction)


    if (direction == Vertical ){
        newImage = BufferedImage(width-1, height, BufferedImage.TYPE_INT_RGB)
        newHeight = height
        newWidth = width - 1
    } else{
        newImage = BufferedImage(width, height-1, BufferedImage.TYPE_INT_RGB)
        newHeight = height - 1
        newWidth = width
    }

    if (direction == Vertical) {

        var i = 0
        var j = 0
        var k = 0
        while (i < newHeight) {
            for (l in 0 until width) {
                if (path[width*k +l] == null) {
                    //println("newx: $j, newy: $i, oldx: $l, oldy: $k")
                    newImage.setRGB(j, i, image.getRGB(l, k))
                    j += 1
                }
            }
            k += 1
            i += 1
            j = 0
        }
    } else {
        var i = 0
        var j = 0
        var l = 0
        while (j < newWidth) {
            for (k in 0 until height) {
                if (path[width*k +l] == null) {
                    //println("newx: $j, newy: $i, oldx: $l, oldy: $k")
                    newImage.setRGB(j, i, image.getRGB(l, k))
                    i += 1
                }
            }
            l += 1
            j += 1
            i = 0
        }
    }

    return newImage
}


fun main(args: Array<String>) {
    val input = args[args.indexOf("-in") + 1]
    val output = args[args.indexOf("-out") + 1]
    val verticalSeams = args[args.indexOf("-width") + 1].toInt()
    val horizontalSeams = args[args.indexOf("-height") + 1].toInt()

    var image = ImageIO.read(File(input))

    for(i in 0 until verticalSeams) {
        image = resize(image, image.width, image.height, 1)
    }

    for(i in 0 until horizontalSeams) {
        image = resize(image, image.width, image.height, 0)
    }

    ImageIO.write(image, "png", File(output))

    /*
    val image = ImageIO.read(File(input))
    val newImage = ImageIO.read(File(output))
    println("newH: ${newImage.height} oldH: ${image.height} newW: ${newImage.width}  oldW: ${image.width}")
    */

}
