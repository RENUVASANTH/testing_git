
# 1. List
students = ["Renu", "Arun", "Kevin"]

students.append("Priya")
students.remove("Arun")

print("Student List:", students)


# 2. Tuple
courses = ("Python", "Data Science", "Web Development")

print("Courses:", courses)
print("First Course:", courses[0])


# 3. Set
numbers = {10, 20, 30, 20, 10}

print("Unique Numbers:", numbers)

numbers.add(40)
print("Updated Set:", numbers)


# 4. Dictionary
student = {
    "name": "Renu",
    "course": "Python Full Stack",
    "fee": 2500
}

print("Student Details:", student)

student["fee"] = 3000

print("Updated Student:", student)


# 5. Function to count word frequency
def word_frequency(text):
    words = text.lower().split()

    frequency = {}

    for word in words:
        frequency[word] = frequency.get(word, 0) + 1

    return frequency


# Testing the function
sentence = "python is easy python is powerful"

result = word_frequency(sentence)

print("Word Frequency:", result)
