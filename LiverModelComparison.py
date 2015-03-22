#!/usr/bin/python

import argparse

from vtk import vtkXMLPolyDataReader
from vtk import vtkPolyDataMapper
from vtk import vtkActor
from vtk import vtkRenderer
from vtk import vtkRenderWindowInteractor
from vtk import vtkRenderWindow
from vtk import vtkInteractorStyleTrackballCamera
from vtk import vtkLineSource
from vtk import vtkActor2D
from vtk import vtkPolyDataMapper2D
from vtk import vtkCoordinate
from vtk import vtkTextActor

scene_elements =['parenchyma','hepatic','portal','tumor']

##------------------------------------------------------------------------------
def parse_arguments():
    parser = argparse.ArgumentParser(description='Side-by-side visualization of liver models for comparison')

    parser.add_argument('-pa', type=str, dest=scene_elements[0]+'_a',
                        action='store', required=True,
                        help='Parenchyma A model (.vtp format)')

    parser.add_argument('-pb', type=str, dest=scene_elements[0]+'_b',
                        action='store',
                        required=True,
                        help='Parenchyma B model (.vtp format)')

    parser.add_argument('-ha', type=str, dest=scene_elements[1]+'_a',
                        action='store', required=True,
                        help='Hepatic A model (.vtp format)')

    parser.add_argument('-hb', type=str, dest=scene_elements[1]+'_b',
                        action='store', required=True,
                        help='Hepatic B model (.vtp format)')

    parser.add_argument('-ma', type=str, dest=scene_elements[2]+'_a',
                        action='store', required=True,
                        help='Portal A model (.vtp format)')

    parser.add_argument('-mb', type=str, dest=scene_elements[2]+'_b',
                        action='store', required=True,
                        help='Portal B model (.vtp format)')

    parser.add_argument('-ta', type=str, dest=scene_elements[3]+'_a',
                        action='store', required=True,
                        help='Tumor A model (.vtp format)')

    parser.add_argument('-tb', type=str, dest=scene_elements[3]+'_b',
                        action='store', required=True,
                        help='Tumor B model (.vtp format)')

    args = parser.parse_args()

    return args
## END parse_arguments


##------------------------------------------------------------------------------
if __name__ == '__main__':

    args = parse_arguments()

    renderer_a = vtkRenderer()
    renderer_a.SetViewport(0.0, 0.0, 0.5, 1.0)
    renderer_a.GradientBackgroundOn()
    renderer_a.SetBackground(0.7,0.7,0.9)
    renderer_a.SetBackground2(0.4,0.4,0.7)
    renderer_b = vtkRenderer()
    renderer_b.SetViewport(0.5, 0.0, 1.0, 1.0)
    renderer_b.SetActiveCamera(renderer_a.GetActiveCamera())
    renderer_b.GradientBackgroundOn()
    renderer_b.SetBackground(0.7,0.7,0.9)
    renderer_b.SetBackground2(0.4,0.4,0.7)
    render_window = vtkRenderWindow()
    render_window.AddRenderer(renderer_a)
    render_window.AddRenderer(renderer_b)
    style = vtkInteractorStyleTrackballCamera()
    render_window_interactor = vtkRenderWindowInteractor()
    render_window_interactor.SetRenderWindow(render_window)
    render_window_interactor.SetInteractorStyle(style)
    
    scene_a_readers = {}
    scene_a_mappers = {}
    scene_a_actors = {}
    scene_b_readers = {}
    scene_b_mappers = {}
    scene_b_actors = {}

    for i in scene_elements:

        ## Create and set the models readers
        scene_a_readers[i] = vtkXMLPolyDataReader()
        scene_a_readers[i].SetFileName(vars(args)[i+'_a'])

        scene_b_readers[i] = vtkXMLPolyDataReader()
        scene_b_readers[i].SetFileName(vars(args)[i+'_b'])

        scene_a_mappers[i] = vtkPolyDataMapper()
        scene_a_mappers[i].SetInputConnection(scene_a_readers[i].GetOutputPort())

        scene_b_mappers[i] = vtkPolyDataMapper()
        scene_b_mappers[i].SetInputConnection(scene_b_readers[i].GetOutputPort())

        scene_a_actors[i] = vtkActor()
        scene_a_actors[i].SetMapper(scene_a_mappers[i])

        scene_b_actors[i] = vtkActor()
        scene_b_actors[i].SetMapper(scene_b_mappers[i])

        renderer_a.AddActor(scene_a_actors[i])
        renderer_b.AddActor(scene_b_actors[i])

    #Add line dividing viewports
    line = vtkLineSource()
    line.SetPoint1(0.0, 0.0, 0.0)
    line.SetPoint2(0.0, 1.0, 0.0)
    coordinate = vtkCoordinate()
    coordinate.SetCoordinateSystemToNormalizedViewport()
    line_mapper = vtkPolyDataMapper2D()
    line_mapper.SetInputConnection(line.GetOutputPort())
    line_mapper.SetTransformCoordinate(coordinate)
    line_mapper.ScalarVisibilityOn()
    line_mapper.SetScalarModeToUsePointData()
    line_actor = vtkActor2D()
    line_actor.SetMapper(line_mapper)
    line_actor.GetProperty().SetColor(1.0,1.0,1.0)
    line_actor.GetProperty().SetLineWidth(10)
    renderer_b.AddActor2D(line_actor)

    #Add text labels
    text_a = vtkTextActor()
    text_a.GetTextProperty().SetFontSize(72)
    text_a.GetTextProperty().SetColor(0.0, 0.0, 0.0)
    text_a.SetInput("A")
    text_a.SetPosition(10,10)
    renderer_a.AddActor2D(text_a)

    #Add text labels
    text_b = vtkTextActor()
    text_b.GetTextProperty().SetFontSize(72)
    text_b.GetTextProperty().SetColor(0.0, 0.0, 0.0)
    text_b.SetInput("B")
    text_b.SetPosition(10,10)
    renderer_b.AddActor2D(text_b)

    render_window_interactor.Initialize()
    renderer_a.ResetCamera()
    render_window.Render()
    render_window_interactor.Start()

## END: if __name__ == '__main__'
