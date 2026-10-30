"use strict";

(function ($) {

  var SPATIAL_TYPES = [
    'vector', 'vector_point', 'vector_polygon', 'vector_polyline',
    'vector_line', 'vector_3d', 'point_cloud', 'voxel_grid', 'mesh_3d', 'raster'
  ];

  var CRS_FIELDS = [
    'reference_system_type',
    'default_horizontal_crs',
    'default_vertical_crs',
    'horizontal_resolution',
    'vertical_resolution'
  ];

  function isSpatial(value) {
    return SPATIAL_TYPES.indexOf(value) !== -1;
  }

  function updateCrsFields() {
    var spatial = isSpatial($('#field-data_type').val());
    $.each(CRS_FIELDS, function (_, fieldName) {
      var $control = $('#field-' + fieldName).closest('.form-group');
      if (spatial) {
        $control.show();
      } else {
        $control.hide();
      }
    });
  }

  $(document).ready(function () {
    if ($('#field-data_type').length === 0) return;
    updateCrsFields();
    $('#field-data_type').on('change', updateCrsFields);
  });

})(jQuery);
