import tkinter as tk
from tkinter import ttk, filedialog, messagebox, colorchooser
import struct
import os
from PIL import Image, ImageTk
import webbrowser

class ModernXBMEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Avatar XBM Color Editor | Made By: Advanced Modding Tools | Version 2.1")
        self.root.geometry("1600x1000")
        self.root.resizable(False, False)
        self.root.configure(bg='#2c2c2c')
        
        self.file_path = None
        self.file_data = None
        self.illumination_color_position = None
        self.current_colors = {'red': 0.0, 'green': 0.0, 'blue': 0.0, 'alpha': 1.0}
        self.original_colors = {'red': 0.0, 'green': 0.0, 'blue': 0.0, 'alpha': 1.0}
        self.hdr_scale = 1.0
        self.background_image = None
        self.auto_normalize = True  # Auto-normalization toggle
        
        # Set up window icon
        self._setup_window_icon()
        
        # Setup the modern interface
        self._setup_background_image()
        self.setup_modern_ui()
    
    def _setup_window_icon(self):
        """Set up the window icon"""
        try:
            # Try different possible icon locations - updated to use your new icon
            icon_paths = [
                os.path.join("assets", "XBM_Color_Editor_Icon.png"),  # Your new icon (first priority)
                os.path.join("assets", "editor_icon.png"),
                os.path.join("assets", "editor_icon.ico"),
                os.path.join("Background", "editor_background.png"),
                "XBM_Color_Editor_Icon.png",  # Fallback if in root directory
                "editor_icon.png",
                "editor_icon.ico"
            ]
            
            for icon_path in icon_paths:
                if os.path.exists(icon_path):
                    try:
                        if icon_path.lower().endswith('.ico'):
                            self.root.iconbitmap(icon_path)
                            break
                        elif icon_path.lower().endswith(('.png', '.jpg', '.jpeg')):
                            icon_image = Image.open(icon_path)
                            icon_image = icon_image.resize((32, 32), Image.Resampling.LANCZOS)
                            icon_photo = ImageTk.PhotoImage(icon_image)
                            self.root.iconphoto(True, icon_photo)
                            self.window_icon = icon_photo  # Keep reference to prevent garbage collection
                            break
                    except Exception:
                        continue
        except Exception:
            pass
    
    def _setup_background_image(self):
        """Load and set up the background image"""
        try:
            bg_image_path = os.path.join("Background", "editor_background.png")
            
            if os.path.exists(bg_image_path):
                pil_image = Image.open(bg_image_path)
                pil_image = pil_image.resize((1600, 1000), Image.Resampling.LANCZOS)
                self.background_image = ImageTk.PhotoImage(pil_image)
                
                self.canvas = tk.Canvas(self.root, width=1600, height=1000, highlightthickness=0)
                self.canvas.pack(fill=tk.BOTH, expand=True)
                self.canvas.create_image(0, 0, anchor=tk.NW, image=self.background_image)
            else:
                self.canvas = tk.Canvas(self.root, width=1600, height=1000, bg='#2c2c2c', highlightthickness=0)
                self.canvas.pack(fill=tk.BOTH, expand=True)
        except Exception:
            self.canvas = tk.Canvas(self.root, width=1600, height=1000, bg='#2c2c2c', highlightthickness=0)
            self.canvas.pack(fill=tk.BOTH, expand=True)
    
    def setup_modern_ui(self):
        """Create the modern UI layout"""
        self._create_header_section()
        self._create_file_selection_section()
        self._create_color_editor_section()
        self._create_preview_section()
        self._create_log_section()
        self._create_footer_section()
    
    def _create_header_section(self):
        """Create the modern header section"""
        # Main title
        self.canvas.create_text(
            80, 20,
            text="🎨 Avatar XBM Color Editor | Version 2.1",
            font=('Segoe UI', 32, 'bold'),
            fill='white',
            anchor=tk.NW
        )
        
        # Subtitle
        self.canvas.create_text(
            80, 90,
            text="Enhanced IlluminationColor1 Editor - Smart Auto-Normalization & Advanced Color Picker",
            font=('Segoe UI', 14),
            fill='#dddddd',
            anchor=tk.NW
        )
        
        # Version info
        self.canvas.create_text(
            80, 115,
            text="Professional Edition | Real-time Preview & Intelligent HDR Management",
            font=('Segoe UI', 10),
            fill='#bbbbbb',
            anchor=tk.NW
        )
    
    def _create_file_selection_section(self):
        """Create modern file selection section"""
        # Create a frame for file selection widgets
        file_frame = tk.Frame(self.root, bg='#3a3a3a', relief='solid', bd=1)
        self.file_frame_window = self.canvas.create_window(80, 170, anchor=tk.NW, window=file_frame, width=750, height=110)
        
        # Title
        title_label = tk.Label(file_frame, text="📂 File Operations", 
                              font=('Segoe UI', 12, 'bold'), fg='white', bg='#3a3a3a')
        title_label.pack(anchor=tk.W, padx=15, pady=(10, 5))
        
        # File path section
        path_frame = tk.Frame(file_frame, bg='#3a3a3a')
        path_frame.pack(fill=tk.X, padx=15, pady=(0, 5))
        
        tk.Label(path_frame, text="XBM File:", 
                font=('Segoe UI', 10), fg='#dddddd', bg='#3a3a3a').pack(side=tk.LEFT)
        
        self.file_entry = tk.Entry(path_frame, font=('Segoe UI', 10), bg='#2c2c2c', fg='black',
                                  insertbackground='white', relief='solid', bd=1, state='readonly')
        self.file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 10))
        
        # Buttons
        button_frame = tk.Frame(file_frame, bg='#3a3a3a')
        button_frame.pack(fill=tk.X, padx=15, pady=(0, 10))
        
        self.open_btn = tk.Button(button_frame, text="📁 Open XBM File", 
                                 command=self.open_file,
                                 bg='#2a7fff', fg='white',
                                 font=('Segoe UI', 10, 'bold'),
                                 relief='flat', padx=20, pady=8,
                                 cursor='hand2')
        self.open_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.save_btn = tk.Button(button_frame, text="💾 Save File", 
                                 command=self.save_file,
                                 bg='#107c10', fg='white',
                                 font=('Segoe UI', 10, 'bold'),
                                 relief='flat', padx=20, pady=8,
                                 cursor='hand2', state='disabled')
        self.save_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Status
        self.file_status = tk.Label(button_frame, text="No file loaded",
                                   bg='#3a3a3a', fg='#bbbbbb',
                                   font=('Segoe UI', 9))
        self.file_status.pack(side=tk.LEFT, padx=(20, 0))
    
    def _create_color_editor_section(self):
        """Create modern color editor section"""
        # Color editor frame
        color_frame = tk.Frame(self.root, bg='#3a3a3a', relief='solid', bd=1)
        self.color_frame_window = self.canvas.create_window(80, 290, anchor=tk.NW, window=color_frame, width=750, height=561)
        
        # Title
        title_label = tk.Label(color_frame, text="🎨 IlluminationColor1 Editor", 
                              font=('Segoe UI', 12, 'bold'), fg='white', bg='#3a3a3a')
        title_label.pack(anchor=tk.W, padx=15, pady=(10, 5))
        
        # Auto-normalization toggle section
        auto_norm_frame = tk.Frame(color_frame, bg='#3a3a3a')
        auto_norm_frame.pack(fill=tk.X, padx=15, pady=(0, 10))
        
        self.auto_normalize_var = tk.BooleanVar(value=True)
        auto_norm_check = tk.Checkbutton(auto_norm_frame, text="🔄 Smart Auto-Normalization", 
                                        variable=self.auto_normalize_var,
                                        command=self.toggle_auto_normalize,
                                        font=('Segoe UI', 10, 'bold'), 
                                        fg='#28a745', bg='#3a3a3a',
                                        selectcolor='#2c2c2c',
                                        activebackground='#3a3a3a',
                                        activeforeground='#28a745')
        auto_norm_check.pack(side=tk.LEFT)
        
        tk.Label(auto_norm_frame, text="• Automatically adjusts display values for HDR colors", 
                font=('Segoe UI', 9), fg='#bbbbbb', bg='#3a3a3a').pack(side=tk.LEFT, padx=(20, 0))
        
        # HDR Status section
        hdr_frame = tk.Frame(color_frame, bg='#3a3a3a')
        hdr_frame.pack(fill=tk.X, padx=15, pady=(0, 10))
        
        tk.Label(hdr_frame, text="HDR Status:", 
                font=('Segoe UI', 10, 'bold'), fg='#dddddd', bg='#3a3a3a').pack(side=tk.LEFT)
        
        self.hdr_indicator = tk.Label(hdr_frame, text="SDR (1.0x)", 
                                     font=('Segoe UI', 10, 'bold'), fg='#28a745', bg='#3a3a3a')
        self.hdr_indicator.pack(side=tk.LEFT, padx=(10, 0))
        
        # Color preview section
        preview_frame = tk.Frame(color_frame, bg='#3a3a3a')
        preview_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        tk.Label(preview_frame, text="Color Preview:",
                font=('Segoe UI', 10, 'bold'), fg='white', bg='#3a3a3a').pack(side=tk.LEFT)
        
        self.color_display = tk.Canvas(preview_frame, width=80, height=80, 
                                      bg='gray', highlightthickness=2,
                                      highlightbackground='#666666')
        self.color_display.pack(side=tk.LEFT, padx=(15, 20))
        
        # Current values display
        values_frame = tk.Frame(preview_frame, bg='#3a3a3a')
        values_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        self.values_label = tk.Label(values_frame, text="RGB: 0.000, 0.000, 0.000\nAlpha: 1.000\nHex: #000000",
                                    font=('Consolas', 9), fg='#dddddd', bg='#3a3a3a', justify=tk.LEFT)
        self.values_label.pack(anchor=tk.W)
        
        # Color sliders
        sliders_frame = tk.Frame(color_frame, bg='#3a3a3a')
        sliders_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        # Create sliders
        self.color_vars = {}
        self._create_color_slider(sliders_frame, "Red", "red", 0, '#ff4444')
        self._create_color_slider(sliders_frame, "Green", "green", 1, '#44ff44')
        self._create_color_slider(sliders_frame, "Blue", "blue", 2, '#4444ff')
        self._create_color_slider(sliders_frame, "Alpha", "alpha", 3, '#888888', max_val=1.0)
        
        # Action buttons
        action_frame = tk.Frame(color_frame, bg='#3a3a3a')
        action_frame.pack(fill=tk.X, padx=15, pady=(10, 15))
        
        # Color picker buttons row 1
        picker_frame1 = tk.Frame(action_frame, bg='#3a3a3a')
        picker_frame1.pack(fill=tk.X, pady=(0, 5))
        
        self.color_picker_btn = tk.Button(picker_frame1, text="🎨 Standard Color Picker",
                                         command=self.pick_color,
                                         bg='#2a7fff', fg='white',
                                         font=('Segoe UI', 9, 'bold'),
                                         relief='flat', padx=15, pady=6,
                                         cursor='hand2', state='disabled')
        self.color_picker_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.hdr_picker_btn = tk.Button(picker_frame1, text="⚡ HDR Color Picker",
                                       command=self.pick_hdr_color,
                                       bg='#ff8c00', fg='white',
                                       font=('Segoe UI', 9, 'bold'),
                                       relief='flat', padx=15, pady=6,
                                       cursor='hand2', state='disabled')
        self.hdr_picker_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Action buttons row 2
        action_frame2 = tk.Frame(action_frame, bg='#3a3a3a')
        action_frame2.pack(fill=tk.X)
        
        self.reset_btn = tk.Button(action_frame2, text="↻ Reset to Original",
                                  command=self.reset_to_original,
                                  bg='#4B4B4B', fg='white',
                                  font=('Segoe UI', 9),
                                  relief='flat', padx=15, pady=6,
                                  cursor='hand2', state='disabled')
        self.reset_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.normalize_btn = tk.Button(action_frame2, text="⚖️ Manual Normalize",
                                      command=self.normalize_hdr,
                                      bg='#6f42c1', fg='white',
                                      font=('Segoe UI', 9),
                                      relief='flat', padx=15, pady=6,
                                      cursor='hand2', state='disabled')
        self.normalize_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.copy_hex_btn = tk.Button(action_frame2, text="📋 Copy Hex",
                                     command=self.copy_hex_to_clipboard,
                                     bg='#17a2b8', fg='white',
                                     font=('Segoe UI', 9),
                                     relief='flat', padx=15, pady=6,
                                     cursor='hand2', state='disabled')
        self.copy_hex_btn.pack(side=tk.LEFT)
    
    def _create_color_slider(self, parent, label, color_name, row, color_hint, max_val=3.0):
        """Create a modern color slider"""
        # Container for this slider
        slider_container = tk.Frame(parent, bg='#3a3a3a')
        slider_container.pack(fill=tk.X, pady=5)
        
        # Label
        label_widget = tk.Label(slider_container, text=f"{label}:",
                               bg='#3a3a3a', fg='white',
                               font=('Segoe UI', 10, 'bold'), width=6, anchor='w')
        label_widget.pack(side=tk.LEFT, padx=(0, 15))
        
        # Variable
        var = tk.DoubleVar()
        var.trace('w', self.on_color_change)  # More responsive tracking
        self.color_vars[color_name] = var
        
        # Modern slider
        slider = tk.Scale(slider_container, from_=0, to=max_val, resolution=0.001,
                         variable=var, orient=tk.HORIZONTAL,
                         bg='#3a3a3a', fg='white',
                         highlightthickness=0, troughcolor='#404040',
                         activebackground=color_hint, length=380,
                         command=self.on_slider_change)
        slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 15))
        
        # Value entry
        entry = tk.Entry(slider_container, textvariable=var, width=8,
                        bg='#2c2c2c', fg='white',
                        relief='flat', font=('Consolas', 9),
                        insertbackground='white')
        entry.pack(side=tk.RIGHT)
        entry.bind('<Return>', self.on_entry_change)
        entry.bind('<FocusOut>', self.on_entry_change)
    
    def _create_preview_section(self):
        """Create texture info and large preview section"""
        # Preview frame - adjusted height to accommodate expanded color editor
        preview_frame = tk.Frame(self.root, bg='#3a3a3a', relief='solid', bd=1)
        self.preview_window = self.canvas.create_window(840, 170, anchor=tk.NW, window=preview_frame, width=700, height=420)
        
        # Title
        title_label = tk.Label(preview_frame, text="🖼️ Color Analysis & Preview",
                              font=('Segoe UI', 12, 'bold'), fg='white', bg='#3a3a3a')
        title_label.pack(anchor=tk.W, padx=15, pady=(10, 5))
        
        # Content frame
        content_frame = tk.Frame(preview_frame, bg='#3a3a3a')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        # Large color preview
        self.large_color_display = tk.Canvas(content_frame, width=230, height=230, 
                                            bg='gray', highlightthickness=2,
                                            highlightbackground='#666666')
        self.large_color_display.pack(side=tk.LEFT, padx=(0, 20))
        
        # Info panel
        info_panel = tk.Frame(content_frame, bg='#3a3a3a')
        info_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # File info
        tk.Label(info_panel, text="File Information:",
                font=('Segoe UI', 10, 'bold'), fg='white', bg='#3a3a3a').pack(anchor=tk.W, pady=(0, 5))
        
        self.file_info_label = tk.Label(info_panel, text="No file loaded",
                                       font=('Consolas', 9), fg='#dddddd', bg='#3a3a3a', anchor='w', justify=tk.LEFT)
        self.file_info_label.pack(anchor=tk.W, fill=tk.X, pady=(0, 15))
        
        # Color info
        tk.Label(info_panel, text="Color Information:",
                font=('Segoe UI', 10, 'bold'), fg='white', bg='#3a3a3a').pack(anchor=tk.W, pady=(0, 5))
        
        self.color_info_label = tk.Label(info_panel, text="RGB: -, -, -\nAlpha: -\nHDR Scale: 1.0x\nHex Values: -",
                                        font=('Consolas', 9), fg='#dddddd', bg='#3a3a3a', anchor='w', justify=tk.LEFT)
        self.color_info_label.pack(anchor=tk.W, fill=tk.X, pady=(0, 15))
        
        # Pattern info
        tk.Label(info_panel, text="Pattern Information:",
                font=('Segoe UI', 10, 'bold'), fg='white', bg='#3a3a3a').pack(anchor=tk.W, pady=(0, 5))
        
        self.pattern_info_label = tk.Label(info_panel, text="Position: -\nPattern: IlluminationColor1\nStatus: Not found",
                                          font=('Consolas', 9), fg='#dddddd', bg='#3a3a3a', anchor='w', justify=tk.LEFT)
        self.pattern_info_label.pack(anchor=tk.W, fill=tk.X)
    
    def _create_log_section(self):
        """Create modern log section"""
        # Log frame - adjusted position to accommodate new layout
        log_frame = tk.Frame(self.root, bg='#3a3a3a', relief='solid', bd=1)
        self.log_window = self.canvas.create_window(840, 600, anchor=tk.NW, window=log_frame, width=700, height=250)
        
        # Title
        title_label = tk.Label(log_frame, text="📋 Operation Log", 
                              font=('Segoe UI', 12, 'bold'), fg='white', bg='#3a3a3a')
        title_label.pack(anchor=tk.W, padx=15, pady=(10, 5))
        
        # Log text area with scrollbar
        log_content_frame = tk.Frame(log_frame, bg='#3a3a3a')
        log_content_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        self.log_text = tk.Text(log_content_frame, height=15, wrap=tk.WORD,
                               font=('Consolas', 9), bg='#2c2c2c', fg='#dddddd',
                               insertbackground='white', relief='solid', bd=1)
        
        scrollbar = tk.Scrollbar(log_content_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Initial log messages
        self.log_message("🎨 Avatar XBM Color Editor v2.1 - Enhanced Edition Ready")
        self.log_message("✨ New Features: Smart auto-normalization, HDR color picker, hex copy")
        self.log_message("💡 Auto-normalization: Intelligently manages HDR values for optimal display")
        self.log_message("📂 Open an XBM file to begin editing IlluminationColor1 values")
    
    def _create_footer_section(self):
        """Create modern footer section"""
        # Separator line
        self.canvas.create_line(
            80, 870, 1520, 870,
            fill='#404040',
            width=1
        )
        
        # Tips
        self.canvas.create_text(
            80, 890,
            text="💡 Smart Auto-Normalization: Automatically adjusts HDR values for optimal preview while preserving original intensity.",
            font=('Segoe UI', 10),
            fill='#bbbbbb',
            anchor=tk.NW
        )
        
        self.canvas.create_text(
            80, 915,
            text="💡 HDR Color Picker: Use for colors that exceed normal 0-1 range. Perfect for bright emissive materials.",
            font=('Segoe UI', 10),
            fill='#bbbbbb',
            anchor=tk.NW
        )
        
        # Link to other tools
        self.canvas.create_text(
            80, 940,
            text="💡 Check out my XBT to DDS Converter: ",
            font=('Segoe UI', 10),
            fill='#bbbbbb',
            anchor=tk.NW
        )
        
        # Clickable link
        link_text = self.canvas.create_text(
            315, 940,
            text="XBT <-> DDS Converter",
            font=('Segoe UI', 10, 'underline'),
            fill='#2a7fff',
            anchor=tk.NW,
            tags="tools_link"
        )
        
        def open_tools_link(event):
            webbrowser.open("https://github.com/JasperZebra/AVATAR-Save-Editor/releases")
        
        self.canvas.tag_bind("tools_link", "<Button-1>", open_tools_link)
        
        # Hover effects
        def on_link_enter(event):
            self.canvas.itemconfig(link_text, fill='#4d9fff')
            self.root.config(cursor="hand2")
        
        def on_link_leave(event):
            self.canvas.itemconfig(link_text, fill='#2a7fff')
            self.root.config(cursor="")
        
        self.canvas.tag_bind("tools_link", "<Enter>", on_link_enter)
        self.canvas.tag_bind("tools_link", "<Leave>", on_link_leave)
        
        # Status
        self.canvas.create_text(
            80, 965,
            text="Status: ",
            font=('Segoe UI', 10, 'bold'),
            fill='#2a7fff',
            anchor=tk.NW
        )
        
        self.status_text = self.canvas.create_text(
            130, 965,
            text="Ready - Open an XBM file to begin",
            font=('Segoe UI', 10),
            fill='#dddddd',
            anchor=tk.NW
        )
    
    def toggle_auto_normalize(self):
        """Toggle auto-normalization feature"""
        self.auto_normalize = self.auto_normalize_var.get()
        status = "enabled" if self.auto_normalize else "disabled"
        self.log_message(f"🔄 Smart auto-normalization {status}")
        
        # Immediately update display if colors are loaded
        if hasattr(self, 'color_vars') and self.color_vars:
            self.on_color_change()
    
    def on_slider_change(self, value):
        """Handle slider changes"""
        # Prevent recursive calls during programmatic updates
        if not hasattr(self, '_updating_sliders'):
            self.on_color_change()
    
    def on_entry_change(self, event=None):
        """Handle entry field changes"""
        # Prevent recursive calls during programmatic updates
        if not hasattr(self, '_updating_sliders'):
            self.on_color_change()
    
    def on_color_change(self, *args):
        """Handle color changes with smart auto-normalization"""
        if not hasattr(self, 'color_vars') or not self.color_vars:
            return
        
        # Prevent recursive updates
        if hasattr(self, '_updating_colors'):
            return
        
        try:
            self._updating_colors = True
            
            # Get current values
            r = self.color_vars['red'].get()
            g = self.color_vars['green'].get()
            b = self.color_vars['blue'].get()
            a = self.color_vars['alpha'].get()
            
            # Store raw values (these are what get saved to file)
            self.current_colors = {'red': r, 'green': g, 'blue': b, 'alpha': a}
            
            # Calculate HDR scale
            max_rgb = max(r, g, b)
            
            # Determine display values based on auto-normalization setting
            if self.auto_normalize and max_rgb > 1.0:
                # Smart auto-normalization for display only
                self.hdr_scale = max_rgb
                display_r = r / max_rgb
                display_g = g / max_rgb
                display_b = b / max_rgb
                
                # Update HDR indicator
                self.hdr_indicator.config(text=f"HDR ({max_rgb:.2f}x) - Auto", fg='#ff8c00')
                
                # Log the normalization when it first kicks in
                if not hasattr(self, '_last_auto_norm_state') or not self._last_auto_norm_state:
                    self.log_message(f"🔄 Auto-normalization active: scaling by {max_rgb:.3f}x for display")
                    self._last_auto_norm_state = True
                    
            else:
                # No normalization - show raw values
                self.hdr_scale = max_rgb if max_rgb > 1.0 else 1.0
                display_r, display_g, display_b = r, g, b
                
                if max_rgb > 1.0:
                    self.hdr_indicator.config(text=f"HDR ({max_rgb:.2f}x) - Raw", fg='#dc3545')
                else:
                    self.hdr_indicator.config(text="SDR (1.0x)", fg='#28a745')
                
                # Reset auto-norm state
                if hasattr(self, '_last_auto_norm_state') and self._last_auto_norm_state:
                    if not self.auto_normalize:
                        self.log_message("🔄 Auto-normalization disabled - showing raw values")
                    self._last_auto_norm_state = False
            
            # Update color displays with the appropriate values
            self.update_color_displays(display_r, display_g, display_b)
            
            # Update info displays with raw values
            self.update_info_displays(r, g, b, a)
        
        except (ValueError, tk.TclError):
            # Handle invalid input gracefully
            pass
        finally:
            # Always clean up the update flag
            if hasattr(self, '_updating_colors'):
                delattr(self, '_updating_colors')
    
    def update_color_displays(self, r, g, b):
        """Update color preview displays with proper clamping"""
        # Clamp values for display (0-1 range only)
        r_clamped = max(0, min(1, r))
        g_clamped = max(0, min(1, g))
        b_clamped = max(0, min(1, b))
        
        # Convert to hex
        r_int = int(r_clamped * 255)
        g_int = int(g_clamped * 255)
        b_int = int(b_clamped * 255)
        
        color_hex = f"#{r_int:02x}{g_int:02x}{b_int:02x}"
        
        # Update small preview
        self.color_display.config(bg=color_hex)
        
        # Update large preview
        self.large_color_display.config(bg=color_hex)
        self.large_color_display.delete("all")
        
        # Create color square with border
        self.large_color_display.create_rectangle(10, 10, 220, 220, 
                                                 fill=color_hex, outline='#666666', width=2)
        
        # Add hex value overlay
        brightness = (r_int + g_int + b_int) / 3
        text_color = 'white' if brightness < 128 else 'black'
        
        # Show if this is normalized or raw
        display_text = color_hex.upper()
        if self.auto_normalize and max(self.current_colors['red'], self.current_colors['green'], self.current_colors['blue']) > 1.0:
            display_text += "\n(Auto-Norm)"
        
        self.large_color_display.create_text(115, 115, text=display_text, 
                                            fill=text_color, font=('Consolas', 12, 'bold'),
                                            justify=tk.CENTER)
    
    def update_info_displays(self, r, g, b, a):
        """Update information displays with raw values"""
        # Update values label with raw values and normalized hex
        display_r = max(0, min(1, r))
        display_g = max(0, min(1, g))
        display_b = max(0, min(1, b))
        
        self.values_label.config(text=f"Raw RGB: {r:.3f}, {g:.3f}, {b:.3f}\nAlpha: {a:.3f}\nDisplay Hex: #{int(display_r*255):02x}{int(display_g*255):02x}{int(display_b*255):02x}")
        
        # Update color info with both raw and display values
        r_bytes = struct.pack('<f', r).hex().upper()
        g_bytes = struct.pack('<f', g).hex().upper()
        b_bytes = struct.pack('<f', b).hex().upper()
        a_bytes = struct.pack('<f', a).hex().upper()
        
        # Calculate what's being displayed
        max_rgb = max(r, g, b)
        if self.auto_normalize and max_rgb > 1.0:
            norm_note = f"Display: Normalized by {max_rgb:.3f}x"
        else:
            norm_note = "Display: Raw values"
        
        color_info = f"Raw RGB: {r:.3f}, {g:.3f}, {b:.3f}\nAlpha: {a:.3f}\nHDR Scale: {self.hdr_scale:.3f}x\n{norm_note}\nHex Bytes:\n  R: {r_bytes}\n  G: {g_bytes}\n  B: {b_bytes}\n  A: {a_bytes}"
        self.color_info_label.config(text=color_info)
    
    def open_file(self):
        """Open XBM file"""
        file_path = filedialog.askopenfilename(
            title="Open Avatar XBM File",
            filetypes=[("XBM files", "*.xbm"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'rb') as f:
                    self.file_data = bytearray(f.read())
                
                self.file_path = file_path
                filename = os.path.basename(file_path)
                
                # Update file entry
                self.file_entry.config(state='normal')
                self.file_entry.delete(0, tk.END)
                self.file_entry.insert(0, file_path)
                self.file_entry.config(state='readonly')
                
                if self.find_illumination_color():
                    self.load_current_colors()
                    self.enable_controls()
                    
                    # Update status
                    self.file_status.config(text=f"✓ {filename}", fg='#28a745')
                    self.update_status(f"File loaded: {filename}")
                    
                    # Update file info
                    file_size = len(self.file_data)
                    file_info = f"Filename: {filename}\nSize: {file_size:,} bytes\nType: Avatar XBM File"
                    self.file_info_label.config(text=file_info)
                    
                    # Update pattern info
                    pattern_info = f"Position: {self.illumination_color_position}\nPattern: IlluminationColor1\nStatus: Found ✓"
                    self.pattern_info_label.config(text=pattern_info)
                    
                    self.log_message(f"✅ Successfully loaded: {filename}")
                    self.log_message(f"📍 IlluminationColor1 found at position {self.illumination_color_position}")
                    
                else:
                    messagebox.showwarning("Warning", "IlluminationColor1 pattern not found in file!")
                    self.log_message("⚠️ Warning: IlluminationColor1 pattern not found!")
                    self.pattern_info_label.config(text="Position: -\nPattern: IlluminationColor1\nStatus: Not found ❌")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open file: {str(e)}")
                self.log_message(f"❌ Error loading file: {str(e)}")
    
    def find_illumination_color(self):
        """Find IlluminationColor1 pattern"""
        pattern = b'\x49\x6C\x6C\x75\x6D\x69\x6E\x61\x74\x69\x6F\x6E\x43\x6F\x6C\x6F\x72\x31'
        
        pos = self.file_data.find(pattern)
        if pos != -1:
            search_start = pos + len(pattern)
            null_pos = self.file_data.find(b'\x00', search_start)
            
            if null_pos != -1:
                self.illumination_color_position = null_pos + 1
                return True
        
        return False
    
    def load_current_colors(self):
        """Load color values from file"""
        if self.illumination_color_position and len(self.file_data) >= self.illumination_color_position + 16:
            pos = self.illumination_color_position
            
            # Read RGBA values
            red_bytes = self.file_data[pos:pos+4]
            green_bytes = self.file_data[pos+4:pos+8]
            blue_bytes = self.file_data[pos+8:pos+12]
            alpha_bytes = self.file_data[pos+12:pos+16]
            
            r = struct.unpack('<f', red_bytes)[0]
            g = struct.unpack('<f', green_bytes)[0]
            b = struct.unpack('<f', blue_bytes)[0]
            a = struct.unpack('<f', alpha_bytes)[0]
            
            # Store original and current values
            self.original_colors = {'red': r, 'green': g, 'blue': b, 'alpha': a}
            self.current_colors = self.original_colors.copy()
            
            # Prevent change events during loading
            self._updating_sliders = True
            
            try:
                # Update UI sliders
                self.color_vars['red'].set(r)
                self.color_vars['green'].set(g)
                self.color_vars['blue'].set(b)
                self.color_vars['alpha'].set(a)
            finally:
                delattr(self, '_updating_sliders')
            
            # Reset auto-norm state for new file
            self._last_auto_norm_state = False
            
            # Trigger initial color update
            self.on_color_change()
            
            max_rgb = max(r, g, b)
            hdr_status = "HDR" if max_rgb > 1.0 else "SDR"
            self.log_message(f"📊 Loaded {hdr_status} colors - R:{r:.3f} G:{g:.3f} B:{b:.3f} A:{a:.3f}")
            
            if max_rgb > 1.0:
                self.log_message(f"⚡ HDR detected with scale factor: {max_rgb:.3f}x")
                if self.auto_normalize:
                    self.log_message(f"🔄 Auto-normalization will scale display by {max_rgb:.3f}x")
    
    def enable_controls(self):
        """Enable controls after file load"""
        self.save_btn.config(state='normal')
        self.color_picker_btn.config(state='normal')
        self.hdr_picker_btn.config(state='normal')
        self.reset_btn.config(state='normal')
        self.normalize_btn.config(state='normal')
        self.copy_hex_btn.config(state='normal')
    
    def pick_color(self):
        """Open standard color picker (0-1 range)"""
        # Get current values for color picker
        r = self.color_vars['red'].get()
        g = self.color_vars['green'].get()
        b = self.color_vars['blue'].get()
        
        # If auto-normalize is on and we have HDR values, use normalized values for picker
        max_val = max(r, g, b)
        if self.auto_normalize and max_val > 1:
            display_r = r / max_val
            display_g = g / max_val
            display_b = b / max_val
            preserve_hdr_scale = max_val  # Remember the HDR scale
        else:
            display_r, display_g, display_b = r, g, b
            preserve_hdr_scale = 1.0
        
        # Clamp for color picker
        display_r = max(0, min(1, display_r))
        display_g = max(0, min(1, display_g))
        display_b = max(0, min(1, display_b))
        
        initial_color = (int(display_r * 255), int(display_g * 255), int(display_b * 255))
        
        color = colorchooser.askcolor(color=initial_color, title="Choose Standard Color (0-1 Range)")
        if color[0]:
            r_new, g_new, b_new = color[0]
            
            # Convert back to 0-1 range and apply HDR scale if we had one
            final_r = (r_new / 255.0) * preserve_hdr_scale
            final_g = (g_new / 255.0) * preserve_hdr_scale
            final_b = (b_new / 255.0) * preserve_hdr_scale
            
            self.color_vars['red'].set(final_r)
            self.color_vars['green'].set(final_g)
            self.color_vars['blue'].set(final_b)
            
            self.log_message(f"🎨 Standard color picked: RGB({r_new:.0f}, {g_new:.0f}, {b_new:.0f})")
            if preserve_hdr_scale > 1.0:
                self.log_message(f"📏 Applied HDR scale {preserve_hdr_scale:.3f}x: R:{final_r:.3f} G:{final_g:.3f} B:{final_b:.3f}")
            else:
                self.log_message(f"📏 Color values: R:{final_r:.3f} G:{final_g:.3f} B:{final_b:.3f}")
    
    def pick_hdr_color(self):
        """Advanced HDR color picker with intensity multiplier"""
        # Create HDR color picker dialog
        hdr_dialog = tk.Toplevel(self.root)
        hdr_dialog.title("HDR Color Picker")
        hdr_dialog.geometry("500x400")
        hdr_dialog.configure(bg='#2c2c2c')
        hdr_dialog.transient(self.root)
        hdr_dialog.grab_set()
        
        # Center the dialog
        hdr_dialog.geometry("+{}+{}".format(
            self.root.winfo_rootx() + 50,
            self.root.winfo_rooty() + 50
        ))
        
        # Main frame
        main_frame = tk.Frame(hdr_dialog, bg='#3a3a3a', relief='solid', bd=1)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        tk.Label(main_frame, text="⚡ HDR Color Picker", 
                font=('Segoe UI', 14, 'bold'), fg='white', bg='#3a3a3a').pack(pady=(10, 20))
        
        # Current color display
        current_frame = tk.Frame(main_frame, bg='#3a3a3a')
        current_frame.pack(pady=(0, 20))
        
        r = self.color_vars['red'].get()
        g = self.color_vars['green'].get()
        b = self.color_vars['blue'].get()
        
        # Normalize for display
        max_val = max(r, g, b, 1)
        display_r = min(r / max_val, 1) if max_val > 0 else 0
        display_g = min(g / max_val, 1) if max_val > 0 else 0
        display_b = min(b / max_val, 1) if max_val > 0 else 0
        
        color_hex = f"#{int(display_r*255):02x}{int(display_g*255):02x}{int(display_b*255):02x}"
        
        tk.Label(current_frame, text="Current Color:", 
                font=('Segoe UI', 10, 'bold'), fg='white', bg='#3a3a3a').pack()
        
        current_color_canvas = tk.Canvas(current_frame, width=100, height=50, bg=color_hex)
        current_color_canvas.pack(pady=5)
        
        # Base color selection
        base_frame = tk.Frame(main_frame, bg='#3a3a3a')
        base_frame.pack(pady=(0, 15))
        
        tk.Label(base_frame, text="1. Choose Base Color:", 
                font=('Segoe UI', 10, 'bold'), fg='white', bg='#3a3a3a').pack()
        
        base_color_var = tk.StringVar(value=color_hex)
        base_color_canvas = tk.Canvas(base_frame, width=100, height=50, bg=color_hex)
        base_color_canvas.pack(pady=5)
        
        def pick_base_color():
            initial = (int(display_r * 255), int(display_g * 255), int(display_b * 255))
            color = colorchooser.askcolor(color=initial, title="Choose Base Color")
            if color[0]:
                r_base, g_base, b_base = color[0]
                new_hex = f"#{int(r_base):02x}{int(g_base):02x}{int(b_base):02x}"
                base_color_var.set(new_hex)
                base_color_canvas.config(bg=new_hex)
                update_preview()
        
        tk.Button(base_frame, text="Pick Base Color", command=pick_base_color,
                 bg='#2a7fff', fg='white', font=('Segoe UI', 9, 'bold')).pack(pady=5)
        
        # Intensity multiplier
        intensity_frame = tk.Frame(main_frame, bg='#3a3a3a')
        intensity_frame.pack(pady=(0, 20), fill=tk.X, padx=20)
        
        tk.Label(intensity_frame, text="2. HDR Intensity Multiplier:", 
                font=('Segoe UI', 10, 'bold'), fg='white', bg='#3a3a3a').pack()
        
        intensity_var = tk.DoubleVar(value=max_val)
        intensity_scale = tk.Scale(intensity_frame, from_=0.1, to=5.0, resolution=0.1,
                                  variable=intensity_var, orient=tk.HORIZONTAL,
                                  bg='#3a3a3a', fg='white', highlightthickness=0,
                                  troughcolor='#404040', activebackground='#ff8c00',
                                  command=lambda x: update_preview())
        intensity_scale.pack(fill=tk.X, pady=5)
        
        intensity_label = tk.Label(intensity_frame, text="1.0x (Standard)", 
                                  font=('Segoe UI', 9), fg='#dddddd', bg='#3a3a3a')
        intensity_label.pack()
        
        # Preview
        preview_frame = tk.Frame(main_frame, bg='#3a3a3a')
        preview_frame.pack(pady=(0, 15))
        
        tk.Label(preview_frame, text="Preview (Normalized):", 
                font=('Segoe UI', 10, 'bold'), fg='white', bg='#3a3a3a').pack()
        
        preview_canvas = tk.Canvas(preview_frame, width=150, height=75, bg=color_hex)
        preview_canvas.pack(pady=5)
        
        preview_label = tk.Label(preview_frame, text="RGB: 0.000, 0.000, 0.000", 
                                font=('Consolas', 9), fg='#dddddd', bg='#3a3a3a')
        preview_label.pack()
        
        def update_preview():
            try:
                # Get base color
                base_hex = base_color_var.get()
                if base_hex.startswith('#'):
                    r_base = int(base_hex[1:3], 16) / 255.0
                    g_base = int(base_hex[3:5], 16) / 255.0
                    b_base = int(base_hex[5:7], 16) / 255.0
                else:
                    r_base = g_base = b_base = 0.5
                
                # Apply intensity
                intensity = intensity_var.get()
                r_hdr = r_base * intensity
                g_hdr = g_base * intensity
                b_hdr = b_base * intensity
                
                # Update intensity label
                intensity_label.config(text=f"{intensity:.1f}x {'(HDR)' if intensity > 1 else '(Standard)'}")
                
                # Normalize for preview
                max_hdr = max(r_hdr, g_hdr, b_hdr, 1)
                r_norm = r_hdr / max_hdr if max_hdr > 0 else 0
                g_norm = g_hdr / max_hdr if max_hdr > 0 else 0
                b_norm = b_hdr / max_hdr if max_hdr > 0 else 0
                
                preview_hex = f"#{int(r_norm*255):02x}{int(g_norm*255):02x}{int(b_norm*255):02x}"
                preview_canvas.config(bg=preview_hex)
                preview_label.config(text=f"HDR RGB: {r_hdr:.3f}, {g_hdr:.3f}, {b_hdr:.3f}")
                
                # Store values for application
                hdr_dialog.hdr_values = (r_hdr, g_hdr, b_hdr)
                
            except:
                pass
        
        # Initial preview update
        update_preview()
        
        # Buttons
        button_frame = tk.Frame(main_frame, bg='#3a3a3a')
        button_frame.pack(pady=10)
        
        def apply_hdr_color():
            if hasattr(hdr_dialog, 'hdr_values'):
                r_hdr, g_hdr, b_hdr = hdr_dialog.hdr_values
                self.color_vars['red'].set(r_hdr)
                self.color_vars['green'].set(g_hdr)
                self.color_vars['blue'].set(b_hdr)
                
                self.log_message(f"⚡ HDR color applied: R:{r_hdr:.3f} G:{g_hdr:.3f} B:{b_hdr:.3f}")
                self.log_message(f"📏 Intensity multiplier: {intensity_var.get():.1f}x")
                
            hdr_dialog.destroy()
        
        def cancel_hdr():
            hdr_dialog.destroy()
        
        tk.Button(button_frame, text="Apply HDR Color", command=apply_hdr_color,
                 bg='#ff8c00', fg='white', font=('Segoe UI', 10, 'bold'),
                 padx=20, pady=8).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(button_frame, text="Cancel", command=cancel_hdr,
                 bg='#6c757d', fg='white', font=('Segoe UI', 10),
                 padx=20, pady=8).pack(side=tk.LEFT)
    
    def reset_to_original(self):
        """Reset to original values"""
        if self.original_colors:
            self.color_vars['red'].set(self.original_colors['red'])
            self.color_vars['green'].set(self.original_colors['green'])
            self.color_vars['blue'].set(self.original_colors['blue'])
            self.color_vars['alpha'].set(self.original_colors['alpha'])
            self.log_message("↻ Reset to original values")
    
    def normalize_hdr(self):
        """Manually normalize HDR values to 0-1 range"""
        r = self.color_vars['red'].get()
        g = self.color_vars['green'].get()
        b = self.color_vars['blue'].get()
        
        max_val = max(r, g, b)
        
        if max_val > 1:
            self.color_vars['red'].set(r / max_val)
            self.color_vars['green'].set(g / max_val)
            self.color_vars['blue'].set(b / max_val)
            
            self.log_message(f"⚖️ Manual HDR normalization applied")
            self.log_message(f"📏 Normalized by factor of {max_val:.3f} (was HDR, now SDR)")
        else:
            self.log_message("ℹ️ No manual normalization needed (max value <= 1.0)")
    
    def copy_hex_to_clipboard(self):
        """Copy current hex color to clipboard"""
        try:
            # Get the display values (what the user sees)
            r = self.color_vars['red'].get()
            g = self.color_vars['green'].get()
            b = self.color_vars['blue'].get()
            
            # Apply auto-normalization if active
            max_rgb = max(r, g, b)
            if self.auto_normalize and max_rgb > 1.0:
                r_display = r / max_rgb
                g_display = g / max_rgb
                b_display = b / max_rgb
            else:
                r_display = min(r, 1)
                g_display = min(g, 1)
                b_display = min(b, 1)
            
            hex_color = f"#{int(r_display*255):02x}{int(g_display*255):02x}{int(b_display*255):02x}"
            
            self.root.clipboard_clear()
            self.root.clipboard_append(hex_color.upper())
            self.root.update()
            
            self.log_message(f"📋 Display hex color copied to clipboard: {hex_color.upper()}")
            if self.auto_normalize and max_rgb > 1.0:
                self.log_message(f"📏 Note: This is the normalized display color (scaled from {max_rgb:.3f}x HDR)")
            
            # Show temporary confirmation
            original_text = self.copy_hex_btn.cget("text")
            self.copy_hex_btn.config(text="✓ Copied!")
            self.root.after(1500, lambda: self.copy_hex_btn.config(text=original_text))
            
        except Exception as e:
            self.log_message(f"❌ Failed to copy hex color: {str(e)}")
    
    def save_file(self):
        """Save modified file"""
        if not self.file_path or not self.file_data:
            messagebox.showwarning("Warning", "No file loaded!")
            return
        
        try:
            pos = self.illumination_color_position
            
            # Get current raw values (not display values)
            r = self.color_vars['red'].get()
            g = self.color_vars['green'].get()
            b = self.color_vars['blue'].get()
            a = self.color_vars['alpha'].get()
            
            # Pack new values
            red_bytes = struct.pack('<f', r)
            green_bytes = struct.pack('<f', g)
            blue_bytes = struct.pack('<f', b)
            alpha_bytes = struct.pack('<f', a)
            
            # Update file data
            self.file_data[pos:pos+4] = red_bytes
            self.file_data[pos+4:pos+8] = green_bytes
            self.file_data[pos+8:pos+12] = blue_bytes
            self.file_data[pos+12:pos+16] = alpha_bytes
            
            # Save file
            save_path = filedialog.asksaveasfilename(
                title="Save XBM File",
                defaultextension=".xbm",
                filetypes=[("XBM files", "*.xbm"), ("All files", "*.*")],
                initialfile=os.path.basename(self.file_path)
            )
            
            if save_path:
                with open(save_path, 'wb') as f:
                    f.write(self.file_data)
                
                filename = os.path.basename(save_path)
                max_rgb = max(r, g, b)
                
                self.log_message(f"💾 File saved successfully: {filename}")
                self.log_message(f"📊 Final raw values - R:{r:.3f} G:{g:.3f} B:{b:.3f} A:{a:.3f}")
                
                if max_rgb > 1.0:
                    self.log_message(f"⚡ HDR values preserved: {max_rgb:.3f}x intensity")
                
                self.update_status(f"File saved: {filename}")
                
                # Show success message
                hdr_info = f"\nHDR Scale: {max_rgb:.3f}x" if max_rgb > 1.0 else ""
                messagebox.showinfo("Success", f"File saved successfully!\n\n{filename}{hdr_info}")
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {str(e)}")
            self.log_message(f"❌ Error saving: {str(e)}")
    
    def log_message(self, message):
        """Add message to log with timestamp"""
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def update_status(self, message):
        """Update status text"""
        self.canvas.itemconfig(self.status_text, text=message)
        self.root.update_idletasks()

def main():
    root = tk.Tk()
    
    # Set modern window properties
    try:
        root.wm_attributes('-alpha', 0.98)
    except:
        pass
    
    app = ModernXBMEditor(root)
    root.mainloop()

if __name__ == "__main__":
    main()