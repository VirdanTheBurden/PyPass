from src.exceptions import FileCreationError
import os.path
import time


def create_new_user(usr_dir, *, folder=None):
    """Creates folder with the name given by the user in the PyPass/userdata folder.
        usr_dir = The location of the userdata folder.
        folder (optional) = The name of the directory to be created."""

    if not folder:

        try:

            make_dir = input("No directory was given. Please type in your name to make one: ")
            os.mkdir(f"{os.path.join(usr_dir, make_dir.title().replace(' ', ''))}")
            print(f'User "{make_dir}" was created.')

        except OSError:

            raise FileCreationError(f'Something went wrong in creating user "{make_dir}".')

        else:

            return os.path.join(usr_dir, make_dir)

    else:

        try:

            os.mkdir(f"{os.path.join(usr_dir, folder)}")
            print(f'User "{folder}" was created.')

        except OSError:

            raise FileCreationError(f'Something went wrong in creating user "{folder}".')

        else:

            return os.path.join(usr_dir, folder)


def compare_directory(user_input, dir_in_iter):
    """Creates a generator object that will return the amount of times a character in the same index in each argument
    are the same character. Cannot be used without other iterable object satisfying the dir_in_iter argument.
    user_input = The name of the directory the user gave. This should not change iteration to iteration.
    dir_in_iter = The name of a directory given by an iterable object.
    """

    # determines which file is shorter
    stop_length = len(user_input) if len(user_input) < len(dir_in_iter) else len(dir_in_iter)

    # creates a list, appends 1 for everytime a character in user_input and file_in_iter
    # are the same, returns sum of 1s
    yield sum([1 for i in range(stop_length) if user_input[i] == dir_in_iter[i]])


def check_for_dir(filepath, directory):
    """Checks if the string passed has an associated directory that exists.
    If not, checks for possible user input error. Creates user if both fail.
    filepath = The location of the userdata folder.
    directory = The directory the user entered."""

    # if no directories exist, go to user creation with the directory name
    if not os.listdir(filepath):
        return create_new_user(directory)

    # otherwise, try to find the directory specified
    else:

        try:

            if directory in os.listdir(filepath):
                return directory

            else:
                raise FileNotFoundError

        except FileNotFoundError:

            print("\nThat user doesn't exist. Here's a few users that do exist:\n")
            if len(os.listdir(filepath)) > 3:

                # returns a dictionary; each key is the directory, each value is the
                # confidence in the file being the correct one (from 0 - exactly the same)
                possible_files = {dir_name: confidence for dir_name in os.listdir(filepath)
                                  for confidence in compare_directory(directory, dir_name)}

                # returns a list of keys (user directories) sorted by program confidence value in
                # descending order, prints the top 3
                sorted_keys = sorted(possible_files, key=possible_files.get, reverse=True)
                for i in range(3):
                    print(f"{sorted_keys[i]}\n")

            else:

                # prints all directories in the userdata directory if count is less than or equal to 3
                for user_directory in os.listdir(filepath):
                    print(f"{user_directory}\n")

            # asks user if any of the directories is theirs
            while True:

                choice = input("Do you happen to mean any of the following users? ").lower()

                if choice == "yes":

                    while True:

                        pick = input("Type the user's name: ")

                        if pick.lower().title() in sorted_keys:
                            return directory

                        else:

                            print("That is not a valid option.")
                            continue

                elif choice == "no":

                    print("User not found in directory. Redirecting to user creation...")
                    create_new_user(filepath)

                else:

                    print("That is not a valid option.")
                    continue


def greet():
    """Startup script, asks user for their name to find their directory."""

    print("Welcome to PyPass, giving you an easy way to store passwords locally!")
    time.sleep(2)

    # determines directory
    users_dir = os.path.join(os.path.dirname(__file__).rstrip('src'), "userdata")

    while True:

        response = input("Do you have a user profile already? (Yes or No) ").lower()

        if response == "yes":

            time.sleep(1)
            intake_dir = input("What is your name? ").title().replace(" ", "")
            return check_for_dir(users_dir, intake_dir)

        elif response == "no":

            while True:

                time.sleep(1)
                want_create = input("Do you want to create a user? ").lower()

                if want_create == "yes":

                    time.sleep(1)
                    intake_dir = input("What would you like your name to be? ").title().replace(" ", "")
                    return create_new_user(users_dir, folder=intake_dir)

                elif want_create == "no":

                    print("Exiting PyPass.")
                    time.sleep(1)
                    return None

                else:

                    print("Not a valid option.")
                    time.sleep(1)
                    continue

        else:

            print("That is not a valid option.")
            continue
