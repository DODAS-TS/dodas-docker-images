/**
 *
 *
 * Placeholder for custom user javascript
 * mainly to be overridden in profile/static/custom/custom.js
 * This will always be an empty file in IPython
 *
 * User could add any javascript in the `profile/static/custom/custom.js` file.
 * It will be executed by the ipython notebook at load time.
 *
 * Same thing with `profile/static/custom/custom.css` to inject custom css into the notebook.
 *
 *
 * The object available at load time depend on the version of IPython in use.
 * there is no guaranties of API stability.
 *
 * The example below explain the principle, and might not be valid.
 *
 * Instances are created after the loading of this file and might need to be accessed using events:
 *     define([
 *        'base/js/namespace',
 *        'base/js/promises'
 *     ], function(IPython, promises) {
 *         promises.app_initialized.then(function (appName) {
 *             if (appName !== 'NotebookApp') return;
 *             IPython.keyboard_manager....
 *         });
 *     });
 *
 * __Example 1:__
 *
 * Create a custom button in toolbar that execute `%qtconsole` in kernel
 * and hence open a qtconsole attached to the same kernel as the current notebook
 *
 *    define([
 *        'base/js/namespace',
 *        'base/js/promises'
 *    ], function(IPython, promises) {
 *        promises.app_initialized.then(function (appName) {
 *            if (appName !== 'NotebookApp') return;
 *            IPython.toolbar.add_buttons_group([
 *                {
 *                    'label'   : 'run qtconsole',
 *                    'icon'    : 'icon-terminal', // select your icon from http://fortawesome.github.io/Font-Awesome/icons
 *                    'callback': function () {
 *                        IPython.notebook.kernel.execute('%qtconsole')
 *                    }
 *                }
 *                // add more button here if needed.
 *                ]);
 *        });
 *    });
 *
 * __Example 2:__
 *
 * At the completion of the dashboard loading, load an unofficial javascript extension
 * that is installed in profile/static/custom/
 *
 *    define([
 *        'base/js/events'
 *    ], function(events) {
 *        events.on('app_initialized.DashboardApp', function(){
 *            requirejs(['custom/unofficial_extension.js'])
 *        });
 *    });
 *
 *
 *
 * @module IPython
 * @namespace IPython
 * @class customjs
 * @static
 */

var li = document.createElement('li');

var a = document.createElement('a');
var linkText = document.createTextNode("Collaborative Python 3 (Beta)");
a.appendChild(linkText);
a.title = "Jupyter collaborative";
a.href = "/services/Collaborative-Jupyter/";
a.target = "_blank";

li.appendChild(a);

var menu_new = document.getElementById("new-menu");
var dropHeader = menu_new.children[0];
var python3 = menu_new.children[1];
menu_new.prepend(li);
menu_new.removeChild(dropHeader);
menu_new.removeChild(python3);
menu_new.prepend(python3);
menu_new.prepend(dropHeader);