from dataclasses import dataclass
from typing import Dict


# for English users please rename this variables
UNKNOWN_TRAINING = 'Указанный тип тренировки не задан.'
DATA_MESSAGES = {
  'type': 'Тип тренировки',
  'duration': 'Длительность',
  'distance': 'Дистанция',
  'speed': 'Ср. скорость',
  'calories': 'Потрачено ккал'
}


@dataclass
class InfoMessage:
    """Information message about training."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        """Data rounding and returning message."""
        return (
            f'{DATA_MESSAGES['type']}: {self.training_type}; '
            f'{DATA_MESSAGES['duration']}: {self.duration:.3f} ч.; '
            f'{DATA_MESSAGES['distance']}: {self.distance:.3f} км; '
            f'{DATA_MESSAGES['speed']}: {self.speed:.3f} км/ч; '
            f'{DATA_MESSAGES['calories']}: {self.calories:.3f}.'
        )


class Training:
    """Base training class."""
    # class constants
    HOUR: int = 60  # minutes in HOUR
    M_IN_KM: int = 1000  # meters in km
    LEN_STEP: float = 0.65  # step length

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Getting distance in km."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Get average speed."""
        mean_speed = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Get spent calories."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Return information message about training."""
        training_type = self.__class__.__name__
        duration = self.duration
        distance = self.get_distance()
        speed = self.get_mean_speed()
        calories = self.get_spent_calories()
        return InfoMessage(training_type,
                           duration,
                           distance,
                           speed,
                           calories
                           )


class Running(Training):
    """Training: run."""
    # coefficients to calculate in formulas
    SPEED_FACTOR: int = 18
    MINUS_SPEED_COEFF: int = 20

    def get_spent_calories(self) -> float:
        """Get spent calories."""
        spent_calories = (
            (
                (
                    self.SPEED_FACTOR * self.get_mean_speed()
                ) - self.MINUS_SPEED_COEFF
            ) * self.weight / self.M_IN_KM * self.duration * self.HOUR
        )
        return spent_calories


class SportsWalking(Training):
    """Training: sports walk."""
    # coefficients to calculate in formulas
    WEIGHT_FACTOR: float = 0.035
    HEIGHT_FACTOR: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Get spent calories."""
        spent_calories = (
            self.get_mean_speed() ** 2 // self.height * self.HEIGHT_FACTOR
            * self.weight + self.WEIGHT_FACTOR * self.weight
            * self.duration * self.HOUR
        )
        return spent_calories


class Swimming(Training):
    """Training: swim."""
    LEN_STEP: float = 1.38  # step length
    SWIM_SPEED_COEFF: float = 1.1
    SWIM_CALORIES_FACTOR: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Get average speed."""
        mean_speed = (
            self.length_pool * self.count_pool
            / self.M_IN_KM / self.duration
        )
        return mean_speed

    def get_spent_calories(self) -> float:
        """Get spent calories."""
        spent_calories = (
            (
                self.get_mean_speed() + self.SWIM_SPEED_COEFF
            ) * self.SWIM_CALORIES_FACTOR * self.weight
        )
        return spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Read data from sensors."""
    workout_types: Dict[str, Training] = {
        'RUN': Running,
        'WLK': SportsWalking,
        'SWM': Swimming,
    }
    if workout_type in workout_types:
        return workout_types[workout_type](*data)
    elif workout_type not in workout_types:
        raise ValueError(UNKNOWN_TRAINING)


def main(training: Training) -> None:
    """Main function."""
    info: Training = training.show_training_info()
    print(info.get_message())


# test data from sensors
if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training: Training = read_package(workout_type, data)
        main(training)
