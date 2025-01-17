#
# common-dependencies.py
# Convenience script to check dependencies and add libs and sources for Marlin Enabled Features
#
<<<<<<< HEAD
import subprocess,os,re,pioutil
Import("env")

# Detect that 'vscode init' is running
if pioutil.is_vscode_init():
	env.Exit(0)

PIO_VERSION_MIN = (5, 0, 3)
try:
	from platformio import VERSION as PIO_VERSION
	weights = (1000, 100, 1)
	version_min = sum([x[0] * float(re.sub(r'[^0-9]', '.', str(x[1]))) for x in zip(weights, PIO_VERSION_MIN)])
	version_cur = sum([x[0] * float(re.sub(r'[^0-9]', '.', str(x[1]))) for x in zip(weights, PIO_VERSION)])
	if version_cur < version_min:
		print()
		print("**************************************************")
		print("******      An update to PlatformIO is      ******")
		print("******  required to build Marlin Firmware.  ******")
		print("******                                      ******")
		print("******      Minimum version: ", PIO_VERSION_MIN, "    ******")
		print("******      Current Version: ", PIO_VERSION, "    ******")
		print("******                                      ******")
		print("******   Update PlatformIO and try again.   ******")
		print("**************************************************")
		print()
		exit(1)
except SystemExit:
	exit(1)
except:
	print("Can't detect PlatformIO Version")

from platformio.package.meta import PackageSpec
from platformio.project.config import ProjectConfig

#print(env.Dump())

try:
	verbose = int(env.GetProjectOption('custom_verbose'))
except:
	verbose = 0

def blab(str,level=1):
	if verbose >= level:
		print("[deps] %s" % str)
=======
import pioutil
if pioutil.is_pio_build():
>>>>>>> bugfix-2.0.x

	import subprocess,os,re
	Import("env")

	from platformio.package.meta import PackageSpec
	from platformio.project.config import ProjectConfig

	verbose = 0
	FEATURE_CONFIG = {}

	def validate_pio():
		PIO_VERSION_MIN = (5, 0, 3)
		try:
			from platformio import VERSION as PIO_VERSION
			weights = (1000, 100, 1)
			version_min = sum([x[0] * float(re.sub(r'[^0-9]', '.', str(x[1]))) for x in zip(weights, PIO_VERSION_MIN)])
			version_cur = sum([x[0] * float(re.sub(r'[^0-9]', '.', str(x[1]))) for x in zip(weights, PIO_VERSION)])
			if version_cur < version_min:
				print()
				print("**************************************************")
				print("******      An update to PlatformIO is      ******")
				print("******  required to build Marlin Firmware.  ******")
				print("******                                      ******")
				print("******      Minimum version: ", PIO_VERSION_MIN, "    ******")
				print("******      Current Version: ", PIO_VERSION, "    ******")
				print("******                                      ******")
				print("******   Update PlatformIO and try again.   ******")
				print("**************************************************")
				print()
				exit(1)
		except SystemExit:
			exit(1)
		except:
			print("Can't detect PlatformIO Version")

	def blab(str,level=1):
		if verbose >= level:
			print("[deps] %s" % str)

	def add_to_feat_cnf(feature, flines):

		try:
			feat = FEATURE_CONFIG[feature]
		except:
			FEATURE_CONFIG[feature] = {}

		# Get a reference to the FEATURE_CONFIG under construction
		feat = FEATURE_CONFIG[feature]

		# Split up passed lines on commas or newlines and iterate
		# Add common options to the features config under construction
		# For lib_deps replace a previous instance of the same library
		atoms = re.sub(r',\\s*', '\n', flines).strip().split('\n')
		for line in atoms:
			parts = line.split('=')
			name = parts.pop(0)
			if name in ['build_flags', 'extra_scripts', 'src_filter', 'lib_ignore']:
				feat[name] = '='.join(parts)
				blab("[%s] %s=%s" % (feature, name, feat[name]), 3)
			else:
				for dep in re.split(r",\s*", line):
					lib_name = re.sub(r'@([~^]|[<>]=?)?[\d.]+', '', dep.strip()).split('=').pop(0)
					lib_re = re.compile('(?!^' + lib_name + '\\b)')
					feat['lib_deps'] = list(filter(lib_re.match, feat['lib_deps'])) + [dep]
					blab("[%s] lib_deps = %s" % (feature, dep), 3)

	def load_config():
		blab("========== Gather [features] entries...")
		items = ProjectConfig().items('features')
		for key in items:
			feature = key[0].upper()
			if not feature in FEATURE_CONFIG:
				FEATURE_CONFIG[feature] = { 'lib_deps': [] }
			add_to_feat_cnf(feature, key[1])

		# Add options matching custom_marlin.MY_OPTION to the pile
		blab("========== Gather custom_marlin entries...")
		all_opts = env.GetProjectOptions()
		for n in all_opts:
			key = n[0]
			mat = re.match(r'custom_marlin\.(.+)', key)
			if mat:
				try:
					val = env.GetProjectOption(key)
				except:
					val = None
				if val:
					opt = mat.group(1).upper()
					blab("%s.custom_marlin.%s = '%s'" % ( env['PIOENV'], opt, val ))
					add_to_feat_cnf(opt, val)

	def get_all_known_libs():
		known_libs = []
		for feature in FEATURE_CONFIG:
			feat = FEATURE_CONFIG[feature]
			if not 'lib_deps' in feat:
				continue
			for dep in feat['lib_deps']:
