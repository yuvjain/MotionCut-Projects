import os

def reverse_character_order(text):
    """Reverses the character order of the input text."""
    return text[::-1]

def reverse_word_order(text):
    """Reverses the order of words in the input text."""
    words = text.split()
    return ' '.join(reversed(words))

def save_to_file(reversed_text):
    """Saves the reversed text to a file."""
    with open('reversed_text.txt', 'w') as file:
        file.write(reversed_text)
    print("Reversed text saved to 'reversed_text.txt'.")

def main():
    while True:
        print("\n--- Text Reverser Menu ---")
        print("1. Reverse Character Order")
        print("2. Reverse Word Order")
        print("3. Exit")
        
        choice = input("Choose an option (1-3): ")
        
        if choice == '3':
            print("Exiting the program. Goodbye!")
            break
        
        text = input("Enter a sentence: ")
        
        if not text:
            print("Error: You entered an empty string. Please try again.")
            continue
        
        if choice == '1':
            reversed_text = reverse_character_order(text)
            print(f"Reversed Character Order: {reversed_text}")
        elif choice == '2':
            reversed_text = reverse_word_order(text)
            print(f"Reversed Word Order: {reversed_text}")
        else:
            print("Invalid choice. Please select 1 or 2.")
            continue
        
        save_option = input("Would you like to save the reversed text to a file? (yes/no): ").strip().lower()
        if save_option == 'yes':
            save_to_file(reversed_text)

if __name__ == "__main__":
    main()
