# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
For releases `< 1.0.0` minor version steps may indicate breaking changes too.

## [Unreleased]

### Changed
- Resources are now optional when creating a catalog entry — clicking **Finish** on the resource step without adding a resource activates the dataset and redirects to its page directly.

### Added
- Category marker colors on dataset listing and detail pages now use named CSS classes based on main category instead of positional classes (`zero`–`eight`), so colors remain correct regardless of category order.
- Hovering over a main category card on the new catalog entry page now shows a short description of that category.

### Fixed
- Multiple topics can now be assigned to a catalog entry — a new `ckan theme-sddi setup-solr` command registers the `topic` Solr field as `multiValued`, preventing the 500 error that occurred when more than one topic was selected (see [#21](https://github.com/MarijaKnezevic/ckanext-theme-sddi/issues/21)).

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

[Unreleased]: https://github.com/MarijaKnezevic/ckanext-theme-sddi/compare/0.0.3...HEAD
[0.0.4]: https://github.com/MarijaKnezevic/ckanext-theme-sddi/compare/0.0.3...0.0.4
[0.0.3]: https://github.com/MarijaKnezevic/ckanext-theme-sddi/compare/0.0.2...0.0.3
[0.0.2]: https://github.com/MarijaKnezevic/ckanext-theme-sddi/compare/0.0.1...0.0.2
[0.0.1]: https://github.com/MarijaKnezevic/ckanext-theme-sddi/releases/tag/0.0.1
[template]: https://keepachangelog.com/en/1.0.0/
