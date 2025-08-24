class LaTeXDiagramExporter:
    """Export commutative diagrams to various LaTeX formats."""
    
    @staticmethod
    def to_tikz_cd(diagram: CommutativeDiagram, 
                   scale: float = 1.0,
                   arrow_style: str = "->",
                   node_style: str = "") -> str:
        """Export diagram to TikZ-CD format (modern LaTeX package)."""
        
        # Ensure we have positions for all objects
        if not all(obj in diagram.positions for obj in diagram.objects):
            diagram.auto_layout()
        
        # Find grid bounds
        positions = diagram.positions
        min_x = min(pos[0] for pos in positions.values())
        max_x = max(pos[0] for pos in positions.values())
        min_y = min(pos[1] for pos in positions.values())
        max_y = max(pos[1] for pos in positions.values())
        
        # Create grid
        grid = {}
        for obj, (x, y) in positions.items():
            grid[(x - min_x, y - min_y)] = obj
        
        # Start building LaTeX
        latex = "\\begin{tikzcd}[scale=" + str(scale) + "]\n"
        
        # Build grid row by row
        for y in range(max_y - min_y + 1):
            row_items = []
            for x in range(max_x - min_x + 1):
                if (x, y) in grid:
                    obj = grid[(x, y)]
                    if node_style:
                        row_items.append(f"{{{obj.name}}}")
                    else:
                        row_items.append(obj.name)
                else:
                    row_items.append("")
            
            latex += " & ".join(row_items)
            if y < max_y - min_y:
                latex += " \\\\\n"
            else:
                latex += "\n"
        
        # Add arrows
        for morph in diagram.morphisms:
            if morph.source in positions and morph.target in positions:
                src_pos = positions[morph.source]
                tgt_pos = positions[morph.target]
                
                # Calculate relative position
                rel_x = tgt_pos[0] - src_pos[0]
                rel_y = tgt_pos[1] - src_pos[1]
                
                # Convert to tikz-cd arrow notation
                arrow_dir = ""
                if rel_x > 0:
                    arrow_dir += "r" * abs(rel_x)
                elif rel_x < 0:
                    arrow_dir += "l" * abs(rel_x)
                
                if rel_y > 0:
                    arrow_dir += "d" * abs(rel_y)
                elif rel_y < 0:
                    arrow_dir += "u" * abs(rel_y)
                
                if arrow_dir:
                    # Find the row and column of source
                    src_row = src_pos[1] - min_y
                    src_col = src_pos[0] - min_x
                    
                    # Add arrow command as comment for manual insertion
                    latex += f"% Add to position ({src_row+1},{src_col+1}): \\arrow[{arrow_dir}, \"{morph.name}\"]\n"
        
        latex += "\\end{tikzcd}\n"
        
        # Add package requirements as comments
        preamble = """% Required packages:
% \\usepackage{tikz-cd}
% \\usepackage{amsmath}
% \\usepackage{amsfonts}

"""
        
        return preamble + latex
    
    @staticmethod
    def to_xy_pic(diagram: CommutativeDiagram, 
                  cell_size: str = "2em") -> str:
        """Export diagram to Xy-pic format (classic LaTeX package)."""
        
        if not all(obj in diagram.positions for obj in diagram.objects):
            diagram.auto_layout()
        
        positions = diagram.positions
        min_x = min(pos[0] for pos in positions.values())
        max_x = max(pos[0] for pos in positions.values())
        min_y = min(pos[1] for pos in positions.values())
        max_y = max(pos[1] for pos in positions.values())
        
        # Create grid
        grid = {}
        for obj, (x, y) in positions.items():
            grid[(x - min_x, y - min_y)] = obj
        
        # Start building Xy-pic
        latex = f"\\xymatrix@C={cell_size}@R={cell_size}{{\n"
        
        # Build grid
        for y in range(max_y - min_y + 1):
            row_items = []
            for x in range(max_x - min_x + 1):
                if (x, y) in grid:
                    obj = grid[(x, y)]
                    
                    # Find arrows from this object
                    arrows = []
                    for morph in diagram.morphisms:
                        if morph.source == obj and morph.target in positions:
                            tgt_pos = positions[morph.target]
                            rel_x = tgt_pos[0] - positions[obj][0]
                            rel_y = tgt_pos[1] - positions[obj][1]
                            
                            # Convert to xy-pic direction
                            if rel_x == 1 and rel_y == 0:  # right
                                arrows.append(f"\\ar[r]^{{{morph.name}}}")
                            elif rel_x == -1 and rel_y == 0:  # left
                                arrows.append(f"\\ar[l]^{{{morph.name}}}")
                            elif rel_x == 0 and rel_y == 1:  # down
                                arrows.append(f"\\ar[d]^{{{morph.name}}}")
                            elif rel_x == 0 and rel_y == -1:  # up
                                arrows.append(f"\\ar[u]^{{{morph.name}}}")
                            elif rel_x == 1 and rel_y == 1:  # down-right
                                arrows.append(f"\\ar[dr]^{{{morph.name}}}")
                            elif rel_x == -1 and rel_y == 1:  # down-left
                                arrows.append(f"\\ar[dl]^{{{morph.name}}}")
                            elif rel_x == 1 and rel_y == -1:  # up-right
                                arrows.append(f"\\ar[ur]^{{{morph.name}}}")
                            elif rel_x == -1 and rel_y == -1:  # up-left
                                arrows.append(f"\\ar[ul]^{{{morph.name}}}")
                            else:
                                # Complex arrow - use coordinates
                                arrows.append(f"\\ar@{{->}}[{rel_x},{rel_y}]^{{{morph.name}}}")
                    
                    cell_content = obj.name + "".join(arrows)
                    row_items.append(cell_content)
                else:
                    row_items.append("")
            
            latex += " & ".join(row_items)
            if y < max_y - min_y:
                latex += " \\\\\n"
            else:
                latex += "\n"
        
        latex += "}\n"
        
        # Add package requirements
        preamble = """% Required packages:
% \\usepackage[all]{xy}
% \\usepackage{amsmath}

"""
        
        return preamble + latex
    
    @staticmethod
    def to_amscd(diagram: CommutativeDiagram) -> str:
        """Export diagram to AMSmath CD format (basic, limited)."""
        
        if not all(obj in diagram.positions for obj in diagram.objects):
            diagram.auto_layout()
        
        # AMScd only supports simple rectangular diagrams
        positions = diagram.positions
        min_x = min(pos[0] for pos in positions.values())
        max_x = max(pos[0] for pos in positions.values())
        min_y = min(pos[1] for pos in positions.values())
        max_y = max(pos[1] for pos in positions.values())
        
        if max_x - min_x > 3 or max_y - min_y > 3:
            return "% AMScd format only supports up to 4x4 diagrams\n% Consider using tikz-cd or xy-pic instead\n"
        
        # Create grid
        grid = {}
        for obj, (x, y) in positions.items():
            grid[(x - min_x, y - min_y)] = obj
        
        latex = "\\begin{CD}\n"
        
        for y in range(max_y - min_y + 1):
            row_items = []
            arrow_row_items = []
            
            for x in range(max_x - min_x + 1):
                if (x, y) in grid:
                    obj = grid[(x, y)]
                    row_items.append(obj.name)
                    
                    # Look for horizontal arrow
                    h_arrow = ""
                    for morph in diagram.morphisms:
                        if (morph.source == obj and 
                            morph.target in positions and
                            positions[morph.target] == (positions[obj][0] + 1, positions[obj][1])):
                            h_arrow = f"@>{{{morph.name}}}>"
                            break
                    arrow_row_items.append(h_arrow)
                else:
                    row_items.append("")
                    arrow_row_items.append("")
            
            # Add object row
            latex += " & ".join(row_items) + " \\\\\n"
            
            # Add arrow row (if not last row)
            if y < max_y - min_y:
                v_arrows = []
                for x in range(max_x - min_x + 1):
                    v_arrow = ""
                    if (x, y) in grid:
                        obj = grid[(x, y)]
                        for morph in diagram.morphisms:
                            if (morph.source == obj and 
                                morph.target in positions and
                                positions[morph.target] == (positions[obj][0], positions[obj][1] + 1)):
                                v_arrow = f"@VV{{{morph.name}}}V"
                                break
                    v_arrows.append(v_arrow)
                
                latex += " & ".join(v_arrows) + " \\\\\n"
        
        latex += "\\end{CD}\n"
        
        preamble = """% Required packages:
% \\usepackage{amscd}
% \\usepackage{amsmath}

"""
        
        return preamble + latex
    
    @staticmethod
    def to_quiver(diagram: CommutativeDiagram) -> str:
        """Export diagram to quiver format (for the online quiver editor)."""
        
        if not all(obj in diagram.positions for obj in diagram.objects):
            diagram.auto_layout()
        
        # Create quiver JSON-like format
        objects_data = []
        for i, obj in enumerate(diagram.objects):
            pos = diagram.positions[obj]
            objects_data.append({
                "id": i,
                "label": obj.name,
                "x": pos[0] * 100,  # Scale for visibility
                "y": pos[1] * 100
            })
        
        # Create mapping from objects to IDs
        obj_to_id = {obj: i for i, obj in enumerate(diagram.objects)}
        
        arrows_data = []
        for morph in diagram.morphisms:
            if morph.source in obj_to_id and morph.target in obj_to_id:
                arrows_data.append({
                    "source": obj_to_id[morph.source],
                    "target": obj_to_id[morph.target],
                    "label": morph.name
                })
        
        # Format as a readable string
        result = "% Quiver diagram data\n"
        result += "% Objects:\n"
        for obj_data in objects_data:
            result += f"% {obj_data}\n"
        
        result += "% Arrows:\n"
        for arrow_data in arrows_data:
            result += f"% {arrow_data}\n"
        
        result += "\n% You can copy this data to https://q.uiver.app/ for editing\n"
        
        return result


