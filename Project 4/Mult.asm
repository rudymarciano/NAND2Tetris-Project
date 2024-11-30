// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
// The algorithm is based on repetitive addition.

//// Replace this comment with your code.

@R0        // Load R0
D=M        // D = M[R0] (value of R0)

@R2        // Initialize R2 to 0
M=0        // M[R2] = 0

@R1        // Load R1 
D=M        // D = M[R1] (value of R1)

@COUNT     // Stock R1 value in COUNT (loop counter)
M=D        // M[COUNT] = D

(LOOP)
  @COUNT     // Load COUNT
  D=M        // D = M[COUNT]

  @END       // If D (COUNT) == 0, END
  D;JEQ

  @R0        // Load R0
  D=M        // D = M[R0]

  @R2        // ADD D to M[R2]
  M=D+M      // M[R2] = M[R2] + D

  @COUNT     // Decrement COUNT
  M=M-1      // M[COUNT] = M[COUNT] - 1

  @LOOP      // Loop
  0;JMP

(END)
  @END   
  0;JMP



