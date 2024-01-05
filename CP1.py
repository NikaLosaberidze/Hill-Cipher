import numpy as np
import random
import wave




dct = {"A" : 0.,"B" : 1.,"C" : 2.,"D" : 3.,"E" : 4.,
       "F" : 5.,"G" : 6.,"H" : 7.,"I" : 8.,"J" : 9.,
       "K" : 10.,"L" : 11.,"M" : 12.,"N" : 13.,"O" : 14.,
       "P" : 15.,"Q" : 16.,"R" : 17.,"S" : 18.,"T" : 19.,
       "U" : 20.,"V" : 21.,"W" : 22.,"X" : 23.,"Y" : 24.,
       "Z" : 25.," " : 26.,"," : 27.,"." : 28.,"?" : 29.,
       "!" : 30.}  # my way of changing letters to numbers

dct1 = {0. : "A",1. : "B",2. : "C",3. : "D",4. : "E",
        5. : "F",6. : "G",7. : "H",8. : "I",9. : "J",
        10. : "K",11. : "L",12. : "M",13. : "N",14. : "O",
        15. : "P",16. : "Q",17. : "R",18. : "S",19. : "T",
        20. : "U",21. : "V",22. : "W",23. : "X",24. : "Y",
        25. : "Z",26. : " ",27. : ",",28. : ".",29. : "?",
        30. : "!"}


float_key = np.array([[float(random.randint(5,500)) % 31,float(random.randint(5,500)) % 31,float(random.randint(5,500)) % 31],
                      [float(random.randint(5,500)) % 31,float(random.randint(5,500)) % 31,float(random.randint(5,500)) % 31],
                      [float(random.randint(5,500)) % 31,float(random.randint(5,500)) % 31,float(random.randint(5,500)) % 31]])  # making random matrix key with floating numbers


det_A = int(round(np.linalg.det(float_key))) # calculating determinant

while np.gcd(det_A, 31) != 1: # checking invertibility
    float_key = np.array([[float(random.randint(5,500)) % 31,float(random.randint(5,500)) % 31,float(random.randint(5,500)) % 31],
                      [float(random.randint(5,500)) % 31,float(random.randint(5,500)) % 31,float(random.randint(5,500)) % 31],
                      [float(random.randint(5,500)) % 31,float(random.randint(5,500)) % 31,float(random.randint(5,500)) % 31]])
    det_A = int(round(np.linalg.det(float_key)))




integer_key = np.array([[random.randint(5,500) % 31 ,random.randint(5,500) % 31 ,random.randint(5,500) % 31 ],
                        [random.randint(5,500) % 31 ,random.randint(5,500) % 31 ,random.randint(5,500) % 31 ],
                        [random.randint(5,500) % 31 ,random.randint(5,500) % 31 ,random.randint(5,500) % 31 ]]) # making random matrix key with integer numbers

det_A = int(round(np.linalg.det(integer_key))) # calculating determinant

while np.gcd(det_A, 31) != 1: # checking invertibility
    integer_key = np.array([[random.randint(5,500) % 31 ,random.randint(5,500) % 31 ,random.randint(5,500) % 31 ],
                        [random.randint(5,500) % 31 ,random.randint(5,500) % 31 ,random.randint(5,500) % 31 ],
                        [random.randint(5,500) % 31 ,random.randint(5,500) % 31 ,random.randint(5,500) % 31 ]])
    det_A = int(round(np.linalg.det(integer_key)))




def make_vector(str): # for string
    return np.array([[dct[str[0].upper()]],[dct[str[1].upper()]],[dct[str[2].upper()]]]) # creating vector for string which has 3 letters.



def read_text(textfile):  # input should be string of text file. (for example: "random.txt")
    f = open(textfile,"r")
    lst = ""
    for x in f: # with for loop I make a string named "lst" in which there are all the words from text file.
        lst += x.removesuffix("\n").upper() + " "  

    lst = lst.removesuffix(" ") 
    return lst



def read_audio(audiofile): # input shoud be string of audio file(.wav).

    
    with wave.open(audiofile, 'rb') as wav_file: # oppening file
    
        num_frames = wav_file.getnframes()

    
        audio_data = wav_file.readframes(num_frames)

        numerical_values = np.frombuffer(audio_data, dtype=np.int16) # Convert the byte object to a NumPy array

    return numerical_values

 


def matrix_inverse_modulo(matrix, n): 
    det_A = int(round(np.linalg.det(matrix))) # calculating determinant
    
    adjugate_matrix = np.round(det_A * np.linalg.inv(matrix)).astype(int) # finding adjugate matrix
    det_inverse = pow(det_A, -1, n) # calculating inverse of determinant
    inverse_matrix = (det_inverse * adjugate_matrix) % n # calculationg inverse of matrix modulo n

    return inverse_matrix








def Encrypt(plain,key): # plain is text
    
    result = ""
    i = 0
    while i <= len(plain)-3:  # i am encrypting text containing 3 letters
        str = plain[i:i+3]
        vect = make_vector(str)
        new_matrix = np.dot(key,vect) # key matrix multiplication on vector of 3 letters from text


        result += dct1[new_matrix[0][0] % 31 ] + dct1[new_matrix[1][0] % 31 ] + dct1[new_matrix[2][0] % 31 ]  # converting vector numbers to letters
        i += 3
    if plain[i:] != "": # in case when there is a less that 3 letters left in text I add dashes(" ") till it comes up to 3.
        temp = plain[i:]
        while len(temp) != 3:
            temp += " "
        vect = make_vector(temp)
        new_matrix = np.dot(key,vect)
        result += dct1[new_matrix[0][0] % 31 ] + dct1[new_matrix[1][0] % 31 ] + dct1[new_matrix[2][0] % 31 ]

    return result



