left = (False, False)
right = (False, False)
up = (True, False)
down = (False, False)

direction = (left, right, up, down)

for index, val in enumerate(direction):
        for index_2, val_2 in enumerate(val):
            if index_2 == 0:
                if val_2 == True:
                    
                    if index == 0:
                        print('links')

                    if index == 1:
                        print('rechts')

                    if index == 2:
                        print('up')

                    if index == 3:
                        print('down')

            else:
                pass

        # print('Der Index ist:' , str(index))
        # print('Der Value ist:' , str(val))
        # print('Der 2. Index ist:' , str(index_2))
        # print('Der 2. Value ist:' , str(val_2))