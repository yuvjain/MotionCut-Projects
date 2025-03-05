def count_words(text):
    # Handle empty input
    if not text.strip():
        return 0
    
    # Split the text by whitespace and count the words
    words = text.split()
    return len(words)

def main():
    print("=" * 50)
    print("WORD COUNTER PROGRAM")
    print("=" * 50)
    print("This program counts the number of words in your text.")
    
    while True:
        # Get user input
        user_input = input("\nEnter a sentence or paragraph (or type 'exit' to quit): ")
        
        # Check if user wants to exit
        if user_input.lower() == 'exit':
            print("\nThank you for using the Word Counter program!")
            break
        
        # Count words and display the result
        word_count = count_words(user_input)
        
        if word_count == 0:
            print("You entered an empty text. Please try again.")
        elif word_count == 1:
            print(f"Your text contains 1 word.")
        else:
            print(f"Your text contains {word_count} words.")

if __name__ == "__main__":
    main()