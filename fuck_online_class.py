from datetime import datetime
from time import sleep
from csv import reader
import webbrowser

import pyautogui
import os


def process_meetings():
    with open('meeting.csv', newline='') as csv_file:

        all_meetings = reader(csv_file)
        print("Meeting List:")
        for line in all_meetings:
            print(", ".join(line))
        print("\n")

    with open('meeting.csv', newline='') as csv_file:

        meetings = reader(csv_file)
        for row in meetings:
            link, start_time, end_time = row

            print("\nCurrent Meeting: ")
            print("Link  :\t" + link)
            print("Start :\t" + start_time)
            print("End   :\t" + end_time + "\n")

            start_datetime_obj = datetime.strptime(
                datetime.now().strftime("%d/%m/%y") + " " + start_time, '%d/%m/%y %H:%M'
            )

            end_datetime_obj = datetime.strptime(
                datetime.now().strftime("%d/%m/%y") + " " + end_time, '%d/%m/%y %H:%M'
            )

            if datetime.now() > end_datetime_obj:
                print("Skipping Meeting: " + ", ".join(row) + "\n")
                continue

            while datetime.now() < start_datetime_obj:
                sleep(10)
                pass

            webbrowser.open(link)

            sleep(30)

            leave_button = None
            for i in range(10):
                if i < 3:
                    pyautogui.hotkey('alt', 'q')
                sleep(3)
                leave_button = pyautogui.locateCenterOnScreen('leave_button.png')
                sleep(2)
                if leave_button is not None:
                    break

            while datetime.now() < end_datetime_obj:
                sleep(30)
                pass

            if leave_button is not None:
                pyautogui.moveTo(leave_button)
                pyautogui.click()
                pyautogui.move(0, -100)
                sleep(5)
            else:
                print("Failed to detect 'Leave Meeting' button!")
                print("Please leave the meeting manually!")


if __name__ == "__main__":
    is_fucked = False
    if not os.path.exists("leave_button.png"):
        print(
            '''
        #####################################################################
        #     Please drop the "leave_button.png" file in this directory     #
        #####################################################################
            '''
        )
        is_fucked = True

    if not os.path.exists("meeting.csv"):
        print(
            '''
        #####################################################################
        #        Please create a "meeting.csv" file in this directory       #
        #####################################################################
            '''
        )
        is_fucked = True

    print(
        '''
        #####################################################################
        #      Please enter your meeting details in "meeting.csv" file      #
        #-------------------------------------------------------------------#
        #                       "meeting.csv" file format                   #
        #-------------------------------------------------------------------#
        #                   zoom_meeting_link,start_time,end_time           #              
        #-------------------------------------------------------------------#
        # e.g:                                                              #
        # https://us02web.zoom.us/j/xyz?pwd=abc,04:30,13:50                 #
        # https://us02web.zoom.us/j/xyz?pwd=abc,14:25,15:50                 #
        #-------------------------------------------------------------------#
        # - Please check the option for "Always allow zoom.us to open links #
        #   of this type in the associated app" before using this tool      #
        # - Time Format: 24 Hrs, HH:MM form                                 #
        # - There should be no space in the beginning of a line             #
        # - There should be no space after , (comma)                        #
        #####################################################################
        '''
    )

    if not is_fucked:
        process_meetings()

    print(
'''
                                      __            
           _____ ____   ____   _____ / /____ _ _  __
          / ___// __ \ / __ \ / ___// // __ `/| |/_/
         (__  )/ / / // /_/ // /   / // /_/ /_>  <  
        /____//_/ /_/ \____//_/   /_/ \__,_//_/|_|  
                                                    
'''
          )
    input("\nPress 'Enter' to exit...")
