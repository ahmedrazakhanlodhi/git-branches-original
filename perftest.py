import timeit
from pay_gap import get_top_pay_disparities


if __name__ == "__main__":
    number = 100
    
    elapsed = timeit.timeit(
        lambda: get_top_pay_disparities(10),
        number=number
    )
    
    avg_time = elapsed / number
    
    print(f"Total time:   {elapsed:.4f} seconds")
    print(f"Average time: {avg_time:.4f} seconds")
    print(f"Per call:     {avg_time * 1000:.2f} ms")
