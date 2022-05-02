#  Copyright 2008-2015 Nokia Networks
#  Copyright 2016-     Robot Framework Foundation
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

import os.path
import unittest

from resources.setting_utils import TestSettingsHelper
from robotide.preferences.settings import SettingsMigrator


class TestMergeSettings(TestSettingsHelper):

    def setUp(self):
        base = os.path.join(os.path.dirname(__file__), '..', 'resources')
        self.settings_cfg = os.path.join(base, 'settings2.cfg')
        self.user_cfg = os.path.join(base, 'user2.cfg')

    def tearDown(self):
        pass

    def test_merge_settings(self):
        SettingsMigrator(self.settings_cfg, self.user_cfg).merge()
        SettingsMigrator(self.settings_cfg, self.user_cfg).merge()
        content = self._read_settings_file_content(self.user_cfg)
        line_count = len(content.splitlines())
        self.assertEqual(line_count, 34, "line count should be 34 was %s" %
                         line_count)


if __name__ == "__main__":
    unittest.main()