class DiagramBuilder:
    """Builder pattern for constructing commutative diagrams."""
    
    def __init__(self, name: str, category: Category):
        self.diagram = CommutativeDiagram(name, category)
    
    def with_objects(self, *objects: Object) -> 'DiagramBuilder':
        """Add objects to the diagram."""
        for obj in objects:
            self.diagram.add_object(obj)
        return self
    
    def with_morphisms(self, *morphisms: Morphism) -> 'DiagramBuilder':
        """Add morphisms to the diagram."""
        for morph in morphisms:
            self.diagram.add_morphism(morph)
        return self
    
    def with_square(self, top_left: Object, top_right: Object,
                   bottom_left: Object, bottom_right: Object,
                   top: Morphism, right: Morphism, 
                   bottom: Morphism, left: Morphism) -> 'DiagramBuilder':
        """Add a commutative square."""
        
        # Set positions
        self.diagram.set_object_position(top_left, 0, 0)
        self.diagram.set_object_position(top_right, 1, 0)
        self.diagram.set_object_position(bottom_left, 0, 1)
        self.diagram.set_object_position(bottom_right, 1, 1)
        
        # Add morphisms
        self.diagram.add_morphism(top)
        self.diagram.add_morphism(right)
        self.diagram.add_morphism(bottom)
        self.diagram.add_morphism(left)
        
        # Require commutativity
        top_right_path = Path([top, right])
        left_bottom_path = Path([left, bottom])
        self.diagram.require_commutativity(top_right_path, left_bottom_path)
        
        return self
    
    def with_triangle(self, A: Object, B: Object, C: Object,
                     f: Morphism, g: Morphism, h: Morphism) -> 'DiagramBuilder':
        """Add a triangle A->B->C with potential commutativity."""
        
        # Set positions in triangle
        self.diagram.set_object_position(A, 0, 0)
        self.diagram.set_object_position(B, 1, 0)
        self.diagram.set_object_position(C, 0, 1)
        
        self.diagram.add_morphism(f)  # A -> B
        self.diagram.add_morphism(g)  # B -> C
        self.diagram.add_morphism(h)  # A -> C
        
        # Check if triangle commutes: h = g ∘ f
        composite_path = Path([f, g])
        direct_path = Path([h])
        self.diagram.require_commutativity(composite_path, direct_path)
        
        return self
    
    def with_pullback(self, P: Object, A: Object, B: Object, C: Object,
                     p1: Morphism, p2: Morphism, f: Morphism, g: Morphism) -> 'DiagramBuilder':
        """Add a pullback square."""
        
        # Standard pullback layout
        self.diagram.set_object_position(P, 0, 0)
        self.diagram.set_object_position(A, 1, 0)
        self.diagram.set_object_position(B, 0, 1)
        self.diagram.set_object_position(C, 1, 1)
        
        self.diagram.add_morphism(p1)  # P -> A
        self.diagram.add_morphism(p2)  # P -> B
        self.diagram.add_morphism(f)   # A -> C
        self.diagram.add_morphism(g)   # B -> C
        
        # Pullback condition: f ∘ p1 = g ∘ p2
        path1 = Path([p1, f])
        path2 = Path([p2, g])
        self.diagram.require_commutativity(path1, path2)
        
        return self
    
    def with_pushout(self, A: Object, B: Object, C: Object, Q: Object,
                    f: Morphism, g: Morphism, i1: Morphism, i2: Morphism) -> 'DiagramBuilder':
        """Add a pushout square."""
        
        # Standard pushout layout
        self.diagram.set_object_position(A, 0, 0)
        self.diagram.set_object_position(B, 1, 0)
        self.diagram.set_object_position(C, 0, 1)
        self.diagram.set_object_position(Q, 1, 1)
        
        self.diagram.add_morphism(f)   # A -> B
        self.diagram.add_morphism(g)   # A -> C
        self.diagram.add_morphism(i1)  # B -> Q
        self.diagram.add_morphism(i2)  # C -> Q
        
        # Pushout condition: i1 ∘ f = i2 ∘ g
        path1 = Path([f, i1])
        path2 = Path([g, i2])
        self.diagram.require_commutativity(path1, path2)
        
        return self
    
    def auto_layout(self) -> 'DiagramBuilder':
        """Apply automatic layout."""
        self.diagram.auto_layout()
        return self
    
    def build(self) -> CommutativeDiagram:
        """Build the diagram."""
        return self.diagram

