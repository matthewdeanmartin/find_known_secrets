# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.3.0] - 2023-05-29

### Changed

- Massive modernization of the codebase
- Standardized build script to match conventions used across all maintained projects

## [1.0.30] - 2018-08-10

### Added

- Start using hooks
- Colorized output
- Formatting and improved error handling
- Initial publication of the package as a novel approach to scanning for known secrets in source code

### Changed

- Build script improvements
- Improved hook code
- Error style improvements with exit codes and reduced pynt stack noise

### Fixed

- FileNotFoundError handling
- Python 2 compatibility fixes
- JSON handling for Python 2

[1.3.0]: https://github.com/matthewdeanmartin/find_known_secrets/compare/v1.0.30...v1.3.0
[1.0.30]: https://github.com/matthewdeanmartin/find_known_secrets/releases/tag/v1.0.30
