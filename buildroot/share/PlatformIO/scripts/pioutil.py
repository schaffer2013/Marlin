#
<<<<<<< HEAD
# buildroot/share/PlatformIO/scripts/pioutil.py
#

# Detect that 'vscode init' is running
def is_vscode_init():
	from SCons.Script import COMMAND_LINE_TARGETS
	return "idedata" in COMMAND_LINE_TARGETS or "_idedata" in COMMAND_LINE_TARGETS
=======
# pioutil.py
#

# Make sure 'vscode init' is not the current command
def is_pio_build():
	from SCons.Script import COMMAND_LINE_TARGETS
	return "idedata" not in COMMAND_LINE_TARGETS and "_idedata" not in COMMAND_LINE_TARGETS
>>>>>>> bugfix-2.0.x
