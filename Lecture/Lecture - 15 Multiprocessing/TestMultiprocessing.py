from multiprocessing import Value, Process

def increment(shared_num):
    shared_num.value += 1

if __name__ == "__main__":
    shared_num = Value('i', 0) #i for int
    processes = [Process(target=increment, args=(shared_num,)) 
                for _ in range(10)] #group them all

    for p in processes:
        p.start()
    for p in processes:
        p.join()

    print(shared_num.value)