<<<<<<< HEAD
				deps_to_add[PackageSpec(dep).name] = dep
				blab("==================== %s... " % dep, 2)

			# Does the env already have the dependency?
			deps = env.GetProjectOption('lib_deps')
			for dep in deps:
				name = PackageSpec(dep).name
				if name in deps_to_add:
					del deps_to_add[name]

			# Are there any libraries that should be ignored?
			lib_ignore = env.GetProjectOption('lib_ignore')
			for dep in deps:
				name = PackageSpec(dep).name
				if name in deps_to_add:
					del deps_to_add[name]

			# Is there anything left?
			if len(deps_to_add) > 0:
				# Only add the missing dependencies
				set_env_field('lib_deps', deps + list(deps_to_add.values()))

		if 'build_flags' in feat:
			f = feat['build_flags']
			blab("========== Adding build_flags for %s: %s" % (feature, f), 2)
			new_flags = env.GetProjectOption('build_flags') + [ f ]
			env.Replace(BUILD_FLAGS=new_flags)

		if 'extra_scripts' in feat:
			blab("Running extra_scripts for %s... " % feature, 2)
			env.SConscript(feat['extra_scripts'], exports="env")

		if 'src_filter' in feat:
			blab("========== Adding src_filter for %s... " % feature, 2)
			src_filter = ' '.join(env.GetProjectOption('src_filter'))
			# first we need to remove the references to the same folder
			my_srcs = re.findall(r'[+-](<.*?>)', feat['src_filter'])
			cur_srcs = re.findall(r'[+-](<.*?>)', src_filter)
			for d in my_srcs:
				if d in cur_srcs:
					src_filter = re.sub(r'[+-]' + d, '', src_filter)

			src_filter = feat['src_filter'] + ' ' + src_filter
			set_env_field('src_filter', [src_filter])
			env.Replace(SRC_FILTER=src_filter)

		if 'lib_ignore' in feat:
			blab("========== Adding lib_ignore for %s... " % feature, 2)
			lib_ignore = env.GetProjectOption('lib_ignore') + [feat['lib_ignore']]
			set_env_field('lib_ignore', lib_ignore)

#
# Find a compiler, considering the OS
#
ENV_BUILD_PATH = os.path.join(env.Dictionary('PROJECT_BUILD_DIR'), env['PIOENV'])
GCC_PATH_CACHE = os.path.join(ENV_BUILD_PATH, ".gcc_path")
def search_compiler():
	try:
		filepath = env.GetProjectOption('custom_gcc')
		blab("Getting compiler from env")
		return filepath
	except:
		pass

	if os.path.exists(GCC_PATH_CACHE):
		with open(GCC_PATH_CACHE, 'r') as f:
			return f.read()

	# Find the current platform compiler by searching the $PATH
	# which will be in a platformio toolchain bin folder
	path_regex = re.escape(env['PROJECT_PACKAGES_DIR'])

	# See if the environment provides a default compiler
	try:
		gcc = env.GetProjectOption('custom_deps_gcc')
	except:
		gcc = "g++"

	if env['PLATFORM'] == 'win32':
		path_separator = ';'
		path_regex += r'.*\\bin'
		gcc += ".exe"
	else:
		path_separator = ':'
		path_regex += r'/.+/bin'

	# Search for the compiler
	for pathdir in env['ENV']['PATH'].split(path_separator):
		if not re.search(path_regex, pathdir, re.IGNORECASE):
			continue
		for filepath in os.listdir(pathdir):
			if not filepath.endswith(gcc):
