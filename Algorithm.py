import math
import random
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from tkinter import font as tkfont
import time

class RSA_Implementation:
    def __init__(self):
        """Initialize the RSA implementation with default values"""
        self.p = 0
        self.q = 0
        self.n = 0
        self.phi_n = 0
        self.e = 0
        self.d = 0
        self.public_key = (0, 0)
        self.private_key = (0, 0)
        self.steps = []  # To store step-by-step details
        
    def is_prime(self, num):
        """Check if a number is prime"""
        if num <= 1:
            return False
        if num <= 3:
            return True
        if num % 2 == 0 or num % 3 == 0:
            return False
        i = 5
        while i * i <= num:
            if num % i == 0 or num % (i + 2) == 0:
                return False
            i += 6
        return True
    
    def generate_prime(self, min_val=100, max_val=1000):
        """Generate a random prime number within the given range"""
        while True:
            num = random.randint(min_val, max_val)
            if self.is_prime(num):
                return num
    
    def gcd(self, a, b):
        """Calculate the greatest common divisor of two numbers"""
        while b:
            a, b = b, a % b
        return a
    
    def mod_inverse(self, e, phi):
        """Calculate the modular multiplicative inverse"""
        def extended_gcd(a, b):
            if a == 0:
                return b, 0, 1
            else:
                gcd, x, y = extended_gcd(b % a, a)
                return gcd, y - (b // a) * x, x
        
        gcd, x, y = extended_gcd(e, phi)
        if gcd != 1:
            raise ValueError("Modular inverse does not exist")
        else:
            return x % phi
    
    def generate_keys(self):
        """Generate public and private keys with detailed steps"""
        self.steps = []  # Clear previous steps
        
        # Step 1: Generate two distinct prime numbers
        self.steps.append("Step 1: Generating two distinct prime numbers p and q...")
        self.p = self.generate_prime(100, 500)
        self.q = self.generate_prime(100, 500)
        
        # Ensure p and q are different
        while self.p == self.q:
            self.q = self.generate_prime(100, 500)
        
        self.steps.append(f"Selected prime p = {self.p}")
        self.steps.append(f"Selected prime q = {self.q}")
        
        # Step 2: Calculate n = p * q
        self.steps.append("\nStep 2: Calculating n = p × q...")
        self.n = self.p * self.q
        self.steps.append(f"n = {self.p} × {self.q} = {self.n}")
        
        # Step 3: Calculate phi(n) = (p-1) * (q-1)
        self.steps.append("\nStep 3: Calculating φ(n) = (p-1) × (q-1)...")
        self.phi_n = (self.p - 1) * (self.q - 1)
        self.steps.append(f"φ(n) = ({self.p}-1) × ({self.q}-1) = {self.p-1} × {self.q-1} = {self.phi_n}")
        
        # Step 4: Choose e such that 1 < e < phi(n) and gcd(e, phi(n)) = 1
        self.steps.append("\nStep 4: Selecting public exponent e...")
        
        # For educational purposes, try some common values first
        common_e_values = [65537, 17, 5, 3]  # Common choices for e
        e_found = False
        
        for potential_e in common_e_values:
            if potential_e < self.phi_n and self.gcd(potential_e, self.phi_n) == 1:
                self.e = potential_e
                e_found = True
                self.steps.append(f"Selected e = {self.e} (a common choice)")
                self.steps.append(f"Verified gcd({self.e}, {self.phi_n}) = 1")
                break
        
        # If no common value works, find another suitable e
        if not e_found:
            attempts = 0
            while True:
                attempts += 1
                self.e = random.randint(3, self.phi_n - 1)
                if self.gcd(self.e, self.phi_n) == 1:
                    self.steps.append(f"Selected e = {self.e} after {attempts} attempts")
                    self.steps.append(f"Verified gcd({self.e}, {self.phi_n}) = 1")
                    break
        
        # Step 5: Calculate d, the modular multiplicative inverse of e (mod phi(n))
        self.steps.append("\nStep 5: Calculating private exponent d...")
        self.steps.append(f"d = e⁻¹ mod φ(n) = {self.e}⁻¹ mod {self.phi_n}")
        self.d = self.mod_inverse(self.e, self.phi_n)
        self.steps.append(f"d = {self.d}")
        
        # Step 6: Set public and private keys
        self.steps.append("\nStep 6: Forming the key pairs...")
        self.public_key = (self.n, self.e)
        self.private_key = (self.n, self.d)
        
        self.steps.append(f"Public key (n, e) = {self.public_key}")
        self.steps.append(f"Private key (n, d) = {self.private_key}")
        
        return self.public_key, self.private_key, self.steps
    
    def encrypt(self, message):
        """Encrypt a message using the public key, showing all steps"""
        n, e = self.public_key
        encrypted_steps = []
        encrypted_message = []
        
        encrypted_steps.append("ENCRYPTION PROCESS")
        encrypted_steps.append("Using public key (n, e) = " + str(self.public_key))
        
        for i, char in enumerate(message):
            m = ord(char)
            c = pow(m, e, n)
            encrypted_message.append(c)
            
            # Show detailed steps
            encrypted_steps.append(f"\nEncrypting character '{char}' (position {i+1}):")
            encrypted_steps.append(f"1. Convert to ASCII: '{char}' → {m}")
            encrypted_steps.append(f"2. Apply formula c = m^e mod n:")
            encrypted_steps.append(f"   c = {m}^{e} mod {n}")
            encrypted_steps.append(f"3. Result: c = {c}")
            
        return encrypted_message, encrypted_steps
    
    def decrypt(self, encrypted_message):
        """Decrypt a message using the private key, showing all steps"""
        n, d = self.private_key
        decrypted_steps = []
        decrypted_message = ""
        
        decrypted_steps.append("DECRYPTION PROCESS")
        decrypted_steps.append("Using private key (n, d) = " + str(self.private_key))
        
        for i, c in enumerate(encrypted_message):
            m = pow(c, d, n)
            char = chr(m)
            decrypted_message += char
            
            # Show detailed steps
            decrypted_steps.append(f"\nDecrypting cipher value {c} (position {i+1}):")
            decrypted_steps.append(f"1. Apply formula m = c^d mod n:")
            decrypted_steps.append(f"   m = {c}^{d} mod {n}")
            decrypted_steps.append(f"2. Result: m = {m}")
            decrypted_steps.append(f"3. Convert to character: {m} → '{char}'")
            
        decrypted_steps.append(f"\nFinal decrypted message: '{decrypted_message}'")
        return decrypted_message, decrypted_steps

class ModernRSA_Interface:
    def __init__(self, root):
        """Initialize the GUI interface"""
        self.root = root
        self.root.title("RSA Cryptography System")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        
        # Create RSA instance
        self.rsa = RSA_Implementation()
        
        # Configure theme colors
        self.bg_color = "#f5f5f5"
        self.header_bg = "#3a6ea5"
        self.header_fg = "white"
        self.accent_color = "#4a86e8"
        self.success_color = "#43a047"
        
        # Set background color
        self.root.configure(bg=self.bg_color)
        
        # Configure styles
        self.style = ttk.Style()
        self.style.theme_use('alt')  # Use clam theme as base
        
        # Define custom fonts
        self.default_font = tkfont.nametofont("TkDefaultFont")
        self.default_font.configure(family="Segoe UI", size=10)
        
        self.header_font = tkfont.Font(family="Segoe UI", size=14, weight="bold")
        self.section_font = tkfont.Font(family="Segoe UI", size=12, weight="bold")
        self.code_font = tkfont.Font(family="Consolas", size=10)
        
        # Configure ttk styles
        self.style.configure("TFrame", background=self.bg_color)
        self.style.configure("TLabel", background=self.bg_color, font=self.default_font)
        self.style.configure("TLabelframe", background=self.bg_color)
        self.style.configure("TLabelframe.Label", background=self.bg_color, font=self.section_font)
        
        # Button styles
        self.style.configure("TButton", 
                             background=self.accent_color, 
                             foreground="white", 
                             font=("Segoe UI", 11),
                             relief="flat", 
                             borderwidth=0)
        
        self.style.map("TButton",
                       background=[('active', '#2a5db0')],
                       relief=[('pressed', 'sunken')])
        
        # Primary button style
        self.style.configure("Primary.TButton", 
                             background=self.accent_color, 
                             foreground="white", 
                             font=("Segoe UI", 11, "bold"))
        
        self.style.map("Primary.TButton",
                       background=[('active', '#2a5db0')],
                       relief=[('pressed', 'sunken')])
        
        # Create main container with padding
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create header
        self.create_header()
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=(10, 5))
        
        # Create tabs
        self.create_key_generation_tab()
        self.create_encryption_tab()
        self.create_step_by_step_tab()
        
        # Status bar
        self.status_frame = ttk.Frame(self.main_frame)
        self.status_frame.pack(fill=tk.X, pady=(5, 0))
        
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        
        self.status_bar = ttk.Label(self.status_frame, textvariable=self.status_var, 
                                   relief=tk.SUNKEN, padding=(5, 2))
        self.status_bar.pack(fill=tk.X)
        
        # Initialize encryption/decryption result storage
        self.encrypted_result = []
        self.encryption_steps = []
        self.decryption_steps = []
    
    def create_header(self):
        """Create the application header"""
        header_frame = ttk.Frame(self.main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Application icon/logo placeholder
        logo_label = ttk.Label(header_frame, text="🔒", font=("Segoe UI", 24))
        logo_label.pack(side=tk.LEFT, padx=(0, 10))
        
        # Title and subtitle
        title_frame = ttk.Frame(header_frame)
        title_frame.pack(side=tk.LEFT)
        
        title_label = ttk.Label(title_frame, text="RSA Cryptography System (Musaafir)", 
                               font=self.header_font)
        title_label.pack(anchor=tk.W)
        
        subtitle_label = ttk.Label(title_frame, 
                                  text="A step-by-step demonstration of public key encryption")
        subtitle_label.pack(anchor=tk.W)
    
    def create_key_generation_tab(self):
        """Create the key generation tab"""
        key_tab = ttk.Frame(self.notebook)
        self.notebook.add(key_tab, text=" Key Generation ")
        
        # Configure custom style for Checkbutton
        self.style.configure("Custom.TCheckbutton",
                            font=("Segoe UI", 10),
                            indicatorsize=15)
        self.style.map("Custom.TCheckbutton",
                    indicator=[('selected', '✔'), ('!selected', '☐')])  # Unicode tick and empty box
        
        # Instructions frame
        instruction_frame = ttk.LabelFrame(key_tab, text="Instructions")
        instruction_frame.pack(fill=tk.X, padx=5, pady=5)
        
        instruction_text = ("RSA encryption requires generating a pair of keys: a public key for encryption "
                           "and a private key for decryption. Click 'Generate Keys' to create a new key pair.")
        
        instruction_label = ttk.Label(instruction_frame, text=instruction_text, wraplength=900)
        instruction_label.pack(fill=tk.X, padx=10, pady=10)
        
        # Action frame
        action_frame = ttk.Frame(key_tab)
        action_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Add smaller primes checkbox for demonstration
        self.use_small_primes = tk.BooleanVar(value=True)
        small_primes_check = ttk.Checkbutton(action_frame, text="Use smaller primes for demonstration purposes",
                                            variable=self.use_small_primes)
        small_primes_check.pack(side=tk.LEFT, padx=5)
        
        # Add spacer
        spacer = ttk.Frame(action_frame)
        spacer.pack(side=tk.LEFT, expand=True)
        
        # Generate keys button
        self.generate_button = ttk.Button(action_frame, text="Generate Keys", 
                                         style="Primary.TButton",
                                         command=self.generate_keys)
        self.generate_button.pack(side=tk.RIGHT, padx=5, pady=5)
        
        # Results frame
        results_frame = ttk.LabelFrame(key_tab, text="Key Parameters")
        results_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Key display using grid layout for better organization
        params_frame = ttk.Frame(results_frame)
        params_frame.pack(fill=tk.BOTH, padx=10, pady=10)
        
        # Prime numbers
        ttk.Label(params_frame, text="Prime p:", font=("Segoe UI", 11, "bold")).grid(row=0, column=0, sticky=tk.W, pady=3)
        self.p_var = tk.StringVar()
        ttk.Label(params_frame, textvariable=self.p_var, font=self.code_font).grid(row=0, column=1, sticky=tk.W, padx=10)
        
        ttk.Label(params_frame, text="Prime q:", font=("Segoe UI", 11, "bold")).grid(row=1, column=0, sticky=tk.W, pady=3)
        self.q_var = tk.StringVar()
        ttk.Label(params_frame, textvariable=self.q_var, font=self.code_font).grid(row=1, column=1, sticky=tk.W, padx=10)
        
        # Modulus and totient
        ttk.Label(params_frame, text="Modulus n = p × q:", font=("Segoe UI", 11, "bold")).grid(row=2, column=0, sticky=tk.W, pady=3)
        self.n_var = tk.StringVar()
        ttk.Label(params_frame, textvariable=self.n_var, font=self.code_font).grid(row=2, column=1, sticky=tk.W, padx=10)
        
        ttk.Label(params_frame, text="φ(n) = (p-1) × (q-1):", font=("Segoe UI", 11, "bold")).grid(row=3, column=0, sticky=tk.W, pady=3)
        self.phi_var = tk.StringVar()
        ttk.Label(params_frame, textvariable=self.phi_var, font=self.code_font).grid(row=3, column=1, sticky=tk.W, padx=10)
        
        # Keys
        key_frame = ttk.Frame(results_frame)
        key_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # Public key
        public_key_frame = ttk.LabelFrame(key_frame, text="Public Key")
        public_key_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        public_key_content = ttk.Frame(public_key_frame)
        public_key_content.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(public_key_content, text="n:", font=("Segoe UI", 11, "bold")).grid(row=0, column=0, sticky=tk.W, pady=3)
        self.pub_n_var = tk.StringVar()
        ttk.Label(public_key_content, textvariable=self.pub_n_var, font=self.code_font).grid(row=0, column=1, sticky=tk.W, padx=10)
        
        ttk.Label(public_key_content, text="e:", font=("Segoe UI", 11, "bold")).grid(row=1, column=0, sticky=tk.W, pady=3)
        self.e_var = tk.StringVar()
        ttk.Label(public_key_content, textvariable=self.e_var, font=self.code_font).grid(row=1, column=1, sticky=tk.W, padx=10)
        
        # Private key
        private_key_frame = ttk.LabelFrame(key_frame, text="Private Key")
        private_key_frame.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(5, 0))
        
        private_key_content = ttk.Frame(private_key_frame)
        private_key_content.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(private_key_content, text="n:", font=("Segoe UI", 11, "bold")).grid(row=0, column=0, sticky=tk.W, pady=3)
        self.priv_n_var = tk.StringVar()
        ttk.Label(private_key_content, textvariable=self.priv_n_var, font=self.code_font).grid(row=0, column=1, sticky=tk.W, padx=10)
        
        ttk.Label(private_key_content, text="d:", font=("Segoe UI", 11, "bold")).grid(row=1, column=0, sticky=tk.W, pady=3)
        self.d_var = tk.StringVar()
        ttk.Label(private_key_content, textvariable=self.d_var, font=self.code_font).grid(row=1, column=1, sticky=tk.W, padx=10)
    
    def create_encryption_tab(self):
        """Create the encryption/decryption tab"""
        encrypt_tab = ttk.Frame(self.notebook)
        self.notebook.add(encrypt_tab, text=" Encryption & Decryption ")
        
        # Instructions frame
        instruction_frame = ttk.LabelFrame(encrypt_tab, text="Instructions")
        instruction_frame.pack(fill=tk.X, padx=5, pady=5)
        
        instruction_text = ("Enter your message below and click 'Process' to see the encryption and decryption results. "
                           "Make sure you've generated keys in the Key Generation tab first.")
        
        instruction_label = ttk.Label(instruction_frame, text=instruction_text, wraplength=900)
        instruction_label.pack(fill=tk.X, padx=10, pady=10)
        
        # Input frame
        input_frame = ttk.LabelFrame(encrypt_tab, text="Input")
        input_frame.pack(fill=tk.X, padx=5, pady=5)
        
        input_content = ttk.Frame(input_frame)
        input_content.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(input_content, text="Enter message:").grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.message_var = tk.StringVar()
        self.message_entry = ttk.Entry(input_content, textvariable=self.message_var, width=50)
        self.message_entry.grid(row=0, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # Process button
        button_frame = ttk.Frame(input_content)
        button_frame.grid(row=1, column=0, columnspan=2, pady=5)
        
        self.process_button = ttk.Button(button_frame, text="Process", 
                                        style="Primary.TButton",
                                        command=self.process_message)
        self.process_button.pack(pady=5)
        
        # Results frames
        results_pane = ttk.PanedWindow(encrypt_tab, orient=tk.VERTICAL)
        results_pane.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Encrypted results
        encrypted_frame = ttk.LabelFrame(results_pane, text="Encrypted Message")
        results_pane.add(encrypted_frame, weight=1)
        
        self.encrypted_text = scrolledtext.ScrolledText(encrypted_frame, wrap=tk.WORD, 
                                                       font=self.code_font, height=5)
        self.encrypted_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Decrypted results
        decrypted_frame = ttk.LabelFrame(results_pane, text="Decrypted Message")
        results_pane.add(decrypted_frame, weight=1)
        
        self.decrypted_text = scrolledtext.ScrolledText(decrypted_frame, wrap=tk.WORD, 
                                                       font=self.code_font, height=5)
        self.decrypted_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def create_step_by_step_tab(self):
        """Create the step-by-step details tab"""
        steps_tab = ttk.Frame(self.notebook)
        self.notebook.add(steps_tab, text=" Step-by-Step Details ")
        
        # Create notebook for detailed steps
        self.steps_notebook = ttk.Notebook(steps_tab)
        self.steps_notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Key generation steps tab
        key_steps_tab = ttk.Frame(self.steps_notebook)
        self.steps_notebook.add(key_steps_tab, text=" Key Generation Steps ")
        
        self.key_steps_text = scrolledtext.ScrolledText(key_steps_tab, wrap=tk.WORD, 
                                                      font=self.code_font)
        self.key_steps_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Encryption steps tab
        enc_steps_tab = ttk.Frame(self.steps_notebook)
        self.steps_notebook.add(enc_steps_tab, text=" Encryption Steps ")
        
        self.encryption_steps_text = scrolledtext.ScrolledText(enc_steps_tab, wrap=tk.WORD, 
                                                             font=self.code_font)
        self.encryption_steps_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Decryption steps tab
        dec_steps_tab = ttk.Frame(self.steps_notebook)
        self.steps_notebook.add(dec_steps_tab, text=" Decryption Steps ")
        
        self.decryption_steps_text = scrolledtext.ScrolledText(dec_steps_tab, wrap=tk.WORD, 
                                                             font=self.code_font)
        self.decryption_steps_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def generate_keys(self):
        """Generate RSA key pairs and display the parameters"""
        try:
            # Show "working" status
            self.status_var.set("Generating keys...")
            self.root.update_idletasks()
            
            # Set prime number range based on checkbox selection
            if self.use_small_primes.get():
                # Use smaller primes (2 digits) for demonstration
                min_val, max_val = 10, 99
            else:
                # Use larger primes (5+ digits) for better security
                min_val, max_val = 10000, 99999
                
            # Modify the RSA implementation to use our specified range
            self.rsa.p = self.rsa.generate_prime(min_val, max_val)
            self.rsa.q = self.rsa.generate_prime(min_val, max_val)
            
            # Ensure p and q are different
            while self.rsa.p == self.rsa.q:
                self.rsa.q = self.rsa.generate_prime(min_val, max_val)
                
            # Now proceed with key generation using these primes
            self.rsa.n = self.rsa.p * self.rsa.q
            self.rsa.phi_n = (self.rsa.p - 1) * (self.rsa.q - 1)
            
            # Choose e such that 1 < e < phi(n) and gcd(e, phi(n)) = 1
            common_e_values = [65537, 17, 5, 3]  # Common choices for e
            e_found = False
            
            for potential_e in common_e_values:
                if potential_e < self.rsa.phi_n and self.rsa.gcd(potential_e, self.rsa.phi_n) == 1:
                    self.rsa.e = potential_e
                    e_found = True
                    break
            
            # If no common value works, find another suitable e
            if not e_found:
                while True:
                    self.rsa.e = random.randint(3, self.rsa.phi_n - 1)
                    if self.rsa.gcd(self.rsa.e, self.rsa.phi_n) == 1:
                        break
            
            # Calculate d, the modular multiplicative inverse of e (mod phi(n))
            self.rsa.d = self.rsa.mod_inverse(self.rsa.e, self.rsa.phi_n)
            
            # Set public and private keys
            self.rsa.public_key = (self.rsa.n, self.rsa.e)
            self.rsa.private_key = (self.rsa.n, self.rsa.d)
            
            # Generate steps for display (calling a modified method that accepts our generated values)
            steps = self.generate_key_steps()
            
            # Update key parameter displays
            self.p_var.set(str(self.rsa.p))
            self.q_var.set(str(self.rsa.q))
            self.n_var.set(str(self.rsa.n))
            self.phi_var.set(str(self.rsa.phi_n))
            
            # Update public key display
            self.pub_n_var.set(str(self.rsa.public_key[0]))
            self.e_var.set(str(self.rsa.public_key[1]))
            
            # Update private key display
            self.priv_n_var.set(str(self.rsa.private_key[0]))
            self.d_var.set(str(self.rsa.private_key[1]))
            
            # Update key generation steps
            self.key_steps_text.delete(1.0, tk.END)
            self.key_steps_text.insert(tk.END, "\n".join(steps))
            
            # Update status
            self.status_var.set("Keys generated successfully")
            
            # Switch to the step-by-step tab and show key generation steps
            self.notebook.select(2)  # Select Step-by-Step tab
            self.steps_notebook.select(0)  # Select Key Generation Steps tab
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate keys: {str(e)}")
            self.status_var.set("Error generating keys")
            
    def generate_key_steps(self):
        """Generate step-by-step details for key generation"""
        steps = []
        
        # Step 1: Prime selection
        steps.append("Step 1: Generating two distinct prime numbers p and q...")
        steps.append(f"Selected prime p = {self.rsa.p}")
        steps.append(f"Selected prime q = {self.rsa.q}")
        
        # Step 2: Calculate n = p * q
        steps.append("\nStep 2: Calculating n = p × q...")
        steps.append(f"n = {self.rsa.p} × {self.rsa.q} = {self.rsa.n}")
        
        # Step 3: Calculate phi(n) = (p-1) * (q-1)
        steps.append("\nStep 3: Calculating φ(n) = (p-1) × (q-1)...")
        steps.append(f"φ(n) = ({self.rsa.p}-1) × ({self.rsa.q}-1) = {self.rsa.p-1} × {self.rsa.q-1} = {self.rsa.phi_n}")
        
        # Step 4: Select e
        steps.append("\nStep 4: Selecting public exponent e...")
        steps.append(f"Selected e = {self.rsa.e}")
        steps.append(f"Verified gcd({self.rsa.e}, {self.rsa.phi_n}) = 1")
        
        # Step 5: Calculate d
        steps.append("\nStep 5: Calculating private exponent d...")
        steps.append(f"d = e⁻¹ mod φ(n) = {self.rsa.e}⁻¹ mod {self.rsa.phi_n}")
        steps.append(f"d = {self.rsa.d}")
        
        # Step 6: Form key pairs
        steps.append("\nStep 6: Forming the key pairs...")
        steps.append(f"Public key (n, e) = {self.rsa.public_key}")
        steps.append(f"Private key (n, d) = {self.rsa.private_key}")
        
        return steps
    
    def process_message(self):
        """Process the input message - encrypt and decrypt with detailed steps"""
        message = self.message_var.get()
        if not message:
            messagebox.showwarning("Warning", "Please enter a message")
            return
            
        if self.rsa.public_key == (0, 0) or self.rsa.private_key == (0, 0):
            messagebox.showwarning("Warning", "Please generate keys first")
            return
            
        try:
            # Show "working" status
            self.status_var.set("Processing message...")
            self.root.update_idletasks()
            
            # Encrypt the message
            self.encrypted_result, self.encryption_steps = self.rsa.encrypt(message)
            
            # Format encrypted data for display
            encrypted_display = "Encrypted values (decimal):\n"
            encrypted_display += str(self.encrypted_result)
            
            # Show encrypted text
            self.encrypted_text.delete(1.0, tk.END)
            self.encrypted_text.insert(tk.END, encrypted_display)
            
            # Decrypt the message
            decrypted_message, self.decryption_steps = self.rsa.decrypt(self.encrypted_result)
            
            # Show decrypted text
            self.decrypted_text.delete(1.0, tk.END)
            self.decrypted_text.insert(tk.END, decrypted_message)
            
            # Update step-by-step details
            self.encryption_steps_text.delete(1.0, tk.END)
            self.encryption_steps_text.insert(tk.END, "\n".join(self.encryption_steps))
            
            self.decryption_steps_text.delete(1.0, tk.END)
            self.decryption_steps_text.insert(tk.END, "\n".join(self.decryption_steps))
            
            # Switch to the step-by-step tab
            self.notebook.select(2)  # Select Step-by-Step tab
            self.steps_notebook.select(1)  # Start with encryption steps
            
            self.status_var.set("Message processed successfully")
            
        except Exception as e:
            messagebox.showerror("Error", f"Processing error: {str(e)}")
            self.status_var.set("Error processing message")

    def show_animation(self, process_type):
        """Show a visual animation of the encryption or decryption process"""
        if process_type not in ["encrypt", "decrypt"]:
            return
            
        # Create animation window
        anim_window = tk.Toplevel(self.root)
        anim_window.title(f"{'Encryption' if process_type == 'encrypt' else 'Decryption'} Animation")
        anim_window.geometry("600x400")
        anim_window.transient(self.root)
        anim_window.grab_set()
        
        # Animation canvas
        canvas = tk.Canvas(anim_window, bg="white")
        canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Animation controls
        control_frame = ttk.Frame(anim_window)
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        speed_label = ttk.Label(control_frame, text="Animation Speed:")
        speed_label.pack(side=tk.LEFT, padx=5)
        
        speed_var = tk.DoubleVar(value=1.0)
        speed_scale = ttk.Scale(control_frame, from_=0.5, to=3.0, 
                              orient=tk.HORIZONTAL, variable=speed_var,
                              length=200)
        speed_scale.pack(side=tk.LEFT, padx=5)
        
        close_button = ttk.Button(control_frame, text="Close",
                                 command=anim_window.destroy)
        close_button.pack(side=tk.RIGHT, padx=5)
        
        # TO-DO: Implement animation based on the process type

def main():
    """Main function to run the application"""
    root = tk.Tk()
    app = ModernRSA_Interface(root)
    
    # Center window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    # Set window icon
    # If you have an icon file, you can use:
    # root.iconbitmap('icon.ico')
    
    root.mainloop()

if __name__ == "__main__":
    main()