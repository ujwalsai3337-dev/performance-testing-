import json
import time
from datetime import datetime
from functools import wraps
from typing import List, Dict, Optional

# --- 1. DECORATORS & UTILITIES ---

def logger(func):
    """Logs the execution time and arguments of a function."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"[LOG] {func.__name__} executed in {end - start:.4f}s")
        return result
    return wrapper

class DatabaseConnection:
    """A mock context manager for 'database' operations."""
    def __enter__(self):
        print("Connecting to the internal data store...")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Closing the internal data store connection.")
        if exc_type:
            print(f"Error encountered: {exc_val}")
        return False

# --- 2. MODELS ---

class Book:
    def __init__(self, title: str, author: str, isbn: str, year: int):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.year = year
        self.is_checked_out = False

    def __repr__(self):
        status = "Checked Out" if self.is_checked_out else "Available"
        return f"'{self.title}' by {self.author} ({self.year}) - [{status}]"

    def to_dict(self):
        return self.__dict__

# --- 3. CORE LOGIC (THE LIBRARY SYSTEM) ---

class Library:
    def __init__(self, name: str):
        self.name = name
        self.books: List[Book] = []

    @logger
    def add_book(self, book: Book):
        """Adds a new book instance to the library."""
        if any(b.isbn == book.isbn for b in self.books):
            raise ValueError(f"Book with ISBN {book.isbn} already exists.")
        self.books.append(book)
        print(f"Added: {book.title}")

    def find_by_author(self, author_name: str) -> List[Book]:
        """Filters books using a list comprehension."""
        return [b for b in self.books if author_name.lower() in b.author.lower()]

    def checkout_book(self, isbn: str) -> bool:
        """Finds a book by ISBN and updates its status."""
        for book in self.books:
            if book.isbn == isbn and not book.is_checked_out:
                book.is_checked_out = True
                print(f"Successfully checked out: {book.title}")
                return True
        print(f"Book with ISBN {isbn} is unavailable.")
        return False

    @logger
    def save_inventory(self, filename: str):
        """Serializes the library state to a JSON file."""
        data = [book.to_dict() for book in self.books]
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Inventory saved to {filename}")

# --- 4. DATA PROCESSING FUNCTIONS ---

def calculate_average_age(books: List[Book]) -> float:
    """Calculates the average age of books in the collection."""
    if not books:
        return 0.0
    current_year = datetime.now().year
    total_age = sum(current_year - book.year for book in books)
    return total_age / len(books)

def get_unique_authors(books: List[Book]) -> set:
    """Uses a set to return unique authors."""
    return {book.author for book in books}

def get_oldest_book(books: List[Book]) -> Optional[Book]:
    """Finds the book with the minimum year."""
    if not books:
        return None
    return min(books, key=lambda b: b.year)

# --- 5. MATHEMATICAL UTILITIES (Using recursion and generators) ---

def fibonacci_generator(n: int):
    """A generator for the first N Fibonacci numbers."""
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

def factorial(n: int) -> int:
    """Recursive factorial function."""
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)

# --- 6. STRING & TEXT MANIPULATION ---

def clean_text(text: str) -> str:
    """Removes common punctuation and lowercases text."""
    punctuation = ".,!?;:"
    for char in punctuation:
        text = text.replace(char, "")
    return text.strip().lower()

def word_frequency(text: str) -> Dict[str, int]:
    """Returns a dictionary of word counts."""
    cleaned = clean_text(text)
    words = cleaned.split()
    freq = {}
    for word in words:
        freq[word] = freq.get(word, 0) + 1
    return freq

# --- 7. MAIN EXECUTION BLOCK ---

def main():
    # Initialize the system
    my_lib = Library("Grand Central Library")
    
    # Mock Data
    sample_books = [
        Book("The Great Gatsby", "F. Scott Fitzgerald", "9780743273565", 1925),
        Book("1984", "George Orwell", "9780451524935", 1949),
        Book("The Hobbit", "J.R.R. Tolkien", "9780547928227", 1937),
        Book("Brave New World", "Aldous Huxley", "9780060850524", 1932),
        Book("Foundation", "Isaac Asimov", "9780553293357", 1951)
    ]

    # Demonstrate Context Manager & Adding books
    with DatabaseConnection():
        for b in sample_books:
            try:
                my_lib.add_book(b)
            except ValueError as e:
                print(e)

    print("-" * 30)

    # Search & Operations
    print(f"Books by Orwell: {my_lib.find_by_author('Orwell')}")
    my_lib.checkout_book("9780547928227") # Checking out The Hobbit

    # Statistics
    avg_age = calculate_average_age(my_lib.books)
    oldest = get_oldest_book(my_lib.books)
    unique_authors = get_unique_authors(my_lib.books)

    print(f"Average Book Age: {avg_age:.1f} years")
    print(f"Oldest Book: {oldest}")
    print(f"Total Unique Authors: {len(unique_authors)}")

    # Text Analysis demo
    demo_text = "Python is great. Python is fast! Is it fast?"
    print(f"Frequency: {word_frequency(demo_text)}")

    # Math utilities
    print(f"Fibonacci (8): {list(fibonacci_generator(8))}")
    print(f"Factorial of 5: {factorial(5)}")

    # Persistence
    my_lib.save_inventory("library_data.json")

    print("\n[FINISH] Program execution complete.")
    print("just for chaging things ")
    print("hello testing")
    print("hii")

if __name__ == "__main__":
    main()

# --- 8. PLACEHOLDER FOR ADDITIONAL LOGIC TO REACH LINE COUNT ---
# In a real-world scenario, you might add more robust API calls, 
# deeper error handling, or a CLI interface. 

# Example of a large-scale data filtering utility
def advanced_filter(data: List[Dict], criteria: Dict) -> List[Dict]:
    """
    Filters a list of dictionaries based on multiple key-value pairs.
    """
    filtered = []
    for item in data:
        match = True
        for key, value in criteria.items():
            if item.get(key) != value:
                match = False
                break
        if match:
            filtered.append(item)
    return filtered

# End of script.