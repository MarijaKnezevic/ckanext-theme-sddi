"use strict";

(function ($) {

  function updateSpatialField() {
    var val = $('#field-is_sensor_group').val();
    var $spatial = $('#field-spatial').closest('.form-group');
    if (val === 'true') {
      $spatial.show();
    } else {
      $spatial.hide();
    }
    updateDrawToolbar();
    $('#sensor-group-geo-error').remove();
  }

  function updateDrawToolbar() {
    // Delay to ensure Leaflet.draw toolbar is rendered before toggling
    setTimeout(function () {
      var isSensorGroup = $('#field-is_sensor_group').val() === 'true';
      $('.leaflet-draw-draw-polygon').toggle(!isSensorGroup);
      $('.leaflet-draw-draw-rectangle').toggle(!isSensorGroup);
      $('.leaflet-draw-draw-marker').toggle(isSensorGroup);
    }, 300);
  }

  function validateSensorGroupGeometry(e) {
    if ($('#field-is_sensor_group').val() !== 'true') return;
    var spatialVal = $.trim($('#field-spatial').val());
    if (!spatialVal) return;
    try {
      var geom = JSON.parse(spatialVal);
      if (geom.type !== 'MultiPoint') {
        e.preventDefault();
        $('#sensor-group-geo-error').remove();
        $('#field-spatial').before(
          '<div id="sensor-group-geo-error" class="error-block" style="color:#d9534f;margin-bottom:5px;">' +
          'When Is Sensor Group is Yes, the location must be a MultiPoint geometry. Use the marker tool to draw points.' +
          '</div>'
        );
        $('html, body').animate({ scrollTop: $('#field-spatial').offset().top - 100 }, 300);
      }
    } catch (err) { /* invalid JSON — let server handle */ }
  }

  $(document).ready(function () {
    if ($('#field-is_sensor_group').length === 0) return;
    updateSpatialField();
    $('#field-is_sensor_group').on('change', updateSpatialField);
    $('form[data-module="basic-form"]').on('submit', validateSensorGroupGeometry);
  });

})(jQuery);