=======
				known_libs.append(PackageSpec(dep).name)
		return known_libs

	def get_all_env_libs():
		env_libs = []
		lib_deps = env.GetProjectOption('lib_deps')
		for dep in lib_deps:
			env_libs.append(PackageSpec(dep).name)
		return env_libs

	def set_env_field(field, value):
		proj = env.GetProjectConfig()
		proj.set("env:" + env['PIOENV'], field, value)

	# All unused libs should be ignored so that if a library
	# exists in .pio/lib_deps it will not break compilation.
	def force_ignore_unused_libs():
		env_libs = get_all_env_libs()
		known_libs = get_all_known_libs()
		diff = (list(set(known_libs) - set(env_libs)))
		lib_ignore = env.GetProjectOption('lib_ignore') + diff
		blab("Ignore libraries: %s" % lib_ignore)
		set_env_field('lib_ignore', lib_ignore)

	def apply_features_config():
		load_config()
		blab("========== Apply enabled features...")
		for feature in FEATURE_CONFIG:
			if not env.MarlinFeatureIsEnabled(feature):
>>>>>>> bugfix-2.0.x
				continue

			feat = FEATURE_CONFIG[feature]

			if 'lib_deps' in feat and len(feat['lib_deps']):
				blab("========== Adding lib_deps for %s... " % feature, 2)

				# feat to add
				deps_to_add = {}
				for dep in feat['lib_deps']:
					deps_to_add[PackageSpec(dep).name] = dep
					blab("==================== %s... " % dep, 2)

				# Does the env already have the dependency?
				deps = env.GetProjectOption('lib_deps')
				for dep in deps:
					name = PackageSpec(dep).name
					if name in deps_to_add:
						del deps_to_add[name]

				# Are there any libraries that should be ignored?
				lib_ignore = env.GetProjectOption('lib_ignore')
				for dep in deps:
					name = PackageSpec(dep).name
					if name in deps_to_add:
						del deps_to_add[name]

				# Is there anything left?
				if len(deps_to_add) > 0:
					# Only add the missing dependencies
					set_env_field('lib_deps', deps + list(deps_to_add.values()))

			if 'build_flags' in feat:
				f = feat['build_flags']
				blab("========== Adding build_flags for %s: %s" % (feature, f), 2)
				new_flags = env.GetProjectOption('build_flags') + [ f ]
				env.Replace(BUILD_FLAGS=new_flags)

			if 'extra_scripts' in feat:
				blab("Running extra_scripts for %s... " % feature, 2)
				env.SConscript(feat['extra_scripts'], exports="env")

			if 'src_filter' in feat:
				blab("========== Adding src_filter for %s... " % feature, 2)
				src_filter = ' '.join(env.GetProjectOption('src_filter'))
				# first we need to remove the references to the same folder
				my_srcs = re.findall(r'[+-](<.*?>)', feat['src_filter'])
				cur_srcs = re.findall(r'[+-](<.*?>)', src_filter)
				for d in my_srcs:
					if d in cur_srcs:
						src_filter = re.sub(r'[+-]' + d, '', src_filter)

				src_filter = feat['src_filter'] + ' ' + src_filter
				set_env_field('src_filter', [src_filter])
				env.Replace(SRC_FILTER=src_filter)

			if 'lib_ignore' in feat:
				blab("========== Adding lib_ignore for %s... " % feature, 2)
				lib_ignore = env.GetProjectOption('lib_ignore') + [feat['lib_ignore']]
				set_env_field('lib_ignore', lib_ignore)

	#
	# Find a compiler, considering the OS
	#
	ENV_BUILD_PATH = os.path.join(env.Dictionary('PROJECT_BUILD_DIR'), env['PIOENV'])
	GCC_PATH_CACHE = os.path.join(ENV_BUILD_PATH, ".gcc_path")
	def search_compiler():
		try:
			filepath = env.GetProjectOption('custom_gcc')
			blab("Getting compiler from env")
			return filepath
		except:
			pass

		if os.path.exists(GCC_PATH_CACHE):
			with open(GCC_PATH_CACHE, 'r') as f:
				return f.read()

		# Find the current platform compiler by searching the $PATH
		# which will be in a platformio toolchain bin folder
		path_regex = re.escape(env['PROJECT_PACKAGES_DIR'])

		# See if the environment provides a default compiler
		try:
			gcc = env.GetProjectOption('custom_deps_gcc')
		except:
			gcc = "g++"

		if env['PLATFORM'] == 'win32':
			path_separator = ';'
			path_regex += r'.*\\bin'
			gcc += ".exe"
		else:
			path_separator = ':'
			path_regex += r'/.+/bin'

