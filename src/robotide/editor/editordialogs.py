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

import wx

from robotide.validators import ScalarVariableNameValidator,\
    ListVariableNameValidator, TimeoutValidator, NonEmptyValidator, ArgumentsValidator
from robotide import utils
from robotide.context import Font

from fieldeditors import ValueEditor, ListValueEditor, MultiLineEditor,\
    ContentAssistEditor, VariableNameEditor
from dialoghelps import get_help


def EditorDialog(obj):
    return globals()[obj.label.replace(' ', '') + 'Dialog']


class _Dialog(wx.Dialog):
    _title = property(lambda self: utils.name_from_class(self, drop='Dialog'))

    def __init__(self, parent, controller, plugin=None, item=None):
        wx.Dialog.__init__(self, parent, -1, self._title,
                           style=wx.DEFAULT_DIALOG_STYLE|wx.THICK_FRAME)
        self.SetExtraStyle(wx.WS_EX_VALIDATE_RECURSIVELY)
        self.plugin = plugin
        self._controller = controller
        self._item = item
        self._sizer = wx.BoxSizer(wx.VERTICAL)
        self._editors = self._get_editors(item)
        for editor in self._editors:
            self._sizer.Add(editor, editor.expand_factor, wx.EXPAND)
        self._create_help()
        self._create_line()
        self._create_buttons()
        self.SetSizer(self._sizer)
        self._sizer.Fit(self)
        self._editors[0].set_focus()

    def _create_line(self):
        line = wx.StaticLine(self, size=(20,-1), style=wx.LI_HORIZONTAL)
        self._sizer.Add(line, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.TOP, 5)

    def _create_help(self):
        text = wx.StaticText(self, label=get_help(self._title))
        text.SetFont(Font().help)
        self._sizer.Add(text, flag=wx.ALL, border=2)

    def _create_buttons(self):
        buttons = self.CreateStdDialogButtonSizer(wx.OK|wx.CANCEL)
        self._sizer.Add(buttons, 0, wx.ALIGN_CENTER|wx.ALL, 5)

    def get_value(self):
        return [ e.get_value() for e in self._editors ]


class ScalarVariableDialog(_Dialog):

    def _get_editors(self, var):
        name, value = (var.name, var.value[0]) if var else ('${}', '')
        validator = ScalarVariableNameValidator(self._controller, name)
        return [VariableNameEditor(self, name, 'Name', validator),
                ValueEditor(self, value, 'Value')]

class ListVariableDialog(_Dialog):

    def _get_editors(self, var):
        name, value = (var.name, var.value) if var else ('@{}', '')
        validator = ListVariableNameValidator(self._controller, name)
        return [VariableNameEditor(self, name, 'Name', validator),
                ListValueEditor(self, value, 'Value')]


class LibraryDialog(_Dialog):

    def _get_editors(self, item):
        name = item and item.name or ''
        args = item and item.args or ''
        alias = item.alias if item else ''
        return [ValueEditor(self, name, 'Name',
                            validator=NonEmptyValidator(self._title)),
                ValueEditor(self, args, 'Args'),
                ValueEditor(self, alias, 'Alias')]

class VariablesDialog(LibraryDialog):
    pass

class ResourceDialog(LibraryDialog):
    pass


class DocumentationDialog(_Dialog):

    def _get_editors(self, doc):
        return [MultiLineEditor(self, doc)]

    def get_value(self):
        return _Dialog.get_value(self)


class _SettingDialog(_Dialog):
    _validator = None

    def _get_editors(self, item):
        editor = ValueEditor(self, item.value)
        if self._validator:
            editor.set_validator(self._validator())
        return [editor]


class ForceTagsDialog(_SettingDialog):
    pass

class DefaultTagsDialog(_SettingDialog):
    pass

class TagsDialog(_SettingDialog):
    pass


class _FixtureDialog(_SettingDialog):

    def _get_editors(self, item):
        return [ContentAssistEditor(self, item.value)]

class SuiteSetupDialog(_FixtureDialog): pass

class SuiteTeardownDialog(_FixtureDialog): pass

class TestSetupDialog(_FixtureDialog): pass

class TestTeardownDialog(_FixtureDialog): pass

class SetupDialog(_FixtureDialog): pass

class TeardownDialog(_FixtureDialog): pass


class TemplateDialog(_FixtureDialog): pass

class TestTemplateDialog(_FixtureDialog): pass


class ArgumentsDialog(_SettingDialog):
    _validator = ArgumentsValidator

class ReturnValueDialog(_SettingDialog):
    pass

class TestTimeoutDialog(_SettingDialog):
    _validator = TimeoutValidator

class TimeoutDialog(TestTimeoutDialog):
    pass


class MetadataDialog(_Dialog):

    def _get_editors(self, item):
        name, value = item and (item.name, item.value) or ('', '')
        return [ValueEditor(self, name, 'Name'),
                ValueEditor(self, value, 'Value')]
