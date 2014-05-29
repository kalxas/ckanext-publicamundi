/* Module for handling a spatial query by drawing a bbox
 */
this.ckan.module('publicamundi-spatial-query', function ($, _) {
  return {
    options: {
      i18n: {
      },
      style: {
        color: '#F06F64',
        weight: 2,
        opacity: 1,
        fillColor: '#F06F64',
        fillOpacity: 0.15
      },
      default_extent: [[90, 180], [-90, -180]]
    },
    template: {
      buttons: [
        '<div id="dataset-map-edit-buttons">',
        '<a href="javascript:;" class="btn cancel">Cancel</a> ',
        '<a href="javascript:;" class="btn apply disabled">Apply</a>',
        '</div>'
      ].join('')
    },

    initialize: function () {
      var module = this;
      $.proxyAll(this, /_on/);

      var user_default_extent = this.el.data('default_extent');
      if (user_default_extent ){
        if (user_default_extent instanceof Array) {
          // Assume it's a pair of coords like [[90, 180], [-90, -180]]
          this.options.default_extent = user_default_extent;
        } else if (user_default_extent instanceof Object) {
          // Assume it's a GeoJSON bbox
          this.options.default_extent = new L.GeoJSON(user_default_extent).getBounds();
        }
      }
      
      this.el.ready(this._onReady);
      
      return;
    },

    _getParameterByName: function (name) {
      var match = RegExp('[?&]' + name + '=([^&]*)').exec(window.location.search);
      return match ? decodeURIComponent(match[1].replace(/\+/g, ' ')) : null;
    },

    _drawExtentFromCoords: function(xmin, ymin, xmax, ymax) {
        if ($.isArray(xmin)) {
            var coords = xmin;
            xmin = coords[0]; ymin = coords[1]; xmax = coords[2]; ymax = coords[3];
        }
        return new L.Rectangle([[ymin, xmin], [ymax, xmax]], this.options.style);
    },

    _drawExtentFromGeoJSON: function(geom) {
        return new L.GeoJSON(geom, {style: this.options.style});
    },

    _onReady: function() {
      var module = this;
      var map;
      var extentLayer;
      var previous_box;
      var previous_extent;
      var is_expanded = false;
      var should_zoom = true;
      var form = $("#dataset-search");
      var buttons;

      // Add necessary fields to the search form if not already created
      $(['ext_bbox', 'ext_prev_extent']).each(function(index, item){
        if ($("#" + item).length === 0) {
          $('<input type="hidden" />').attr({'id': item, 'name': item}).appendTo(form);
        }
      });

      // OK map time
      map = new L.Map('dataset-map-container', {attributionControl: false});

      // MapQuest OpenStreetMap base map
      map.addLayer(new L.TileLayer(
        'http://otile{s}.mqcdn.com/tiles/1.0.0/osm/{z}/{x}/{y}.png',
         {maxZoom: 18, subdomains: '1234'}
      ));

      // Initialize the draw control
      map.addControl(new L.Control.Draw({
        position: 'topright',
        polyline: false, polygon: false,
        circle: false, marker: false,
        rectangle: {
          shapeOptions: module.options.style,
          title: 'Draw rectangle'
        }
      }));

      // OK add the expander
      $('.leaflet-control-draw a', module.el).on('click', function(e) {
        if (!is_expanded) {
          $('body').addClass('dataset-map-expanded');
          if (should_zoom && !extentLayer) {
            map.zoomIn();
          }
          resetMap();
          is_expanded = true;
        }
      });

      // Setup the expanded buttons
      buttons = $(module.template.buttons).insertBefore('#dataset-map-attribution');

      // Handle the cancel expanded action
      $('.cancel', buttons).on('click', function() {
        $('body').removeClass('dataset-map-expanded');
        if (extentLayer) {
          map.removeLayer(extentLayer);
        }
        setPreviousExtent();
        setPreviousBBBox();
        resetMap();
        is_expanded = false;
      });

      // Handle the apply expanded action
      $('.apply', buttons).on('click', function() {
        if (extentLayer) {
          $('body').removeClass('dataset-map-expanded');
          is_expanded = false;
          resetMap();
          // Eugh, hacky hack.
          setTimeout(function() {
            map.fitBounds(extentLayer.getBounds());
            submitForm();
          }, 200);
        }
      });

      // When user finishes drawing the box, record it and add it to the map
      map.on('draw:rectangle-created', function (e) {
        if (extentLayer) {
          map.removeLayer(extentLayer);
        }
        extentLayer = e.rect;
        $('#ext_bbox').val(extentLayer.getBounds().toBBoxString());
        map.addLayer(extentLayer);
        $('.apply', buttons).removeClass('disabled').addClass('btn-primary');
      });

      // Record the current map view so we can replicate it after submitting
      map.on('moveend', function(e) {
        $('#ext_prev_extent').val(map.getBounds().toBBoxString());
      });

      // Ok setup the default state for the map
      var previous_bbox;
      setPreviousBBBox();
      setPreviousExtent();

      // OK, when we expand we shouldn't zoom then
      map.on('zoomstart', function(e) {
        should_zoom = false;
      });


      // Is there an existing box from a previous search?
      function setPreviousBBBox() {
        previous_bbox = module._getParameterByName('ext_bbox');
        if (previous_bbox) {
          $('#ext_bbox').val(previous_bbox);
          extentLayer = module._drawExtentFromCoords(previous_bbox.split(','))
          map.addLayer(extentLayer);
          map.fitBounds(extentLayer.getBounds());
        }
      }

      // Is there an existing extent from a previous search?
      function setPreviousExtent() {
        previous_extent = module._getParameterByName('ext_prev_extent');
        if (previous_extent) {
          coords = previous_extent.split(',');
          map.fitBounds([[coords[1], coords[0]], [coords[3], coords[2]]]);
        } else {
          if (!previous_bbox){
              map.fitBounds(module.options.default_extent);
          }
        }
      }

      // Reset map view
      function resetMap() {
        L.Util.requestAnimFrame(map.invalidateSize, map, !1, map._container);
      }

      function submitForm() {
        setTimeout(function() {
          form.submit();
        }, 800);
      }
    }
  }
});


