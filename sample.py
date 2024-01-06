import argparse

def main():
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(description='Sample script with command-line argument')

    # Add a command-line argument (--myvar) to the parser
    parser.add_argument('--myvar', type=int, help='An example command-line argument')

    # Parse the command-line arguments
    args = parser.parse_args()

    # Access the value of the parsed argument
    myvar_value = args.myvar

    # Perform actions based on the value of myvar_value
    if myvar_value is not None:
        print(f'The value of myvar is: {myvar_value}')
        # Your script logic here
    else:
        print('The --myvar argument is not provided.')

if __name__ == '__main__':
    main()
