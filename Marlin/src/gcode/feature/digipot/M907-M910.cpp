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

#include "../../../inc/MarlinConfig.h"

#if HAS_MOTOR_CURRENT_SPI || HAS_MOTOR_CURRENT_PWM || HAS_MOTOR_CURRENT_I2C || HAS_MOTOR_CURRENT_DAC

#include "../../gcode.h"

#if HAS_MOTOR_CURRENT_SPI || HAS_MOTOR_CURRENT_PWM
  #include "../../../module/stepper.h"
#endif

#if HAS_MOTOR_CURRENT_I2C
  #include "../../../feature/digipot/digipot.h"
#endif

#if HAS_MOTOR_CURRENT_DAC
  #include "../../../feature/dac/stepper_dac.h"
#endif

/**
 * M907: Set digital trimpot motor current using axis codes X, Y, Z, E, B, S
 */
void GcodeSuite::M907() {
  #if HAS_MOTOR_CURRENT_SPI

    if (!parser.seen("BS" LOGICAL_AXES_STRING))
      return M907_report();

    LOOP_LOGICAL_AXES(i) if (parser.seenval(axis_codes[i])) stepper.set_digipot_current(i, parser.value_int());
    if (parser.seenval('B')) stepper.set_digipot_current(4, parser.value_int());
    if (parser.seenval('S')) LOOP_LE_N(i, 4) stepper.set_digipot_current(i, parser.value_int());

  #elif HAS_MOTOR_CURRENT_PWM

    if (!parser.seen(
      #if ANY_PIN(MOTOR_CURRENT_PWM_X, MOTOR_CURRENT_PWM_Y, MOTOR_CURRENT_PWM_XY)
        "XY"
      #endif
      #if PIN_EXISTS(MOTOR_CURRENT_PWM_Z)
        "Z"
      #endif
      #if PIN_EXISTS(MOTOR_CURRENT_PWM_E)
        "E"
      #endif
    )) return M907_report();

    #if ANY_PIN(MOTOR_CURRENT_PWM_X, MOTOR_CURRENT_PWM_Y, MOTOR_CURRENT_PWM_XY)
      if (parser.seenval('X') || parser.seenval('Y')) stepper.set_digipot_current(0, parser.value_int());
    #endif
    #if PIN_EXISTS(MOTOR_CURRENT_PWM_Z)
      if (parser.seenval('Z')) stepper.set_digipot_current(1, parser.value_int());
    #endif
    #if PIN_EXISTS(MOTOR_CURRENT_PWM_E)
      if (parser.seenval('E')) stepper.set_digipot_current(2, parser.value_int());
    #endif

  #endif

  #if HAS_MOTOR_CURRENT_I2C
    // this one uses actual amps in floating point
    LOOP_LOGICAL_AXES(i) if (parser.seenval(axis_codes[i])) digipot_i2c.set_current(i, parser.value_float());
    // Additional extruders use B,C,D for channels 4,5,6.
    // TODO: Change these parameters because 'E' is used. B<index>?
    #if HAS_EXTRUDERS
      for (uint8_t i = E_AXIS + 1; i < DIGIPOT_I2C_NUM_CHANNELS; i++)
        if (parser.seenval('B' + i - (E_AXIS + 1))) digipot_i2c.set_current(i, parser.value_float());
    #endif
  #endif

  #if HAS_MOTOR_CURRENT_DAC
    if (parser.seenval('S')) {
      const float dac_percent = parser.value_float();
      LOOP_LE_N(i, 4) stepper_dac.set_current_percent(i, dac_percent);
    }
    LOOP_LOGICAL_AXES(i) if (parser.seenval(axis_codes[i])) stepper_dac.set_current_percent(i, parser.value_float());
  #endif
}

#if HAS_MOTOR_CURRENT_SPI || HAS_MOTOR_CURRENT_PWM

  void GcodeSuite::M907_report(const bool forReplay/*=true*/) {
<<<<<<< HEAD
    report_heading_etc(forReplay, PSTR(STR_STEPPER_MOTOR_CURRENTS));
=======
    report_heading_etc(forReplay, F(STR_STEPPER_MOTOR_CURRENTS));
>>>>>>> bugfix-2.0.x
    #if HAS_MOTOR_CURRENT_PWM
      SERIAL_ECHOLNPGM_P(                                    // PWM-based has 3 values:
          PSTR("  M907 X"), stepper.motor_current_setting[0]  // X and Y
        , SP_Z_STR,         stepper.motor_current_setting[1]  // Z
        , SP_E_STR,         stepper.motor_current_setting[2]  // E
      );
    #elif HAS_MOTOR_CURRENT_SPI
      SERIAL_ECHOPGM("  M907");                               // SPI-based has 5 values:
      LOOP_LOGICAL_AXES(q) {                                  // X Y Z (I J K) E (map to X Y Z (I J K) E0 by default)
        SERIAL_CHAR(' ', axis_codes[q]);
        SERIAL_ECHO(stepper.motor_current_setting[q]);
      }
      SERIAL_CHAR(' ', 'B');                                  // B (maps to E1 by default)
      SERIAL_ECHOLN(stepper.motor_current_setting[4]);
    #endif
  }

#endif // HAS_MOTOR_CURRENT_SPI || HAS_MOTOR_CURRENT_PWM

#if HAS_MOTOR_CURRENT_SPI || HAS_MOTOR_CURRENT_DAC

  /**
   * M908: Control digital trimpot directly (M908 P<pin> S<current>)
   */
  void GcodeSuite::M908() {
    TERN_(HAS_MOTOR_CURRENT_SPI, stepper.set_digipot_value_spi(parser.intval('P'), parser.intval('S')));
    TERN_(HAS_MOTOR_CURRENT_DAC, stepper_dac.set_current_value(parser.byteval('P', -1), parser.ushortval('S', 0)));
  }

  #if HAS_MOTOR_CURRENT_DAC

    void GcodeSuite::M909() { stepper_dac.print_values(); }
    void GcodeSuite::M910() { stepper_dac.commit_eeprom(); }

  #endif // HAS_MOTOR_CURRENT_DAC

#endif // HAS_MOTOR_CURRENT_SPI || HAS_MOTOR_CURRENT_DAC

#endif // HAS_MOTOR_CURRENT_SPI || HAS_MOTOR_CURRENT_PWM || HAS_MOTOR_CURRENT_I2C || HAS_MOTOR_CURRENT_DAC
