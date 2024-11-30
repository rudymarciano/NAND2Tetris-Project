// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, 
// the screen should be cleared.


(LOOP)          // Infinite loop keyboard input
  @SCREEN       // screen's base address
  D=A           // Store the screen address in D
  @i            // Pointer to current screen pixel
  M=D           // Initialize i to first screen pixel

  @KBD          // Address of the keyboard register
  D=M           // Load the current keyboard state
  @ALLWHITE    // If no key is pressed (D == 0), jump to FILLWHITE
  D;JEQ         
  @ALLBLACK    // If a key is pressed (D != 0), jump to FILLBLACK
  0;JEQ         

(ALLWHITE)     // Fill the screen with white pixels
  @TEMPCOLOR       // Temporary storage for the pixel color
  M=0           // Set CHANGE to 0 (white)
  @SETPIXEL     // Jump to the pixel filling loop
  0;JMP 

(ALLBLACK)     // Fill the screen with black pixels
  @TEMPCOLOR       // Temporary storage for the pixel color
  M=-1          // Set CHANGE to -1 (black)
  @SETPIXEL     // Jump to the pixel filling loop
  0;JMP

(SETPIXEL)      // Fill each pixel on the screen
  @i            // Get the current screen pixel address
  D=M           // Load the current pixel pointer into D
  @KBD   // Address just past the screen memory
  D=D-A         // Check if we've reached the end of the screen
  @LOOP         // If so, restart the process
  D;JEQ         

  @TEMPCOLOR       // Get the current color to set the pixel
  D=M           // Load the color (black or white)
  @i            // Get the current pixel pointer
  A=M           // Dereference i to point to the screen pixel
  M=D           // Set the pixel to the desired color

  @i            // Increment the pixel pointer
  M=M+1         // Move to the next pixel
  @SETPIXEL     // Repeat for the next pixel
  0;JMP         