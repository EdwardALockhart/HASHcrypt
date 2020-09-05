'''
HASHcrypt_v17

Created By:
    Edward Lockhart
    September 2020

Multi-Key One-Time Pad Cipher:
    Key1: Random state dictating the character-value mapping
    Key2: Randomly generated alphanumeric decryption key
    Operation: XOR bit encryption

Description:
    Encrypts and decrypts messages using a character-value dictionary controlled
    by a user-defined random state and a secure randomly generated decryption key
    unique to each encrypted message.
    
Usage:
    The resulting ciphertext will be impossible to decrypt as long as:

    The key is truly random (achieved in code).
    The key is at least as long as the plaintext (achieved in code).
    The key is never reused in whole or in part (achieved in code).
    The key and random state are kept completely secret.

'''

#-------------------------------------------------------------------------------

import random
#Random library (https://github.com/python/cpython/blob/3.8/Lib/random.py)

#-------------------------------------------------------------------------------

def dictionary_values(seed):   
    ''' Produces the character dictionary and value dictionary
    INPUTS: seed (integer)
    OUTPUTS: char_dictionary, value_dictionary '''
    
    # Produce a list of extended ascii characters
    dic_char_list = [chr(i) for i in range(256)]
    # Produce a list of integers which is the same length
    dic_value_list = [i for i in range(len(dic_char_list))]
    
    # Shuffle the values according to a desired seed
    random.seed(seed)
    random.shuffle(dic_value_list)
   
    # Combine the lists to produce each dictionary
    char_dictionary = dict(zip(dic_char_list, dic_value_list))
    value_dictionary = dict(zip(dic_value_list, dic_char_list))
    
    # Return each dictionary
    return char_dictionary, value_dictionary

#-------------------------------------------------------------------------------

def charstring_to_valuelist(char_string, seed):
    ''' Translates a string of characters into a list of integers
    INPUTS: input_char_string (string), seed (integer)
    OUTPUTS: value_list (integer list) '''
    
    # Get each dictionary
    char_dictionary, value_dictionary = dictionary_values(seed)
    
    # Create a blank list
    value_list = []
    # Loop through the characters and add the translated value to the new list
    for char in char_string:
        value_list.append(char_dictionary.get(char))
    
    # Return the list of values
    return value_list

#-------------------------------------------------------------------------------

def valuelist_to_charstring(value_list, seed):
    ''' Translates a list of integers into a string of characters
    INPUTS: input_value_list (integer list), seed (integer)
    OUTPUTS: char_list (string) '''

    # Get each dictionary
    char_dictionary, value_dictionary = dictionary_values(seed)
    
    # Create a blank list
    char_list = []
    # Loop through the values and add the translated character to the new list
    for value in value_list:
        char_list.append(value_dictionary.get(value))

    # Return the string
    return ''.join(char_list)

#-------------------------------------------------------------------------------

def xor(data, key):
    ''' Conducts XOR bitwise operation between integers
    INPUTS: data (integer list), key (integer list)
    OUTPUTS: result (integer list) '''
    
    result = [(c ^ k) for c, k in zip(data, key)]
    
    # Return the list of results
    return result

#-------------------------------------------------------------------------------

def op_selection():
    ''' Gets the user operation selection
    INPUTS: user
    OUTPUTS: input_value (integer) '''
    
    while True:
        # Add code that might cause errors due to user input
        try:
            
            # Ask the user to input their selection
            input_value = int(input("\nSelect the required operation:\n[1] Encryption\n[2] Decryption\nINPUT:"))
            
            # Check that the input is a 1 or 2
            if input_value != 1 and input_value != 2:
                # Raise an error
                raise Exception
        
        # If an error is produced...
        except:
            # Restart the loop
            print('\n***Restarting***')
            continue
        # If no error, break out of the loop
        break
    
    # Return the integer input value
    return input_value

#-------------------------------------------------------------------------------