def Decrypt(plain,key): # plain should be encrypted text 
    result = ""
    inverse_key = matrix_inverse_modulo(key,31)
    
    i = 0
    while i <= len(plain)-3:  # i am encrypting text containing 3 letters
        str = plain[i:i+3]
        vect = make_vector(str)
        new_matrix = np.dot(inverse_key,vect) # key matrix multiplication on vector of 3 letters from text

        result += dct1[new_matrix[0][0] % 31] + dct1[new_matrix[1][0] % 31] + dct1[new_matrix[2][0] % 31]  # converting vector numbers to letters
        i += 3
    if plain[i:] != "": # in case when there is a less that 3 letters left in text I add dashes(" ") till it comes up to 3.
        temp = plain[i:]
        while len(temp) != 3:
            temp += " "
        vect = make_vector(temp)
        new_matrix = np.dot(inverse_key,vect)
        result += dct1[new_matrix[0][0] % 31] + dct1[new_matrix[1][0] % 31] + dct1[new_matrix[2][0] % 31]

    return result






# To read textfile -> read_text("string.txt")  
# To encrypt textfile -> Encrypt(textfile,float_key) or Ecnrypt("textfile,integer_key")
# To Decrypt textfile -> Decrypt(encrypted,floatkey) or integer_key (P.S Only one key must be used when encrypting and decrypting at the same time)



# Encryption and Decryption on textfile works without a flaw. P.S. Text can have only letters commas dots question marks and exclamation marks

# textfile = read_text("kkk.txt")  
# encrypted_text = Encrypt(textfile,float_key)                          
# decrypted_text = Decrypt(encrypted_text,float_key)
# print(f"Plain Text: {textfile}")
# print(f"Encrypted Text: {encrypted_text}")
# print(f"Decrypted Text: {decrypted_text}")









"""       From There You Can Encrypt And Decrypt Audio File           """







def generate_invertible_matrix(n): # matrix for remainder
    while True:
        # Generate an n x n matrix with random values between 0 and 1
        matrix = np.random.rand(n, n)
        
        # Check if the matrix is invertible
        if np.linalg.matrix_rank(matrix) == n:
            return matrix

remainder_matrix_inverse = []



def inverse_matrix(matrix): 
    try:
        # Attempt to calculate the inverse of the matrix
        inverse = np.linalg.inv(matrix)
        return inverse
    except np.linalg.LinAlgError:
        # Handle the case where the matrix is singular (non-invertible)
        print("Error: The matrix is singular and does not have an inverse.")


def read_audio(audiofile): # input shoud be string of audio file(.wav).

    
    with wave.open(audiofile, 'rb') as wav_file: # oppening file
    
        num_frames = wav_file.getnframes()

    
        audio_data = wav_file.readframes(num_frames)

        numerical_values = np.frombuffer(audio_data, dtype=np.int16) # Convert the byte object to a NumPy array

    return numerical_values




audio = read_audio("ბაშიაჩუკიიი.wav")    # there you should write path to wav file

if len(audio) % 3 != 0:
    remainder_matrix = generate_invertible_matrix(len(audio) % 3)
    remainder_matrix_inverse = inverse_matrix(remainder_matrix)

def Encrypt_Wav(plain,key): # plain is numerical value of wav file.
    result = []
    i = 0
    while i<= len(plain)-3:
        vect = plain[i:i+3]
        new_matrix = np.dot(key,vect)
        result += list(new_matrix)
        
        i += 3
    if plain[i:].size > 0:
        new_matrix = np.dot(remainder_matrix,plain[i:])
        result += list(new_matrix)
    
    return result


def Decrypt_Wav(plain,key):
    result = []
    i = 0
    while i<= len(plain)-3:
        vect = plain[i:i+3]
        new_matrix = np.dot(inverse_key,vect)
        result += list(new_matrix)

        i += 3
    if len(plain[i:]) > 0:
       
        new_matrix = np.dot(remainder_matrix_inverse,plain[i:]) # for remainder we should multilplie remainder matrix inverse and not key_inverse
        result += list(new_matrix)

    return result



key = generate_invertible_matrix(3) 
inverse_key = inverse_matrix(key)


"""                   You Should Write Path Of Wav File on Line 227                         """

# print(f"PLAIN : {audio}")
encrypt = Encrypt_Wav(audio,key)
# print(f"Encrypt : {encrypt}")
decrypt = Decrypt_Wav(encrypt,inverse_key)
# print(f"Decrypt : {decrypt[0],decrypt[len(decrypt)-1]}")  ia am getting zero and last element just for convinience






audio_data  = decrypt
audio_array = np.array(audio_data, dtype=np.int16)


file_name = "output.wav"

# Set the parameters for the WAV file
desired_sampling_rate = 96000 # Set the desired sampling rate
duration = len(audio_data) / desired_sampling_rate

# Open the WAV file in write mode
with wave.open(file_name, 'w') as wave_file:
    wave_file.setnchannels(1)  # mono audio
    wave_file.setsampwidth(2)  # 16-bit audio
    wave_file.setframerate(desired_sampling_rate)  # Set the desired sampling rate

    # Convert the NumPy array to a bytes object
    audio_bytes = audio_array.tobytes()

    # Write the audio data to the WAV file
    wave_file.writeframes(audio_bytes)

print(f"WAV file '{file_name}' has been created.")




