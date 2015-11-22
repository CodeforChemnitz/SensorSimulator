/*
 * Bind/Unbind events
 *
 * Usage:
 *   var el = document.getElementyById('#container');
 *   b(el, 'click', function() {
 *     console.log('clicked');
 *   });
 *
 * Copyright (C) 2011 Jed Schmidt <http://jed.is> - WTFPL
 * More: https://gist.github.com/968186
 *
 */

var p = function(
  a, // a DOM element
  b, // an event name such as "click"
  c, // (placeholder)
  d  // (placeholder)
){
  c = c || document; // use the document by default
  d = c[             // save the current onevent　handler
    b = "on" + b     // prepent the event name with "on"
  ];
  a = c[b] =                 // cache and replace the current handler
    function(e) {            // with a function that
      d = d && d(            // executes/caches the previous handler
        e = e || c.event     // with a cross-browser object,
      );

      return (a = a && b(e)) // and calls the passed function,
        ? b                  // returning the current handler if it rebinds
        : d                  // and the previous handler otherwise.
    };
  c = this // cache the window to fetch IE events
};

