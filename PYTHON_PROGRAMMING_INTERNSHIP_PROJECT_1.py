import random
import string

class UsernameGenerator:
    def __init__(self):
        self.adjectives = ["Happy", "Cool", "Brave", "Clever", "Swift", "Mighty", "Epic"]
        self.nouns = ["Tiger", "Dragon", "Panda", "Eagle", "Wolf", "Phoenix", "Warrior"]
        
    def generate_username(self, include_numbers=True, include_special=True, max_number=999):
        username = f"{random.choice(self.adjectives)}{random.choice(self.nouns)}"
        
        if include_numbers:
            username += str(random.randint(1, max_number))
            
        if include_special:
            special_chars = "!#$%&*"
            username += random.choice(special_chars)
            
        return username
    
    def save_usernames(self, usernames, filename="usernames.txt"):
        try:
            with open(filename, 'w') as file:
                for username in usernames:
                    file.write(username + '\n')
            return True
        except Exception as e:
            print(f"Error saving to file: {e}")
            return False

def main():
    generator = UsernameGenerator()
    
    print("Welcome to the Username Generator!")
    print("=================================")
    
    try:
        num_usernames = int(input("How many usernames would you like to generate? "))
        include_numbers = input("Include numbers? (y/n): ").lower() == 'y'
        include_special = input("Include special characters? (y/n): ").lower() == 'y'
        
        # Generate usernames
        usernames = []
        for _ in range(num_usernames):
            username = generator.generate_username(include_numbers, include_special)
            usernames.append(username)
            print(f"Generated username: {username}")
        
        # Save to file
        save_option = input("Would you like to save these usernames to a file? (y/n): ").lower()
        if save_option == 'y':
            if generator.save_usernames(usernames):
                print("Usernames saved successfully to 'usernames.txt'")
            else:
                print("Failed to save usernames")
                
    except ValueError:
        print("Please enter a valid number")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
