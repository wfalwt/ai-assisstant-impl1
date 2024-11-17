from abc import ABC, abstractmethod

from agent.chart.data_type import is_number, is_date


class ChartData:
    def __init__(self):
        self._x = ""
        self._y = 0.0
        self._legend = ""

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x_value):
        self._x = x_value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y_value):
        self._y = y_value

    @property
    def legend(self):
        return self._legend

    @legend.setter
    def legend(self, legend_value):
        self._legend = legend_value


class Chart(ABC):
    dimension: int
    x_type: str
    y_type: str
    legend_type: str

    def get_chart_data_keys(self, data: list[dict]) -> ([], [], []):
        str_keys = []
        date_keys = []
        number_keys = []
        data_sampling = data[0]
        for key, val in data_sampling.items():
            if is_date(val, key):
                date_keys.append(key)
            elif is_number(val):
                number_keys.append(key)
            else:
                str_keys.append(key)
        if hasattr(self, "x_type"):
            if self.x_type == "date":
                x_keys = date_keys
            elif self.x_type == "number":
                x_keys = number_keys
            else:
                x_keys = str_keys
        else:
            x_keys = []

        if hasattr(self, "y_type"):
            if self.y_type == "date":
                y_keys = date_keys
            elif self.y_type == "number":
                y_keys = number_keys
            else:
                y_keys = str_keys
        else:
            y_keys = []

        if hasattr(self, "legend_type"):
            if self.legend_type == "date":
                legend_keys = date_keys
            elif self.legend_type == "number":
                legend_keys = number_keys
            else:
                legend_keys = str_keys
        else:
            legend_keys = []

        return x_keys, y_keys, legend_keys

    def check_data_dimension(self, data: list[dict]) -> bool:
        if len(data) > 0:
            if len(data[0].keys()) >= self.dimension:
                return True
            else:
                return False
        else:
            return False

    @abstractmethod
    def parse_data(self, params: list[dict], **kwargs) -> list[ChartData]:
        raise NotImplementedError


class ChartProducer:
    @staticmethod
    def make_chart_data(chart_type: str, params: list[dict]) -> list[ChartData]:
        chart_name = chart_type.title() + "Chart"
        return eval(chart_name)().parse_data(params)


class LineChart(Chart):
    dimension = 3
    x_type = "date"
    y_type = "number"
    legend_type = "text"

    def parse_data(self, params: list[dict], **kwargs) -> list[ChartData]:
        if not self.check_data_dimension(params):
            raise Exception("not enough dimension for data")
        x_keys, y_keys, legend_keys = self.get_chart_data_keys(params)
        if len(x_keys) == 0:
            raise Exception("x axis data not found")
        if len(y_keys) == 0:
            raise Exception("y axis data not found")
        if len(legend_keys) == 0:
            raise Exception("legend data not found")
        chart_data: list[ChartData] = []
        x_key: str = x_keys[0]
        y_key: str = y_keys[0]
        legend_key: str = legend_keys[0]
        for param in params:
            _char_data = ChartData()
            _char_data.x = param[x_key]
            _char_data.y = float(param[y_key])
            _char_data.legend = param[legend_key]
            chart_data.append(_char_data)
        return chart_data


class IntervalChart(Chart):
    dimension = 3
    x_type = "date"  # or text
    y_type = "number"
    legend_type = "text"

    def parse_data(self, params: list[dict], **kwargs) -> list[ChartData]:
        if not self.check_data_dimension(params):
            raise Exception("not enough dimension for data")
        x_keys, y_keys, legend_keys = self.get_chart_data_keys(params)
        if len(x_keys) == 0 and len(legend_keys) == 0:
            raise Exception("x axis data and legend data must have one ")
        if len(y_keys) == 0:
            raise Exception("y axis data not found")
        chart_data: list[ChartData] = []
        x_key: str = ""
        if len(x_keys) > 0:
            x_key = x_keys[0]
        elif len(legend_keys) > 1:
            x_key = legend_keys[0]
        y_key: str = y_keys[0]
        legend_key: str = legend_keys[0]
        if x_key == legend_key:
            legend_key = legend_keys[1]

        for param in params:
            _char_data = ChartData()
            _char_data.x = param[x_key]
            _char_data.y = float(param[y_key])
            _char_data.legend = param[legend_key]
            chart_data.append(_char_data)
        return chart_data


class PieChart(Chart):
    dimension = 2
    x_type = "number"
    legend_type = "text"

    def parse_data(self, params: list[dict], **kwargs) -> list[ChartData]:
        if not self.check_data_dimension(params):
            raise Exception("not enough dimension for data")
        x_keys, _, legend_keys = self.get_chart_data_keys(params)
        if len(x_keys) == 0:
            raise Exception("x axis data not found ")
        if len(legend_keys) == 0:
            raise Exception("legend data not found")
        x_key: str = x_keys[0]
        legend_key: str = legend_keys[0]
        chart_data: list[ChartData] = []
        for param in params:
            _char_data = ChartData()
            _char_data.x = float(param[x_key])
            _char_data.y = ""
            _char_data.legend = param[legend_key]
            chart_data.append(_char_data)
        return chart_data


class FunnelChart(Chart):
    dimension = 2
    x_type = "text"
    y_type = "number"

    def parse_data(self, params: list[dict], **kwargs) -> list[ChartData]:
        if not self.check_data_dimension(params):
            raise Exception("not enough dimension for data")
        x_keys, y_keys, _ = self.get_chart_data_keys(params)
        if len(x_keys) == 0:
            raise Exception("x axis data not found ")
        if len(y_keys) == 0:
            raise Exception("y axis data not found")

        x_key: str = x_keys[0]
        y_key: str = y_keys[0]
        chart_data: list[ChartData] = []
        for param in params:
            _char_data = ChartData()
            _char_data.x = param[x_key]
            _char_data.y = float(param[y_key])
            _char_data.legend = param[x_key]
            chart_data.append(_char_data)
        return chart_data


class SymmetricalFunnelChart(Chart):
    dimension = 3
    x_type = "text"
    y_type = "number"
    legend_type = "text"

    def parse_data(self, params: list[dict], **kwargs) -> list[ChartData]:
        if not self.check_data_dimension(params):
            raise Exception("not enough dimension for data")
        x_keys, y_keys, legend_keys = self.get_chart_data_keys(params)
        if len(x_keys) == 0:
            raise Exception("x axis data not found ")
        if len(y_keys) == 0:
            raise Exception("y axis data not found")
        if len(legend_keys) == 0:
            raise Exception("legend data not found")

        x_key: str = x_keys[0]
        y_key: str = y_keys[0]
        if x_key == legend_keys[0]:
            legend_key = legend_keys[1]
        else:
            legend_key = legend_keys[0]
        chart_data: list[ChartData] = []
        for param in params:
            _char_data = ChartData()
            _char_data.x = param[x_key]
            _char_data.y = float(param[y_key])
            _char_data.legend = param[legend_key]
            chart_data.append(_char_data)
        return chart_data
