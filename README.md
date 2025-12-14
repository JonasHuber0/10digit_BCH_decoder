# Syndrome Decoder for a 10-ary BCH Code over GF(11)

This project implements a syndrome decoding algorithm for a length-10 BCH code over the finite field GF(11). The decoder corrects up to two symbol errors using standard techniques from coding theory.

The goal of this project is to demonstrate how abstract algebra and coding theory can be translated into a working, practical error-correction system.

## Overview

The program takes a 10-digit vector of GF(11)
as input and attempts to recover the originally transmitted codeword.

Decoding is performed by:

Computing the syndrome vector 

Solving the associated non-linear system of equations derived from the syndrome

Distinguishing between the four possible cases:

- No errors

- One symbol error

- Two symbol errors

- Three or more errors (not decodable)

If decoding is successful, the corrected codeword is returned. Otherwise, the decoder requests retransmission.

## Features

Finite field arithmetic implemented explicitly over GF(11)

Syndrome-based BCH decoding

Detection and correction of up to two symbol errors

Clear separation between algebraic logic and program flow

## Usage

Build a standalone executable:

py -m PyInstaller --onefile BCH_decoder.py

Then enter any 10-digit code over GF(11). The program will report whether the word is correct, corrected, or not decodable.

## Examples
Input Code  |   Result
3417168201  |   Correct codeword
5382842390  |   Two errors detected and corrected
1013022030  |   One error detected and corrected
2317528101  |   Three or more errors detected, retransmission requested

## Extensibility

The decoder can be adapted to other two-error-correcting BCH codes.
Only the parity-check matrix needs to be changed; the decoding logic remains unchanged.

## Mathematical Background

The implementation follows standard syndrome decoding methods as presented in classical coding theory literature and demonstrates the practical use of finite fields, polynomial equations, and algebraic structure in reliable communication systems.
