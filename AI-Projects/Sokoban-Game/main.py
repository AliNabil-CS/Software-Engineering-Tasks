import heapq
import time
from collections import deque
import math
import os
from functools import lru_cache
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import io

class SokobanGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sokoban AI Solver")
        self.root.geometry("1200x800")
        self.root.configure(bg='#2c3e50')
        
        # ===== ADDED: Set application icon =====
        try:
            # Load and set the application icon
            icon_path = "images/player.png"  # Use the same path as in your code
            icon_img = Image.open(icon_path)
            icon_photo = ImageTk.PhotoImage(icon_img)
            self.root.iconphoto(True, icon_photo)
            print(f"✓ Application icon set from: {icon_path}")
        except Exception as e:
            print(f"Warning: Could not load application icon: {e}")
            print("Using default Tkinter icon instead.")
        # ===== END OF ADDED CODE =====
        
        # Game solver instance
        self.solver = None
        self.current_level = None
        self.solution_path = None
        self.current_step = 0
        self.player_direction = 'down'  # CHANGED: Default to down instead of right
        
        # ===== ADDED: Fullscreen state =====
        self.fullscreen_state = False
        # ===== END OF ADDED CODE =====
        
        # Colors and styling
        self.colors = {
            'background': '#2c3e50',
            'panel_bg': '#34495e',
            'text_color': '#ecf0f1',
            'button_bg': '#3498db',
            'button_hover': '#2980b9',
            'wall_color': '#7f8c8d',
            'player_color': '#e74c3c',
            'box_color': '#e67e22',
            'goal_color': '#27ae60',
            'box_on_goal_color': '#2ecc71',
            'grid_bg': '#1a252f'
        }
        
        # Icons - initialize empty
        self.icons = {}
        
        # Setup GUI first, then create icons
        self.setup_gui()
        self.create_icons()
        
        # ===== ADDED: Bind F11 key for fullscreen toggle =====
        self.root.bind('<F11>', self.toggle_fullscreen)
        # ===== END OF ADDED CODE =====

    def create_icons(self, size=40):
        """Create icons for game elements with directional player images"""
        self.icons = {}
        
        try:
            # Load images from file paths
            box_image_path = "images/box.png"
            box_img = Image.open(box_image_path)
            box_img = box_img.resize((size, size), Image.Resampling.LANCZOS)
            self.icons['box'] = ImageTk.PhotoImage(box_img)
            
            goal_image_path = "images/goal.png"
            goal_img = Image.open(goal_image_path)
            goal_img = goal_img.resize((size, size), Image.Resampling.LANCZOS)
            self.icons['goal'] = ImageTk.PhotoImage(goal_img)
            
            box_on_goal_image_path = "images/box_on_goal.png"
            box_on_goal_img = Image.open(box_on_goal_image_path)
            box_on_goal_img = box_on_goal_img.resize((size, size), Image.Resampling.LANCZOS)
            self.icons['box_on_goal'] = ImageTk.PhotoImage(box_on_goal_img)
            
            # Load directional player images
            player_right_path = "images/player_right.png"
            player_right_img = Image.open(player_right_path)
            player_right_img = player_right_img.resize((size, size), Image.Resampling.LANCZOS)
            self.icons['player_right'] = ImageTk.PhotoImage(player_right_img)
            
            player_left_path = "images/player_left.png"
            player_left_img = Image.open(player_left_path)
            player_left_img = player_left_img.resize((size, size), Image.Resampling.LANCZOS)
            self.icons['player_left'] = ImageTk.PhotoImage(player_left_img)
            
            player_up_path = "images/player_up.png"
            player_up_img = Image.open(player_up_path)
            player_up_img = player_up_img.resize((size, size), Image.Resampling.LANCZOS)
            self.icons['player_up'] = ImageTk.PhotoImage(player_up_img)
            
            player_down_path = "images/player_down.png"
            player_down_img = Image.open(player_down_path)
            player_down_img = player_down_img.resize((size, size), Image.Resampling.LANCZOS)
            self.icons['player_down'] = ImageTk.PhotoImage(player_down_img)
            
            # Load directional player on goal images
            player_on_goal_right_path = "images/player_on_goal_right.png"
            player_on_goal_right_img = Image.open(player_on_goal_right_path)
            player_on_goal_right_img = player_on_goal_right_img.resize((size, size), Image.Resampling.LANCZOS)
            self.icons['player_on_goal_right'] = ImageTk.PhotoImage(player_on_goal_right_img)
            
            player_on_goal_left_path = "images/player_on_goal_left.png"
            player_on_goal_left_img = Image.open(player_on_goal_left_path)
            player_on_goal_left_img = player_on_goal_left_img.resize((size, size), Image.Resampling.LANCZOS)
            self.icons['player_on_goal_left'] = ImageTk.PhotoImage(player_on_goal_left_img)
            
            player_on_goal_up_path = "images/player_on_goal_up.png"
            player_on_goal_up_img = Image.open(player_on_goal_up_path)
            player_on_goal_up_img = player_on_goal_up_img.resize((size, size), Image.Resampling.LANCZOS)
            self.icons['player_on_goal_up'] = ImageTk.PhotoImage(player_on_goal_up_img)
            
            player_on_goal_down_path = "images/player_on_goal_down.png"
            player_on_goal_down_img = Image.open(player_on_goal_down_path)
            player_on_goal_down_img = player_on_goal_down_img.resize((size, size), Image.Resampling.LANCZOS)
            self.icons['player_on_goal_down'] = ImageTk.PhotoImage(player_on_goal_down_img)
            
            wall_image_path = "images/wall.png"
            wall_img = Image.open(wall_image_path)
            wall_img = wall_img.resize((size, size), Image.Resampling.LANCZOS)
            self.icons['wall'] = ImageTk.PhotoImage(wall_img)
            
            # Empty cell
            empty_img = Image.new('RGB', (size, size), color=self.colors['grid_bg'])
            self.icons['empty'] = ImageTk.PhotoImage(empty_img)
            
            print("All images loaded successfully!")
            
        except Exception as e:
            print(f"Error loading images: {e}")
            print("Falling back to colored squares...")
            # Fallback to original colored squares if images fail to load
            self.create_fallback_icons(size)

    def create_fallback_icons(self, size):
        """Create fallback colored icons if images can't be loaded"""
        # Box icon (fallback)
        box_img = Image.new('RGB', (size, size), color=self.colors['box_color'])
        self.icons['box'] = ImageTk.PhotoImage(box_img)
        
        # Goal icon (flag) - fallback
        goal_img = Image.new('RGB', (size, size), color=self.colors['goal_color'])
        self.icons['goal'] = ImageTk.PhotoImage(goal_img)
        
        # Box on goal icon - fallback
        box_on_goal_img = Image.new('RGB', (size, size), color=self.colors['box_on_goal_color'])
        self.icons['box_on_goal'] = ImageTk.PhotoImage(box_on_goal_img)
        
        # Player icons - fallback (all directions same color)
        player_img = Image.new('RGB', (size, size), color=self.colors['player_color'])
        self.icons['player_right'] = ImageTk.PhotoImage(player_img)
        self.icons['player_left'] = ImageTk.PhotoImage(player_img)
        self.icons['player_up'] = ImageTk.PhotoImage(player_img)
        self.icons['player_down'] = ImageTk.PhotoImage(player_img)
        
        # Player on goal icons - fallback
        player_on_goal_img = Image.new('RGB', (size, size), color=self.colors['player_color'])
        self.icons['player_on_goal_right'] = ImageTk.PhotoImage(player_on_goal_img)
        self.icons['player_on_goal_left'] = ImageTk.PhotoImage(player_on_goal_img)
        self.icons['player_on_goal_up'] = ImageTk.PhotoImage(player_on_goal_img)
        self.icons['player_on_goal_down'] = ImageTk.PhotoImage(player_on_goal_img)
        
        # Wall icon - fallback
        wall_img = Image.new('RGB', (size, size), color=self.colors['wall_color'])
        self.icons['wall'] = ImageTk.PhotoImage(wall_img)
        
        # Empty cell
        empty_img = Image.new('RGB', (size, size), color=self.colors['grid_bg'])
        self.icons['empty'] = ImageTk.PhotoImage(empty_img)
        
        print("Fallback colored icons created successfully!")
    
    def setup_gui(self):
        """Setup the main GUI layout"""
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel - Level selection and controls
        left_frame = ttk.Frame(main_frame, style='Custom.TFrame')
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # Right panel - Game display
        right_frame = ttk.Frame(main_frame, style='Custom.TFrame')
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Configure styles
        self.configure_styles()
        
        # Setup left panel
        self.setup_left_panel(left_frame)
        
        # Setup right panel
        self.setup_right_panel(right_frame)
    
    def configure_styles(self):
        """Configure ttk styles"""
        style = ttk.Style()
        style.configure('Custom.TFrame', background=self.colors['panel_bg'])
        style.configure('Title.TLabel', background=self.colors['panel_bg'], 
                       foreground=self.colors['text_color'], font=('Arial', 16, 'bold'))
        style.configure('Subtitle.TLabel', background=self.colors['panel_bg'],
                       foreground=self.colors['text_color'], font=('Arial', 12, 'bold'))
        style.configure('Normal.TLabel', background=self.colors['panel_bg'],
                       foreground=self.colors['text_color'], font=('Arial', 10))
        style.configure('Game.TFrame', background=self.colors['grid_bg'])
    
    def setup_left_panel(self, parent):
        """Setup the left control panel - FIXED VERSION WITH tk.Radiobutton"""
        # Title
        title_label = ttk.Label(parent, text="SOKOBAN AI SOLVER", style='Title.TLabel')
        title_label.pack(pady=(0, 20))
        
        # Level selection
        level_frame = ttk.Frame(parent, style='Custom.TFrame')
        level_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(level_frame, text="Select Level:", style='Subtitle.TLabel').pack(anchor=tk.W)
        
        self.level_var = tk.StringVar()
        levels = [
            "Tutorial - Single Box",
            "Two Box Challenge", 
            "Double Stack",
            "In The Way",
            "Zig Zag",
            "Boxes",
            "No Way"
        ]
        
        level_combo = ttk.Combobox(level_frame, textvariable=self.level_var, values=levels, state="readonly")
        level_combo.pack(fill=tk.X, pady=(5, 0))
        level_combo.set(levels[0])
        level_combo.bind('<<ComboboxSelected>>', self.on_level_select)
        
        # Algorithm selection - FIXED: Use standard tk Radiobutton
        algo_frame = ttk.Frame(parent, style='Custom.TFrame')
        algo_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(algo_frame, text="Solving Algorithm:", style='Subtitle.TLabel').pack(anchor=tk.W)
        
        self.algo_var = tk.StringVar(value="A* (Recommended)")
        algorithms = ["A* (Recommended)", "BFS (Shortest Path)", "DFS (Memory Efficient)"]
        
        for algo in algorithms:
            # Use tk.Radiobutton instead of ttk.Radiobutton
            rb = tk.Radiobutton(algo_frame, text=algo, variable=self.algo_var, 
                              value=algo, bg=self.colors['panel_bg'], fg=self.colors['text_color'],
                              selectcolor=self.colors['button_bg'], font=('Arial', 10),
                              anchor='w')
            rb.pack(anchor=tk.W, pady=2, fill=tk.X)
        
        # Control buttons
        button_frame = ttk.Frame(parent, style='Custom.TFrame')
        button_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.solve_btn = ttk.Button(button_frame, text="Solve Level", command=self.solve_level)
        self.solve_btn.pack(fill=tk.X, pady=2)
        
        self.reset_btn = ttk.Button(button_frame, text="Reset", command=self.reset_level, state=tk.DISABLED)
        self.reset_btn.pack(fill=tk.X, pady=2)
        
        # ===== ADDED: Fullscreen toggle button =====
        self.fullscreen_btn = ttk.Button(button_frame, text="Toggle Fullscreen (F11)", 
                                       command=self.toggle_fullscreen_button)
        self.fullscreen_btn.pack(fill=tk.X, pady=2)
        # ===== END OF ADDED CODE =====
        
        # Navigation buttons
        nav_frame = ttk.Frame(parent, style='Custom.TFrame')
        nav_frame.pack(fill=tk.X, pady=(0, 20))
        
        nav_btn_frame = ttk.Frame(nav_frame, style='Custom.TFrame')
        nav_btn_frame.pack(fill=tk.X)
        
        self.prev_btn = ttk.Button(nav_btn_frame, text="◀ Previous", command=self.previous_step, state=tk.DISABLED)
        self.prev_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 2))
        
        self.next_btn = ttk.Button(nav_btn_frame, text="Next ▶", command=self.next_step, state=tk.DISABLED)
        self.next_btn.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(2, 0))
        
        # Step info
        self.step_label = ttk.Label(nav_frame, text="Step: 0/0", style='Normal.TLabel')
        self.step_label.pack(pady=5)
        
        # Performance metrics
        metrics_frame = ttk.Frame(parent, style='Custom.TFrame')
        metrics_frame.pack(fill=tk.X)
        
        ttk.Label(metrics_frame, text="Performance Metrics:", style='Subtitle.TLabel').pack(anchor=tk.W)
        
        self.metrics_text = tk.Text(metrics_frame, height=8, width=30, bg=self.colors['panel_bg'],
                                  fg=self.colors['text_color'], font=('Arial', 9), relief=tk.FLAT)
        self.metrics_text.pack(fill=tk.X, pady=(5, 0))
        self.metrics_text.insert(tk.END, "No solution computed yet.\nSelect a level and click 'Solve Level'.")
        self.metrics_text.config(state=tk.DISABLED)
    
    def setup_right_panel(self, parent):
        """Setup the right game display panel"""
        # Game title
        self.level_title = ttk.Label(parent, text="Select a level to begin", style='Title.TLabel')
        self.level_title.pack(pady=(0, 10))
        
        # Game canvas frame
        canvas_frame = ttk.Frame(parent, style='Game.TFrame')
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create canvas with scrollbars
        self.canvas = tk.Canvas(canvas_frame, bg=self.colors['grid_bg'], highlightthickness=0)
        
        v_scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        h_scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        
        self.canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Legend
        legend_frame = ttk.Frame(parent, style='Custom.TFrame')
        legend_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Label(legend_frame, text="Legend:", style='Subtitle.TLabel').pack(anchor=tk.W)
        
        legend_items = [
            ("Wall", self.colors['wall_color']),
            ("Player", self.colors['player_color']),
            ("Box", self.colors['box_color']),
            ("Goal", self.colors['goal_color']),
            ("Box on Goal", self.colors['box_on_goal_color'])
        ]
        
        legend_inner = ttk.Frame(legend_frame, style='Custom.TFrame')
        legend_inner.pack(fill=tk.X, pady=5)
        
        for text, color in legend_items:
            item_frame = ttk.Frame(legend_inner, style='Custom.TFrame')
            item_frame.pack(side=tk.LEFT, padx=(0, 15))
            
            color_canvas = tk.Canvas(item_frame, width=20, height=20, bg=color, highlightthickness=0)
            color_canvas.pack(side=tk.LEFT, padx=(0, 5))
            
            ttk.Label(item_frame, text=text, style='Normal.TLabel').pack(side=tk.LEFT)
    
    # ===== ADDED: Fullscreen toggle methods =====
    def toggle_fullscreen(self, event=None):
        """Toggle fullscreen mode with F11 key"""
        self.fullscreen_state = not self.fullscreen_state
        self.root.attributes("-fullscreen", self.fullscreen_state)
        
        # Update button text
        if self.fullscreen_state:
            self.fullscreen_btn.config(text="Exit Fullscreen (F11)")
            print("Entered fullscreen mode")
        else:
            self.fullscreen_btn.config(text="Toggle Fullscreen (F11)")
            print("Exited fullscreen mode")
        
        # Update display after toggling fullscreen
        if self.solver:
            self.display_current_state()
    
    def toggle_fullscreen_button(self):
        """Toggle fullscreen mode with button click"""
        self.toggle_fullscreen()
    # ===== END OF ADDED CODE =====
    
    def on_level_select(self, event=None):
        """Handle level selection"""
        level_name = self.level_var.get()
        level_index = [
            "Tutorial - Single Box",
            "Two Box Challenge", 
            "Double Stack",
            "In The Way",
            "Zig Zag",
            "Boxes",
            "Stairs",
            "No Way"
        ].index(level_name)
        
        self.load_level(level_index)
    
    def load_level(self, level_index):
        """Load a specific level"""
        levels = self.get_levels()
        self.current_level = levels[level_index]
        self.solver = EnhancedSokobanSolver(self.current_level)
        self.solution_path = None
        self.current_step = 0
        self.player_direction = 'down'  # CHANGED: Reset to down instead of right
        
        self.level_title.config(text=f"Level {level_index + 1}: {self.level_var.get()}")
        self.reset_btn.config(state=tk.DISABLED)
        self.prev_btn.config(state=tk.DISABLED)
        self.next_btn.config(state=tk.DISABLED)
        self.step_label.config(text="Step: 0/0")
        
        self.display_current_state()
        self.update_metrics("Level loaded. Click 'Solve Level' to find solution.")
    
    def get_levels(self):
        """Return the available levels"""
        LEVEL_1 = """
#######
#.   @#
#  $  #
#     #
#     #
#######
"""

        LEVEL_2 = """
#########
#.     .#
#       #
#  $ $  #
#   @   #
#########
"""

        LEVEL_3 = """
########
#  @   #
#  $   #
#  $   #
#  .   #
#  .   #
########
"""

        LEVEL_4 = """
#######
#     #
# @$  #
#  #  #
#  $. #
#   . #
#######
"""

        LEVEL_5 = """
########
#  #   #
# @$   #
#  #$  #
#  #   #
#  $. .#
#   .  #
########
"""
        LEVEL_6 = """
###########
#      @  #
#    # $  #
#    #   .#
##   ######
#         #
#.$     $ #
####  #   #
#     # . #
#.$   #   #
###########
"""


        LEVEL_7 = """
#######
#### $#
# @# $#
####  #
#   . #
#   . #
#######
"""
        
        return [LEVEL_1, LEVEL_2, LEVEL_3, LEVEL_4, LEVEL_5, LEVEL_6, LEVEL_7]
    
    def solve_level(self):
        """Solve the current level with selected algorithm - UPDATED WITH ALGORITHM INFO"""
        if not self.solver:
            messagebox.showwarning("Warning", "Please select a level first.")
            return
        
        # Determine algorithm
        algo_map = {
            "A* (Recommended)": "astar",
            "BFS (Shortest Path)": "bfs", 
            "DFS (Memory Efficient)": "dfs"
        }
        selected_algo = self.algo_var.get()
        algorithm = algo_map.get(selected_algo, "astar")
        
        # Solve the level
        self.update_metrics(f"Solving with {selected_algo}... Please wait...")
        self.root.update()
        
        start_time = time.time()
        self.solution_path = self.solver.solve(algorithm)
        solve_time = time.time() - start_time
        
        if self.solution_path:
            self.current_step = 0
            self.player_direction = 'down'  # CHANGED: Reset to down for new solution
            self.display_current_state()
            self.reset_btn.config(state=tk.NORMAL)
            self.prev_btn.config(state=tk.DISABLED)
            self.next_btn.config(state=tk.NORMAL if len(self.solution_path) > 1 else tk.DISABLED)
            self.step_label.config(text=f"Step: 0/{len(self.solution_path)-1}")
            
            # Update metrics with algorithm info
            metrics_text = f"Solution Found!\n\n"
            metrics_text += f"Algorithm: {selected_algo}\n"
            metrics_text += f"Explored nodes: {self.solver.explored_nodes:,}\n"
            metrics_text += f"Solution depth: {self.solver.solution_depth}\n"
            metrics_text += f"Execution time: {solve_time:.4f}s\n"
            metrics_text += f"Nodes per second: {self.solver.explored_nodes/solve_time:,.0f}\n"
            
            self.update_metrics(metrics_text)
        else:
            self.update_metrics(f"No solution found with {selected_algo}!")
            messagebox.showinfo("No Solution", f"No solution found for this level with {selected_algo}.")
    
    def reset_level(self):
        """Reset to the initial state"""
        if self.solver and self.solution_path:
            self.current_step = 0
            self.player_direction = 'down'  # CHANGED: Reset to down
            self.display_current_state()
            self.prev_btn.config(state=tk.DISABLED)
            self.next_btn.config(state=tk.NORMAL if len(self.solution_path) > 1 else tk.DISABLED)
            self.step_label.config(text=f"Step: 0/{len(self.solution_path)-1}")
    
    def previous_step(self):
        """Go to previous step in solution"""
        if self.current_step > 0 and self.solution_path:
            self.current_step -= 1
            self.update_player_direction()  # Update direction based on movement
            self.display_current_state()
            self.next_btn.config(state=tk.NORMAL)
            if self.current_step == 0:
                self.prev_btn.config(state=tk.DISABLED)
            self.step_label.config(text=f"Step: {self.current_step}/{len(self.solution_path)-1}")
    
    def next_step(self):
        """Go to next step in solution"""
        if self.solution_path and self.current_step < len(self.solution_path) - 1:
            self.current_step += 1
            self.update_player_direction()  # Update direction based on movement
            self.display_current_state()
            self.prev_btn.config(state=tk.NORMAL)
            if self.current_step == len(self.solution_path) - 1:
                self.next_btn.config(state=tk.DISABLED)
            self.step_label.config(text=f"Step: {self.current_step}/{len(self.solution_path)-1}")
    
    def update_player_direction(self):
        """Update player direction based on movement between steps"""
        if self.current_step > 0 and self.solution_path:
            current_state = self.solution_path[self.current_step]
            previous_state = self.solution_path[self.current_step - 1]
            
            current_player, _ = current_state
            previous_player, _ = previous_state
            
            # Calculate movement direction
            dx = current_player[0] - previous_player[0]
            dy = current_player[1] - previous_player[1]
            
            if dx > 0:
                self.player_direction = 'right'
            elif dx < 0:
                self.player_direction = 'left'
            elif dy > 0:
                self.player_direction = 'down'
            elif dy < 0:
                self.player_direction = 'up'
            # If no movement (shouldn't happen), keep current direction
    
    def display_current_state(self):
        """Display the current game state on canvas with directional player"""
        self.canvas.delete("all")
        
        if not self.solver:
            return
        
        # Get current state
        if self.solution_path and self.current_step < len(self.solution_path):
            state = self.solution_path[self.current_step]
        else:
            state = (self.solver.player, frozenset(self.solver.boxes))
        
        player, boxes = state
        
        # Calculate canvas size and scaling
        all_positions = self.solver.walls.union(boxes, {player}, self.solver.goals)
        if not all_positions:
            return
        
        max_x = max(pos[0] for pos in all_positions)
        max_y = max(pos[1] for pos in all_positions)
        
        cell_size = 45
        margin = 20
        
        # Calculate required canvas size
        required_width = (max_x + 1) * cell_size + 2 * margin
        required_height = (max_y + 1) * cell_size + 2 * margin
        
        # Configure canvas scroll region
        self.canvas.config(scrollregion=(0, 0, required_width, required_height))
        
        # Draw grid and elements USING ICONS
        for y in range(max_y + 1):
            for x in range(max_x + 1):
                pos = (x, y)
                x1 = x * cell_size + margin
                y1 = y * cell_size + margin
                
                # Determine what to draw at this position
                if pos in self.solver.walls:
                    self.canvas.create_image(x1, y1, image=self.icons['wall'], anchor=tk.NW)
                elif pos == player and pos in self.solver.goals:
                    # Use directional player on goal image
                    icon_key = f'player_on_goal_{self.player_direction}'
                    self.canvas.create_image(x1, y1, image=self.icons[icon_key], anchor=tk.NW)
                elif pos == player:
                    # Use directional player image
                    icon_key = f'player_{self.player_direction}'
                    self.canvas.create_image(x1, y1, image=self.icons[icon_key], anchor=tk.NW)
                elif pos in boxes and pos in self.solver.goals:
                    self.canvas.create_image(x1, y1, image=self.icons['box_on_goal'], anchor=tk.NW)
                elif pos in boxes:
                    self.canvas.create_image(x1, y1, image=self.icons['box'], anchor=tk.NW)
                elif pos in self.solver.goals:
                    self.canvas.create_image(x1, y1, image=self.icons['goal'], anchor=tk.NW)
                else:
                    self.canvas.create_image(x1, y1, image=self.icons['empty'], anchor=tk.NW)
    
    def update_metrics(self, text):
        """Update the metrics text area"""
        self.metrics_text.config(state=tk.NORMAL)
        self.metrics_text.delete(1.0, tk.END)
        self.metrics_text.insert(tk.END, text)
        self.metrics_text.config(state=tk.DISABLED)


