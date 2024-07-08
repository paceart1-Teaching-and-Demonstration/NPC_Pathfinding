import pygame as py


class NPCs:
    def __init__(self, screen):
        self.screen = screen
        # list of type tuple
        self.npc_list = []

    def add_npc(self, npc, color: tuple = (255, 255, 255)):
        """

        :param npc:
        :param color:
        :return:
        """
        self.npc_list.append((npc, color))

    def set_npc_list(self, npcs: list, color: tuple = (255, 255, 255)):
        """

        :param npcs:
        :param color:
        :return:
        """
        self.npc_list = []
        for n in npcs:
            self.npc_list.append((n, color))

    def draw_npcs(self):
        """

        :return:
        """
        rad = 5
        for n in self.npc_list:
            py.draw.circle(self.screen, n[1], n[0].location, rad)
            border_col = (0, 0, 0)
            py.draw.circle(self.screen, border_col, n[0].location, rad, width=1)


class NodeOverlay:
    def __init__(self, screen, game_map):
        self.screen = screen
        self.game_map = game_map

    def draw_overlay(self):
        """

        :return:
        """
        # draw nodes

        node_size = 6
        for n in self.game_map.Nodes:
            if self.game_map.Nodes[n].is_key:
                c = (255, 255, 255)
            else:
                c = (200, 0, 0)
            node_loc = self.game_map.Nodes[n].location
            py.draw.circle(self.screen, c, node_loc, node_size)

            # draw connections
            for neighbor in self.game_map.Nodes[n].neighbors:
                neighbor_loc = self.game_map.Nodes[neighbor].location
                py.draw.line(self.screen, c, node_loc, neighbor_loc)


class Background:
    def __init__(self, screen, game_map):
        self.screen = screen
        self.game_map = game_map
        self.background_image = py.image.load(self.game_map.background_file).convert()
        ow = self.background_image.get_width()
        oh = self.background_image.get_height()
        self.display_width = screen.get_width()
        self.display_height = screen.get_height()

        bg_scaled_height = (self.display_width / ow) * oh
        self.background_image = py.transform.scale(self.background_image, (self.display_width, bg_scaled_height))

    def draw_outside_block(self):
        """

        :return:
        """
        py.draw.rect(self.screen,
                     (0, 0, 0),
                     (0, self.background_image.get_height()-10,
                      self.display_width,
                      self.display_height-self.background_image.get_height()))

    def draw_background(self):
        """

        :return:
        """
        self.screen.blit(self.background_image, (0, 0))


class GraphicsManager:
    def __init__(self, screen, game_map):
        self.npc_graphics = NPCs(screen)
        self.node_graphics = NodeOverlay(screen, game_map)
        self.background_graphics = Background(screen, game_map)
