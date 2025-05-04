"""
Dynamic DES (Data Encryption Standard) Implementation
This project implements the DES encryption algorithm with all the necessary components
including S-Boxes, P-Box, Initial Permutation (IP), and Final Permutation (FP).
"""

import random

class DES:
    def __init__(self):
        # Initial Permutation (IP) Table
        self.IP = [
            58, 50, 42, 34, 26, 18, 10, 2,
            60, 52, 44, 36, 28, 20, 12, 4,
            62, 54, 46, 38, 30, 22, 14, 6,
            64, 56, 48, 40, 32, 24, 16, 8,
            57, 49, 41, 33, 25, 17, 9, 1,
            59, 51, 43, 35, 27, 19, 11, 3,
            61, 53, 45, 37, 29, 21, 13, 5,
            63, 55, 47, 39, 31, 23, 15, 7
        ]

        # Final Permutation (FP) Table
        self.FP = [
            40, 8, 48, 16, 56, 24, 64, 32,
            39, 7, 47, 15, 55, 23, 63, 31,
            38, 6, 46, 14, 54, 22, 62, 30,
            37, 5, 45, 13, 53, 21, 61, 29,
            36, 4, 44, 12, 52, 20, 60, 28,
            35, 3, 43, 11, 51, 19, 59, 27,
            34, 2, 42, 10, 50, 18, 58, 26,
            33, 1, 41, 9, 49, 17, 57, 25
        ]

        # Permutation (P) Box Table for key
        self.P_BOX = [
            16, 7, 20, 21, 29, 12, 28, 17,
            1, 15, 23, 26, 5, 18, 31, 10,
            2, 8, 24, 14, 32, 27, 3, 9,
            19, 13, 30, 6, 22, 11, 4, 25
        ]
        
        # Expansion (E) Box Table 32 -> 48 bits
        self.E_BOX = [
            32, 1, 2, 3, 4, 5,
            4, 5, 6, 7, 8, 9,
            8, 9, 10, 11, 12, 13,
            12, 13, 14, 15, 16, 17,
            16, 17, 18, 19, 20, 21,
            20, 21, 22, 23, 24, 25,
            24, 25, 26, 27, 28, 29,
            28, 29, 30, 31, 32, 1
        ]

        # S-Boxes in DES heart 48 -> 32 bits
        self.S_BOXES = [
            # S1
            [
                [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
                [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
                [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
                [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
            ],
            # S2
            [
                [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
                [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
                [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
                [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]
            ],
            # S3
            [
                [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
                [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
                [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
                [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]
            ],
            # S4
            [
                [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
                [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
                [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
                [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]
            ],
            # S5
            [
                [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
                [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
                [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
                [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]
            ],
            # S6
            [
                [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
                [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
                [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
                [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]
            ],
            # S7
            [
                [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
                [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
                [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
                [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]
            ],
            # S8
            [
                [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
                [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
                [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
                [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
            ]
        ]

        # Permuted Choice 1 (PC-1) table for key preparation (56 bits)
        self.PC1 = [
            57, 49, 41, 33, 25, 17, 9,
            1, 58, 50, 42, 34, 26, 18,
            10, 2, 59, 51, 43, 35, 27,
            19, 11, 3, 60, 52, 44, 36,
            63, 55, 47, 39, 31, 23, 15,
            7, 62, 54, 46, 38, 30, 22,
            14, 6, 61, 53, 45, 37, 29,
            21, 13, 5, 28, 20, 12, 4
        ]

        # Permuted Choice 2 (PC-2) table for subkey generation (48 bits)
        self.PC2 = [
            14, 17, 11, 24, 1, 5, 3, 28,
            15, 6, 21, 10, 23, 19, 12, 4,
            26, 8, 16, 7, 27, 20, 13, 2,
            41, 52, 31, 37, 47, 55, 30, 40,
            51, 45, 33, 48, 44, 49, 39, 56,
            34, 53, 46, 42, 50, 36, 29, 32
        ]

        # Rotation schedule for key bits - number of bits to rotate left per round
        self.ROTATIONS = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]
        
        # Parity bit positions
        self.PARITY_BITS = [8, 16, 24, 32, 40, 48, 56, 64]
        
        # Bits removed during PC-2
        self.REMOVED_PC2_BITS = [9, 18, 22, 25, 35, 38, 43, 54]

    def _str_to_binary(self, text):
        """Convert a string to its binary representation."""
        return ''.join(format(ord(char), '08b') for char in text)
    
    def _hex_to_binary(self, hex_str):
        """Convert a hexadecimal string to its binary representation."""
        return bin(int(hex_str, 16))[2:].zfill(len(hex_str) * 4)
    
    def _binary_to_hex(self, binary):
        """Convert a binary string to its hexadecimal representation."""
        return hex(int(binary, 2))[2:].zfill(len(binary) // 4)
    
    def _binary_to_str(self, binary):
        """Convert a binary string to its ASCII representation."""
        binary = binary.zfill((len(binary) + 7) // 8 * 8)  # Ensure multiple of 8
        return ''.join(chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8))
    
    def _apply_permutation(self, block, table):
        """Apply a permutation table to a bit string."""
        return ''.join(block[i-1] for i in table)
    
    def _left_shift(self, bits, n_shifts):
        """Perform a circular left shift on the bit string."""
        return bits[n_shifts:] + bits[:n_shifts]
    
    def _xor(self, bits1, bits2):
        """Perform bitwise XOR on two bit strings."""
        return ''.join('1' if b1 != b2 else '0' for b1, b2 in zip(bits1, bits2))
    
    def _generate_random_key(self):
        """Generate a random 64-bit key."""
        return ''.join(random.choice('01') for _ in range(64))
    
    def _generate_random_message(self):
        """Generate a random 64-bit message."""
        return ''.join(random.choice('01') for _ in range(64))
    
    def _prepare_input(self, input_data, input_type='binary', block_size=64):
        """
        Prepare the input for processing.
        - input_data: the data to be prepared (string, hex, or binary)
        - input_type: 'text', 'hex', or 'binary'
        - block_size: the desired block size (default 64 bits for DES)
        """
        if input_type == 'text':
            binary = self._str_to_binary(input_data)
        elif input_type == 'hex':
            binary = self._hex_to_binary(input_data)
        elif input_type == 'binary':
            binary = input_data
        else:
            raise ValueError("Input type must be 'text', 'hex', or 'binary'")
        
        # Pad the binary to be a multiple of block_size
        if len(binary) % block_size != 0:
            padding_length = block_size - (len(binary) % block_size)
            binary += '0' * padding_length
        
        # Split the binary into blocks
        blocks = [binary[i:i+block_size] for i in range(0, len(binary), block_size)]
        return blocks
    
    def generate_subkeys(self, key):
        """
        Generate the 16 subkeys for DES encryption/decryption.
        - key: 64-bit key string (in binary)
        """
        # Step 1: Remove parity bits (bits at positions 8, 16, 24, 32, 40, 48, 56, 64)
        # Convert to a list of bits for easier manipulation
        key_bits = list(key)
        key_without_parity = ''.join(key_bits[i-1] for i in range(1, 65) if i not in self.PARITY_BITS)
        
        # Step 2: Apply PC-1 permutation
        key_pc1 = self._apply_permutation(key, self.PC1)
        
        # Step 3: Split into C and D parts
        c = key_pc1[:28]
        d = key_pc1[28:]
        
        subkeys = []
        
        # Step 4 & 5: Generate 16 subkeys with rotations and PC-2
        for i in range(16):
            # Rotate bits according to the rotation schedule
            c = self._left_shift(c, self.ROTATIONS[i])
            d = self._left_shift(d, self.ROTATIONS[i])
            
            # Combine C and D
            cd = c + d
            
            # Apply PC-2 permutation to get the subkey
            subkey = self._apply_permutation(cd, self.PC2)
            subkeys.append(subkey)
        
        return subkeys
    
    def _feistel_function(self, right_half, subkey):
        """
        Implement the Feistel function for DES.
        - right_half: 32-bit right half of the block
        - subkey: 48-bit subkey for the current round
        """
        # Step 1: Expand the 32-bit right half to 48 bits using E-BOX
        expanded = self._apply_permutation(right_half, self.E_BOX)
        
        # Step 2: XOR the expanded right half with the subkey
        xor_result = self._xor(expanded, subkey)
        
        # Step 3: Divide the 48-bit result into 8 groups of 6 bits
        s_box_input = [xor_result[i:i+6] for i in range(0, 48, 6)]
        
        s_box_output = ""
        
        # Step 4: Apply S-boxes to each group
        for i in range(8):
            # Get the row and column for the S-box lookup
            row = int(s_box_input[i][0] + s_box_input[i][5], 2)
            col = int(s_box_input[i][1:5], 2)
            
            # Get the value from the S-box
            value = self.S_BOXES[i][row][col]
            
            # Convert the value to 4-bit binary and add to output
            s_box_output += format(value, '04b')
        
        # Step 5: Apply P-box permutation to the 32-bit S-box output
        return self._apply_permutation(s_box_output, self.P_BOX)
    
    def encrypt_block(self, block, subkeys):
        """
        Encrypt a single 64-bit block using DES.
        - block: 64-bit block to encrypt (in binary)
        - subkeys: List of 16 subkeys for encryption
        """
        # Step 1: Apply initial permutation (IP)
        ip_output = self._apply_permutation(block, self.IP)
        
        # Step 2: Split the output into left and right halves
        left = ip_output[:32]
        right = ip_output[32:]
        
        # Step 3: Perform 16 Feistel rounds
        for i in range(16):
            # Save the current right half
            old_right = right
            
            # Calculate new right half: left XOR f(right, subkey)
            right = self._xor(left, self._feistel_function(right, subkeys[i]))
            
            # Update left half
            left = old_right
        
        # Step 4: Swap the final left and right halves
        combined = right + left
        
        # Step 5: Apply final permutation (FP)
        return self._apply_permutation(combined, self.FP)
    
    def encrypt(self, plaintext, key=None, input_type='text', output_type='hex'):
        """
        Encrypt the plaintext using DES.
        - plaintext: The text to encrypt
        - key: 64-bit key (binary) or None for random key
        - input_type: 'text', 'hex', or 'binary'
        - output_type: 'hex' or 'binary'
        """
        # Generate a random key if none provided
        if key is None:
            key = self._generate_random_key()
        
        # Generate subkeys
        subkeys = self.generate_subkeys(key)
        
        # Prepare plaintext into 64-bit blocks
        blocks = self._prepare_input(plaintext, input_type)
        
        # Encrypt each block
        encrypted_blocks = [self.encrypt_block(block, subkeys) for block in blocks]
        
        # Combine the encrypted blocks
        encrypted_binary = ''.join(encrypted_blocks)
        
        # Return in the cipher in format of binary.
        if output_type == 'hex':
            return self._binary_to_hex(encrypted_binary)
        else:
            return encrypted_binary