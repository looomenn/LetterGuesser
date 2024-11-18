# Changelog

## [Unreleased] - 2024-11-18

### Fixed
- Localisation for `MenuBar`

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
