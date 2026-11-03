# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
For releases `< 1.0.0` minor version steps may indicate breaking changes too.

## [0.1.0] - 2026-11-03

> Requires `ckanext-scheme-sddi >= 0.1.0`

### Added
- HTML for selection of predefined schemas on catalog entry creation
- Auto-select main category group based on dataset type selection
- Hover tooltips with descriptions on main category cards
- `isRawData` and `dataModification` fields with conditional UI visibility for Device category
- Multi-select field for involved organizations
- CSS counter for composite repeating field group numbering
- Category marker colors now use named CSS classes based on main category instead of positional classes

### Changed
- Resources are now optional when creating a catalog entry — clicking **Finish** without adding a resource redirects directly to the dataset page
- Registered `IResourceController` so resource update hooks fire correctly for email notifications

### Fixed
- Removed deprecated `h.popular` helper call from resource template that caused a crash when a restricted resource was rendered
- Composite repeating display crash when `form_blanks` is not defined
- Composite repeating display: each subfield now shown on its own line
- MultiPoint geometry constraint enforced for sensor group devices
- CRS fields shown only when a spatial data type is selected in Dataset and Documents form
- Leaflet.draw toolbar icons now visible in the spatial extent form
- Multiple topics can now be assigned to a catalog entry (see [#21](https://github.com/MarijaKnezevic/ckanext-theme-sddi/issues/21))
- Images in markdown descriptions can now be resized using `width`, `height`, and `style` attributes (see [#20](https://github.com/MarijaKnezevic/ckanext-theme-sddi/issues/20))

## [0.0.4] - 2025-02-18

### Fixed
 - Middleware fix (see [#15](https://github.com/MarijaKnezevic/ckanext-theme-sddi/pull/15) )
 - Update logic for the missing resources (see [#18](https://github.com/MarijaKnezevic/ckanext-theme-sddi/pull/18) )
 - Typo fixing
 - Show map when displaying spatial metadata field

## [0.0.3] - 2025-02-04
### Fixed
Facets to correctly show topics

## [0.0.2] - 2025-01-23

### Added
Translations for filters on dataset page

### Fixed
Path to the location of the images in the main category and theme, and the images on the mail page
  
## [0.0.1] - 2024-10-04
- Initial release
- Compatibility with CKAN 2.11.

## [template] - YYYY-MM-DD

### Added

### Changed

### Removed

### Fixed

### Security

### Deprecated

### Known issues

[Unreleased]: https://github.com/MarijaKnezevic/ckanext-theme-sddi/compare/0.1.0...HEAD
[0.1.0]: https://github.com/MarijaKnezevic/ckanext-theme-sddi/compare/0.0.4...0.1.0
[0.0.4]: https://github.com/MarijaKnezevic/ckanext-theme-sddi/compare/0.0.3...0.0.4
[0.0.3]: https://github.com/MarijaKnezevic/ckanext-theme-sddi/compare/0.0.2...0.0.3
[0.0.2]: https://github.com/MarijaKnezevic/ckanext-theme-sddi/compare/0.0.1...0.0.2
[0.0.1]: https://github.com/MarijaKnezevic/ckanext-theme-sddi/releases/tag/0.0.1
[template]: https://keepachangelog.com/en/1.0.0/
