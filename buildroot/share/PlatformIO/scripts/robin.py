#
<<<<<<< HEAD
# buildroot/share/PlatformIO/scripts/robin.py
#
import marlin

# Apply customizations for a MKS Robin
def prepare(address, ldname, fwname):
	def encrypt(source, target, env):
		marlin.encrypt_mks(source, target, env, fwname)
	marlin.relocate_firmware(address)
	marlin.custom_ld_script(ldname)
	marlin.add_post_action(encrypt);
=======
# robin.py
#

# Apply customizations for a MKS Robin
def prepare(address, ldname, fwname):
	import pioutil
	if pioutil.is_pio_build():
		import marlin
		def encrypt(source, target, env):
			marlin.encrypt_mks(source, target, env, fwname)
		marlin.relocate_firmware(address)
		marlin.custom_ld_script(ldname)
		marlin.add_post_action(encrypt);
>>>>>>> bugfix-2.0.x
