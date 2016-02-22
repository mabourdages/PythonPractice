# Ca manque de docstring tout ca!!! :P

import sys


class Commands(object):
    def __init__(self, text, isAlive):
        self.Text = text
        self.NextStepList = {}
        self.Alive = isAlive

    def DisplayText(self):
        print "{0}".format(self.Text)

    def GetInput(self):
        Trying = True
        while Trying:
            try:
                answer = raw_input("Choose an answer.\n")
                if int(answer) - 1 in range(len(self.NextStepList)):
                    Trying = False
                    nextRoom = self.NextStepList[int(answer)]
                    nextRoom.DisplayText()
                    nextRoom.ReturnChoiceList(nextRoom.NextStepList)
                    if self.Alive == nextRoom.Alive:
                        self.GetInput()
                    else:
                        raw_input("Type anything to restart.\n")
                        LaunchGame().Start()
            except ValueError:
                print ("Enter a valid answer.", sys.exc_info()[0])

    def ReturnChoiceList(self, nextStepList):
        self.NextStepList = nextStepList
        return self.NextStepList


class Forward(Commands):
    def __init__(self, text, isAlive=True):
        super(Forward, self).__init__(text, isAlive=True)
        self.Alive = isAlive


class Lost(Commands):
    def __init__(self, text, isAlive=False):
        super(Lost, self).__init__(text, isAlive=False)
        self.Alive = isAlive


class LaunchGame(object):

    def __init__(self):
        self.GameStart = Forward("Hello Renaud, where do you enter?\n",
                                 {"Front Door": self.FrontDoor}
                                 "[2] Side Window\n"
                                 "[3] Rear Door\n")

        self.FrontDoor = Lost("You get shot in the face. You die.\n")

        self.SideWindow = Forward("You enter the side window and see a guy standing in the entrance hall\n"
                                  "What do you do?\n"
                                  "[1] Kill him\n"
                                  "[2] Go to kitchen stealthy\n"
                                  "[3] Go downstairs slowly\n")

        self.KillFromWindow = Lost("You get shot in the face by his friend. You die.\n")

        self.RearDoor = Forward("You enter from the rear door.\n"
                                "Where do you go?\n"
                                "[1] Garage\n"
                                "[2] Kitchen\n"
                                "[3] Entrance Hall\n")

        self.Kitchen = Forward("Kitchen\n"
                                 "[1] Garage\n"
                                 "[2] Downstairs\n"
                                 "[3] Entrance Hall\n")

        self.EntranceHall = Forward("EntranceHall\n"
                                 "[1] Garage\n"
                                 "[2] Kitchen\n"
                                 "[3] Entrance Hall\n")

        self.DownStairs = Forward("DownStairs\n"
                                 "[1] Garage\n"
                                 "[2] Kitchen\n"
                                 "[3] Entrance Hall\n")

        self.Garage = Forward("Garage\n"
                                 "[1] Garage\n"
                                 "[2] Kitchen\n"
                                 "[3] Entrance Hall\n")

        self.GameStart.NextStepList = {1: self.FrontDoor, 2: self.SideWindow, 3: self.RearDoor}
        self.SideWindow.NextStepList = {1: self.KillFromWindow, 2: self.EntranceHall, 3: self.DownStairs}
        self.Kitchen.NextStepList = {1: self.Garage, 2: self.DownStairs, 3: self.EntranceHall}

        self.Start()

    def Start(self):
        self.GameStart.DisplayText()
        self.GameStart.GetInput()


LaunchGame()
