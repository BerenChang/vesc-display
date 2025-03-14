from enum import Enum

from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QMenu, QAction

from config import Config
from nsec_calculation import NSec

class ButtonPos(Enum):
    # RIGHT_PARAM = "right_param"
    LEFT_PARAM = "left_param"
    CENTER_PARAM = "center_param"

class ParamIndicators(Enum):
    BatteryPercent = 0
    SessionDistance = 1
    UpdatesPerSecond = 3
    BatteryEstDistance = 6
    WhKmH = 7
    FullPower = 9
    NSec = 10           # not saved in config, only for open menu choose nsec
    PhaseCurrent = 11
    BatteryCurrent = 12
    Voltage = 13
    ControllerTemp = 14
    MotorTemp = 15

    nsec_min_voltage = 100
    nsec_max_voltage = 101
    nsec_min_b_current = 102
    nsec_max_b_current = 103
    nsec_min_p_current = 104
    nsec_max_p_current = 105
    nsec_min_speed = 106
    nsec_max_speed = 107
    nsec_distance = 108
    nsec_watts_used = 109
    nsec_watts_on_km = 110
    nsec_max_diff_voltage = 111

class ParamIndicatorsChanger:
    gui = None
    ui = None

    last_menu_event = None

    def __init__(self, gui):
        self.gui = gui
        self.ui = gui.ui

    def get_indicators_by_state(self, state) -> dict:

        all_params_values = dict()
        all_params_values[0] = f"{state.battery_percent}%"
        all_params_values[1] = str(round(state.session_distance, 1))
        all_params_values[3] = str(self.gui.updates_in_sec)
        all_params_values[6] = str(round(state.estimated_battery_distance, 1))
        all_params_values[7] = str(state.wh_km_h)
        all_params_values[9] = f'{state.full_power}W'
        all_params_values[10] = "---"
        all_params_values[11] = f'{int(state.esc_a_state.phase_current + state.esc_b_state.phase_current)}A'
        all_params_values[12] = f'{int(state.esc_a_state.battery_current + state.esc_b_state.battery_current)}A'
        all_params_values[13] = str(round(state.esc_a_state.voltage, 1))
        all_params_values[14] = str(round(max(state.esc_a_state.temperature, state.esc_b_state.temperature), 1))
        all_params_values[15] = str(round(max(state.esc_a_state.motor_temperature, state.esc_b_state.motor_temperature), 1))


        #from nsec_calculation import NSec
        nsec: NSec.NSecResult = state.nsec.last_result
        all_params_values[100] = str(nsec.min_voltage)
        all_params_values[101] = str(nsec.max_voltage)
        all_params_values[102] = str(nsec.min_b_current)
        all_params_values[103] = str(nsec.max_b_current)
        all_params_values[104] = str(nsec.min_p_current)
        all_params_values[105] = str(nsec.max_p_current)
        all_params_values[106] = str(nsec.min_speed)
        all_params_values[107] = str(nsec.max_speed)
        all_params_values[108] = str(round(nsec.distance, 2))
        all_params_values[109] = str(round(nsec.watts_used, 2))
        all_params_values[110] = str(round(nsec.watts_on_km, 2))
        all_params_values[111] = str(round(nsec.max_diff_voltage, 2))
        return all_params_values

    def fill_indicators(self, state):
        if hasattr(self.gui, "center_param"):
            self.gui.center_param.setText(self.get_value_by_indicator_num(state, self.gui.center_param_active_ind.value))
        self.gui.left_param.setText(self.get_value_by_indicator_num(state, self.gui.left_param_active_ind.value))
        # self.gui.right_param.setText(self.get_value_by_indicator_num(state, self.gui.right_param_active_ind.value))
        pass

    def get_value_by_indicator_num(self, state, num: int) -> str:
        # TODO: refactor to switch-case in python 3.10

        if   num == 0:
            return f"{state.battery_percent}%"
        elif num == 1:
            return str(round(state.session_distance, 1))
        elif num == 3:
            return str(self.gui.updates_in_sec)
        elif num == 6:
            return str(round(state.estimated_battery_distance, 1))
        elif num == 7:
            return str(state.wh_km_h)
        elif num == 9:
            return f'{state.full_power}W'
        elif num == 10:
            return "---"
        elif num == 11:
            return f'{int(state.esc_a_state.phase_current + state.esc_b_state.phase_current)}A'
        elif num == 12:
            return f'{int(state.esc_a_state.battery_current + state.esc_b_state.battery_current)}A'
        elif num == 13:
            return str(round(state.esc_a_state.voltage, 1))
        elif num == 14:
            return str(round(max(state.esc_a_state.temperature, state.esc_b_state.temperature), 1))
        elif num == 15:
            return str(round(max(state.esc_a_state.motor_temperature, state.esc_b_state.motor_temperature), 1))

        nsec: NSec.NSecResult = state.nsec.last_result
        if   num == 100:
            return str(nsec.min_voltage)
        elif num == 101:
            return str(nsec.max_voltage)
        elif num == 102:
            return str(nsec.min_b_current)
        elif num == 103:
            return str(nsec.max_b_current)
        elif num == 104:
            return str(nsec.min_p_current)
        elif num == 105:
            return str(nsec.max_p_current)
        elif num == 106:
            return str(nsec.min_speed)
        elif num == 107:
            return str(nsec.max_speed)
        elif num == 108:
            return str(round(nsec.distance, 2))
        elif num == 109:
            return str(round(nsec.watts_used, 2))
        elif num == 110:
            return str(round(nsec.watts_on_km, 2))
        elif num == 111:
            return str(round(nsec.max_diff_voltage, 2))

        return ""


    def have_enabled_nsec(self) -> bool:
        from gui import GUIApp as NormalApp

        if type(self.gui) == NormalApp:
            # if ParamIndicators[Config.right_param_active_ind].value < 100 and \
            #     ParamIndicators[Config.left_param_active_ind].value < 100:
            if ParamIndicators[Config.left_param_active_ind].value < 100:
                return False
        # else:
        #     if ParamIndicators[Config.right_param_active_ind].value < 100 and \
        #         ParamIndicators[Config.center_param_active_ind].value < 100 and \
        #         ParamIndicators[Config.left_param_active_ind].value < 100:
        #         return False

        return False

    def is_menu_item_now_using(self, param_position: ButtonPos, indicator: ParamIndicators):
        if param_position == ButtonPos.LEFT_PARAM:
            if self.gui.left_param_active_ind == indicator:
                return True

            if indicator == ParamIndicators.NSec and self.gui.left_param_active_ind.value > 99:
                return True

        if param_position == ButtonPos.CENTER_PARAM:
            if self.gui.center_param_active_ind == indicator:
                return True

            if indicator == ParamIndicators.NSec and self.gui.center_param_active_ind.value > 99:
                return True

        # if param_position == ButtonPos.RIGHT_PARAM:
        #     if self.gui.right_param_active_ind == indicator:
        #         return True

            # if indicator == ParamIndicators.NSec and self.gui.right_param_active_ind.value > 99:
            if indicator == ParamIndicators.NSec:
                return True

    def show_menu_param_change(self, event: QMouseEvent, param_position: ButtonPos):
        menu = QMenu(self.ui)
        menu.setStyleSheet('color: rgb(255, 255, 255);font: 22pt "Consolas"; font-weight: bold; border-style: outset; border-width: 2px; border-color: beige;')

        actions = []
        # if param_position == ButtonPos.LEFT_PARAM or param_position == ButtonPos.RIGHT_PARAM or param_position == ButtonPos.CENTER_PARAM:
        if param_position == ButtonPos.LEFT_PARAM or param_position == ButtonPos.CENTER_PARAM:
            for indicator in [i for i in ParamIndicators]:
                if indicator.value > 99: continue # NSec
                name: str = indicator.name
                if self.is_menu_item_now_using(param_position, indicator):
                    name = "✔ " + name
                action = QAction()
                action.setData(param_position)
                action.setText(name)
                actions.append(action)

        self.last_menu_event = event
        menu.triggered.connect(self.menu_handler_1lvl)
        menu.addActions(actions)
        menu.exec(event.globalPos())

    def menu_handler_1lvl(self, action: QAction):
        choosen_item = action.text()
        param_position = action.data()
        if "NSec" in choosen_item:
            choosen_item = "NSec"
        if " " in choosen_item: return

        print("set", choosen_item, "to", param_position)

        if choosen_item == ParamIndicators.NSec.name:
            menu = QMenu(self.ui)
            menu.setStyleSheet('color: rgb(255, 255, 255);font: 22pt "Consolas"; font-weight: bold; border-style: outset; border-width: 2px; border-color: beige;')

            actions = []

            for indicator in [i for i in ParamIndicators]:
                if indicator.value < 100: continue # hide non-NSec
                name: str = indicator.name

                if self.is_menu_item_now_using(param_position, indicator):
                    name = "✔ " + name

                action = QAction()
                action.setData(param_position)
                action.setText(name)
                actions.append(action)

            menu.addActions(actions)
            menu.triggered.connect(self.menu_handler_2lvl_nsec)
            menu.exec(self.last_menu_event.globalPos())
            return

        self.apply_and_save_indicator(choosen_item, param_position)

    def menu_handler_2lvl_nsec(self, action: QAction):
        choosen_item = action.text()
        param_position = action.data()
        if " " in choosen_item: return

        print("set", choosen_item, "to", param_position)
        self.apply_and_save_indicator(choosen_item, param_position)


    def apply_and_save_indicator(self, indicator_name, button_pos):
        # if button_pos == ButtonPos.RIGHT_PARAM:
        #     self.gui.right_param_active_ind = ParamIndicators[indicator_name]
        #     Config.right_param_active_ind = ParamIndicators[indicator_name].name
        if button_pos == ButtonPos.LEFT_PARAM:
            self.gui.left_param_active_ind = ParamIndicators[indicator_name]
            Config.left_param_active_ind = ParamIndicators[indicator_name].name
        if button_pos == ButtonPos.CENTER_PARAM:
            self.gui.center_param_active_ind = ParamIndicators[indicator_name]
            Config.center_param_active_ind = ParamIndicators[indicator_name].name
        Config.save()