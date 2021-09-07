
def check_user_input(userQuestion, in_range=(0,0), y_or_n = False, is_date = False):

    checking = True
    while checking:
        userInput = input(userQuestion + '\n')

        if is_date:
            if userInput[2] == '/' and userInput[5] == '/' and len(userInput) == 10:
                try:
                    test = int(userInput[0:2])
                    test = int(userInput[3:5])
                    test = int(userInput[6:10])
                except:
                    print('Error: Incorrect date format')
                else:
                    checking = False
                    return userInput
            else:
                print('Error: Incorrect date format')

        if in_range != (0,0):
            try:
                test = int(userInput)
            except:
                print('Error: Input is not number')
            else:
                if int(userInput) in range(in_range[0], in_range[1]):
                    checking = False
                    return int(userInput)
                else:
                    print('Error: Number not an option')
        
        if y_or_n:
            yn = ['Y', 'y', 'N', 'n']
            if userInput in yn:
                if userInput in yn[:2]:
                    checking = False
                    return True
                else:
                    checking = False
                    return False
            else:
                print('Error: Input not Y/N')


