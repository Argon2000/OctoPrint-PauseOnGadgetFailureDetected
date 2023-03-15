# coding=utf-8
from __future__ import absolute_import

### (Don't forget to remove me)
# This is a basic skeleton for your plugin's __init__.py. You probably want to adjust the class name of your plugin
# as well as the plugin mixins it's subclassing from. This is really just a basic skeleton to get you started,
# defining your plugin as a template plugin, settings and asset plugin. Feel free to add or remove mixins
# as necessary.
#
# Take a look at the documentation on what other plugin mixins are available.

import octoprint.plugin
from flask import request
from flask import jsonify

class PauseOnGadgetFailureDetectedPlugin(octoprint.plugin.BlueprintPlugin):
    @octoprint.plugin.BlueprintPlugin.route("/hello_world", methods=["GET"])
    def hello_world(self):
        return "Hello world!"

    @octoprint.plugin.BlueprintPlugin.route("/pause_on_possible_failure", methods=["POST"])
    @octoprint.plugin.BlueprintPlugin.csrf_exempt()
    def pause_on_possible_failure(self):
        self._logger.info("Pause on gadget failure detected: Got event")
        self._logger.info("Pause on gadget failure detected: Is JSON: {}".format(request.is_json))
        if request.is_json:
            content = request.get_json()
            self._logger.info("Pause on gadget failure detected: Content: {}".format(content))
        resp = jsonify(success=True)
        return resp

    def is_blueprint_csrf_protected(self):
        return True

    ##~~ Softwareupdate hook
    def get_update_information(self):
        # Define the configuration for your plugin to use with the Software Update
        # Plugin here. See https://docs.octoprint.org/en/master/bundledplugins/softwareupdate.html
        # for details.
        return {
            "pause_on_gadget_failure_detected": {
                "displayName": "Pause on gadget failure detected",
                "displayVersion": self._plugin_version,

                # version check: github repository
                "type": "github_release",
                "user": "Argon2000",
                "repo": "OctoPrint-PauseOnGadgetFailureDetected",
                "current": self._plugin_version,

                # update method: pip
                "pip": "https://github.com/Argon2000/OctoPrint-PauseOnGadgetFailureDetected/archive/{target_version}.zip",
            }
        }


# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "Pause on gadget failure detected"


# Set the Python version your plugin is compatible with below. Recommended is Python 3 only for all new plugins.
# OctoPrint 1.4.0 - 1.7.x run under both Python 3 and the end-of-life Python 2.
# OctoPrint 1.8.0 onwards only supports Python 3.
__plugin_pythoncompat__ = ">=3,<4"  # Only Python 3

def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = PauseOnGadgetFailureDetectedPlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }
