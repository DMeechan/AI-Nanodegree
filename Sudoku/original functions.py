def original_grid_values(input):
    all_digits = '123456789'
    # Check for valid input
    if (len(input) == 81):
        dict = {}
        counter = 0
        # Associate each letter in input with a grid value
        for letter in input:
            if (letter == "."):
                dict.update({boxes[counter]: all_digits})
            else:
                dict.update({boxes[counter]: letter})
            counter += 1

    return dict


def original_only_choice(values):
    all_digits = '123456789'
    for unit_boxes in unitlist:
        remaining_digits = all_digits

        for digit in remaining_digits:
            found = False
            num_possible_boxes = 0
            last_box_digit_found_in = ''

            for box in unit_boxes:
                # Check if the digit has already been solved
                if values[box] == digit:
                    remaining_digits = remaining_digits.replace(digit, '')
                    found = True
                    break

                else:
                    # for list_of_peers_of_box in units[box]:
                        # print('List: ', list_of_peers_of_box)
                    for peers_of_box in units[box]:
                        for peer_of_box in peers_of_box:
                            if digit in values[peer_of_box]:
                                num_possible_boxes += 1
                                last_box_digit_found_in = peer_of_box
            if found == True:
                break

            if num_possible_boxes == 1:
                values[last_box_digit_found_in] = digit
    return values