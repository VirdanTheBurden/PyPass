from src.usercreation import greet

# runs various scripts for proper program functionality
if __name__ == '__main__':
    status = greet()

    if not status:
        print("Closed successfully.")

    else:
        pass