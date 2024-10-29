# Changelog

## [Unreleased]

### Added
- Changelog
- `Event` class for managing event registration and notifications.
- `ListItem` and `List` implementation
- Localisation for the `guessed chars` table
- Alphabets for two supported locales
- `get_alphabet` for `Localisation` class
- `AttemptsTable` implementation
- `BaseScrollFrame`, a scrollable version of `BaseFrame`
- `BaseTable` class for table components
- Windget Loading: added support for loading widgets in `self.manager` using `load_widgets` method
- New methods for `Button` and `ButtonGroup` classes
- Integrated [Py-Babel](https://babel.pocoo.org/en/latest/) for localisation
- Corresponding files for the localisations (`assets/locales/`)
- Context for the app (`context.py`)
- Separate folders for GUI elements, frames, and widgets
- `BaseFrame` for other frames to be based on it + pass context to them
- `__init__.py` files for corresponding folders
- `CardGroup` Class that can dynamically create `Card` elements
- New `Localisation` Class that handles localisation :>
- Localisation for tables
- Integrated `CTkTable` for advanced table support
- Toggle language logic
- Placeholder for the `ProbabilityTable`
- Headers for the `ProbabilityTable` and new headers translation logic
- `GuessedChars` table
- `load_right_frame` method to load tables in `ExperimentManager`
- Probability calculation method (`calc_prob`)
- Shortcut `Ctrl-l` to `toggle_language`
- Line height constants
- `ProbabilityTable` class (extending `CTkScrollableFrame`)
- `ProbabilityTable` to `RightFrame`
- `maxsize()` to `App`
- Localization keys for Ukrainian and English translations
- Sample text for Ukrainian and English translations
- `load_texts` method to load sample text based on `lang_code`
- `reset` method in `TextBlockSegment`
- Pass `ExperimentManager` as `manager` to frames
- Key binding for `Return` (Enter) in `input_field`
- `input_handler` in `InputSegment` as entry point for `ExperimentManager`
- `clear` method in `InputSegment`
- Colours for `OptionMenu`
- Experiment reset on language change
- Custom hover effect for OptionMenu (`on_enter`, `on_leave`)
- `set_command` method in `Button`
- Next experiment and reset button logic
- `update_status` method in `StatusFrame`
- `get_widgets` method in `LeftFrame`
- Localization and widget logic in `ExperimentManager`
- `start_experiment` logic in `ExperimentManager`
- Replacement of spaces with underscores in `input_handler`
- Modular UI elements like `Card`, `Cards`, `TextBlockSegment`, `InputSegment`, `Topframe`, and `Actions`.
- Custom `Button` class with `dafault`, `primary`, and `danger` styles, including hover and disabled states.
- Localisation functions for loading, binding, and updating widget text in multiple languages (Ukrainian/English)
- Experiment Manager to control state, user input validation, and updates UI dynamically.
- Helper function `get_resource_path()` for resource loading with `PyInstaller`

### Changed
- `AttemptsTable` renamed to `AttemptsList` as it uses `List` as base
- App dimensions to `1300x740`
- Moved `load_texts()` to `logic/utils.py`
- App font to `Segoe UI`
- `BUTTON_DANGER_TEXT_DISABLED` colours
- Linked `InputFrame` button commands to `ExperimentManager`
- ExperimentManager: Reactivated previously non-functional features
- Switching langauge: Reactivated previously non-functional feature by uncommenting `self.manager.reset_experiment()`
- `.gitignore` to cover JetBrains IDes
- Project file structure
- Separated frames into corresponding files (`gui/frames/`)
- Separated widgets into corresponding files (`gui/widgets/`)
- Separated core logic into corresponding folder and files (`logic/`)
- Separated styles into corresponding files (`styles/`)
- Cleaned `main.py`
- Styles constants naming format from `upprecase` to `lowercase`
- Paddings names starts from 0 px (`pad_0`) ip to 96 (`pad_11`)
- App width to `1240` (previously `1200`)
- `ProbabilityTable` and `RightFrame` grid configuration
- App font to `Calibri`
- `RightFrame` grid configuration
- Color tokens for all `Button` styles
- Initial value of string cards from `None` to `-` (dash)
- Disabled `Button` style logic
- `LeftFrame` grid configuration
- Display of used chars as a string, not as a dictionary
- Improved Ukrainian and English translations
- Set app constants and minimum size constraints for improved UI experience

### Fixed
- Incorrect `command` property for `reset_button`

### Removed
- `cursor` property from `Button` and `OptionMenu` (in `disabled` state) due to OS conflicts
- Requirement to pass `main_widgets: list` into `ExperimentManager`
- Support for the `json` localisation
- `Actions` Class
- Unused logic in `ProbabilityTable`
- Testing `fg_color` in `MainFrame` for `RightFrame`
- Debug prints
- `winfo_height()` check after `100ms` in some frames