/* Module for handling a spatial query by specifying a location (by name)
 */
this.ckan.module('publicamundi-location-query', function ($, _) {
  return {
    options: {
    },
    
    _getParameterByName: function (name) {
      var re1 = new RegExp('[?&]' + name + '=([^&]*)');
      var m1 = re1.exec(window.location.search);
      return m1 ? decodeURIComponent(m1[1].replace(/\+/g, ' ')):null;
    },

    initialize: function() 
    { 
        var module = this;

        $.proxyAll(this, /_on/);
 
        this.el.ready(this._onReady);

        return;
    },

    teardown: function() 
    {
        /* nop */
    },
    
    _onReady: function()
    {
        var module = this;
        var form = $("#dataset-search");
        var prev_code = module._getParameterByName('ext_location');
        var re_code = new RegExp('^[0-9]+$')
        var api_url = '/api/action/location_get?'

        // Append a hidden input in search form
        var input = $('<input/>');
        input.attr({
            'type': 'hidden',
            'name': 'ext_location',
            'id': 'ext_location',
        });
        input.appendTo(form);
         
        // Bind change handlers
        $("#input-ext_location").on('change', function (ev) {
            var $t = $(this);
            var code = $t.val(), bbox = null;
            if (re_code.test(code)) {
                var xhr = $.getJSON(api_url + $.param({'code':code}))
                .done(function(response) {
                    var geojson_bbox = response.result.bbox;
                    var minx = geojson_bbox.coordinates[0][0][0],
                        miny = geojson_bbox.coordinates[0][0][1],
                        maxx = geojson_bbox.coordinates[0][2][0],
                        maxy = geojson_bbox.coordinates[0][2][1];
                    var bbox = [minx, miny, maxx, maxy];
                    setTimeout(function () {
                        $('#ext_location').val(code);
                        $('#ext_bbox').val(bbox.join(','));
                        $('#ext_prev_extent').val('')
                        form.submit();
                    }, 200)
                })
                .fail(function() {
                    console.error('Cannot fetch object from '+api_url)
                })
            } else {
                console.info ('Nothing to search for (unknown code)')
            }
            return false;
        })
        
        return;
    },
  }
});
