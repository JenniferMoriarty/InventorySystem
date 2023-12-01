import pygame

# Define the Item class to represent items in the inventory
class Item:
    def __init__(self, xpos, ypos, itemName: str):
        # Initializing the position and name of the item
        self.xpos = xpos
        self.ypos = ypos
        self.itemName = itemName
        self.inventoryFrame = pygame.image.load("ItemFrame.png").convert_alpha()

    def draw(self):
        # Drawing the item's frame and name on the screen
        screen.blit(self.inventoryFrame, (self.xpos, self.ypos))
        fontObj = pygame.font.Font('freesansbold.ttf', 12)
        textSurfaceObj = fontObj.render(self.itemName, True, ((0,0,0)), None) 
        screen.blit(textSurfaceObj, (self.xpos + 15, self.ypos + 50))

    def is_point_inside(self, point):
        # Checking if a given point (mouse click) is inside this item's frame
        x, y = point
        return self.xpos <= x < self.xpos + 100 and self.ypos <= y < self.ypos + 100

    def inspecting(self, xpos, ypos, Lclicked, mouse_pos):
        # Handling the display and interaction with the Equip, Delete, and Cancel options
        Equip = pygame.image.load("Equip.png").convert_alpha()
        screen.blit(Equip, (xpos, ypos))

        Remove = pygame.image.load("Delete.png").convert_alpha()
        screen.blit(Remove, (xpos, ypos + 22))

        Cancel = pygame.image.load("Cancel.png").convert_alpha()
        screen.blit(Cancel, (xpos, ypos + 44))

        if Lclicked and mouse_pos[0] < xpos + 95 and mouse_pos[0] >= xpos:
            if mouse_pos[1] < ypos + 22 and mouse_pos[1] >= ypos:
                return "Equipped"
            elif mouse_pos[1] < ypos + 44 and mouse_pos[1] >= ypos:
                return "Delete"
            elif mouse_pos[1] < ypos + 66 and mouse_pos[1] >= ypos:
                return "Cancel"

# Initialize Pygame and set up the main display
pygame.init()
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption('InventoryShop')
clock = pygame.time.Clock()
running = True

# Initial inventory items
inventory = ["ExampleItem1", "ExampleItem2", "ExampleItem3", "ExampleItem4", "ExampleItem5", "ExampleItem6", "Item 2"]

# Create a dictionary to map Item instances to their indices in the inventory list
item_objects = {}
for i, item_name in enumerate(inventory):
    xpos = 215 - 15 + 125 * (i % 3)
    ypos = 180 + 125 * (i // 3)
    item_objects[Item(xpos, ypos, item_name)] = i

CurrentlyInspecting = False
xposTemp = 0
yposTemp = 0

# Main game loop
while running:
    # Process Pygame events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:  # Right click
            mouse_pos = pygame.mouse.get_pos()
            for item_obj, index in list(item_objects.items()):
                if item_obj.is_point_inside(mouse_pos):
                    CurrentlyInspecting = True
                    xposTemp = mouse_pos[0]
                    yposTemp = mouse_pos[1]
                    inspecting_item = item_obj
                    break

    # Fill the screen with black
    screen.fill("black")

    # Load and display the inventory UI
    inventoryFrame = pygame.image.load("InventorySprite.png").convert_alpha()
    screen.blit(inventoryFrame, (150, 75))

    # Draw each item in the inventory
    for item_obj in item_objects.keys():
        item_obj.draw()

    # Handle item inspection (Equip, Delete, Cancel)
    if CurrentlyInspecting:
        option = inspecting_item.inspecting(xposTemp, yposTemp, pygame.mouse.get_pressed()[0], pygame.mouse.get_pos())
        if option == "Cancel":
            CurrentlyInspecting = False
        elif option == "Delete":
            # Delete the item from both the inventory list and the item_objects dictionary
            del inventory[item_objects[inspecting_item]]
            del item_objects[inspecting_item]
            CurrentlyInspecting = False

    # Update the display and control the loop speed
    pygame.display.flip()
    clock.tick(60)

# End of the InventoryLoop function

