"""Homework #3. Car racing game."""

# Write a class Car that has attributes:
# fuel(fuel, specified using random.randrange(0, 9)),
# trip_distance (Distance traveled by the car),
# model(car model), color(color)
# Implement the move method in the class that takes distance as an argument.
# Create 3 instances of this class
# In the while race_dist < desired_dist loop:
# call the move method for each instance of the class
# and pass it the value random.randrange(0, 9).
# The move method should add to trip_distance the value that was returned
# by the random range method and reduce the amount of fuel by the same value
# As soon as one of the cars has traveled a distance greater
# than or equal to desired_dist - display a message that the car has won,
# indicating the brand and distance traveled by this car.
# In this case, the loop should be interrupted
# After the loop, it is necessary to display a message
# about how much and which car has traveled, and what fuel reserve it has

import secrets  # Used instead of random for security purposes


class Car:
    """Class Car that has attributes: fuel, trip_distance, model, color."""

    def __init__(self, model, color):
        """Initialize Car class.

        Args:
            model (string): Car model.
            color (string): Car color.
        """
        self.fuel = secrets.randbelow(10)
        self.trip_distance = 0
        self.model = model
        self.color = color

    def move(self, distance):
        """Move method that takes distance as an argument.

        Args:
            distance (int): Distance to move.
        """
        if self.fuel <= 0:
            return

        actual_distance = min(distance, self.fuel)
        self.trip_distance += actual_distance
        self.fuel -= actual_distance

    def __str__(self):
        """Return string representation of Car class.

        Returns:
            string: Car class attributes.
        """
        return (f'Model: {self.model}, Color: {self.color}, '
                f'Trip distance: {self.trip_distance} km, '
                f'Fuel: {self.fuel} liters.')


if __name__ == '__main__':

    while True:
        try:
            desired_dist = int(input('Enter desired distance: '))
            if desired_dist <= 0:
                raise ValueError('Distance must be a positive integer.')
            break
        except ValueError as e:
            print(
                f'Invalid input: {e}, please enter a valid positive integer.')

    car1 = Car('Bugatti', 'Black')
    car2 = Car('McLaren', 'Orange')
    car3 = Car('Ferrari', 'Red')

    cars = [car1, car2, car3]

    for car in cars:
        print(car)

    print('Race Start!')
    while True:
        if all(car.fuel <= 0 for car in cars):
            print('All cars ran out of fuel! '
                  'The race ended without a winner.')
            break

        for car in cars:
            if car.fuel > 0:
                move_distance = secrets.randbelow(10)
                car.move(move_distance)
                print(f'{car.model} moved {move_distance} km. '
                      f'Total Distance: {car.trip_distance} km., '
                      f'Fuel left: {car.fuel} liters.')

            if car.trip_distance >= desired_dist:
                print(f'{car.model} has won the race! '
                      f'Distance: {car.trip_distance}')
                break

        else:
            continue
        break

    print('Results:')
    for car in cars:
        print(car)
