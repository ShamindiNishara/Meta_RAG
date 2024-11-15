run : streamlit run main.py
testing:

question: A traditional telephone keypad assigns each of the digits 2 through 9 to a group of three letters. For instance, the digit 2 is associated with the letters A, B, and C, 3 with D, E, and F, and so on. This system allows us to convert phone numbers into words. Some companies use this method to create memorable phone numbers for their customers. For example, 1800-MEDICARE translates to 1800-63342273. Your task is to write a function named 'translate' that takes a string as input and translates all the letters within the string to their equivalent digits as described above. The function should be case insensitive and return the translated string. A hint to solve this problem is to use a list to store the associated digit for each of the 26 alphabets.

student answer: mapping = [2, 3, 4, 5, 6, 7, 8, 9] 
def translate(tele_str):
    ans = ""
    for i in range(0, len(tele_str)):
        if tele_str[i].isdigit() == False:
            ans += str(tele_str[i])
        elif tele_str[i] == "a" or tele_str[i] == "b" or tele_str[i] == "c" or tele_str[i] == "A" or tele_str[i] == "B" or tele_str[i] == "C"::
            ans += "2"
        elif tele_str[i] == "c" or tele_str[i] == "d" or tele_str[i] == "e" or tele_str[i] == "C" or tele_str[i] == "D" or tele_str[i] == "E":
            ans += "3"
        elif tele_str[i] == "g" or tele_str[i] == "h" or tele_str[i] == "i" or tele_str[i] == "G" or tele_str[i] == "H" or tele_str[i] == "I":
            ans += "4"
        elif tele_str[i] == "j" or tele_str[i] == "k" or tele_str[i] == "l" or tele_str[i] == "J" or tele_str[i] == "K" or tele_str[i] == "L":
            ans += "5"
        elif tele_str[i] == "m" or tele_str[i] == "n" or tele_str[i] == "o" or tele_str[i] == "M" or tele_str[i] == "N" or tele_str[i] == "O":
            ans += "6"
        elif tele_str[i] == "p" or tele_str[i] == "q" or tele_str[i] == "r" or tele_str[i] == "s" or tele_str[i] == "P" or tele_str[i] == "Q" or tele_str[i] == "R" or tele_str[i] == "S":
            ans += "7"
        elif tele_str[i] == "t" or tele_str[i] == "u" or tele_str[i] == "v" or tele_str[i] == "T" or tele_str[i] == "U" or tele_str[i] == "V":
            ans += "8"
        elif tele_str[i] == "w" or tele_str[i] == "x" or tele_str[i] == "y" or tele_str[i] == "z" or tele_str[i] == "W" or tele_str[i] == "X" or tele_str[i] == "Y" or tele_str[i] == "Z":
            ans += "9"
        
 

    return ans
            
                   
    pass

metacognitive profile:  [2, 2, 1, 2, 3, 2, 2, 1, 1, 2, 1, 2, 2, 2, 2, 3]