<<<<<<< HEAD
	filepath = env.get('CXX')
	if filepath == 'CC':
		filepath = gcc
	blab("Couldn't find a compiler! Fallback to %s" % filepath)
	return filepath
=======
		# Search for the compiler
		for pathdir in env['ENV']['PATH'].split(path_separator):
			if not re.search(path_regex, pathdir, re.IGNORECASE):
				continue
			for filepath in os.listdir(pathdir):
				if not filepath.endswith(gcc):
					continue
				# Use entire path to not rely on env PATH
				filepath = os.path.sep.join([pathdir, filepath])
				# Cache the g++ path to no search always
				if os.path.exists(ENV_BUILD_PATH):
					with open(GCC_PATH_CACHE, 'w+') as f:
						f.write(filepath)

				return filepath

		filepath = env.get('CXX')
		if filepath == 'CC':
			filepath = gcc
		blab("Couldn't find a compiler! Fallback to %s" % filepath)
		return filepath
>>>>>>> bugfix-2.0.x

	#
	# Use the compiler to get a list of all enabled features
	#
	def load_marlin_features():
		if 'MARLIN_FEATURES' in env:
			return

		# Process defines
		build_flags = env.get('BUILD_FLAGS')
		build_flags = env.ParseFlagsExtended(build_flags)

		cxx = search_compiler()
		cmd = ['"' + cxx + '"']

		# Build flags from board.json
		#if 'BOARD' in env:
		#	cmd += [env.BoardConfig().get("build.extra_flags")]
		for s in build_flags['CPPDEFINES']:
			if isinstance(s, tuple):
				cmd += ['-D' + s[0] + '=' + str(s[1])]
			else:
				cmd += ['-D' + s]

		cmd += ['-D__MARLIN_DEPS__ -w -dM -E -x c++ buildroot/share/PlatformIO/scripts/common-dependencies.h']
		cmd = ' '.join(cmd)
		blab(cmd, 4)
		define_list = subprocess.check_output(cmd, shell=True).splitlines()
		marlin_features = {}
		for define in define_list:
			feature = define[8:].strip().decode().split(' ')
			feature, definition = feature[0], ' '.join(feature[1:])
			marlin_features[feature] = definition
		env['MARLIN_FEATURES'] = marlin_features

	#
	# Return True if a matching feature is enabled
	#
	def MarlinFeatureIsEnabled(env, feature):
		load_marlin_features()
		r = re.compile('^' + feature + '$')
		found = list(filter(r.match, env['MARLIN_FEATURES']))

		# Defines could still be 'false' or '0', so check
		some_on = False
		if len(found):
			for f in found:
				val = env['MARLIN_FEATURES'][f]
				if val in [ '', '1', 'true' ]:
					some_on = True
				elif val in env['MARLIN_FEATURES']:
					some_on = env.MarlinFeatureIsEnabled(val)

		return some_on

	validate_pio()

	try:
		verbose = int(env.GetProjectOption('custom_verbose'))
	except:
		pass

	# Add a method for other PIO scripts to query enabled features
	env.AddMethod(MarlinFeatureIsEnabled)

	# Add dependencies for enabled Marlin features
	apply_features_config()
	force_ignore_unused_libs()
