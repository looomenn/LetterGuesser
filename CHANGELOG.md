# Changelog

## Unreleased - 2024-12-02

### Added
- Toast notification widget
- ComboBox widget
- Icon for the `ComboBox`

### Changed
- Move app settings to the `QSettings`
- Adjust `Buttons` styles
- Migrate `Button` to `PyQt6`

### Deprecated
- Status Frame
- OptionMenu widget

## [2.0.0-alpha.2] - 2024-11-27

### Added
- Light theme
- Dark theme
- SCSS compilation
- Primitives file for the basic style variables 
- User settings (for theme and langauge)

### Changed
- Migrate `InputBlock` to PyQt6
- Migrate `Card` to PyQt6
- Migrate `CardGoup` to PyQt6

### Fixed
- Localisation for `MenuBar`

### Deprecated
- `TextBlockSegment` widget (use `InputBlock` instead)
- Style variables (in styles sub-package)
- `BaseFrame` (use `QFrame` instead)

### Removed
- Debug prints

## [2.0.0-alpha.1] - 2024-11-18

### Added
- Localisation keys for the `MenuBar`
- `flake8` additional modules for tests (see dev deps)
- `MenuBar` class

### Changed
- `Localisation` migration to PyQt6
- Entry point base from `customtkinter` to `QApplication`

### Fixed
- App window `center` method

### Deprecated
- `HeaderFrame` class

### Removed
- `tox` integration 

## [2.0.0-alpha.0] - 2024-11-15

### Added
- `PyQt6` to `poetry` dependencies

### Removed
- `customtkinter` from `poetry` dependencies
- `ctktable` from `poetry` dependencies


## [1.0.0] - 2024-11-14

### Fixed
- Not loading `.mo` files
