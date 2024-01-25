import multiprocessing

def worker_function(name):
    print(f"Worker {name} is doing some work")

if __name__ == "__main__":
    # 프로세스 생성
    process1 = multiprocessing.Process(target=worker_function, args=(1,))
    process2 = multiprocessing.Process(target=worker_function, args=(2,))

    # 프로세스 시작
    process1.start()
    process2.start()

    # 프로세스 종료 대기
    process1.join()
    process2.join()

    print("Main process finished")