

# synchronous version

commented = '''
def factorize(*numbers):
    factors_list = []

    for number in numbers:
        factors = []
        for i in range(1, number + 1):
            if number % i == 0:
                factors.append(i)

        factors_list.append(factors)

    return factors_list

list_1 = factorize(128, 255, 99999, 10651060)

for element in list_1:
    print(element)
'''

# asynchronous version
#import threadingimport math
import math
import multiprocessing
import os


def calculate_divisors(numbers, start, end, result):
    for number in numbers[start:end]:
        divisors = []
        for i in range(1, math.isqrt(number) + 1):
            if number % i == 0:
                divisors.append(i)
                if i != number // i:  # Avoid adding duplicate divisors for square numbers
                    divisors.append(number // i)
        divisors.sort()  # Sort the divisors for better readability
        result[number] = divisors  # each process in Python has its own separate memory space. Therefore, changes made to variables within one process do not affect the variables in other processes.

def main():
    try:
        numbers = [128, 255, 99999, 10651060]  # Example numbers

        manager = multiprocessing.Manager()  
        result = manager.dict()   # each process in Python has its own separate memory space. Therefore, changes made to variables within one process do not affect the variables in other processes.

        num_cores = os.cpu_count() or 1  # Get the number of CPU cores
        if num_cores > len(numbers): 
            num_cores = len(numbers)

        step = (len(numbers) + num_cores - 1) // num_cores
        processes = []
        for i in range(num_cores):
            start = step * i
            end = min(step * (i + 1), len(numbers))
            process = multiprocessing.Process(target=calculate_divisors, args=(numbers, start, end, result))
            process.start()
            processes.append(process)

        for process in processes:
            process.join()

        # Print results
        for number in numbers:
            print("Divisors of", number, "are:", result.get(number, "not found"))

    except ValueError:
        print("Please enter valid integers.")

if __name__ == "__main__":
    main()