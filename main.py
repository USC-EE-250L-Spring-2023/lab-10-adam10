import time
import numpy as np
from typing import List, Optional

import threading
import pandas as pd
import requests
import plotly.express as px


def generate_data() -> List[int]:
    """Generate some random data."""
    return np.random.randint(100, 10000, 1000).tolist()

def process1(data: List[int]) -> List[int]:
    """This function will take a list of integers as an input and find the next largest prime number 
    for all of its enteries. It does this by incrementing the given value, checking if it is prime 
    by seeing of all of its modulus value up to it returns a non-zero value, and iterating by 1
    until the next largest prime is found. It returns a list of integers since it does this
    for all enteries in the input list."""
    def foo(x):
        while True:
            x += 1
            if all(x % i for i in range(2, x)):
                return x
    return [foo(x) for x in data]

def process2(data: List[int]) -> List[int]:
    """This function will take a list of integers as an input and find the next largest perfect square
    for all of its enteries. Like the previous function about, the process iterates, incrementing the 
    value by one. The only thing that changes is the conditional which essentially checks if the square
    of the value's square root is the same as the original value when converted to an integer. This condition
    will only return if the value is a perfect square. Since it does this for all enteries in the input, it
    again returns a list of integers that meets these specifications."""
    def foo(x):
        while True:
            x += 1
            if int(np.sqrt(x)) ** 2 == x:
                return x
    return [foo(x) for x in data]

def final_process(data1: List[int], data2: List[int]) -> List[int]:
    """This function will take in 2 lists of integers as an input and zip the 2 lists together into a set of
    essentially key-value pairs. Then, it will iterate through each list simultaneously and take the difference
    between each list's respective entry for each iteration. Finally, the mean of all of these differences will
    be taken. While a single integer will be calculated, the function returns in the form of a list of integers."""
    return np.mean([abs(x - y) for x, y in zip(data1, data2)])

offload_url = 'http://localhost:5000'

def run(offload: Optional[str] = None) -> float:
    """Run the program, offloading the specified function(s) to the server.
    
    Args:
        offload: Which function(s) to offload to the server. Can be None, 'process1', 'process2', or 'both'.

    Returns:
        float: the final result of the program.
    """
    data = generate_data()
    if offload is None: # in this case, we run the program locally
        data1 = process1(data)
        data2 = process2(data)
    elif offload == 'process1':
        data1 = None
        def offload_process1(data):
            nonlocal data1
            response = requests.post(f"{offload_url}/process1", json=data)
            data1 = response.json()
        thread = threading.Thread(target=offload_process1, args=(data,))
        thread.start()
        data2 = process2(data)
        thread.join()
        # Question 2: Why do we need to join the thread here?
        # Question 3: Are the processing functions executing in parallel or just concurrently? What is the difference?
        #   See this article: https://oxylabs.io/blog/concurrency-vs-parallelism
        #   ChatGPT is also good at explaining the difference between parallel and concurrent execution!
        #   Make sure to cite any sources you use to answer this question.
    elif offload == 'process2':
        data2 = None
        def offload_process2(data):
            nonlocal data2
            response = requests.post(f"{offload_url}/process2", json=data)
            data2 = response.json()
        thread = threading.Thread(target=offload_process2, args=(data,))
        thread.start()
        data1 = process1(data)
        thread.join()
    elif offload == 'both':
        data1 = None
        data2 = None
        
        def offload_process1(data):
            nonlocal data1
            response = requests.post(f"{offload_url}/process1", json=data)
            data1 = response.json()
        thread1 = threading.Thread(target=offload_process1, args=(data,))
    
        def offload_process2(data):
            nonlocal data2
            response = requests.post(f"{offload_url}/process2", json=data)
            data2 = response.json()
        thread2 = threading.Thread(target=offload_process2, args=(data,))

        thread1.start()
        thread2.start()

        thread1.join()
        thread2.join()

    ans = final_process(data1, data2)
    return ans 

def main():
    rows = []
    columns = ["none", "p1", "p2", "both"]

    arr = []
    for i in range(5):
        temp = run()
        arr.append(temp)
    mean = np.mean(arr)
    std = np.std(arr)
    total = np.sum(arr)
    arr.append(mean)
    arr.append(std)
    arr.append(total)
    columns = arr
    rows.append(columns)

    arr = []
    for i in range(5):
        temp = run('process1')
        arr.append(temp)
    mean = np.mean(arr)
    std = np.std(arr)
    total = np.sum(arr)
    arr.append(mean)
    arr.append(std)
    arr.append(total)
    columns = arr
    rows.append(columns)

    arr = []
    for i in range(5):
        temp = run('process2')
        arr.append(temp)
    mean = np.mean(arr)
    std = np.std(arr)
    total = np.sum(arr)
    arr.append(mean)
    arr.append(std)
    arr.append(total)
    columns = arr
    rows.append(columns)

    arr = []
    for i in range(5):
        temp = run('both')
        arr.append(temp)
    mean = np.mean(arr)
    std = np.std(arr)
    total = np.sum(arr)
    arr.append(mean)
    arr.append(std)
    arr.append(total)
    columns = arr
    rows.append(columns)

    a = pd.DataFrame(rows)
    df = a.transpose()
    temp = df.iloc[5]
    mea = temp.tolist()
    temp = df.iloc[6]
    err = temp.tolist()
    #print(df)
    #print(err)
    
    names = ["none", "p1", "p2", "both"]

    fig = px.bar(df, x=names, y=mea, error_y=err, title="Time Data for Each Mode")
    fig.update_xaxes(title_text="Trial Type")
    fig.update_yaxes(title_text="Time")

    fig.write_image("makespan.png")


    # Question 4: What is the best offloading mode? Why do you think that is?
    # Question 5: What is the worst offloading mode? Why do you think that is?
    # Question 6: The processing functions in the example aren't very likely to be used in a real-world application. 
    #   What kind of processing functions would be more likely to be used in a real-world application?
    #   When would you want to offload these functions to a server?
    
    
if __name__ == '__main__':
    main()