def encrypt(seed):
    ''' Encrypts the message and outputs the encrypted message and key
    INPUTS: user, seed (integer)
    OUTPUTS: enc_message (string), key (string) '''

    # Ask the user to input the string of the message
    message = input("Enter the message to be encrypted\nINPUT:")
    
    # Check that the message contains all valid characters
    invalid = []
    for char in message:
        if char not in ''.join([chr(i) for i in range(256)]):
            invalid.append(char)
    # Replace invalid characters if detected
    invalid = list(set(invalid))
    if len(invalid) > 0:
        print("\n***Replacing invalid characters with #***")
        print(' '.join(invalid))
        for char in invalid:
            message = message.replace(char, '#')
    
    # Produce a secure random alphanumeric key string from ascii characters
    characters = ''.join([chr(i) for i in range(48, 58)]) + ''.join([chr(i) for i in range(97, 123)])
    key = ''.join(random.SystemRandom().choice(characters) for i in range(len(message)))
    
    # Calculate the value lists for the message and the key
    message_values = charstring_to_valuelist(message, seed)
    key_values = charstring_to_valuelist(key, seed)
    
    # Operate between the message and the key values using XOR
    value_list = xor(message_values, key_values)
    
    # Produce a string of the joined 3-digit value blocks
    enc_message = ' '.join([str(val).zfill(3) for val in value_list])
    
    # Return the string of the encrypted message and the string of the key
    return enc_message, key

#-------------------------------------------------------------------------------

def decrypt(seed):
    ''' Decrypts the encrypted message, requires the corresponding key
    INPUTS: user, seed (integer)
    OUTPUTS: dec_message (string) '''

    while True:
        # Add code that might cause errors due to user input
        try:
            
            # Ask the user to input the string of the encrypted message
            enc_values_string = input("Enter the encrypted message\nINPUT:")
            # Ask the user to input the string of the key
            key = input("Enter the unique alphanumeric key:\nINPUT:")
            
            # Check that the key does not contain symbols or spaces
            if key.isalnum() != True:
                print("\n***Invalid input - Key contains non-alphanumeric characters***")
                # Raise an error
                raise Exception
            # Check that the encrypted message contains only numbers once spaces have been removed
            if enc_values_string.replace(' ', '').isdigit() != True:
                print("\n***Invalid input - Encrypted message contains non-numeric characters***")
                # Raise an error
                raise Exception
            # Separate into the 3-digit value blocks of the encrypted message
            enc_message_value_blocks = enc_values_string.split()
            # Check that the message is the same length as the key
            if len(enc_message_value_blocks) != len(key):
                print("\n***Invalid input - Key and message are not the same length***")
                # Raise an error
                raise Exception
        
        # If an error is produced...
        except:
            # Restart the loop
            print('\n***Restarting***')
            continue
        # If no error, break out of the loop
        break
    
    # Turn the encrypted message value blocks into a list of integers
    enc_message_values = [int(num) for num in enc_message_value_blocks]
    
    # Calculate the value list of the key
    key_values = charstring_to_valuelist(key, seed)
    
    # Operate between the message and the key values using XOR
    message_values = xor(enc_message_values, key_values)
    
    # Translate the value list into characters
    message_string = valuelist_to_charstring(message_values, seed)
   
    # Produce a string of the decrypted message
    dec_message = ''.join(str(char) for char in message_string)
    
    # Return the string of the decrypted message
    return dec_message

#-------------------------------------------------------------------------------

def HASHcrypt():
    ''' Runs operation and prints outputs '''

    print("\nHASHcrypt\nEdward Lockhart - Sep 2020")
    
    while True:
        # Add code that might cause errors due to user input
        try:
            
            # Ask the user to input their selection
            input_seed = input("Enter the desired random state\nINPUT:")
            
            # Check that the input seed is a number
            if input_seed.isdigit() != True:
                print("\n***Invalid input - Seed contains non-numeric characters***")
                # Raise an error
                raise Exception
        
        # If an error is produced...
        except:
            # Print an error statement
            print("\n***Invalid option***")
            # Restart the loop
            continue
        # If no error, break out of the loop
        break

    selection = op_selection()
    # If 1 is selected, run the encryption operation
    if selection == 1:
        enc_message, key = encrypt(input_seed)
        print("\nThe encrypted message is:\n" + enc_message, "\n\nThe unique decryption key is:\n" + key)
    # If 2 is selected, run the decryption and verification operation
    elif selection == 2:
        dec_message = decrypt(input_seed)
        print("\nThe decrypted message is:\n" + dec_message)

#-------------------------------------------------------------------------------

HASHcrypt()