(function ($) {
  'use strict';

  var QUEUE_KEY    = 'sddi_dist_queue';
  var REDIRECT_KEY = 'sddi_dist_redirect';

  // Per dataset_type: list of { field, name } matching the schema has_* fields.
  var TYPE_DIST_MAP = {
    'dataset_documents': [{ field: 'has_distribution',       name: 'Content URL' }],
    'project':           [{ field: 'has_distribution',       name: 'Project URI' }],
    'online-service':    [{ field: 'has_linkage',             name: 'Linkage' },
                          { field: 'has_external_docs',       name: 'External Documentation' },
                          { field: 'has_open_api_document',   name: 'OpenAPI Document' }],
    'software':          [{ field: 'has_software_help',       name: 'Software Help' },
                          { field: 'has_documentation_url',   name: 'Documentation URL' },
                          { field: 'has_code_repository_url', name: 'Code Repository URL' }],
    'online-application':[{ field: 'has_external_docs',       name: 'External Documentation' },
                          { field: 'has_service_doc',         name: 'Service Documentation' }]
  };

  function getDatasetType() {
    var m = window.location.pathname.match(/^\/([^\/]+)\//);
    return m ? m[1] : null;
  }

  // ── 1. Dataset form (new): collect "yes" answers into queue on submit ────────
  function initDatasetForm() {
    // Never run on the resource form — its URL also ends with /new
    if (window.location.pathname.match(/\/resource\/new$/)) return;

    var $btn = $('button[name="save"], input[name="save"]');
    if (!$btn.length) return;
    // Only run on dataset new/edit pages
    if (!$('input[name="_ckan_phase"]').length &&
        !window.location.pathname.match(/\/(new|edit)(\/?$|\/?#|\?)/)) return;

    $btn.on('click', function () {
      var dtype = getDatasetType();
      var dists = (dtype && TYPE_DIST_MAP[dtype]) ? TYPE_DIST_MAP[dtype] : [];
      var queue = [];

      dists.forEach(function (d) {
        if ($('#field-' + d.field).val() === 'yes') {
          queue.push({ name: d.name });
        }
      });

      if (queue.length) {
        sessionStorage.setItem(QUEUE_KEY, JSON.stringify(queue));
      } else {
        sessionStorage.removeItem(QUEUE_KEY);
        sessionStorage.removeItem(REDIRECT_KEY);
      }
    });
  }

  // ── 2. Resource/new page: pre-fill Name from first item in queue ────────────
  function initResourceForm() {
    if (!window.location.pathname.match(/\/resource\/new$/)) return;

    var queue = JSON.parse(sessionStorage.getItem(QUEUE_KEY) || 'null');
    if (!queue || !queue.length) return;

    var item = queue.shift();
    sessionStorage.setItem(QUEUE_KEY, JSON.stringify(queue));

    var $name = $('#field-name');
    if ($name.length && !$name.val()) $name.val(item.name);

    // If more items remain, redirect back after this resource is saved
    if (queue.length) {
      $('form').on('submit', function () {
        sessionStorage.setItem(REDIRECT_KEY, '1');
      });
    }
  }

  // ── 3. Post-save: open resource/new again if queue still has items ───────────
  function checkRedirect() {
    if (!sessionStorage.getItem(REDIRECT_KEY)) return;

    var queue = JSON.parse(sessionStorage.getItem(QUEUE_KEY) || 'null');
    if (!queue || !queue.length) {
      sessionStorage.removeItem(REDIRECT_KEY);
      return;
    }

    // We're on the dataset page after saving a resource: /<type>/<name>
    var match = window.location.pathname.match(/^\/([^\/]+)\/([^\/]+)\/?$/);
    if (match) {
      sessionStorage.removeItem(REDIRECT_KEY);
      window.location.href = '/' + match[1] + '/' + match[2] + '/resource/new';
    }
  }

  $(document).ready(function () {
    initDatasetForm();
    initResourceForm();
    checkRedirect();
  });

}(jQuery));
