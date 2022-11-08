import sys
import pcbnew
import xml.etree.ElementTree as ET
import svgutils.transform as sg
# TODO factor to OOP from DDD

# get the filename from arguments
# filename = sys.argv[1]
filename = 'base.kicad_pcb'

# Where to store plots
outputPath = 'plot/'

# Settings for layers
plot_plan = [
    {
        'pcbnewSuffix': 'CuTop',
        'pcbnewLayer': pcbnew.F_Cu,
        'layerColor': '#ff933e',
        'layerStroke': '#ff933e',
        'viaColor': '#ffffff',
        'viaStroke': '#ffffff',
    },
    {
        'pcbnewSuffix': 'SilkTop',
        'pcbnewLayer': pcbnew.F_SilkS,
        'layerColor': '#000000',
        'layerStroke': '#000000',
        'viaColor': '#ffffff',
        'viaStroke': '#ffffff',
    },
    {
        'pcbnewSuffix': 'EdgeCuts',
        'pcbnewLayer': pcbnew.Edge_Cuts,
        'layerColor': '#000000',
        'layerStroke': '#000000',
        'viaColor': '#ffffff',
        'viaStroke': '#ffffff',
    },
]


def debug(string):
    print(string)


def getvalueandunit(string):
    numeric = '0123456789-.'
    for i, c in enumerate(string):
        if c not in numeric:
            break
    number = string[:i]
    unit = string[i:].lstrip()
    return number, unit


# Load board and initialize plot controller
board = pcbnew.LoadBoard(filename)
pc = pcbnew.PLOT_CONTROLLER(board)
pc.SetColorMode(True)
po = pc.GetPlotOptions()
po.SetPlotFrameRef(False)
po.SetDrillMarksType(pcbnew.PCB_PLOT_PARAMS.FULL_DRILL_SHAPE)
# Where to store pcbnew plots
po.SetOutputDirectory(outputPath)

for layer in plot_plan:
    debug("Plotting layer: "+layer['pcbnewSuffix'])
    pc.SetLayer(layer['pcbnewLayer'])
    pc.OpenPlotfile(layer['pcbnewSuffix'], pcbnew.PLOT_FORMAT_SVG, layer['pcbnewSuffix'])
    pc.PlotLayer()

# Close last plot
pc.ClosePlot()

# Modify SVG files
debug("Get board dimensions from EdgeCuts")
name = outputPath + board.GetFileName().split('.')[0] + '-' + 'EdgeCuts' + '.svg'
tree = ET.parse(name)
root = tree.getroot()
x_min = float('inf')
x_max = float('-inf')
y_min = float('inf')
y_max = float('-inf')
for child in root.findall(".//*[@d]"):
    x = float(str(child.attrib['d'][1:]).split(' ')[0])
    y = float(str(child.attrib['d'][1:]).split(' ')[1])
    if x > x_max:
        x_max = x
    if x < x_min:
        x_min = x
    if y > y_max:
        y_max = y
    if y < y_min:
        y_min = y
debug("Board dimensions: x=" + str(x_min) + "," + str(x_max) + " y=" + str(y_min) + "," + str(y_max))
for layer in plot_plan:
    debug("Modifying: " + board.GetFileName().split('.')[0] + '-' + layer['pcbnewSuffix'] + '.svg')
    name = outputPath + board.GetFileName().split('.')[0] + '-' + layer['pcbnewSuffix'] + '.svg'
    tree = ET.parse(name)
    root = tree.getroot()
    # Set image proportions and size based on EdgeCuts dimensions
    # width = str(root.get('width'))
    # width_val, unit = getvalueandunit(width)
    # height = float(width_val) * ((y_max-y_min)/(x_max-x_min))
    root.set('width', str((x_max-x_min)/100000))
    root.set('height', str((y_max-y_min)/100000))
    # root.set('height', str(height) + unit)
    root.set('viewBox', str(x_min) + " " + str(y_min) + " " + str(x_max-x_min) + " " + str(y_max-y_min))
    # Change layer color
    # Find all elements in XML with the "style" attribute
    # TODO change to iteration on particular element type as arc, line, circle (for line, via etc)
    for child in tree.findall(".//*[@style]"):
        style = str(child.get('style'))
        style = style.replace('fill:#000000', 'fill:' + layer['layerColor'], 1)
        style = style.replace('stroke:#000000', 'stroke:' + layer['layerStroke'], 1)
        style = style.replace('fill:#FFFFFF', 'fill:' + layer['viaColor'], 1)
        style = style.replace('stroke:#FFFFFF', 'stroke:' + layer['viaStroke'], 1)
        child.set('style', style)
    # Save XML/SVG
    tree.write(name)

# Stack SVG files
# TODO do it in a loop
debug("Stacking SVG files")
img = sg.fromfile(outputPath + board.GetFileName().split('.')[0] + '-' + 'CuTop' + '.svg')
img.append(sg.fromfile(outputPath + board.GetFileName().split('.')[0] + '-' + 'SilkTop' + '.svg').getroot())
img.append(sg.fromfile(outputPath + board.GetFileName().split('.')[0] + '-' + 'EdgeCuts' + '.svg').getroot())
# for layer in plot_plan:
#     layout.addSVG(outputPath + board.GetFileName().split('.')[0] + '-' + layer['pcbnewSuffix'] + '.svg', alignment=svg_stack.AlignCenter)
# doc.setLayout(layout)
img.save(outputPath + board.GetFileName().split('.')[0] + '-full.svg')