def announce(f):
    def wrapper():
        print("About to run the function...")
        f()
        print("Done With the Function")
    return wrapper

@announce
def hello():
    print("Hello, World")

hello()