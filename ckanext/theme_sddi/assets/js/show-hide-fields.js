ckan.module("show-hide-fields", function ($, _) {
    "use strict";
    return {
        options: {},

        initialize: function () {
            this._toggleFields(); // Call initially to set the correct visibility

            $('#field-restricted').on('change', this._toggleFields.bind(this));
        },

        _toggleFields: function () {
            const selectedOption = $('#field-restricted').val();
            const organizationField = $('#field-organizations').closest('.form-group');
            const userField = $('#allowed_users').closest('.allowed_users');

            if (selectedOption === 'same_organization') {
                this._showField(organizationField);
                this._hideField(userField);
            } else if (selectedOption === 'only_allowed_users') {
                this._hideField(organizationField);
                this._showField(userField);
            } else {
                this._hideField(organizationField);
                this._hideField(userField);
            }
        },

        _showField: function (field) {
            field.removeClass('hidden');
        },

        _hideField: function (field) {
            field.addClass('hidden');
        }
    };
});
