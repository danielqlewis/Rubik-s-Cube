from enum import Enum

WHITE = 0
YELLOW = 5
GREEN = 1
BLUE = 4
RED = 2
ORANGE = 3


class FaceSection(Enum):
    TOP = 0
    LEFT = 1
    RIGHT = 2
    BOTTOM = 3


class CubeFace:
    Rotation_Permutation = [6, 3, 0, 7, 4, 1, 8, 5, 2]
    Section_Dict = {
        FaceSection.TOP: [2, 1, 0],
        FaceSection.LEFT: [0, 3, 6],
        FaceSection.RIGHT: [8, 5, 2],
        FaceSection.BOTTOM: [6, 7, 8]
    }

    def __init__(self, value):
        self.squares = [value for _ in range(9)]

    def rotate(self):
        temp = self.squares.copy()
        for i in range(9):
            self.squares[i] = temp[self.Rotation_Permutation[i]]

    def swap_section(self, section, new_info=None):
        section_indices = self.Section_Dict[section]
        output_info = [self.squares[section_indices[x]] for x in range(3)]

        if new_info is not None:
            for x in range(3):
                self.squares[section_indices[x]] = new_info[x]

        return output_info


class RubiksCube:
    def __init__(self):
        self.faces = [CubeFace(x) for x in range(6)]

    def move_sections(self, face_list, section_list):
        section_info_hold = None
        for i in range(5):
            active_face = self.faces[face_list[i % 4]]
            active_section = section_list[i % 4]
            section_info_hold = active_face.swap_section(active_section, section_info_hold)

    def get_modified_faces(self, face):
        active_faces = [x for x in range(6) if x != face and x + face != 5]
        active_faces[-1], active_faces[-2] = active_faces[-2], active_faces[-1]
        if face % 2 == 0:
            active_faces.reverse()
        return active_faces

    def get_modified_sections(self, face):
        if face in [0, 5]:
            sections = [FaceSection.BOTTOM if face == 0 else FaceSection.TOP] * 4
        elif face in [1, 4]:
            sections = {1: [FaceSection.TOP, FaceSection.RIGHT, FaceSection.BOTTOM, FaceSection.LEFT],
                        4: [FaceSection.RIGHT, FaceSection.TOP, FaceSection.LEFT, FaceSection.BOTTOM]}[face]
        else:
            middle_sections = {2: FaceSection.LEFT, 3: FaceSection.RIGHT}[face]
            sections = [FaceSection.RIGHT, middle_sections, middle_sections, FaceSection.LEFT]
        return sections

    def rotate_clockwise(self, face):
        self.faces[face].rotate()
        active_faces = self.get_modified_faces(face)
        sections = self.get_modified_sections(face)
        self.move_sections(active_faces, sections)

    def move(self, face, clockwise=True):
        rotation_limit = {True: 1, False: 3}[clockwise]
        for _ in range(rotation_limit):
            self.rotate_clockwise(face)
