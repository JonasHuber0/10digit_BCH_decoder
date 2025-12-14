import sys
import numpy as np


class GF11:
    """Container class for Galois Field 11 arithmetic, we use saticmethod as the class is just a container for GF(11).
       The Rules of Modular arithmetic are univerally correct and independent of the class."""
    
    MOD = 11
    
    # Inverse map for GF(11)
    INV_MAP = {1: 1, 2: 6, 3: 4, 4: 3, 5: 9, 6: 2, 7: 8, 8: 7, 9: 5, 10: 10}
    ROOT_MAP = {0: 0, 1: 1, 3: 5, 4: 2, 5: 4, 9: 3}

    @staticmethod
    def add(a, b): return (a + b) % 11
    
    @staticmethod
    def sub(a, b): return (a - b) % 11
    
    @staticmethod
    def mul(a, b): return (a * b) % 11
    
    @staticmethod
    def inv(a):
        if a == 0: raise ValueError("Division by zero in GF(11) is not possible, fields have no zero divisors.")
        return GF11.INV_MAP[a]
    
    @staticmethod
    def div(a, b): return GF11.mul(a, GF11.inv(b))

    @staticmethod
    def root(a):
        NON_SQUARES=(2, 6, 7, 8, 10)
        if a in NON_SQUARES: 
            raise ValueError(f"{a} is not a perfect square in GF(11).")
        return GF11.ROOT_MAP[a] 


def calculate_syndrome_vector(y):

   H_trans = np.vander([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], increasing=True)[:, 0:4] #define the transpose of the parity check matrix
   S = np.dot(y, H_trans) % 11
   return S


def decode_BCH(input_vector):
    #Calculate syndrom
    S = calculate_syndrome_vector(input_vector)
    S1 = S[0]
    S2 = S[1]
    S3 = S[2]
    S4 = S[3]

    #Case 0 errors
    if all(s == 0 for s in S):
        return input_vector, "The codeword was received with 0 erros."
    
    #Prepare for other cases
    P = GF11.sub(GF11.mul(S2, S2), GF11.mul(S1, S3))
    Q = GF11.sub(GF11.mul(S1, S4), GF11.mul(S2, S3))
    R = GF11.sub(GF11.mul(S3, S3), GF11.mul(S2, S4))
    D = GF11.sub(GF11.mul(Q, Q), GF11.mul(4, GF11.mul(P, R)))

    #Case 1 error
    if all(t == 0 for t in (P, Q, R)):
        #Calculate error postition and magnitude
        error_mag = S1
        error_pos = GF11.div(S2, S1)
        #Correct the error
        corrected_value= GF11.sub(input_vector[error_pos-1], error_mag) #-1 as pyhton indexes from 0 on
        input_vector[error_pos-1] = corrected_value
        final_vector = [int(x) for x in input_vector]
        return final_vector, f"The codeword was received with one error of magnituge {error_mag} in position {error_pos} and corrected." 
        #Here the -1 is not needed as we just assume the user indexes from 1 onward!
    
    #Case 2 erros
    if P != 0 and R != 0 and D in (1, 3, 4, 5, 9):
        #Calculate error postitions and magnitudes
        error_pos_2 = GF11.div(GF11.sub(GF11.sub(0, Q), GF11.root(D)), GF11.mul(2, P))
        error_pos_1 = GF11.div(GF11.add(GF11.sub(0, Q), GF11.root(D)), GF11.mul(2, P))
        error_mag_2 = GF11.div(GF11.sub(GF11.mul(error_pos_1, S1), S2), GF11.sub(error_pos_1, error_pos_2))
        error_mag_1 = GF11.sub(S1, error_mag_2)
        #Correct the error
        corrected_value_1= GF11.sub(input_vector[error_pos_1-1], error_mag_1)
        corrected_value_2= GF11.sub(input_vector[error_pos_2-1], error_mag_2)
        input_vector[error_pos_1-1] = corrected_value_1
        input_vector[error_pos_2-1] = corrected_value_2
        final_vector = [int(x) for x in input_vector]
        return final_vector, f"The codeword was received with two errors of magnituges {error_mag_1} and {error_mag_2} in the respective positions {error_pos_1} and {error_pos_2}. The word has been corrected."
    
    #Case 3 or more erros must have occured as other possibilities have been exhausted
    return input_vector, "Three or more errors occured, word could not be decoded. Request retransmission."


def main():
    print("             --- 10-ary BCH Decoder in GF(11) ---")
    print("Enter the 10-digit code separated by spaces, commas, or as a single string.")
    
    while True:
        try:
            user_input = input("\nInput Vector (or 'q' to quit): ").strip()
            if user_input.lower() == 'q':
                break
            
            # Parse Input
            # Remove brackets and commas if present
            clean_input = user_input.replace(',', ' ').replace('[', '').replace(']', '')
            if ' ' in clean_input:
                vec = [int(x) for x in clean_input.split()]
            else:
                vec = [int(c) for c in clean_input]
            
            if len(vec) != 10:
                print("Error: Vector must be exactly 10 digits.")
                continue
                
            if any(x < 0 or x > 10 for x in vec):
                print("Error: Digits must be in GF(11) (0-10).")
                continue

            # Execute Decoding
            result, status = decode_BCH(vec)
            original_user_input = [int(x) for x in clean_input]

            print("-" * 30)
            if result:
                print(f"Status: {status}")
                print(f"Original: {original_user_input}")
                print(f"Decoded:  {result}")
            else:
                print(f"Status: {status}")
            print("-" * 30)

        except ValueError:
            print("Invalid input format. Please enter integers.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
        main()