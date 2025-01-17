/**
 * Marlin 3D Printer Firmware
 * Copyright (c) 2020 MarlinFirmware [https://github.com/MarlinFirmware/Marlin]
 *
 * Based on Sprinter and grbl.
 * Copyright (c) 2011 Camiel Gubbels / Erik van der Zalm
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
 *
 */

#include "../../inc/MarlinConfig.h"

#if ENABLED(TEMPERATURE_UNITS_SUPPORT)

#include "../gcode.h"

/**
 * M149: Set temperature units
 */
void GcodeSuite::M149() {
       if (parser.seenval('C')) parser.set_input_temp_units(TEMPUNIT_C);
  else if (parser.seenval('K')) parser.set_input_temp_units(TEMPUNIT_K);
  else if (parser.seenval('F')) parser.set_input_temp_units(TEMPUNIT_F);
  else M149_report();
}

void GcodeSuite::M149_report(const bool forReplay/*=true*/) {
<<<<<<< HEAD
  report_heading_etc(forReplay, PSTR(STR_TEMPERATURE_UNITS));
  SERIAL_ECHOPGM("  M149 ", AS_CHAR(parser.temp_units_code()), " ; Units in ");
  SERIAL_ECHOLNPGM_P(parser.temp_units_name());
=======
  report_heading_etc(forReplay, F(STR_TEMPERATURE_UNITS));
  SERIAL_ECHOPGM("  M149 ", AS_CHAR(parser.temp_units_code()), " ; Units in ");
  SERIAL_ECHOLNF(parser.temp_units_name());
>>>>>>> bugfix-2.0.x
}

#endif // TEMPERATURE_UNITS_SUPPORT
