from enum import Enum

# Face color constants mapped to integers 0-5
# These constants create a mapping between the virtual cube and physical cube faces
WHITE = 0    # Maps to white face on physical cube
YELLOW = 5   # Maps to yellow face on physical cube
GREEN = 1    # Maps to green face on physical cube
BLUE = 4     # Maps to blue face on physical cube
RED = 2      # Maps to red face on physical cube
ORANGE = 3   # Maps to orange face on physical cube


class FaceSection(Enum):
    """
    Defines the four possible sections of a cube face that can be affected by moves.
    These sections represent the three squares along each edge of a face.
    """
    TOP = 0    # Top three squares of a face: [2, 1, 0]
    LEFT = 1   # Left three squares of a face: [0, 3, 6]
    RIGHT = 2  # Right three squares of a face: [8, 5, 2]
    BOTTOM = 3 # Bottom three squares of a face: [6, 7, 8]


class CubeFace:
    """
    Represents a single face of the Rubik's cube.
    
    Each face is represented as a list of 9 values (squares) indexed as follows:
    0 1 2
    3 4 5
    6 7 8
    
    The orientation of each face is critical:
    - For faces 1-4 (Green, Red, Orange, Blue): Yellow (5) is considered "up"
    - For face 5 (Yellow): Blue (4) is considered "up"
    - For face 0 (White): Green (1) is considered "up"
    
    This consistent orientation system allows the rotation and section operations
    to work correctly across all faces.
    """
    
    # Defines how square indices change during a clockwise rotation
    # e.g., square at index 6 moves to index 2, 3 to 7, etc.
    Rotation_Permutation = [6, 3, 0, 7, 4, 1, 8, 5, 2]
    
    # Maps each face section to the indices of squares in that section
    Section_Dict = {
        FaceSection.TOP: [2, 1, 0],      # Top edge squares
        FaceSection.LEFT: [0, 3, 6],     # Left edge squares
        FaceSection.RIGHT: [8, 5, 2],    # Right edge squares
        FaceSection.BOTTOM: [6, 7, 8]    # Bottom edge squares
    }

    def __init__(self, value):
        """
        Initialize a face with all squares set to the same value.
        
        Args:
            value (int): The value (0-5) representing the face's color
        """
        self.squares = [value for _ in range(9)]

    def rotate(self):
        """
        Performs a clockwise rotation of the face by rearranging square values
        according to the Rotation_Permutation pattern.
        """
        temp = self.squares.copy()
        for i in range(9):
            self.squares[i] = temp[self.Rotation_Permutation[i]]

    def swap_section(self, section, new_info=None):
        """
        Retrieves or updates a section (edge) of the face.
        
        Args:
            section (FaceSection): Which section of the face to access
            new_info (list[int], optional): If provided, updates the section with these values
        
        Returns:
            list[int]: The values from the requested section (before any updates)
        """
        section_indices = self.Section_Dict[section]
        output_info = [self.squares[section_indices[x]] for x in range(3)]

        if new_info is not None:
            for x in range(3):
                self.squares[section_indices[x]] = new_info[x]

        return output_info


class RubiksCube:
    """
    Represents a complete Rubik's cube with six faces.
    
    The cube maintains proper face relationships and handles moves that affect
    multiple faces. Face orientation is maintained according to the system where:
    - Faces 1-4 (Green, Red, Orange, Blue) have Yellow (5) as their top
    - Face 5 (Yellow) has Blue (4) as its top
    - Face 0 (White) has Green (1) as its top
    """

    def __init__(self):
        """
        Initialize a solved Rubik's cube where each face has all squares
        set to its corresponding color value (0-5).
        """
        self.faces = [CubeFace(x) for x in range(6)]

    def move_sections(self, face_list, section_list):
        """
        Performs a circular movement of sections between faces.
        
        This method handles the transfer of edge values between faces during a move,
        maintaining proper cube relationships.
        
        Args:
            face_list (list[int]): List of face indices involved in the move
            section_list (list[FaceSection]): List of sections to swap for each face
        """
        section_info_hold = None
        for i in range(5):
            active_face = self.faces[face_list[i % 4]]
            active_section = section_list[i % 4]
            section_info_hold = active_face.swap_section(active_section, section_info_hold)

    def get_modified_faces(self, face):
        """
        Determines which faces are affected when the given face is rotated.
        
        Args:
            face (int): The face being rotated
            
        Returns:
            list[int]: Ordered list of face indices that need section updates
        """
        active_faces = [x for x in range(6) if x != face and x + face != 5]
        active_faces[-1], active_faces[-2] = active_faces[-2], active_faces[-1]
        if face % 2 == 0:
            active_faces.reverse()
        return active_faces

    def get_modified_sections(self, face):
        """
        Determines which sections of adjacent faces need to be swapped when
        the given face is rotated.
        
        Args:
            face (int): The face being rotated
            
        Returns:
            list[FaceSection]: Ordered list of sections that need to be swapped
        """
        if face in [0, 5]:  # White or Yellow face
            sections = [FaceSection.BOTTOM if face == 0 else FaceSection.TOP] * 4
        elif face in [1, 4]:  # Green or Blue face
            sections = {1: [FaceSection.TOP, FaceSection.RIGHT, FaceSection.BOTTOM, FaceSection.LEFT],
                       4: [FaceSection.RIGHT, FaceSection.TOP, FaceSection.LEFT, FaceSection.BOTTOM]}[face]
        else:  # Red or Orange face
            middle_sections = {2: FaceSection.LEFT, 3: FaceSection.RIGHT}[face]
            sections = [FaceSection.RIGHT, middle_sections, middle_sections, FaceSection.LEFT]
        return sections

    def rotate_clockwise(self, face):
        """
        Performs a single clockwise quarter turn of the specified face.
        
        This includes rotating the face itself and updating all affected
        sections of adjacent faces.
        
        Args:
            face (int): The face to rotate
        """
        self.faces[face].rotate()
        active_faces = self.get_modified_faces(face)
        sections = self.get_modified_sections(face)
        self.move_sections(active_faces, sections)

    def move(self, face, clockwise=True):
        """
        Performs a move on the specified face.
        
        Args:
            face (int): The face to move
            clockwise (bool): If True, performs a clockwise quarter turn.
                            If False, performs a counterclockwise quarter turn
                            (implemented as three clockwise turns)
        """
        rotation_limit = {True: 1, False: 3}[clockwise]
        for _ in range(rotation_limit):
            self.rotate_clockwise(face)
