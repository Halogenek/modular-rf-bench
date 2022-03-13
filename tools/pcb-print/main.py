import sys
import pcbnew

# get the filename from arguments
# filename = sys.argv[1]
filename = "test.kicad_pcb"

# Load board and initialize plot controller
board = pcbnew.LoadBoard(filename)
pc = pcbnew.PLOT_CONTROLLER(board)
pp = pcbnew.PCB_PLOT_PARAMS()
po = pc.GetPlotOptions()
po.SetPlotFrameRef(False)
po.SetDrillMarksType(pcbnew.PCB_PLOT_PARAMS.FULL_DRILL_SHAPE)
# Where to store pcbnew plots
po.SetOutputDirectory("plot/pcbnew/")

# Set current layer
# pc.SetLayer(pcbnew.F_Cu)

# Plot single layer to file
# pc.OpenPlotfile("front_copper", pcbnew.PLOT_FORMAT_SVG, "front_copper")
# print("Plotting to " + pc.GetPlotFileName())
# pc.PlotLayer()
# pc.ClosePlot()

# plot_plan = [
#     ( "CuTop", pcbnew.F_Cu, "Top layer" ),
#     ( "CuBottom", pcbnew.B_Cu, "Bottom layer" ),
#     ( "PasteBottom", pcbnew.B_Paste, "Paste Bottom" ),
#     ( "PasteTop", pcbnew.F_Paste, "Paste top" ),
#     ( "SilkTop", pcbnew.F_SilkS, "Silk top" ),
#     ( "SilkBottom", pcbnew.B_SilkS, "Silk top" ),
#     ( "MaskBottom", pcbnew.B_Mask, "Mask bottom" ),
#     ( "MaskTop", pcbnew.F_Mask, "Mask top" ),
#     ( "EdgeCuts", pcbnew.Edge_Cuts, "Edges" ),
# ]

plot_plan = [
    ( "CuTop", pcbnew.F_Cu, "Top layer" ),
    ( "SilkTop", pcbnew.F_SilkS, "Silk top" ),
    # ( "MaskTop", pcbnew.F_Mask, "Mask top" ),
    ( "EdgeCuts", pcbnew.Edge_Cuts, "Edges" ),
]

for layer_info in plot_plan:
    pc.SetLayer(layer_info[1])
    pc.OpenPlotfile(layer_info[0], pcbnew.PLOT_FORMAT_SVG, layer_info[2])
    pc.PlotLayer()

pc.ClosePlot()



# # This is a sample Python script.
#
# # Press Shift+F10 to execute it or replace it with your code.
# # Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
#
#
# def print_hi(name):
#     # Use a breakpoint in the code line below to debug your script.
#     print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
#
#
# # Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     print_hi('PyCharm')
#
# # See PyCharm help at https://www.jetbrains.com/help/pycharm/
