#  Copyright 2008-2009 Nokia Siemens Networks Oyj
#  
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#  
#      http://www.apache.org/licenses/LICENSE-2.0
#  
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.


class RobotDataList(list):

    def __init__(self, datafile, data=[]):
        list.__init__(self)
        self.datafile = datafile
        self._parse_data(data)

    def swap(self, index1, index2):
        self[index1], self[index2] = self[index2], self[index1]
        self.datafile.set_dirty()

    def move_up(self, item):
        index = self.index(item)
        if index:
            self.swap(index-1, index)
            self.datafile.set_dirty()
            return True
        return False

    def move_down(self, item):
        index = self.index(item)
        if index < len(self)-1:
            self.swap(index, index+1)
            self.datafile.set_dirty()
            return True
        return False

    def pop(self, index):
        self.datafile.set_dirty()
        list.pop(self, index)