class EnhancedSokobanSolver:
    def __init__(self, level):
        self.level = level
        self.walls = set()
        self.goals = set()
        self.boxes = set()
        self.player = None
        self.explored_nodes = 0
        self.solution_depth = 0
        self.execution_time = 0
        self.deadlock_positions = set()
        
        self.parse_level()
        self.precompute_deadlocks()
    
    def parse_level(self):
        """Parse the level string into game components"""
        lines = self.level.strip().split('\n')
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                pos = (x, y)
                if char == '#':
                    self.walls.add(pos)
                elif char == '.':
                    self.goals.add(pos)
                elif char == '$':
                    self.boxes.add(pos)
                elif char == '@':
                    self.player = pos
                elif char == '*':
                    self.boxes.add(pos)
                    self.goals.add(pos)
                elif char == '+':
                    self.player = pos
                    self.goals.add(pos)
    
    def precompute_deadlocks(self):
        """IMPROVED: Only mark non-goal positions as deadlocks"""
        # Only check positions that might actually be reachable
        max_x = max(pos[0] for pos in self.walls) if self.walls else 10
        max_y = max(pos[1] for pos in self.walls) if self.walls else 10
        
        for x in range(max_x + 1):
            for y in range(max_y + 1):
                pos = (x, y)
                # ONLY mark as deadlock if it's NOT a goal and NOT a wall
                if pos not in self.walls and pos not in self.goals:
                    if self.is_corner_deadlock(pos):
                        self.deadlock_positions.add(pos)
    
    def is_corner_deadlock(self, pos):
        """IMPROVED: Better corner detection that allows goals"""
        x, y = pos
        neighbors = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
        wall_count = 0
        
        for neighbor in neighbors:
            if neighbor in self.walls:
                wall_count += 1
        
        # A position is a corner deadlock if:
        # 1. It has at least 2 adjacent walls that form an actual corner
        # 2. It's NOT a goal position (goals can never be deadlocks)
        if wall_count >= 2 and pos not in self.goals:
            # Check if walls form a real corner (not just any two walls)
            left_wall = (x-1, y) in self.walls
            right_wall = (x+1, y) in self.walls  
            up_wall = (x, y-1) in self.walls
            down_wall = (x, y+1) in self.walls
            
            # Real corners: left+up, left+down, right+up, right+down
            if (left_wall and up_wall) or (left_wall and down_wall) or \
               (right_wall and up_wall) or (right_wall and down_wall):
                return True
        
        return False
    
    def is_valid_move(self, pos):
        """Check if a position is valid (not a wall)"""
        return pos not in self.walls
    
    def is_deadlock_state(self, boxes):
        """IMPROVED: Less aggressive deadlock detection"""
        for box in boxes:
            # NEVER mark a box on goal as deadlock
            if box in self.goals:
                continue
                
            # Only use precomputed deadlocks for boxes not on goals
            if box in self.deadlock_positions:
                return True
            
            # REMOVED the frozen box check - it was too aggressive
            # Simple games don't need complex frozen box detection
        
        return False
    
    def get_neighbors(self, state):
        """Generate all possible next states from current state"""
        player, boxes = state
        moves = [(0, -1), (1, 0), (0, 1), (-1, 0)]  # Up, Right, Down, Left
        neighbors = []
        
        for dx, dy in moves:
            new_player = (player[0] + dx, player[1] + dy)
            
            # If moving to empty space
            if new_player not in boxes and self.is_valid_move(new_player):
                neighbors.append((new_player, boxes))
            
            # If pushing a box
            elif new_player in boxes:
                new_box = (new_player[0] + dx, new_player[1] + dy)
                if (self.is_valid_move(new_box) and 
                    new_box not in boxes):
                    
                    new_boxes = set(boxes)
                    new_boxes.remove(new_player)
                    new_boxes.add(new_box)
                    
                    # Use improved deadlock checking
                    if not self.is_deadlock_state(new_boxes):
                        neighbors.append((new_player, frozenset(new_boxes)))
        
        return neighbors
    
    def manhattan_distance(self, a, b):
        """Calculate Manhattan distance between two points"""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    def heuristic_min_matching(self, boxes):
        """Hungarian algorithm-based heuristic for box-goal matching"""
        if not boxes:
            return 0
            
        # For single box, just return distance to closest goal
        if len(boxes) == 1:
            box = next(iter(boxes))
            min_dist = float('inf')
            for goal in self.goals:
                dist = self.manhattan_distance(box, goal)
                if dist < min_dist:
                    min_dist = dist
            return min_dist
            
        # Multiple boxes - use minimum matching
        boxes_list = list(boxes)
        goals_list = list(self.goals)
        
        n = max(len(boxes_list), len(goals_list))
        cost_matrix = [[0] * n for _ in range(n)]
        
        for i, box in enumerate(boxes_list):
            for j, goal in enumerate(goals_list):
                cost_matrix[i][j] = self.manhattan_distance(box, goal)
            for j in range(len(goals_list), n):
                cost_matrix[i][j] = 1000
                
        # Simple greedy matching
        total_cost = 0
        used_goals = set()
        
        for box in boxes_list:
            min_cost = float('inf')
            best_goal = None
            for goal in self.goals:
                if goal not in used_goals:
                    cost = self.manhattan_distance(box, goal)
                    if cost < min_cost:
                        min_cost = cost
                        best_goal = goal
            if best_goal:
                used_goals.add(best_goal)
                total_cost += min_cost
                
        return total_cost
    
    def heuristic_improved(self, boxes):
        """Improved heuristic combining multiple strategies"""
        if not boxes:
            return 0
            
        matching_cost = self.heuristic_min_matching(boxes)
        
        # Add small penalty for boxes not on goals
        off_goal_penalty = 0
        for box in boxes:
            if box not in self.goals:
                off_goal_penalty += 1  # Reduced penalty
                
        return matching_cost + off_goal_penalty
    
    def is_solved(self, boxes):
        """Check if all boxes are on goals"""
        return all(box in self.goals for box in boxes)
    
    def reconstruct_path(self, came_from, current):
        """Reconstruct the complete path from start to goal"""
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        return path[::-1]
    
    def solve_astar_improved(self):
        """Improved A* with better heuristics and deadlock detection"""
        start_time = time.time()
        
        start_state = (self.player, frozenset(self.boxes))
        
        # DEBUG: Print initial state
        print(f"Solving level - Player: {self.player}, Boxes: {self.boxes}, Goals: {self.goals}")
        
        open_set = []
        heapq.heappush(open_set, (0, start_state))
        
        g_score = {start_state: 0}
        f_score = {start_state: self.heuristic_improved(self.boxes)}
        came_from = {}
        
        self.explored_nodes = 0
        
        while open_set:
            _, current = heapq.heappop(open_set)
            current_player, current_boxes = current
            
            self.explored_nodes += 1
            
            if self.explored_nodes % 1000 == 0:
                print(f"Explored {self.explored_nodes} nodes...")
            
            if self.is_solved(current_boxes):
                self.execution_time = time.time() - start_time
                path = self.reconstruct_path(came_from, current)
                self.solution_depth = len(path) - 1
                print(f"Solution found! Depth: {self.solution_depth}, Nodes: {self.explored_nodes}")
                return path
            
            for neighbor in self.get_neighbors(current):
                tentative_g_score = g_score[current] + 1
                
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic_improved(neighbor[1])
                    
                    found = False
                    for i, (f, state) in enumerate(open_set):
                        if state == neighbor:
                            if tentative_g_score < g_score[neighbor]:
                                open_set[i] = (f_score[neighbor], neighbor)
                                heapq.heapify(open_set)
                            found = True
                            break
                    
                    if not found:
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))
        
        self.execution_time = time.time() - start_time
        print(f"No solution found. Explored {self.explored_nodes} nodes.")
        return None
    
    def solve_bfs(self):
        """Breadth-First Search for guaranteed shortest path"""
        start_time = time.time()
        
        start_state = (self.player, frozenset(self.boxes))
        print(f"BFS Solving - Player: {self.player}, Boxes: {self.boxes}")
        
        queue = deque([start_state])
        visited = {start_state: None}
        
        self.explored_nodes = 0
        
        while queue:
            current = queue.popleft()
            current_player, current_boxes = current
            
            self.explored_nodes += 1
            
            if self.explored_nodes % 1000 == 0:
                print(f"BFS explored {self.explored_nodes} nodes...")
            
            if self.is_solved(current_boxes):
                self.execution_time = time.time() - start_time
                path = []
                while current:
                    path.append(current)
                    current = visited[current]
                path.reverse()
                self.solution_depth = len(path) - 1
                print(f"BFS Solution found! Depth: {self.solution_depth}")
                return path
            
            for neighbor in self.get_neighbors(current):
                if neighbor not in visited:
                    visited[neighbor] = current
                    queue.append(neighbor)
        
        self.execution_time = time.time() - start_time
        print(f"BFS No solution found. Nodes: {self.explored_nodes}")
        return None
    
    def solve_dfs_limited(self, depth_limit=200):
        """Improved Depth-First Search with iterative deepening"""
        start_time = time.time()
        
        start_state = (self.player, frozenset(self.boxes))
        print(f"DFS Solving - Player: {self.player}, Boxes: {self.boxes}")
        
        # Use iterative deepening to find solutions of increasing depth
        for current_depth in range(1, depth_limit + 1):
            result = self.depth_limited_dfs(start_state, current_depth)
            if result:
                self.execution_time = time.time() - start_time
                self.solution_depth = len(result) - 1
                print(f"DFS Solution found at depth {current_depth}! Depth: {self.solution_depth}, Nodes: {self.explored_nodes}")
                return result
        
        self.execution_time = time.time() - start_time
        print(f"DFS No solution found within depth {depth_limit}. Nodes: {self.explored_nodes}")
        return None
    
    def depth_limited_dfs(self, start_state, max_depth):
        """Depth-limited DFS helper function"""
        # Reset explored nodes for this depth iteration
        # We'll accumulate across iterations
        initial_explored = self.explored_nodes
        
        # Stack: (state, depth, path)
        stack = [(start_state, 0, [start_state])]
        visited_at_depth = {start_state}  # Track visited states at this depth
        
        while stack:
            state, depth, path = stack.pop()
            player, boxes = state
            
            self.explored_nodes += 1
            
            if self.explored_nodes % 1000 == 0:
                print(f"DFS explored {self.explored_nodes} nodes at depth {depth}...")
            
            # Check if solved
            if self.is_solved(boxes):
                return path
            
            # Skip if we've reached max depth
            if depth >= max_depth:
                continue
            
            # Generate and explore neighbors
            neighbors = self.get_neighbors(state)
            for neighbor in neighbors:
                if neighbor not in visited_at_depth:
                    visited_at_depth.add(neighbor)
                    new_path = path + [neighbor]
                    stack.append((neighbor, depth + 1, new_path))
        
        return None
    
    def solve(self, algorithm='astar'):
        """Main solve method with algorithm selection"""
        print(f"Attempting to solve with algorithm: {algorithm}")
        
        # Reset exploration metrics
        self.explored_nodes = 0
        self.solution_depth = 0
        
        if algorithm == 'astar':
            return self.solve_astar_improved()
        elif algorithm == 'bfs':
            return self.solve_bfs()
        elif algorithm == 'dfs':
            return self.solve_dfs_limited()
        else:
            return self.solve_astar_improved()


def main():
    """Main function to run the Sokoban GUI"""
    root = tk.Tk()
    app = SokobanGUI(root)
    
    # Load first level by default
    app.load_level(0)
    
    root.mainloop()


if __name__ == "__main__":
    main()