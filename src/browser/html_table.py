# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#####################################
#####################################
#####################################
### DO NOT LOOK INSIDE THIS FILE! ###
#####################################
#####################################
#####################################
#####################################
# This contains spoilers for exercise
# 4b. Reading this code is cheating!
#####################################
#####################################
#####################################
#####################################

class HTMLTable:
    def __init__(self):
        self.rows = list()
    
    def handle_tr_start(self):
        self.rows.append(list())

    def handle_td_start(self):
        if len(self.rows) == 0: # no tr was found
            self.rows.append([""])
        else:
            self.rows[-1].append("")

    def handle_th_start(self):
        if len(self.rows) == 0: # no tr was found
            self.rows.append([None])
        else:
            self.rows[-1].append("")

    def handle_data(self, data):
        if len(self.rows) == 0: # no tr was found
            self.rows.append(list())
        if len(self.rows[-1]) == 0: # no td was found
            self.handle_td_start() # so pretend
        self.rows[-1][-1] += data

    def handle_table_end(self, initial_y_pos, draw_at):
        """
        Draws the table, using the passed function which takes
        x and y positions and content, draws the content,
        and returns a tuple of (x, y) space
        occupied.
        Returns the y position after the table is drawn.
        """
        if len(self.rows) == 0:
            return initial_y_pos
        y_pos = initial_y_pos
        column_widths = list()
        first_row = True
        # Column widths are based on the first row space
        # occupied. A real algorithm would consider other rows.
        for row in self.rows:
            max_height = 0
            if first_row:
                first_row = False
                for cell in row:
                    current_x_pos = sum(column_widths)
                    (width, height) = draw_at(current_x_pos, y_pos, cell)
                    column_widths.append(width + 10) # padding
                    max_height = max(max_height, height)
            else:
                current_x_pos = 0
                for n, cell in enumerate(row):
                    (_, height) = draw_at(current_x_pos, y_pos, cell)
                    max_height = max(max_height, height)
                    if len(column_widths) > n:
                        current_x_pos += column_widths[n]
                    else:
                        # The first row had no such column, just make up a width...
                        current_x_pos += 250
            y_pos += max_height + 10 # padding
        return y_pos