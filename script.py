import random 
import bpy

# Create list of nodes
nodeList = ["test1", "test2", "Sample random"]
print(nodeList)

# Create collections to hold nodes and links

#bpy.data.collections.new('nodes')
#bpy.data.collections.new('links')

nodCol=bpy.data.collections['nodes']
linkCol=bpy.data.collections['links']

# Link these collections to the scene

#bpy.context.scene.collection.children.link(nodCol)
#bpy.context.scene.collection.children.link(linkCol)


def setRandomPoints():
    for i in nodeList:
        # Check system terminal
        print(i)
        
        # Get random coordinates
        Z=random.randint(0,60)
        Y=random.randint(0,60)
        X=random.randint(0,60) 
        
        # Create text curve obj and set location
        textData=bpy.data.curves.new(type="FONT",name=i)
        textData.body=i
        textData.extrude=.1
        textObj = bpy.data.objects.new(i, bpy.data.curves[i])
        textObj.location=(X,Y,Z)
        
              
        # Link to node collection        
        nodCol.objects.link(textObj)
        bpy.context.view_layer.update()
        
        

def makeConnection(prompt1, prompt2):
    # Get vector coordinates of two nodes
    nodeOneLocation = nodCol.objects[prompt1].location
    nodeTwoLocation = nodCol.objects[prompt2].location

    # Creating links between nodes

    # Creating curve data block
    curveData = bpy.data.curves.new('linkLine', type='CURVE')
    curveData.dimensions = '3D'
    curveData.fill_mode="FULL"
    curveData.extrude=0.4
    curveData.bevel_depth = 0.9

    # Smoothness of the segments on the curve.
    curveData.resolution_u = 20
    curveData.render_resolution_u = 32
    curveData.resolution_u = 2
    
    # Map coords to spline
    polyLine = curveData.splines.new('POLY')
    
    # Determine number of random jumps between nodes
    randomJumps=random.randint(1,16)
    polyLine.points.add(randomJumps-1)
    for i in range(0,randomJumps):
        if i==0:
            x,y,z = nodeOneLocation        
        elif i==randomJumps-1:
            x,y,z = nodeTwoLocation
        else:
            z=random.randint(0,60)
            y=random.randint(0,60)
            x=random.randint(0,60) 

        polyLine.points[i].co = (x, y, z, 1)
        
    # Create Object
    linkLineName="Linking" + prompt1 + prompt2
    linkLine = bpy.data.objects.new(linkLineName, curveData)

    
    
    # # Creating a group
    # groupName = "Linking" + prompt1 + prompt2
    # group = bpy.data.collections.new(groupName)
    # group.objects.link(linkLine)
    # group.objects.link(nodCol.objects[prompt1])
    # group.objects.link(nodCol.objects[prompt2])
    # bpy.context.scene.collection.children.link(group)
    
    
    # Link to collection
    setNodeLineColour(linkLine)
    linkCol.objects.link(linkLine)
    bpy.context.view_layer.update()

def setNodeLineColour(line):
    # current = bpy.context.object
    mat = bpy.data.materials.new(name='Material')
    # Assign a diffuse color to the material.
    mat.diffuse_color = (random.randint(1,90), random.randint(1,20), random.randint(1,20), random.randint(1,90))
    mat.specular_intensity=0.1
    line.data.materials.append(mat)    

# Function calls
setRandomPoints()
makeConnection("test1","test2")