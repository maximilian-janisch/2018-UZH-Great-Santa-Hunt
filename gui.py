"""
GUI
Author: Atsuhiro Funatsu
"""

import PyQt5.QtWidgets as Wid
import PyQt5.Qt as Qt

class Santa_GUI(Wid.QMainWindow):
    
    def __init__(self):
        """Initialises the class 'Santa_GUI'."""
        
        super().__init__()
        
        self.setWindowTitle('Visualisation (Santa)')
        self.resize(800, 800)
        self.show()
        
        self.p = Qt.QPainter()
        self.p.begin(self)
        
    def plot_santa_house(self, world):
        """Plots Santa's house into the map.
        
        Args:
            world: An instance of the class 'World', describing the world.
        """
                
        # body
        self.p.setBrush(Qt.QColor(255, 0, 0))
        self.p.drawRect(world.scale*(world.santa_house.center[0]-world.N/40),
                        world.scale*(world.santa_house.center[1]-world.N/40),
                        world.scale*world.N/20,
                        world.scale*world.N/20)
        # roof
        self.p.setBrush(Qt.QColor(0, 0, 0))
        self.p.drawLine(world.scale*(world.santa_house.center[0]-world.N/40),
                        world.scale*(world.santa_house.center[1]-world.N/40),
                        world.scale*(world.santa_house.center[0]+world.N/40),
                        world.scale*(world.santa_house.center[1]+world.N/40))
        self.p.drawLine(world.scale*(world.santa_house.center[0]+world.N/40),
                        world.scale*(world.santa_house.center[1]-world.N/40),
                        world.scale*(world.santa_house.center[0]-world.N/40),
                        world.scale*(world.santa_house.center[1]+world.N/40))
        
    def plot_resources(self, world):
        """Plots resource locations into the map.
        
        Args:
            world: An instance of the class 'World', describing the world.
        """
        
        for location in world.locations:
            self.p.setBrush(Qt.QColor(
                world.colours[location.resource.name][0],
                world.colours[location.resource.name][1],
                world.colours[location.resource.name][2]))
            self.p.drawEllipse(
                world.scale*(location.center[0]-location.radius),
                world.scale*(location.center[1]-location.radius),
                world.scale*location.radius*2,
                world.scale*location.radius*2)
    
    def plot_kids_houses(self, world):
        """Plots kids' houses into the map.
        
        Args:
            world: An instance of the class 'World', describing the world.
        """
        
        for house in world.kids_houses: # todo: change house colour once toy is delivered
            self.p.setBrush(Qt.QColor(0, 0, 0))
            self.p.drawRect(world.scale*(house.center[0]-house.size/2),
                            world.scale*(house.center[1]-house.size/2),
                            world.scale*house.size,
                            world.scale*house.size)
    
    def plot_deers(self, world):
        """Plots deers into the map.
        
        Args:
            world: An instance of the class 'World', describing the world.
        """
        
        for deer in world.deers:
            if deer.loaded == 0:
                self.p.setBrush(Qt.QColor(0, 0, 0))
            else:
                self.p.setBrush(Qt.QColor(178, 34, 34))
            self.p.drawEllipse(world.scale*deer.position[0]-5,
                               world.scale*deer.position[1]-5,
                               10,
                               10)
    
    def plot_markers(self, world):
        """Plots markers into the map.
        
        Args:
            world: An instance of the class 'World', describing the world.
        """

        self.p.setOpacity(0.2)
        for marker in world.markers:
            self.p.setBrush(Qt.QColor(
                world.colours[marker.location.resource.name][0],
                world.colours[marker.location.resource.name][1],
                world.colours[marker.location.resource.name][2]))
            self.p.drawLine(world.scale*marker.endpoint[0],
                            world.scale*marker.endpoint[1],
                            world.scale*marker.startpoint[0],
                            world.scale*marker.startpoint[1])
        self.p.setOpacity(1.0)
            
    def plot_invariable_objects(self, world):
        """Plots invariable objects into the map.
        
        Plots Santa's house.
        
        Args:
            world: An instance of the class 'World', describing the world.
        """
                
        self.plot_santa_house(world)
        
    def plot_variable_objects(self, world):
        """Plots variable objects into the map.
        
        Plots resources, kids' houses, deers and markers.
        
        Args:
            world: An instance of the class 'World', describing the world.
        """
        
        self.plot_resources(world)
        self.plot_kids_houses(world)
        self.plot_deers(world)
        self.plot_markers(world)
        
    def clear_world(self):
        """Clears the map."""
        
        self.p.eraseRect(0, 0, 800, 800)
        
    def update_world(self, world):
        """Updates map.
        
        Plots resources, kids' houses, deers and markers.
        
        Args:
            world: An instance of the class 'World', describing the world.
        """
        
        self.clear_world()
        self.plot_invariable_objects(world)
        self.plot_variable_objects(world)
#        Wid.QApplication.processEvents()