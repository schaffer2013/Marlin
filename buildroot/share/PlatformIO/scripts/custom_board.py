#
# custom_board.py
#
# - For build.address replace VECT_TAB_ADDR to relocate the firmware
# - For build.ldscript use one of the linker scripts in buildroot/share/PlatformIO/ldscripts
#
<<<<<<< HEAD
import marlin
board = marlin.env.BoardConfig()
=======
import pioutil
if pioutil.is_pio_build():
	import marlin
	board = marlin.env.BoardConfig()
>>>>>>> bugfix-2.0.x

	address = board.get("build.address", "")
	if address:
		marlin.relocate_firmware(address)

	ldscript = board.get("build.ldscript", "")
	if ldscript:
		marlin.custom_ld_script(ldscript)
