if __name__ == '__main__':
    screen_width = int(input('screen width: '))
    screen_height = int(input('screen height: '))
    box_width = int(input('box width: '))
    box_height = int(input('box height: '))
    box_distance = int(input('box distance: '))

    x = box_distance
    y = box_distance

    boxes = []

    while y + box_height < screen_height:
        while x + box_width < screen_width:
            boxes.append([[x, y], [x + box_width, y], [x + box_width, y + box_height], [x, y + box_height]])
            x += box_width + box_distance
        x = box_distance
        y += box_height + box_distance

    for box in boxes:
        print(str(box) + ',')

